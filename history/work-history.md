# 작업 기록 (Work History)

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
