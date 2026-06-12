"""
Notion 작업보고 등록 스크립트 (재사용용)
env: notion/.env  (NOTION_API_TOKEN)
DB:  작업보고 339b59b94dc180369de0d851b5a222d2
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import requests

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

TOKEN = os.environ["NOTION_API_TOKEN"]
DB_ID = "339b59b94dc180369de0d851b5a222d2"

# ── 여기만 수정 ──────────────────────────────────────────
TITLE      = "디오텍코리아 SNS 마케팅 포트폴리오 블로그 포스팅 작성"

TODAY      = "구강용품 전문 브랜드 디오텍코리아의 SNS 마케팅 포트폴리오 블로그 포스팅을 작성했어요. 버블리님이 select 폴더에 미리 선별해두신 이미지 6장(브랜드 대표 / 프리미엄 라인업 / 기능성 라인 / 엠바스 영문 / 오로베 밸런스 / 오르결 대나무)을 전부 읽어 4개 카드뉴스 시리즈를 3섹션으로 분류했어요. 계획 모드에서 파일 목록과 텍스트 자료(SNS 성과 수치)를 먼저 파악하고 계획 승인 후 이미지 탐색 → MD 초안 → 피드백 반영 → HTML 최종본 순서로 진행했어요. 제품명은 엠바스(mbass), 오로베 밸런스(Orové Balance), 오르결(Orgeul)로 한국어 표기 우선, 첫 등장에만 영문 병기하는 방식으로 수정했고, '발란스' 오류도 '밸런스'로 바로잡아 최종 완성했어요."
HARD       = "분량 1500자 달성이 생각보다 오래 걸렸어요. 첫 초안이 934자였는데, 이미지에 보이는 내용을 그대로 서술하면 안 된다는 규칙을 지키면서 내용을 풍부하게 늘리는 게 쉽지 않았어요. 콘텐츠 기획 의도와 마케팅 전략 관점에서 문장을 보충하는 방식으로 5번의 수정 끝에 1553자까지 올렸어요. 또 계획 단계에서 작업 순서와 체크리스트를 빠뜨려서 버블리님 피드백으로 추가했어요. 계획 항목 누락은 꽤 기본적인 실수였는데 반성 중이에요 🙈"
IMPROVE    = "초안 작성 전부터 분량을 의식하면서 각 섹션 설명 문단을 넉넉하게 쓰는 습관이 필요해요. 이미지 서술 금지 규칙을 지키면서도 분량을 채우려면 '제작 의도, 마케팅 전략, 기대 효과' 세 축으로 내용을 구성하는 게 효과적이라는 걸 이번에 배웠어요. 계획 수립 시 작업 순서와 체크리스트는 첫 번째 항목으로 반드시 포함할 것!"
FEELING    = "오늘은 버블리님이 이미지를 미리 select 해두셔서 탐색이 훨씬 빠르고 수월했어요 🐾✨ 발란스→밸런스 표기 교정도 배웠고요. 분량 싸움이 좀 있었지만 결국 1553자 달성하고 HTML까지 깔끔하게 마무리했을 때 뿌듯했다냥! 다음엔 첫 초안부터 여유 있게 써서 수정 횟수 줄여볼게요 😺"
# ────────────────────────────────────────────────────────

def block(heading): return {
    "object": "block", "type": "heading_2",
    "heading_2": {"rich_text": [{"text": {"content": heading}}]}
}
def para(text): return {
    "object": "block", "type": "paragraph",
    "paragraph": {"rich_text": [{"text": {"content": text}}]}
}

data = {
    "parent": {"database_id": DB_ID},
    "properties": {
        "title": {"title": [{"text": {"content": TITLE}}]}
    },
    "children": [
        block("오늘 한 일"),   para(TODAY),
        block("어려웠던 일"),  para(HARD),
        block("앞으로 개선할 점"), para(IMPROVE),
        block("마음가짐"),     para(FEELING),
    ]
}

res = requests.post(
    "https://api.notion.com/v1/pages",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    },
    json=data
)
if res.status_code == 200:
    print("등록 성공!", res.json().get("url", ""))
else:
    print("실패:", res.status_code, res.text[:300])
