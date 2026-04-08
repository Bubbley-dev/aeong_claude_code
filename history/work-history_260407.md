# 2026-04-07 작업 상세 기록

---

## ─── 인수인계 노트 (다음 세션의 애옹이에게) ───────────────────────

안녕 내일의 나. 오늘 꽤 많은 걸 정비했으니 빠르게 파악하고 시작해.

### 시스템 현재 상태

- **Discord 봇**: `discord/discord_monitor.py` 실행 중. 재시작 필요 시 →
  ```bash
  cd /mnt/c/Users/ksh/Desktop/Claude/discord
  kill $(cat discord_monitor.pid) 2>/dev/null; rm -f discord_monitor.pid
  nohup python3 discord_monitor.py > discord_monitor.log 2>&1 &
  ```
- **tmux 세션**: `aeong` 이름으로 실행. Claude Code는 이 세션 안에서만 돌린다.
- **Git**: `https://github.com/Bubbley-dev/aeong_claude_code.git` 연결 완료 (master)
- **민감 파일**: git 제외. Drive `Claude_secrets` 폴더(ID: `1cyQ6LRbY3OxPMyJ6s6Fx2QlrBcu2d58K`)에 백업됨.

### Discord 봇 핵심 동작 방식 (오늘 안정화된 부분)

1. **완료 알림**: tmux 화면 파싱 방식은 신뢰 불가 → `/tmp/aeong_fin` 파일 존재 여부로 감지. Claude 명령에 `; touch /tmp/aeong_fin` 꼭 붙여야 알림 옴.
2. **권한 프롬프트 감지**: `line[:100]` 트리밍(펭귄 제거) + `"1." + "2."` 조합 + 승인 키워드. boolean 플래그로 반복 알림 방지.
3. **1/2/3 키 전달**: Claude Code ink UI는 숫자 입력 안 됨 → `Enter` / `Down Enter` / `Down Down Enter` arrow key 방식.
4. **반복 알림 방지**: `permission_alerted`, `yn_alerted` 플래그. 조건 사라지면 자동 리셋.

### Notion DB 구조

| DB | ID | 용도 |
|---|---|---|
| 업무지시 | `339b59b94dc180dab746c0f9fd1d3a3c` | 버블리님이 직접 작성. `대기중` 상태 항목 폴링 |
| 작업보고 | `339b59b94dc180369de0d851b5a222d2` | 작업 완료 시 `add_report()` 로 행 추가 |
| 업무일지 | `339b59b94dc180b6b291df0408b9a247` | 일 단위. `upsert_daily_log()` + 페이지 본문에 4섹션 회고 블록 작성 필수 |

**업무일지 회고 4섹션 필수**: `오늘 한 일` / `어려웠던 일` / `앞으로 개선할 점` / `마음가짐`
DB 속성(요약, 건수)만 채우는 거 부족함 — 반드시 페이지 본문 블록으로 작성.

### Google Drive

- 인증 방식: OAuth2 (`drive/token.json`). 서비스 계정(`drive-key.json`) 없음.
- 토큰 만료 시 Windows에서 `drive/oauth_login.bat` 실행해서 재인증.
- 프로젝트 폴더 ID: `1TfSX6erKTwCwYEF2BUKKwf3bjF5fvAZ6` (주요 작업물 업로드 대상)

### Discord 웹훅 403 미해결

`notion_client.py`의 `notify_discord()` 함수에서 HTTP 403. 봇 자체 webhook URL 만료된 것으로 추정. Discord 서버 설정에서 웹훅 재발급 후 `discord/.env`의 `DISCORD_WEBHOOK_URL` 교체 필요.

### 작업 시작 전 체크리스트

```
1. history/work-history.md 최신 항목 확인
2. Notion 업무지시 DB `대기중` 항목 확인 (!지시 또는 notion_client.get_pending_tasks())
3. tmux aeong 세션 + 봇 프로세스 살아있는지 확인
4. 작업 완료 후: Drive 업로드 → Notion 작업보고 → work-history_{날짜}.md 기록
```

---

## 작업 1 — Discord 봇 안정화

- 완료 알림: `/tmp/aeong_fin` 파일 기반 감지로 교체
- 권한 프롬프트: boolean 플래그 + 줄 트리밍 적용
- 키 입력: arrow key 방식으로 변경
- `proceed` 2지선다 감지 추가
- `!출근/!퇴근/!지시/!help` 복구

## 작업 2 — 블로그 콘텐츠 일정 엑셀 정리

- Drive에서 `blog_content_schedule.xlsx` 다운로드
- 36개 항목 → BLOG 템플릿 형식 변환
- Drive 업로드: `2026_블로그_콘텐츠정리_260407_완성.xlsx` (ID: `1qtbGKRGnCeqwJoGBjCJTdRRKVCSt2yaq`)
- Notion 업무지시 완료 처리 + 작업보고 등록

## 작업 3 — 뉴스레터 HTML 템플릿 제작

- 참조: Jobkorea HReka 뉴스레터 (`newsletter_ref.html`, 544줄)
- 8섹션 구조화, 전체 내용 `[placeholder]` 교체, `<!-- ✏️ [수정가능] -->` 주석 추가
- `works/newsletter_template.html` 생성
- Drive 업로드 (ID: `1SkMsdg0XHSd5kRtw1JW8aJ9Ut9HYbbDP`)
- Notion 업무지시 완료 처리 + 작업보고 등록

## 작업 4 — Git 초기화 및 Drive 민감파일 백업

- `.gitignore` 작성 (env/token/결과물/htdocs 제외)
- `git init` → 초기 커밋 → GitHub push (`Bubbley-dev/aeong_claude_code`)
- Drive `Claude_secrets` 폴더에 env 4종 백업
- `README.md` 작성 (부팅 절차 + 새 컴퓨터 세팅 가이드)
- Notion 작업보고 등록
