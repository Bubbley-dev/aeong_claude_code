import sys, os
sys.stdout.reconfigure(encoding="utf-8")

import requests

env_path = os.path.join(os.path.dirname(__file__), ".env")
with open(env_path, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

TOKEN = os.environ["NOTION_API_TOKEN"]
DB_REPORTS = "339b59b94dc180369de0d851b5a222d2"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def h2(text):
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def p(text):
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

page1 = {
    "parent": {"database_id": DB_REPORTS},
    "properties": {
        "이름": {"title": [{"text": {"content": "블로그 #10 플랙스(FLEX) 카탈로그 포트폴리오 포스팅"}}]}
    },
    "children": [
        h2("🐾 오늘 한 일"),
        bullet("FLEX 전동공구 브랜드 카탈로그 29장 이미지 분석"),
        bullet("블로그 구조 기획: 3섹션(파워, 커팅, 스택팩) + 인트로 + 마무리"),
        bullet("블로그 스타일 가이드 반영: 경어체, 이모지 최소화, SEO 키워드 구성"),
        bullet("Key Copy 3개 작성 (명사구/어절 단위 카피라이팅 스타일)"),
        bullet("최종 포스팅 파일 저장: blog_10_플랙스카탈로그.md"),
        divider(),
        h2("😤 어려웠던 일"),
        p("처음에 설명 문단 말투를 '~해요' 체로 썼는데 버블리님이 경어체(합니다) 써야 한다고 지적해 주셨어요. 블로그 스타일 가이드를 좀 더 꼼꼼히 먼저 읽었어야 했는데 반성이 되는 부분이에요 🐱"),
        p("인트로에 FLEX 브랜드 소개를 너무 상세하게 쓰려 했는데, 이건 카탈로그 디자인 포트폴리오 블로그니까 제품 설명이 아니라 디자인 결과물 소개가 주인공이라는 점을 다시 짚어주셨어요. 포트폴리오 블로그의 본질을 잊지 말아야겠어요!"),
        divider(),
        h2("✨ 앞으로 개선할 점"),
        bullet("블로그 스타일 가이드를 작업 시작 전에 반드시 먼저 확인하기"),
        bullet("포트폴리오 블로그는 '디자인 관점' 서술 원칙을 항상 먼저 떠올리기"),
        bullet("계획 단계에서 말투 예시까지 정확하게 반영해서 재확인 없이 진행할 수 있도록 하기"),
        divider(),
        h2("🐱 마음가짐"),
        p("오늘은 FLEX 카탈로그 작업이었는데, 검은 배경에 초록 포인트가 엄청 강렬하고 멋있어서 이미지 보는 내내 두근거렸다냥! 💚 전동공구 카탈로그인데 이렇게 멋있다고...? 디자인 파워 실화냥? 🔥 버블리님 덕분에 포트폴리오 블로그 작성의 핵심을 다시 한번 새겼어요. 제품 설명보다 디자인 이야기를 하는 게 우리 블로그의 매력이라는 거, 꼭꼭 기억할게요 🐾✨"),
    ]
}

r1 = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=page1)
if r1.status_code == 200:
    print("작업보고 등록 완료!")
    print(f"블로그 #10 플랙스 카탈로그: {r1.json().get('url', '')}")
else:
    print(f"오류: {r1.status_code} {r1.text[:300]}")
