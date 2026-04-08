#!/usr/bin/env python3
"""
Notion API 헬퍼 모듈
- 업무지시 DB 폴링
- 작업보고 DB 행 추가
- 업무일지 DB 행 생성/수정
"""

import os
import json
import requests
import urllib.request
from datetime import datetime, date
from typing import Optional, Dict, List

# 환경변수 로드 (notion/.env + discord/.env 모두 읽기)
def _load_env(path):
    if os.path.exists(path):
        with open(path) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())

_base = os.path.dirname(__file__)
_load_env(os.path.join(_base, ".env"))
_load_env(os.path.join(_base, "..", "discord", ".env"))

NOTION_TOKEN = os.environ.get("NOTION_API_TOKEN")

# DB ID
DB_TASKS = "339b59b94dc180dab746c0f9fd1d3a3c"        # 업무지시
DB_REPORTS = "339b59b94dc180369de0d851b5a222d2"      # 작업보고
DB_LOGS = "339b59b94dc180b6b291df0408b9a247"         # 업무일지

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")


def notify_discord(message: str):
    """Discord 웹훅으로 알림 전송 (Bot 인증 헤더 없이 직접 POST)"""
    if not DISCORD_WEBHOOK:
        return
    try:
        r = requests.post(
            DISCORD_WEBHOOK,
            json={"content": message},
            timeout=5
        )
        r.raise_for_status()
    except Exception as e:
        print(f"[Discord] 알림 전송 실패: {e}")


def _get_property_value(prop_obj: Dict, prop_type: str) -> any:
    """Notion 속성값 추출"""
    if prop_type == "title":
        return "".join(t.get("plain_text", "") for t in prop_obj.get("title", []))
    elif prop_type == "url":
        return prop_obj.get("url")
    elif prop_type == "rich_text":
        return "".join(t.get("plain_text", "") for t in prop_obj.get("rich_text", []))
    elif prop_type == "number":
        return prop_obj.get("number")
    elif prop_type == "select":
        sel = prop_obj.get("select")
        return sel.get("name") if sel else None
    elif prop_type == "status":
        stat = prop_obj.get("status")
        return stat.get("name") if stat else None
    elif prop_type == "date":
        d = prop_obj.get("date")
        return d.get("start") if d else None
    return None


def get_pending_tasks() -> List[Dict]:
    """
    업무지시 DB에서 '대기중' 상태 항목 조회
    Returns: [{"id": "...", "title": "...", "link": "...", "detail": "...", "priority": "..."}, ...]
    """
    try:
        r = requests.post(
            f"https://api.notion.com/v1/databases/{DB_TASKS}/query",
            headers=HEADERS,
            json={
                "filter": {
                    "property": "상태",
                    "status": {"equals": "대기중"}
                },
                "sorts": [{"property": "우선순위", "direction": "descending"}]
            }
        )
        r.raise_for_status()
        results = r.json().get("results", [])

        tasks = []
        for item in results:
            props = item.get("properties", {})
            task = {
                "id": item.get("id"),
                "title": _get_property_value(props.get("이름", {}), "title"),
                "link": _get_property_value(props.get("구글드라이브 링크", {}), "url"),
                "detail": _get_property_value(props.get("상세 지시사항", {}), "rich_text"),
                "priority": _get_property_value(props.get("우선순위", {}), "select")
            }
            tasks.append(task)
        return tasks
    except Exception as e:
        print(f"[Notion] get_pending_tasks 오류: {e}")
        return []


def update_task_status(task_id: str, status: str) -> bool:
    """업무지시 항목 상태 변경"""
    try:
        r = requests.patch(
            f"https://api.notion.com/v1/pages/{task_id}",
            headers=HEADERS,
            json={
                "properties": {
                    "상태": {"status": {"name": status}}
                }
            }
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[Notion] update_task_status 오류: {e}")
        return False


def add_report(title: str, link: str, changes: str, hours: float) -> bool:
    """작업보고 DB에 행 추가"""
    try:
        props = {"이름": {"title": [{"text": {"content": title}}]}}
        if link:
            props["결과물 링크"] = {"url": link}
        if changes:
            props["주요 변경점"] = {"rich_text": [{"text": {"content": changes}}]}
        if hours:
            props["작업 시간"] = {"number": hours}
        r = requests.post(
            f"https://api.notion.com/v1/pages",
            headers=HEADERS,
            json={"parent": {"database_id": DB_REPORTS}, "properties": props}
        )
        r.raise_for_status()
        notify_discord(f"📋 **노션 작업보고 업로드 완료!**\n- 제목: {title}\n- 링크: {link or '없음'}")
        return True
    except Exception as e:
        print(f"[Notion] add_report 오류: {e}")
        return False


def upsert_daily_log(summary: str, task_count: int, notes: str, satisfaction: str) -> bool:
    """
    업무일지 DB에 당일 행 생성 또는 수정

    Args:
        summary: 당일 요약 (제목)
        task_count: 완료 작업 건수
        notes: 특이사항
        satisfaction: 만족도 (🚀 완벽했어요 / 😊 괜찮았어요 / 😐 그냥저냥)
    """
    today = date.today().isoformat()
    today_label = datetime.now().strftime("%Y-%m-%d")

    try:
        # 오늘 날짜의 행 조회
        r_query = requests.post(
            f"https://api.notion.com/v1/databases/{DB_LOGS}/query",
            headers=HEADERS,
            json={
                "filter": {
                    "property": "날짜",
                    "date": {"equals": today}
                }
            }
        )
        r_query.raise_for_status()
        results = r_query.json().get("results", [])

        if results:
            # 기존 행 수정
            page_id = results[0]["id"]
            r_update = requests.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers=HEADERS,
                json={
                    "properties": {
                        "이름": {"title": [{"text": {"content": summary}}]},
                        "총 작업 건수": {"number": task_count},
                        "특이사항": {"rich_text": [{"text": {"content": notes}}]} if notes else {},
                        "만족도": {"select": {"name": satisfaction}} if satisfaction else {}
                    }
                }
            )
            r_update.raise_for_status()
            notify_discord(f"📅 **업무일지 업데이트 완료!** ({today_label})\n- {summary} | 완료 {task_count}건")
            return True
        else:
            # 새 행 생성
            r_create = requests.post(
                f"https://api.notion.com/v1/pages",
                headers=HEADERS,
                json={
                    "parent": {"database_id": DB_LOGS},
                    "properties": {
                        "날짜": {"date": {"start": today}},
                        "이름": {"title": [{"text": {"content": summary}}]},
                        "총 작업 건수": {"number": task_count},
                        "특이사항": {"rich_text": [{"text": {"content": notes}}]} if notes else {},
                        "만족도": {"select": {"name": satisfaction}} if satisfaction else {}
                    }
                }
            )
            r_create.raise_for_status()
            notify_discord(f"📅 **업무일지 생성 완료!** ({today_label})\n- {summary} | 완료 {task_count}건")
            return True
    except Exception as e:
        print(f"[Notion] upsert_daily_log 오류: {e}")
        return False
