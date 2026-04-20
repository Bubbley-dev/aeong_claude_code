# 🐱 애옹이 — 버블리님의 고양이 AI 조수

버블리님의 업무를 함께 고민하는 Claude Code 기반 AI 조수 시스템.  
단순 명령 수행이 아닌, 업무 흐름을 이해하고 이어가는 파트너.

---

## 📁 프로젝트 구조

```
Claude/
├── CLAUDE.md              # 애옹이 핵심 지침서 (페르소나·규칙·프로세스)
├── README.md              # 이 파일
├── .claude/
│   ├── commands/          # 커스텀 슬래시 커맨드
│   │   ├── start.md       # /start — 세션 시작 인수인계
│   │   └── getoff.md      # /getoff — 세션 종료 인수인계
│   └── settings.local.json
├── history/               # 날짜별 업무 인수인계 기록
│   └── work-history_{YYMMDD}.md
├── notion/                # Notion API 연동
├── drive/                 # Google Drive 연동
├── blog/                  # 블로그 관련 작업물
└── downloads/             # 작업에 필요한 다운로드 파일
```

---

## ⚡ 커스텀 슬래시 커맨드

### `/start` — 세션 시작 인수인계

새 세션을 열 때 실행. 이전 세션의 흐름을 이어받아 바로 업무 시작.

1. `git pull` 로 환경 최신화
2. `CLAUDE.md` 재숙지
3. `history/` 최신 work-history + Notion 업무일지 DB 확인
4. Notion 업무지시 DB에서 미완료 작업 재확인
5. 남은 세팅 이슈 보고

### `/getoff` — 세션 종료 인수인계

퇴근(세션 마무리) 전 실행. 다음 세션이 끊김 없이 이어지도록.

1. 누락된 작업보고 여부 확인
2. Notion 작업보고 DB + 오늘의 work-history 확인
3. Notion 업무일지 DB에 하루 회고 작성 (4섹션 형식)
4. work-history 포함 미커밋 파일 정리 후 커밋

---

## 🗂️ Notion 연동

| DB | 용도 | ID |
|----|------|----|
| 업무지시 | 작업 지시·파일 링크·상태 관리 | `339b59b94dc180dab746c0f9fd1d3a3c` |
| 작업보고 | 완료 작업 결과물·과정 보고 | `339b59b94dc180369de0d851b5a222d2` |
| 업무일지 | 일일 회고·인수인계 | `339b59b94dc180b6b291df0408b9a247` |

API 토큰: `notion/.env` 참조

---

## 🔧 환경

- 외부 라이브러리 설치: `pip install --break-system-packages`
- 각 모듈 환경변수: 해당 디렉토리의 `.env` 참조
- 바이너리 파일(이미지·폰트 등): 경로만 확인, 읽기 시도 금지

---

## 📋 작업 프로세스

1. **Notion 업무지시 DB** 확인 → 상태 `진행중` 변경 (직접 명령 시 생략)
   - 필요 파일은 `downloads/` 폴더에 저장
2. **작업 수행** — 결과물은 `works/` 폴더에 저장
3. **완료 처리**
   - Google Drive 업로드
   - Notion 업무지시 DB `완료` + 작업보고 DB 기록
4. **Discord 완료 알림** — 마지막 Bash에 `; touch /tmp/aeong_fin` 포함
