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
TITLE      = "AU 케이스스터디 블로그 포스팅 작성"

TODAY      = "레이더 센서 전문기업 AU의 케이스스터디 블로그 포스팅을 작성했어요. 카탈로그(2022.12) → 홈페이지(2023.06) → CI(2023.12)까지 이어진 통합 브랜딩 사례를 소개하는 내용이에요. 이미지 파일 전체(카탈로그 4장, 홈페이지 디자인 21장, CI 가이드라인 28장+목업) 탐색하고, 실제 홈페이지(au-sensor.com)도 Chrome에서 직접 열어 전 페이지 확인했어요. MD 초안 작성 후 버블리님 피드백 반영(순서 언급 제거, SEO 제목 수정, 인사이트 키워드 균등 처리) 거쳐서 HTML 최종본까지 완성했어요."
HARD       = "CI 가이드라인에서 Roboto·Noto Sans KR이 지정 폰트였는데, 실제 홈페이지에는 Poppins·Pretendard가 적용되어 있었어요. '폰트까지 일관성 있게 적용됐다'고 쓰면 안 되겠다 싶어서 JavaScript로 실제 CSS 폰트를 확인한 뒤 로고와 컬러 측면의 브랜드 일관성만 서술하는 방향으로 조정했어요. 또 제목에서 '케이스스터디'처럼 검색 안 되는 키워드를 냅다 나열해버렸는데, 스타일가이드 패턴을 다시 확인하고 SEO 키워드 하나 + 핵심 가치 서술 구조로 고쳤어요."
IMPROVE    = "제목 패턴(SEO 키워드 하나, 핵심 가치 서술)을 처음부터 스타일가이드 예시와 대조하면서 작성하면 수정 왕복을 줄일 수 있어요. SEO 인사이트에서 굵기 처리 키워드도 모든 서비스 유형에 균등하게 적용하는 것 기억하기! 그리고 HTML 완성 후 미리보기 굳이 실행 안 해도 된다는 것도 이번에 배웠어요."
FEELING    = "이미지를 50장 넘게 다 읽으면서 AU 브랜드가 어떻게 완성되어 왔는지 따라가는 과정이 진짜 재밌었다냥 🐾 특히 홈페이지 디자인 시안에는 텍스트 로고였는데 실제 홈페이지에 CI 로고가 딱 박혀있는 거 발견했을 때 '아 이게 케이스스터디의 포인트구나!' 하고 뿌듯했어요 ✨ 폰트 불일치는 조금 당황했지만 JavaScript로 직접 확인해서 정확하게 판단할 수 있었던 게 좋았어요!"
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
