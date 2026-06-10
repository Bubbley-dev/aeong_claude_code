---
description: 블로그 본문 글자 수 확인 위젯 (공백 제외, 1500자 목표 프로그레스 바)
---

블로그 포스팅 본문의 글자 수를 확인하는 인터랙티브 위젯을 show_widget으로 생성해줘.

## 본문 텍스트 전처리

$ARGUMENTS 또는 현재 대화에서 본문 텍스트(또는 .md 파일)가 제공된 경우, 아래 항목을 제거한 뒤 textarea에 삽입:
- `# 제목` 형식의 H1 타이틀
- `[이미지 N — ...]` 형식의 이미지 캡션
- `#해시태그` 로 시작하는 해시태그 줄
- 마크다운 볼드 마커 `**` (텍스트 내용은 유지)
- `## ` 소제목 마커 (Key Copy 텍스트는 유지)
- `---` 구분선

텍스트가 없으면 textarea를 빈 상태로 두어 사용자가 직접 붙여넣을 수 있게 함.

## 위젯 HTML

show_widget의 widget_code로 아래를 사용. `{BODY_TEXT}` 자리에 전처리된 텍스트 삽입:

```html
<h2 class="sr-only">블로그 본문 글자 수 확인</h2>
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
  <span style="font-size:13px;color:var(--color-text-secondary);">제목·캡션·해시태그 제외 본문 (공백 제외)</span>
  <span style="font-size:13px;font-weight:500;" id="counter">0자</span>
</div>
<textarea id="body" onclick="this.select()" style="width:100%;box-sizing:border-box;height:420px;font-size:14px;line-height:1.8;resize:vertical;font-family:var(--font-sans);color:var(--color-text-primary);background:var(--color-background-secondary);border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-md);padding:12px 14px;">{BODY_TEXT}</textarea>
<div style="display:flex;align-items:center;gap:12px;margin-top:10px;">
  <div style="flex:1;height:6px;border-radius:3px;background:var(--color-background-secondary);overflow:hidden;">
    <div id="bar" style="height:100%;border-radius:3px;background:var(--color-text-secondary);transition:width 0.2s;"></div>
  </div>
  <span style="font-size:12px;color:var(--color-text-secondary);">목표 1500자</span>
</div>
<script>
const ta=document.getElementById('body');
const counter=document.getElementById('counter');
const bar=document.getElementById('bar');
function update(){
  const len=ta.value.replace(/\s/g,'').length;
  counter.textContent=len.toLocaleString()+'자';
  const pct=Math.min(100,Math.round(len/1500*100));
  bar.style.width=pct+'%';
  bar.style.background=len>=1500?'#1D9E75':len>=1200?'#BA7517':'var(--color-text-secondary)';
  counter.style.color=len>=1500?'#1D9E75':len>=1200?'#BA7517':'var(--color-text-primary)';
}
update();
ta.addEventListener('input',update);
</script>
```

## 색상 기준
- 회색: ~1199자 (부족)
- 주황: 1200~1499자 (거의 도달)
- 녹색: 1500자 이상 (목표 달성)

## loading_messages
`["글자 세는 중...", "공백 빼고 계산 중..."]`
