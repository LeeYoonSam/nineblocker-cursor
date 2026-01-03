#!/usr/bin/env python3
"""
엑셀 리그 기록 파일을 JSON으로 변환하는 스크립트
사용법: python3 convert_excel_to_json.py <엑셀파일경로> <시즌코드>
예시: python3 convert_excel_to_json.py "/Users/user/Downloads/2026-01 리그 기록.xlsx" 202601
"""

import json
import sys
import openpyxl
from pathlib import Path


def parse_team_from_rows(ws, start_row, end_row):
    """전체득점 시트에서 선수 데이터를 파싱"""
    players = []
    current_team = None

    for row_idx in range(start_row, end_row + 1):
        row = list(ws.iter_rows(min_row=row_idx, max_row=row_idx, values_only=True))[0]

        # 팀 정보 (A열)
        if row[0] is not None:
            current_team = row[0]

        # 선수명 (B열)과 번호 (C열)
        player_name = row[1]
        player_number = row[2]

        if player_name is None or player_number is None:
            continue

        # 참석수 (S열, 인덱스 18)
        attendance = row[18] if len(row) > 18 and row[18] is not None else 0
        attendance = int(attendance) if attendance else 0

        # 총득점 (T열, 인덱스 19)
        total_score = row[19] if len(row) > 19 and row[19] is not None else 0
        total_score = int(total_score) if total_score else 0

        # 평균득점 (V열, 인덱스 21)
        avg_score = row[21] if len(row) > 21 and row[21] is not None else 0
        avg_score = float(avg_score) if avg_score else 0.0

        players.append({
            'team': current_team,
            'name': player_name,
            'number': int(player_number),
            'attendance': attendance,
            'total_score': total_score,
            'avg_score': round(avg_score, 1)
        })

    return players


def parse_additional_stats(ws):
    """부가기록 계산 시트에서 부가기록 데이터를 파싱"""
    stats = {}

    for row_idx in range(3, ws.max_row + 1):
        row = list(ws.iter_rows(min_row=row_idx, max_row=row_idx, values_only=True))[0]

        player_name = row[0]
        player_number = row[1]

        if player_name is None or player_number is None:
            continue

        # 누적 (C~G열, 인덱스 2~6): 리바운드, 어시스트, 스틸, 블록, 3점슛
        rebound_total = int(row[2]) if row[2] is not None else 0
        assist_total = int(row[3]) if row[3] is not None else 0
        steal_total = int(row[4]) if row[4] is not None else 0
        block_total = int(row[5]) if row[5] is not None else 0
        three_pt_total = int(row[6]) if row[6] is not None else 0

        # 평균 (H~L열, 인덱스 7~11): 리바운드, 어시스트, 스틸, 블록, 3점슛
        rebound_avg = float(row[7]) if row[7] is not None else 0.0
        assist_avg = float(row[8]) if row[8] is not None else 0.0
        steal_avg = float(row[9]) if row[9] is not None else 0.0
        block_avg = float(row[10]) if row[10] is not None else 0.0
        three_pt_avg = float(row[11]) if row[11] is not None else 0.0

        key = (player_name, int(player_number))
        stats[key] = {
            '리바운드': {'누적': rebound_total, '평균': round(rebound_avg, 1)},
            '어시스트': {'누적': assist_total, '평균': round(assist_avg, 1)},
            '스틸': {'누적': steal_total, '평균': round(steal_avg, 1)},
            '블록': {'누적': block_total, '평균': round(block_avg, 1)},
            '3점슛': {'누적': three_pt_total, '평균': round(three_pt_avg, 1)}
        }

    return stats


def count_rounds(ws):
    """전체득점 시트 헤더에서 라운드 수를 계산"""
    header = list(ws.iter_rows(min_row=1, max_row=1, values_only=True))[0]
    round_count = 0

    for cell in header:
        if cell and '라운드' in str(cell):
            round_count += 1

    return round_count


def convert_excel_to_json(excel_path, season_code):
    """엑셀 파일을 JSON으로 변환"""
    wb = openpyxl.load_workbook(excel_path, data_only=True)

    # 전체득점 시트에서 선수 기본 정보 추출
    ws_score = wb['전체득점']

    # 라운드 수 계산
    total_rounds = count_rounds(ws_score)

    # 선수 데이터 추출 (2행부터 데이터 시작, 마지막 행까지)
    players_basic = parse_team_from_rows(ws_score, 2, ws_score.max_row)

    # 부가기록 시트에서 추가 통계 추출
    ws_stats = wb['부가기록 계산']
    additional_stats = parse_additional_stats(ws_stats)

    # 데이터 병합
    players_list = []
    for player in players_basic:
        key = (player['name'], player['number'])
        stats = additional_stats.get(key, {
            '리바운드': {'누적': 0, '평균': 0.0},
            '어시스트': {'누적': 0, '평균': 0.0},
            '스틸': {'누적': 0, '평균': 0.0},
            '블록': {'누적': 0, '평균': 0.0},
            '3점슛': {'누적': 0, '평균': 0.0}
        })

        players_list.append({
            '번호': player['number'],
            '팀': player['team'],
            '선수명': player['name'],
            '득점': {
                '누적득점': player['total_score'],
                '평균득점': player['avg_score']
            },
            '출석': player['attendance'],
            '부가기록': {
                '어시스트': stats['어시스트'],
                '리바운드': stats['리바운드'],
                '스틸': stats['스틸'],
                '블록': stats['블록'],
                '3점슛': stats['3점슛']
            }
        })

    # 시즌 이름 생성 (202601 -> "2026년 1월")
    year = season_code[:4]
    month = int(season_code[4:6])
    season_name = f"{year}년 {month}월"

    result = {
        '시즌': season_name,
        '총라운드': total_rounds,
        '총선수수': len(players_list),
        '선수목록': players_list
    }

    return result


def main():
    if len(sys.argv) < 3:
        print("사용법: python3 convert_excel_to_json.py <엑셀파일경로> <시즌코드>")
        print("예시: python3 convert_excel_to_json.py '/Users/user/Downloads/2026-01 리그 기록.xlsx' 202601")
        sys.exit(1)

    excel_path = sys.argv[1]
    season_code = sys.argv[2]

    if not Path(excel_path).exists():
        print(f"오류: 파일을 찾을 수 없습니다 - {excel_path}")
        sys.exit(1)

    result = convert_excel_to_json(excel_path, season_code)

    # JSON 파일로 저장
    output_path = Path(__file__).parent / f"league_stats_{season_code}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"변환 완료: {output_path}")
    print(f"시즌: {result['시즌']}")
    print(f"총 라운드: {result['총라운드']}")
    print(f"총 선수 수: {result['총선수수']}")


if __name__ == '__main__':
    main()
