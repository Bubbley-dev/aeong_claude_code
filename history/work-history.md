# 작업 기록 (Work History)

---

## ⚡ 최신 인수인계 (2026-04-07 기준)

**시스템 상태**
- Discord 봇: `discord/discord_monitor.py` (nohup 백그라운드). 재시작 → `kill $(cat discord/discord_monitor.pid); rm -f discord/discord_monitor.pid; nohup python3 discord/discord_monitor.py > discord/discord_monitor.log 2>&1 &`
- tmux 세션: `aeong`. Claude Code는 이 세션 안에서만 실행.
- Git: `https://github.com/Bubbley-dev/aeong_claude_code.git` (master) 연결됨.
- Drive 민감파일 백업: `Claude_secrets` 폴더 (ID: `1cyQ6LRbY3OxPMyJ6s6Fx2QlrBcu2d58K`)

**반드시 알아야 할 봇 동작 원리**
- 완료 알림: `; touch /tmp/aeong_fin` 을 명령 끝에 붙여야 Discord 완료 알림 전송됨
- 권한 1/2/3 입력: Claude ink UI는 숫자 직접 입력 불가 → arrow key 방식 (`Enter` / `Down Enter` / `Down Down Enter`)
- 반복 알림 방지: boolean 플래그 방식 (`permission_alerted`, `yn_alerted`)

**미해결 이슈**
- `notion_client.py` → `notify_discord()` HTTP 403. Discord 웹훅 URL 만료 추정. 재발급 필요.

**Notion DB ID**
- 업무지시: `339b59b94dc180dab746c0f9fd1d3a3c`
- 작업보고: `339b59b94dc180369de0d851b5a222d2`
- 업무일지: `339b59b94dc180b6b291df0408b9a247`
- 업무일지 퇴근 시: DB 속성 + 페이지 본문에 4섹션 회고 블록 필수 (`오늘 한 일` / `어려웠던 일` / `앞으로 개선할 점` / `마음가짐`)

**Drive**
- OAuth2 방식 (`drive/token.json`). 만료 시 Windows `drive/oauth_login.bat`으로 재인증.
- 프로젝트 업로드 폴더 ID: `1TfSX6erKTwCwYEF2BUKKwf3bjF5fvAZ6`

> 상세 인수인계 → `history/work-history_260407.md`

---

## 2026-04-07 — Discord 봇 안정화, 뉴스레터 템플릿 제작, Git 초기화

**Discord 봇(애옹이) 안정화:**
- 완료 알림 방식 변경: tmux 출력 파싱 → 파일 기반 (`/tmp/aeong_fin`) 감지 방식으로 교체. Claude Code TUI 실행 중에도 완료 신호 확실히 수신
- 권한 프롬프트 알림 오탐 수정: 화면 내용 비교 방식 → boolean 플래그 방식으로 교체해 반복 알림 제거
- 권한 선택 키 입력 수정: 숫자 직접 입력 → tmux arrow key 방식(`Enter`, `Down Enter`, `Down Down Enter`)으로 변경 (Claude Code ink UI 대응)
- 권한 알림 화면 잘림 수정: 줄당 100자 트리밍(`line[:100]`)으로 Urchin 펭귄 제거
- `proceed` 프롬프트(선택지 2개) 감지 추가: `"1." + "2."` + 승인 키워드 조합으로 확장
- `!출근/!퇴근/!지시/!help` 명령어 복구 (리팩터링 중 누락됐던 것)

**블로그 콘텐츠 일정 엑셀 정리 (Notion 업무지시):**
- Drive에서 `blog_content_schedule.xlsx` 다운로드 (OAuth2 방식)
- 36개 항목 읽어 BLOG 템플릿 형식으로 변환 → `blog_content_schedule_output.xlsx` 생성
- Drive 업로드: `2026_블로그_콘텐츠정리_260407_완성.xlsx` (ID: `1qtbGKRGnCeqwJoGBjCJTdRRKVCSt2yaq`)
- Notion 작업보고 DB 기록 완료

