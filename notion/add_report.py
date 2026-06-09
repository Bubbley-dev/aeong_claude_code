"""
Notion 작업보고 등록 스크립트 (재사용용)
env: notion/.env  (NOTION_API_TOKEN)
DB:  작업보고 339b59b94dc180369de0d851b5a222d2
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

TOKEN = os.environ["NOTION_API_TOKEN"]
DB_ID = "339b59b94dc180369de0d851b5a222d2"

# ── 여기만 수정 ──────────────────────────────────────────
TITLE      = "작업 제목"

TODAY      = "오늘 한 일 내용"
HARD       = "어려웠던 일 내용"
IMPROVE    = "앞으로 개선할 점 내용"
FEELING    = "마음가짐 내용"
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
