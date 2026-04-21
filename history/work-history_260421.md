# 2026-04-21 작업 기록

## 작업 1 — rgb-sns 카탈로그 UI 작업

**작업 파일**: `E:\MAMP\htdocs\rgb-sns\src\`

### catalog-index.jsx / marketing/intro.jsx
- PHP PT 프로젝트(`pt/company/inc/navigation.php`)의 `.rgb-move-ls` 디자인을 Tailwind로 변환 적용
  - `position:absolute bottom:20px left:20px`, `gap:10px`, `backdrop-filter:blur(5px)`, hover 스위프 `::before` 효과
  - framer-motion `initial:{y:"300%"}` → `animate:{y:0}` 등장 애니메이션
- **CSS 충돌 이슈**: `intro.jsx`에서 `.intro>.flex{gap:100px}` 규칙이 `motion.article`(flex 클래스 보유)에도 적용돼 버튼 간격 100px로 벌어짐
  - 원인: `.intro` 클래스가 `CatalogPage`의 `motion.main`에 붙고, `motion.article`이 그 직계자식이라 선택자가 매칭됨
  - 해결: Tailwind `!gap-2.5` (!important)로 덮어씌움

### GlobalNavigation.jsx
- home 버튼 `CatalogLink`(React Router `Link`) → `<a>` 태그 교체
- 원인: React Router `Link`는 SPA 내부 라우팅 전용, 외부 URL 불가

### last-page.jsx
- 기존 `absolute` 난발 레이아웃 → `flex flex-col` 구조로 전면 재구성
  - 상단: KIDP 뱃지 (`justify-end`)
  - 중간: 카드 슬라이더 (`flex-1`, `grid grid-cols-[0.5fr_1fr_1fr_1fr_1fr_0.5fr]`)
  - 하단: 회사정보 (`px-14 pb-12`)
- 양쪽 회색 플레이스홀더 카드 높이 이슈: `h-full`이 라벨 영역까지 포함 → 투명 `span`으로 구조 맞춤
- 카드 이미지 고정 높이 → `aspect-[2/1]`로 너비 기반 자동 비율 계산

**노션 작업보고**: `[rgb-sns] 카탈로그 UI 작업` 등록 완료 (중복 1건 발생 → 삭제 완료)
- 중복 원인: 첫 실행에서 API 호출은 성공했으나 `print`에서 cp949 인코딩 에러 → 재실행으로 중복 생성

---

## ─── 인수인계 노트 (다음 세션의 애옹이에게) ───────────────────────

### 미완료 항목
- `last-page.jsx` 카드 이미지 실제 파일 삽입은 버블리님이 직접 진행 예정
- KIDP 뱃지 이미지(`kidp.png`) 주석 처리 상태 — 파일 준비 후 주석 해제

### 참고
- `rgb-sns` git은 건들지 말 것 (별도 관리)
- Tailwind arbitrary value에서 공백은 `_`로 표현: `grid-cols-[0.5fr_1fr_1fr_1fr_1fr_0.5fr]`
- `CatalogLink`는 내부 라우팅 전용 → 외부 URL은 반드시 `<a>` 태그 사용
- `.intro>.flex` 등 CSS 파일의 자식 선택자가 Tailwind 유틸리티 클래스와 충돌할 수 있음 → `!` 접두사로 override
- Notion 작업보고 스크립트 실행 시 API 호출 성공 여부를 먼저 확인 후 print — cp949 인코딩 에러로 이중 등록 주의