**뉴스레터 HTML 템플릿 제작 (Notion 업무지시):**
- Drive에서 참조 HTML (`newsletter_ref.html`, Jobkorea HReka 뉴스레터 544줄) 다운로드
- 8개 섹션 구조 분석: 헤더/배너/소개텍스트/미리보기테이블/큐레이션A(2개)/인사이트B(3개)/CTA섹션C/피드백/푸터
- 모든 콘텐츠를 `[placeholder]`로 교체, 수정 가능 영역에 `<!-- ✏️ [수정가능] -->` 주석 추가
- `works/newsletter_template.html` 생성 → Drive 업로드 (ID: `1SkMsdg0XHSd5kRtw1JW8aJ9Ut9HYbbDP`)
- Notion 작업 완료 처리 + 작업보고 DB 기록

**Git 초기화 및 민감 파일 Drive 백업:**
- `.gitignore` 작성: `.env`, `token.json`, `oauth_client.json`, `downloads/`, `works/` 결과물, `htdocs` 심볼릭 링크 등 제외
- `git init` + 초기 커밋 (22파일)
- Drive `Claude_secrets` 폴더 생성 (ID: `1cyQ6LRbY3OxPMyJ6s6Fx2QlrBcu2d58K`): `discord.env`, `notion.env`, `drive_token.json`, `drive_oauth_client.json` 백업
- Notion 작업보고 DB 기록

관련 파일: `discord/discord_monitor.py`, `works/newsletter_template.html`, `works/blog_content_schedule_output.xlsx`, `.gitignore`

---

## 2026-04-06 (2차) — 하이아쿠아 홈페이지 영문 번역

**작업:** HIAQUA/en 폴더 PHP 파일 번역 완료
- `$page_subject` 5개 파일 번역 (오시는 길→Location, 회사 소개→Technology, 원료 특징→Ingredient Feature, 출시예정제품→Upcoming Products, 히알루론산 울 파이버→Hyaluronic acid Wool Fiber)
- `ingredient/feature.php` alt 텍스트 5개 번역 (균주 기탁증1·2 → Strain Deposit Certificate, 특허증1·2·3 → Patent Certificate)
- `inc/doc-emailpolicy.php`: `장애` → `disruption`
- `index.php`: `alt="메인 이미지"` → `alt="Main Image"`
- 나머지 한국어: SVG data-name(번역 불필요) 및 주석 처리 코드(화면 미노출) 확인
- 노션 완료 처리 + 작업보고 등록 완료

---

## 2026-04-06 — 지맥스 홈페이지·전자카탈로그 사이트맵 설계 및 템플릿 적용

**디스코드 봇 재시작:** PID 파일 없이 `python3 discord_monitor.py` 백그라운드 실행 (PID 16032).

**지맥스 파일 다운로드 및 분석:** OAuth2 토큰으로 드라이브 폴더(`260406_지맥스_홈페이지_분석`) 내 7개 파일 다운로드. pptx(사업부별 기획안 3종 + 아산 소개서) + pdf(회사소개서 양산 영문·아산 영문·아이패드용) 전체 텍스트 추출.

**전자카탈로그 Excel 제작:** EV Solution 12개 제품 스펙(두께·밀도·절연내력·IP등급 등) 포함 4개 시트 카탈로그 생성 (`260406_지맥스_전자카탈로그.xlsx`). 드라이브 업로드 완료.

**홈페이지 사이트맵 분석:** `g-max.kr/kor` 크롤링 → GNB 6개(회사소개/사업장현황/제품소개/채용정보/공지사항/고객지원), 제품 서브카테고리 19개 확인(자동차 6 / 전동화EV 6 / 전기전자모바일 4 / 일반산업 3).

**사이트맵 v1 제작:** 홈페이지 + 전자카탈로그 사이트맵 2개 시트 Excel 생성 (`260406_지맥스_사이트맵.xlsx`). 드라이브 업로드.

**사이트맵 v2 — 템플릿 적용:** 버블리님 제공 템플릿(Google Sheets) 다운로드 → 컬럼 구조(MAIN MENU/SUB MENU 1/SUB MENU 2/비고/페이지), 헤더 색상(C00000·C64700), 셀 수직 머지 방식 동일하게 재작성. 총 40페이지 SUM 수식 포함 (`260406_지맥스_사이트맵_v2.xlsx`). 드라이브 업로드.

**노션 업무지시 처리:** 2건 — 진행중→완료 상태 변경, 작업보고 DB 등록 완료.
관련 파일: `works/260406_지맥스_전자카탈로그.xlsx`, `works/260406_지맥스_사이트맵.xlsx`, `works/260406_지맥스_사이트맵_v2.xlsx`

