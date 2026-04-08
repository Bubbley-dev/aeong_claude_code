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
- GitHub 커밋 완료 (push는 인증 설정 후 필요)
- Drive 업로드 완료 (ID: 1jTee7ufGFctFrQ0orgD8IYn31EY7ngSb)

**수동 작업 항목**:
- 표 행 수 변동 시 수동 수정
- 포트폴리오 링크 하이퍼링크 설정

## 퇴근 처리

- 노션 업무일지 DB 속성 업데이트 (작업 2건, 만족도 4)
- 업무일지 페이지 본문 4섹션 회고 블록 작성 완료
- GitHub push 완료 (PAT 인증)

---

## ─── 인수인계 노트 (다음 세션의 애옹이에게) ───────────────────────

안녕 내일의 나. 오늘 두 가지 자동화 기반 작업했어.

### 오늘 생성한 것들

- `blog/blog_style_guide.md` — 알지비커뮤니케이션즈 블로그 스타일 가이드 (13섹션)
- `proposal/proposal_template.pptx` — 특허제안서 PPT 템플릿 ({{placeholder}} 방식)
- `proposal/fill_template.py` — JSON → PPT 자동 생성 스크립트
- `proposal/proposal_guide.md` — 작업 가이드 (자동화 가능/수동 항목 구분)

### 시스템 현재 상태

- **GitHub**: PAT가 remote URL에 포함됨. `git push origin master` 바로 가능.
- **Discord 웹훅**: 403 미해결. `discord/.env`의 `DISCORD_WEBHOOK_URL` 교체 필요.
- **Drive 인증**: OAuth2 token.json 방식. drive_client.py는 서비스 계정 방식이라 직접 사용 금지.

### 다음 작업 예상

- fill_template.py 실제 사용 테스트 (버블리님이 HWP+이미지 9장 주면)
- drive_client.py OAuth2 리팩토링
- Discord 웹훅 URL 재발급 요청
