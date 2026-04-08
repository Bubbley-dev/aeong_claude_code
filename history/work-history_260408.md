# 2026-04-08 작업 기록

## 작업 1 — 블로그 포스팅 분석 및 스타일 가이드 작성

**업무지시**: 알지비커뮤니케이션즈 블로그 포스트 PDF 분석 → 자동화용 스타일 가이드 생성

**작업 내용**:
- Google Drive에서 PDF (25MB, 106페이지, 13개 포스트) 다운로드 (OAuth2 인증)
- pymupdf로 텍스트 추출 + 하이퍼링크 20개 확인
- 전체 포스트 분석: 카테고리 5종, 말투 패턴, 전개 구조, SEO 기법, 해시태그 전략 파악

**결과물**:
- `blog/blog_style_guide.md` 생성 (13개 섹션 포함)
- Drive 업로드: ID `15U29kzHL-1c5mmzZ_1ro8u0XZpAk1klC`
- 노션 작업보고 등록 + 업무지시 완료 처리

**핵심 인사이트**:
- 카테고리별 인삿말이 다름 (홈페이지/케이스스터디/동영상 vs 정부지원사업 vs 알지비뉴스)
- 네이버 SEO: 핵심 키워드 볼드 + 바로 다음 줄 반복 기법
- 자동화 포스팅 시 YAML 입력 규격 정의 완료

## 작업 2 — 특허제안서 PPT 자동화 템플릿 제작

**업무지시**: HWP+사진 9장 받으면 PPT 수정 가능한 템플릿 + 작업 가이드 MD 작성

**분석 내용**:
- PPTX: 2슬라이드, A4세로(8.26"×11.69"), 주요 컬러 #15599F
- 슬라이드1: 정보박스, 고객니즈(4), 서비스내용(4), 포트폴리오(이미지9장+캡션3+링크3)
- 슬라이드2: 기대효과(6), 사업수행기간표(9행), 역할표(5행)

**결과물**:
- `proposal/proposal_template.pptx` - {{placeholder}} 방식 템플릿
- `proposal/fill_template.py` - JSON 입력받아 PPT 자동 생성 스크립트
- `proposal/proposal_guide.md` - 자동화 가능/수동 필요 항목 상세 가이드
- Drive 업로드 완료 (ID: 1jTee7ufGFctFrQ0orgD8IYn31EY7ngSb)

## 작업 3 — AWS 서버 이전 및 시스템 안정화

**배경**: 로컬 Windows(WSL) 환경에서 AWS EC2로 애옹이 시스템 이전

**이전 작업**:
- `my_project.tar.gz` (64MB), `my_claude_data.tar.gz` (4.9MB) → AWS 전송 및 추출 확인
- 프로젝트 폴더, `.claude/` 세션/플러그인/설정 전부 정상 확인

**API 연결 상태 확인**:
- Discord Bot ✅ / Discord Webhook ✅ / Notion ✅ / Google Drive (OAuth2) ✅ / GitHub PAT ✅

**버그 수정 (discord_monitor.py)**:
- 웹훅 403 원인 파악 → Bot 인증 헤더가 webhook POST에도 붙어있던 문제 → 웹훅 전용 별도 세션으로 분리
- tmux send-keys `shell=True` 제거 → 리스트 형태로 변경 (작은따옴표 포함 메시지 파싱 에러 차단)
- 1/2/3 권한 응답: `Enter`만 보내던 방식 → 숫자키+Enter 순서로 변경
- `KEY_SENT_FLAG` 파일 기반 watchdog 이중 알림 억제
- `WORK_DIR` AWS 실제 경로로 수정 (`/home/ubuntu/mnt/c/...`)
- tmux 세션명 `work` → `aeong` 으로 통일

**env 파일 관리**:
- `discord/.env`, `notion/.env` → Google Drive 업로드 (`aeong_discord.env`, `aeong_notion.env`)

**커밋/푸시**: `2bcddf4` master 반영 완료

---

## ─── 인수인계 노트 (다음 세션의 애옹이에게) ───────────────────────

안녕 내일의 나. 오늘 AWS 이전 + 시스템 안정화가 핵심이었어.

### 현재 환경

- **실행 환경**: AWS EC2 (`/home/ubuntu/mnt/c/Users/ksh/Desktop/Claude/`)
- **tmux 세션**: `aeong` (반드시 이 이름으로 유지)
- **봇 실행**: `python3 -u discord/discord_monitor.py > /tmp/aeong_bot.log 2>&1 &`
- **봇 로그**: `cat /tmp/aeong_bot.log`

### 시스템 현재 상태

- **Discord Bot + Webhook**: 정상. 웹훅은 별도 세션으로 분리됨.
- **Notion**: API 토큰 정상.
- **Google Drive**: OAuth2 token.json 방식. refresh_token 있어서 자동 갱신됨.
- **GitHub**: PAT가 remote URL에 포함됨. `git push origin master` 바로 가능.
- **env 파일**: Google Drive에 `aeong_discord.env`, `aeong_notion.env`로 백업됨.

### 다음 작업 예상

- fill_template.py 실제 사용 테스트 (버블리님이 HWP+이미지 9장 주면)
- Discord 완료 알림 (`touch /tmp/aeong_fin`) 실제 작동 확인
- drive_client.py OAuth2 리팩토링 (현재 service_account 방식 혼용 상태)