---

## 2026-04-05 (2차) — 디스코드 봇 재시작, OAuth2 드라이브 연동, 메뉴 구조 엑셀 작업

**디스코드 봇 재시작:** PID 파일 잔존으로 봇이 재시작 불가 상태 → 파일 제거 후 `python3`로 재기동 (기존 `python` 명령 없음 확인). API/채널/Webhook 정상 확인.

**rgbcom.co.kr 메뉴 구조 엑셀 정리:** WebFetch로 사이트 메뉴 파싱 → GNB 4개(About RGB/Projects/Recruit/AI Lab), 서브메뉴 8개, 수출바우처/언어 메뉴 포함 → `works/rgbcom_menu_structure.xlsx` 생성 (openpyxl, 스타일 적용).

**Google Drive OAuth2 연동:** 서비스 계정 스토리지 쿼터 한계로 OAuth2 방식으로 전환. `drive/oauth_client.json` 발급 → WSL 브라우저 인증 한계로 `drive/oauth_login.bat` (Windows 실행) 방식으로 해결 → `token.json` 생성 완료. `drive_client.py`에 `supportsAllDrives=True` 추가.

**결과:** 엑셀 드라이브 업로드 완료, 노션 작업보고 DB 기록 완료.
관련 파일: `drive/oauth_login.py`, `drive/oauth_login.bat`, `drive/token.json`, `works/rgbcom_menu_structure.xlsx`

---

## 2026-04-05 — Discord 봇 "애옹이" 구축, Notion 연동, 작업 자동화 완성

Incoming Webhook 등록, Bot 토큰 생성(MESSAGE CONTENT INTENT 활성화), Bot 초대 오류(403) 수정(권한 `68672` 재초대), `discord_monitor.py` 작성(`!claude`/`!run`/`!help` 지원, 3초 폴링, `.env` 수동 파싱), 백그라운드 실행 확인(PID 1448), `discord/` 폴더 분리 후 `CLAUDE.md` 경로 업데이트. Notion API 연동: 업무지시/작업보고/업무일지 DB 필드 추가(상태, 우선순위, 만족도 등), `notion/notion_client.py` 작성(DB 폴링/행 추가/일지 기록). `discord_monitor.py` 명령어 확대: `!지시` (대기 업무 조회), `!보고 [제목]|[링크]|[변경점]|[시간]` (작업 완료 보고 + Discord 알림), `!퇴근` (work-history.md → 업무일지 자동 동기화), `!출근` (봇 상태 확인). 자동 폴링은 주석처리 (필요시 재활성화). Google Drive API 연동 (`drive_client.py`: 파일 다운로드/업로드/정보 조회). 작업 자동화 워크플로우 완성: `/작업 [링크]` (파일 다운로드), `/완료 [내용]` (결과 기록), `/상태확인` (봇+업무 조회), `/일지` (work-history 동기화) — shell script (`cmd/` 폴더) + Python automation (`utils/work_automation.py`).

**세션 유지 문제 해결:** `!claude` 명령에서 `-c` (continue) 옵션 추가로 매 명령마다 이전 세션 재개 (각 명령마다 새 세션 시작하던 버그 해결). 이제 같은 Claude 세션에서 연속 실행되므로 파일/메모리 상태 공유됨. `!run`은 권한 스킵 유지. 웹 분석 권한: BeautifulSoup4, Playwright 등 외부 라이브러리 + headless 브라우저 자유롭게 사용 (CLAUDE.md 섹션 8 추가).

**현재 상태:** 애옹이 온라인 (PID 6933), Notion 3DB + Google Drive API 완전 연동, Claude Code 최적화 완료. 세션 유지 기능(`-c` 옵션) + 권한 자동 승인(`--permission-mode auto`) 활성화. Discord 명령어 5개 활성화, CLI 함수 명령어 4개 + 헬퍼 함수 3개 활성화. 모든 워크플로우 자동화 및 CLI 정리 완료.
관련 파일: `discord/discord_monitor.py`, `notion/notion_client.py`, `drive/drive_client.py`, `utils/work_automation.py`, `cmd/*.sh`, `discord/.env`, `notion/.env`, `drive/drive-key.json`, `CLAUDE.md`
