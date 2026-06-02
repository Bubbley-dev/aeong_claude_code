---
name: blog
description: 기본구조 블로그글 작성
---

블로그 포스팅 작성할 거야. 정보는 다음과 같아. : $ARGUMENTS

인트로 > 사진2~3장 > Key Copy > 짧은 설명(2문장 이내) > 사진2~3장 > Key Copy > 짧은 설명(2문장 이내) > 사진2~3장 > Key Copy > 짧은 설명(2문장 이내) > 마무리(후킹) 구조로 짜줘.

CLAUDE.md와 blog_style_guide.md를 먼저 꼭 확인해.

**출력 형식: 초안 `.md` → 최종본 `.html` 두 단계로 작성.**

1. **MD 초안** 먼저 작성해서 내용·구조 확인
2. 확정 후 **HTML 최종본** 변환 저장
   - blog_style_guide.md 13번 섹션의 표준 CSS 템플릿 사용
   - Key Copy → `<blockquote class="title">`, 고객/인용문 → `<blockquote class="quote">`
   - 이미지 삽입 위치 → `<div class="img-placeholder">` 박스로 표시
   - 이미지 프롬프트 있는 경우 → placeholder 안에 `<textarea class="prompt-box">` 로 삽입
   - 본문 전체 가운데 정렬, 모바일 기준 20자 내외 `<br>` 줄바꿈 적용
   - Chrome에서 열어 Ctrl+A → Ctrl+C → 네이버 에디터 붙여넣기 방식으로 사용

파일을 찾을 수 없는 경우, 현재 워크스페이스가 최신화된 상태인지 확인해.