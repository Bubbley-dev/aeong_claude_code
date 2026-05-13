import sys
sys.path.insert(0, r'E:\김세희\aeong_claude_code')
from notion.notion_client import add_report

reports = [
    {
        "title": "특허영상 제안서 작성 — 주식회사 셀라메스 (전기적 비파괴 실시간 세포 모니터링 장치)",
        "link": "",
        "changes": "PDF 특허(pymupdf 우회 추출) + HWP 기업요구사항 분석. 고객니즈도출/서비스내용(3D모델링·시뮬레이션)/기대효과 작성. 분량 피드백 반영하여 문장 축약.",
        "hours": 2.0
    },
    {
        "title": "특허영상 제안서 작성 — 주식회사 우보테크 (차량용 도어 래치 E-Latch)",
        "link": "",
        "changes": "PDF 특허(단일 모터 록/언록+오픈 메커니즘) + HWP 기업요구사항 분석. 고객니즈도출/서비스내용(3D모델링·시뮬레이션)/기대효과 작성. 글로벌 OEM 타겟 방향 반영.",
        "hours": 1.5
    }
]

for r in reports:
    result = add_report(r["title"], r["link"], r["changes"], r["hours"])
    status = "✅ 성공" if result else "❌ 실패"
    print(f"{status}: {r['title'][:40]}...")
