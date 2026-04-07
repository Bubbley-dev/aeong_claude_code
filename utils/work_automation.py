#!/usr/bin/env python3
"""
작업 자동화 유틸리티
Claude Code에서 호출 가능한 워크플로우 스크립트
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 프로젝트 루트 경로
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from drive import drive_client
from notion import notion_client


def download_work_file(drive_link: str) -> dict:
    """
    /작업 [드라이브링크]
    - 파일 다운로드
    - 작업 폴더 자동 생성
    """
    print(f"📥 파일 다운로드 중: {drive_link}")

    success, result = drive_client.download_file(drive_link)

    if not success:
        return {
            "status": "error",
            "message": f"다운로드 실패: {result}"
        }

    file_path = result
    file_name = os.path.basename(file_path)

    # 작업 세션 폴더 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    work_dir = os.path.join(PROJECT_ROOT, "works", timestamp)
    os.makedirs(work_dir, exist_ok=True)

    # 파일 복사
    import shutil
    work_file = os.path.join(work_dir, file_name)
    shutil.copy(file_path, work_file)

    return {
        "status": "success",
        "file_name": file_name,
        "work_dir": work_dir,
        "file_path": work_file,
        "message": f"✅ {file_name} 준비 완료\n📁 작업 폴더: {work_dir}"
    }


def complete_work(work_summary: str, result_file: str = None, hours: float = 0) -> dict:
    """
    /완료 [내용]
    - 결과물 업로드 (선택사항)
    - Notion 작업보고 DB 기록
    - work-history.md 기록
    - Discord 알림
    """
    print(f"📤 작업 완료 처리 중...")

    result_link = None

    # 결과 파일 업로드 (있으면)
    if result_file and os.path.exists(result_file):
        print(f"  📁 파일 업로드: {result_file}")
        success, upload_result = drive_client.upload_file(result_file)
        if success:
            result_link = upload_result.split(": ")[-1] if ": " in upload_result else upload_result
        else:
            return {
                "status": "error",
                "message": f"파일 업로드 실패: {upload_result}"
            }

    # Notion 작업보고 DB에 기록
    print(f"  📝 Notion에 기록 중...")
    notion_success = notion_client.add_report(
        title=work_summary,
        link=result_link or "",
        changes=work_summary,
        hours=hours
    )

    if not notion_success:
        return {
            "status": "error",
            "message": "Notion 기록 실패"
        }

    # work-history.md에 기록
    today = datetime.now().strftime("%Y-%m-%d")
    work_history_path = os.path.join(PROJECT_ROOT, "history", "work-history.md")

    entry = f"\n- **[{today}]** {work_summary}" + (f" → {result_link}" if result_link else "")

    try:
        with open(work_history_path, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"  ⚠️  work-history 기록 실패: {e}")

    return {
        "status": "success",
        "message": f"✅ 작업 완료 기록됨\n📋 Notion 작업보고 DB 추가\n📝 work-history.md 업데이트",
        "link": result_link
    }


def check_status() -> dict:
    """
    /상태확인
    - 봇 상태 확인
    - 대기 중인 업무 조회
    """
    print("🔍 상태 확인 중...")

    # 봇 상태 확인
    pid_file = os.path.join(PROJECT_ROOT, "discord", "discord_monitor.pid")
    bot_running = False
    if os.path.exists(pid_file):
        try:
            import psutil
            with open(pid_file) as f:
                pid = int(f.read().strip())
            bot_running = psutil.pid_exists(pid)
        except:
            pass

    bot_status = "🟢 온라인" if bot_running else "🔴 오프라인"

    # 대기 업무 조회
    tasks = notion_client.get_pending_tasks()

    task_list = ""
    if tasks:
        for i, task in enumerate(tasks, 1):
            priority_emoji = {"긴급": "🔴", "보통": "🟡", "나중에": "🔵"}.get(task.get("priority", ""), "⚪")
            task_list += f"{i}. {priority_emoji} {task['title']}\n"
    else:
        task_list = "   (없음)"

    return {
        "status": "success",
        "message": f"**애옹이 상태**\n봇: {bot_status}\n\n**대기 업무**\n{task_list}"
    }


def sync_daily_log(satisfaction: str = "😊 괜찮았어요") -> dict:
    """
    /일지
    - work-history.md → Notion 업무일지 동기화
    """
    print(f"📝 업무일지 동기화 중...")

    work_history_path = os.path.join(PROJECT_ROOT, "history", "work-history.md")

    if not os.path.exists(work_history_path):
        return {
            "status": "error",
            "message": "work-history.md를 찾을 수 없습니다"
        }

    with open(work_history_path, "r", encoding="utf-8") as f:
        content = f.read()

    today = datetime.now().strftime("%Y-%m-%d")
    lines = content.split("\n")
    today_section = []
    in_today = False

    for line in lines:
        if line.startswith(f"## {today}"):
            in_today = True
            continue
        if in_today:
            if line.startswith("## ") and not line.startswith(f"## {today}"):
                break
            today_section.append(line)

    if not today_section:
        summary = f"{today} 업무 요약"
        task_count = 0
        notes = "기록 없음"
    else:
        section_text = "\n".join(today_section).strip()
        lines_list = [l.strip() for l in section_text.split("\n") if l.strip()]
        summary = f"{today} 업무 요약"

        # 작업 건수 카운트
        task_count = len([l for l in lines_list if l.startswith("-")])
        notes = "\n".join(lines_list[:10]) if lines_list else "기록 없음"

    success = notion_client.upsert_daily_log(
        summary=summary,
        task_count=task_count,
        notes=notes,
        satisfaction=satisfaction
    )

    if success:
        return {
            "status": "success",
            "message": f"✅ 업무일지 동기화 완료\n📊 작업 건수: {task_count}건"
        }
    else:
        return {
            "status": "error",
            "message": "Notion 기록 실패"
        }


def main():
    """CLI 인터페이스"""
    if len(sys.argv) < 2:
        print("사용법:")
        print("  python3 work_automation.py download <드라이브링크>")
        print("  python3 work_automation.py complete <내용> [결과파일] [시간]")
        print("  python3 work_automation.py status")
        print("  python3 work_automation.py sync [만족도]")
        return

    command = sys.argv[1]

    if command == "download":
        if len(sys.argv) < 3:
            print("❌ 드라이브 링크를 입력하세요")
            return
        result = download_work_file(sys.argv[2])

    elif command == "complete":
        if len(sys.argv) < 3:
            print("❌ 작업 내용을 입력하세요")
            return
        summary = sys.argv[2]
        result_file = sys.argv[3] if len(sys.argv) > 3 else None
        hours = float(sys.argv[4]) if len(sys.argv) > 4 else 0
        result = complete_work(summary, result_file, hours)

    elif command == "status":
        result = check_status()

    elif command == "sync":
        satisfaction = sys.argv[2] if len(sys.argv) > 2 else "😊 괜찮았어요"
        result = sync_daily_log(satisfaction)

    else:
        print(f"❌ 알 수 없는 명령어: {command}")
        return

    # 결과 출력
    print(result.get("message", ""))

    # JSON으로도 출력 (자동화 파이프라인용)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
