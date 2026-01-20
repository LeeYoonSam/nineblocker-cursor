---
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
description: 프로젝트 변경사항과 문서의 동기화 상태를 확인하고 자동으로 업데이트합니다.
---

# 문서 동기화 (sync-docs)

프로젝트의 실제 구조와 문서(README.md)의 싱크를 맞추고, 누락된 문서화를 자동으로 업데이트합니다.

## 분석 대상

1. **README.md** - 메인 프로젝트 문서
2. **CLAUDE.md** - Claude 관련 규칙 (변경 시에만)
3. **.claude/commands/** - 슬래시 커맨드 목록

## 실행 단계

### 1단계: 현재 프로젝트 상태 분석

다음 명령어들을 실행하여 프로젝트 현황을 파악:

```bash
# 프로젝트 루트의 주요 파일 목록
ls -la

# 모든 커맨드 파일 확인
ls -la .claude/commands/

# 최근 커밋 내역 (문서 업데이트 이후 변경사항 파악)
git log --oneline -20

# 시즌 데이터 파일 목록
ls -la league_stats_*.json league_metadata_*.json 2>/dev/null
```

### 2단계: README.md 파일 구조 섹션 비교

README.md의 `📁 파일 구조` 섹션을 읽고 실제 파일과 비교:

**확인할 항목:**
- [ ] 새로 추가된 파일이 문서에 누락되었는지
- [ ] 삭제된 파일이 문서에 여전히 남아있는지
- [ ] 새로운 커맨드가 문서화되었는지
- [ ] 시즌 데이터 파일 목록이 최신인지

### 3단계: 불일치 항목 보고

발견된 불일치 항목을 다음 형식으로 보고:

```
## 📋 문서 동기화 분석 결과

### ✅ 동기화됨
- [항목들...]

### ⚠️ 업데이트 필요
| 항목 | 현재 상태 | 필요 조치 |
|------|----------|----------|
| ... | ... | ... |

### ❓ 확인 필요
- [사용자 확인이 필요한 항목들...]
```

### 4단계: 자동 업데이트 실행

사용자 확인 후, 다음 항목들을 자동 업데이트:

#### 4-1. 파일 구조 섹션 업데이트

README.md의 `📁 파일 구조` 섹션을 실제 프로젝트 구조에 맞게 업데이트.

**포함할 파일/폴더:**
- `.claude/commands/` - 모든 커맨드 파일
- `.github/` - GitHub 관련 설정
- `*.html` - 메인 애플리케이션
- `*.py` - 스크립트 파일
- `*.json` - 데이터 파일 (최신 2-3개 시즌만 표시, 나머지는 "..." 처리)
- `*.md` - 문서 파일

**제외할 파일:**
- `.DS_Store`, `.gitignore` 등 시스템 파일
- `config.local.js` 등 로컬 설정 파일

#### 4-2. 커맨드 문서화 확인

새로운 커맨드가 있다면 README.md에 사용법 추가:
- `/sync-league` - 이미 문서화됨
- `/sync-docs` - 문서화 필요시 추가

#### 4-3. 시즌 배지 업데이트

README.md 상단의 시즌 배지가 최신 시즌을 반영하는지 확인:
```markdown
![Preview](https://img.shields.io/badge/Season-2026.01-orange)
```

### 5단계: 결과 보고

업데이트 완료 후 변경 내역 요약:

```
## ✅ 문서 동기화 완료

### 변경된 파일
- README.md: 파일 구조 섹션 업데이트

### 변경 내용
1. [구체적인 변경 내용...]

### 권장 사항
- [추가로 검토가 필요한 항목...]
```

## 자동 업데이트 규칙

### 파일 구조 템플릿

```
nineblockers-cursor/
├── .claude/
│   └── commands/
│       ├── sync-league.md   # 리그 데이터 동기화 커맨드
│       └── sync-docs.md     # 문서 동기화 커맨드
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── feature_request.md  # 기능 요청 템플릿
├── index.html               # 메인 애플리케이션
├── convert_excel_to_json.py # 엑셀→JSON 변환 스크립트
├── league_stats_YYYYMM.json # 시즌별 통계 데이터
├── league_metadata_YYYYMM.json # 시즌별 메타데이터
├── CLAUDE.md                # Claude 규칙
└── README.md                # 프로젝트 문서
```

## 주의사항

- README.md의 다른 섹션(기능 설명, 사용 방법 등)은 수정하지 않음
- 사용자의 커스텀 내용이 있을 수 있으므로, 큰 변경은 확인 후 진행
- 커밋은 자동으로 하지 않음 (사용자가 `/commit` 또는 "커밋해줘"로 별도 요청)
