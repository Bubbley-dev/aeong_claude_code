#!/usr/bin/env python3
"""
애옹이 봇 상태 확인 및 자동 재시작 스크립트
아침 8시마다 실행되어야 함 (Windows 작업 스케줄러 또는 cron)
"""

import os
import sys
import subprocess
import psutil
from datetime import datetime

# .env 파일 로드
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

PID_FILE = os.path.join(os.path.dirname(__file__), "discord_monitor.pid")
BOT_SCRIPT = os.path.join(os.path.dirname(__file__), "discord_monitor.py")
LOG_FILE = os.path.join(os.path.dirname(__file__), "monitor_bot.log")

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")


def log_message(msg: str):
    """로그 파일에 메시지 기록"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")


def send_discord_notification(message: str):
    """Discord 채널에 알림 전송"""
    if not WEBHOOK_URL:
        return
    try:
        import requests
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        log_message(f"Discord 알림 실패: {e}")


def is_bot_running() -> bool:
    """봇이 현재 실행 중인지 확인"""
    if not os.path.exists(PID_FILE):
        return False

    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())

        # psutil로 프로세스 확인
        if psutil.pid_exists(pid):
            return True
        else:
            return False
    except (ValueError, FileNotFoundError):
        return False


def start_bot():
    """봇 프로세스 시작"""
    try:
        # 백그라운드에서 봇 시작
        subprocess.Popen(
            ["python3", BOT_SCRIPT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        log_message("✅ 애옹이 시작됨")
        send_discord_notification("🟢 애옹이 자동 재시작됨 (모니터링)")
        return True
    except Exception as e:
        log_message(f"❌ 애옹이 시작 실패: {e}")
        send_discord_notification(f"❌ 애옹이 재시작 실패: {e}")
        return False


def main():
    """메인 모니터링 로직"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message(f"--- 모니터링 시작 ({timestamp}) ---")

    if is_bot_running():
        log_message("✅ 애옹이 정상 작동 중")
    else:
        log_message("❌ 애옹이 응답 없음, 재시작 중...")
        start_bot()


if __name__ == "__main__":
    main()
