# 🏀 나인블로커스 리그 통계 대시보드

나인블로커스 농구 리그의 시즌 통계를 시각화하고, AI 채팅 기능을 통해 데이터를 자연어로 분석할 수 있는 웹 애플리케이션입니다.

[![Live Demo](https://img.shields.io/badge/🔗_Live_Demo-Click_Here-ff6b35?style=for-the-badge)](https://leeyoonsam.github.io/nineblocker-cursor/)

![Preview](https://img.shields.io/badge/Season-2026.01-orange)
![Tech](https://img.shields.io/badge/Tech-HTML%20%7C%20CSS%20%7C%20JS-blue)
![AI](https://img.shields.io/badge/AI-Gemini%202.0-green)

## ✨ 주요 기능

### 📊 선수 통계 테이블
- 42명 선수의 상세 기록 조회
- 득점, 어시스트, 리바운드, 스틸, 블록, 3점슛 통계
- 누적/평균 기록 표시
- 팀별 구분 (A, B, C팀)

### 🔍 검색 및 정렬
- 선수 이름으로 실시간 검색
- 모든 컬럼 기준 정렬 (오름차순/내림차순)
- 순위 자동 계산

### 🤖 AI 통계 분석 채팅
- Google Gemini 2.0 기반 AI 채팅
- 득점왕, 어시스트왕 등 부문별 1위 조회
- 선수 비교 및 팀 분석
- 자연어로 통계 질문 가능
- **마크다운 렌더링** (테이블, 리스트, 강조)
- **반응형 디자인** (모바일 최적화)

## 🛠️ 기술 스택

- **Frontend**: Vanilla HTML, CSS, JavaScript (ES Modules)
- **AI**: Google Generative AI (Gemini 2.0 Flash)
- **Data**: JSON 기반 정적 데이터

## 🚀 사용 방법

1. `index.html` 파일을 브라우저에서 열기
2. 테이블에서 선수 통계 확인
3. AI 채팅 사용 시:
   - 우측 하단 채팅 버튼 클릭
   - Gemini API 키 입력 (최초 1회)
   - 자연어로 통계 질문

### AI 채팅 예시 질문
- "득점왕은 누구야?"
- "이민호 선수의 기록 알려줘"
- "A팀 선수들 평균 득점은?"
- "리바운드 1위와 2위 비교해줘"

## 📁 파일 구조

```
nineblockers-cursor/
├── .claude/
│   └── commands/
│       ├── sync-league.md   # 리그 데이터 동기화 커맨드
│       └── sync-docs.md     # 문서 동기화 커맨드
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── feature_request.md  # 기능 요청 템플릿
├── daily_entry/
│   └── team_daily_entry.html   # 팀 데일리 엔트리 페이지
├── index.html               # 메인 애플리케이션 (HTML + CSS + JS 통합)
├── convert_excel_to_json.py # 엑셀→JSON 변환 스크립트
├── config.example.js        # API 설정 예시 파일
├── league_stats_YYYYMM.json # 시즌별 통계 데이터
├── league_metadata_YYYYMM.json # 시즌별 메타데이터
├── metadata_manifest.json   # 메타데이터 매니페스트
├── CLAUDE.md                # Claude 규칙
└── README.md                # 프로젝트 문서
```

## 📥 시즌 데이터 업데이트 방법

매주 새로운 리그 기록이 업데이트되면 엑셀 파일을 JSON으로 변환하여 적용합니다.

### Claude Code 슬래시 커맨드 (권장)

Claude Code CLI에서 `/sync-league` 커맨드를 사용하면 모든 처리가 자동으로 수행됩니다:

```
/sync-league /Users/user/Downloads/2026-01 리그 기록.xlsx
```

**자동 처리 내용:**
1. 파일명에서 시즌 코드 자동 추출 (YYYY-MM → YYYYMM)
2. JSON 파일 생성 (`league_stats_YYYYMM.json`, `league_metadata_YYYYMM.json`)
3. 새 시즌인 경우 `index.html`의 `SEASONS` 배열 자동 업데이트

> **파일명 요구사항:** 파일명에 `YYYY-MM` 형식이 포함되어야 합니다.

### 수동 방법

시즌 코드를 직접 지정하려면 터미널에서 다음 명령어를 사용하세요:

```bash
python3 convert_excel_to_json.py "<엑셀파일경로>" <시즌코드>
```

**예시:**
```bash
python3 convert_excel_to_json.py "/Users/user/Downloads/2026-01-recording.xlsx" 202601
```

**시즌코드 형식:** `YYYYMM` (예: 202601 = 2026년 1월)

수동 방법 사용 시 새 시즌이라면 `index.html`의 `SEASONS` 배열에 시즌 코드를 직접 추가해야 합니다:
```javascript
const SEASONS = ['202701', '202601', '202508', ...];  // 새 시즌을 배열 앞에 추가
```

> **참고:** JSON 파일은 앱 실행 시 자동으로 로딩되므로 별도의 복사 작업이 필요 없습니다.

### 엑셀 파일 요구사항

엑셀 파일은 다음 시트를 포함해야 합니다:
- **전체득점**: 팀, 선수명, 번호, 라운드별 득점, 참석수, 총득점, 평균득점
- **부가기록 계산**: 선수명, 번호, 누적/평균 부가기록(리바운드, 어시스트, 스틸, 블록, 3점슛)

## 📄 문서 동기화

프로젝트 변경사항과 문서가 잘 맞는지 확인하고 자동으로 업데이트합니다.

### Claude Code 슬래시 커맨드

```
/sync-docs
```

**자동 처리 내용:**
1. 프로젝트 파일 구조와 README.md 비교
2. 새로 추가된 파일/커맨드 감지
3. 삭제된 파일 감지
4. README.md 파일 구조 섹션 자동 업데이트

---

## 🎯 프로젝트 개발 과정

### 사용된 프롬프트

이 프로젝트는 Cursor AI를 활용하여 다음과 같은 단계로 개발되었습니다:

#### 1단계: 기본 구조 설계
```
농구 리그 통계를 보여주는 웹 대시보드를 만들어줘.
- 선수 목록과 통계(득점, 어시스트, 리바운드 등)를 테이블로 표시
- 다크 테마로 모던한 UI
- 정렬 및 검색 기능 포함
```

#### 2단계: 데이터 연동
```
JSON 데이터를 읽어서 테이블에 표시해줘.
- 각 통계 항목별로 정렬 가능하게
- 팀별로 다른 색상 뱃지 적용
```

#### 3단계: AI 채팅 기능 추가
```
Gemini API를 연동해서 통계에 대해 자연어로 질문할 수 있는 채팅 기능을 추가해줘.
- 플로팅 버튼으로 채팅 모달 열기
- API 키는 로컬스토리지에 저장
- 리그 데이터를 컨텍스트로 제공해서 통계 관련 질문에만 답변하도록
```

#### 4단계: AI 채팅 가독성 개선
```
채팅 답변의 가독성을 개선해줘.
- 마크다운 렌더링 지원 (테이블, 리스트, 굵은 글씨)
- 좁은 화면/모바일 대응 (반응형 테이블, 가로 스크롤)
- 간결한 답변 형식 유도 (프롬프트 최적화)
```

### 구현 과정

1. **UI/UX 설계**: 다크 테마 기반의 모던한 대시보드 디자인
2. **데이터 구조화**: 선수별 상세 통계를 JSON 형식으로 정리
3. **테이블 기능**: 동적 렌더링, 정렬, 검색 기능 구현
4. **AI 통합**: Gemini API 연동 및 컨텍스트 기반 응답 시스템 구축
5. **반응형 처리**: 모바일 환경 대응
6. **AI 답변 가독성 개선**:
   - 마크다운 파서 구현 (테이블, 리스트, 볼드, 헤더 지원)
   - 반응형 테이블 (가로 스크롤, 최적화된 셀 크기)
   - 프롬프트 엔지니어링으로 간결한 답변 유도

---

### 고도화

1. 모든 리그 기록 통합
2. 모바일 기기에서 더 잘 보이도록 개선
3. AI 채팅 고도화
4. 기록을 고려한 팀 생성(AI 사용)

---

## 📝 라이선스

MIT License

## 👥 기여자

나인블로커스 리그 운영진

