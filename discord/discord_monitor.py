#!/usr/bin/env python3
import os
import sys
import subprocess
import asyncio
import aiohttp
import time
from datetime import datetime

# 1. 경로 설정 및 notion_client 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(BASE_DIR, "..")
sys.path.insert(0, WORK_DIR)

try:
    from notion import notion_client
except ImportError:
    notion_client = None

# 2. .env 환경 변수 로드 (강제 덮어쓰기)
def load_env():
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()

load_env()

# 3. 주요 설정값
BOT_TOKEN  = os.environ.get("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.environ.get("DISCORD_CHANNEL_ID")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
HEADERS  = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
PID_FILE = os.path.join(BASE_DIR, "discord_monitor.pid")
FIN_FLAG = "/tmp/aeong_fin"

CLAUDE_PANE = "aeong:0.1"  # Claude Code 대화 세션이 있는 pane
BOT_PANE   = "aeong:0.0"  # 봇 자신이 실행 중인 pane

_key_sent_at = 0.0
KEY_GRACE   = 10  # 키 전송 후 재알림 억제 시간(초)

# 4. PID 락
def acquire_pid_lock():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            old_pid = f.read().strip()
        try:
            os.kill(int(old_pid), 0)
            print(f"Process already running (PID {old_pid}). Exiting.")
            sys.exit(1)
        except (ProcessLookupError, ValueError, PermissionError):
            pass
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

def release_pid_lock():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

# 5. 웹훅 전송 (Bot 인증 헤더 없이 별도 세션)
async def send_webhook_async(session, content):
    if not content:
        return
    async with aiohttp.ClientSession() as wh_session:
        for i in range(0, len(content), 1990):
            chunk = content[i : i + 1990]
            async with wh_session.post(WEBHOOK_URL, json={"content": f"```\n{chunk}\n```"}) as resp:
                await resp.release()

# 6. 명령 처리
async def handle_command(content):
    content = content.strip()
    if not content:
        return None

    if content == "!help":
        return (
            "**사용 가능한 명령어:**\n"
            "- `<텍스트>` : Claude에게 직접 전달\n"
            "- `!run <명령>` : 쉘 명령 실행 후 결과 반환\n"
            "- `!입력 <값>` : 터미널 대기 시 값 전달\n"
            "- `1` / `2` / `3` : 권한 프롬프트 응답\n"
            "- `!화면` : 현재 Claude 화면 캡처\n"
            "- `!출근` / `!퇴근` / `!지시` : 업무 관리"
        )

    if content == "!출근":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"🟢 **온라인 상태 확인됨 ({now})**\n`!지시`로 업무를 확인하라냥!"

    if content == "!퇴근":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"🌙 **퇴근 처리 ({now})**\n수고하셨다냥! 🐾"

    if content == "!지시":
        if notion_client:
            try:
                tasks = notion_client.get_pending_tasks()
                if not tasks:
                    return "📋 대기 중인 업무가 없다냥."
                msg = "📋 **대기 중인 업무 목록:**\n"
                for i, t in enumerate(tasks, 1):
                    msg += f"{i}. [{t.get('priority','보통')}] {t['title']}\n"
                return msg
            except Exception as e:
                return f"Error: {str(e)}"
        return "Error: notion_client 설정 누락이다냥."

    # 1/2/3: 권한 프롬프트 응답 → Claude pane으로 전송
    if content in ["1", "2", "3"]:
        global _key_sent_at
        labels = {"1": "현재만 승인", "2": "항상 승인", "3": "거절"}
        subprocess.run(['tmux', 'send-keys', '-t', CLAUDE_PANE, content, ''], check=False)
        subprocess.run(['tmux', 'send-keys', '-t', CLAUDE_PANE, 'Enter', ''], check=False)
        _key_sent_at = time.time()
        print(f"[KEY] {content} → Claude pane 전송")
        return f"⌨️ `{content}` ({labels[content]}) 전달했다냥!"

    # !입력: Claude pane에 직접 타이핑
    if content.startswith("!입력 "):
        val = content[4:].strip()
        subprocess.run(['tmux', 'send-keys', '-t', CLAUDE_PANE, val, 'C-m'], check=False)
        return f"⌨️ `{val}` 입력 완료!"

    # !화면: Claude pane 캡처
    if content == "!화면":
        res = subprocess.run(
            ['tmux', 'capture-pane', '-p', '-t', CLAUDE_PANE],
            capture_output=True, text=True
        )
        trimmed = [line[:100].rstrip() for line in res.stdout.split('\n')]
        return "📺 **현재 화면:**\n" + "\n".join(trimmed[-30:])

    # !run: subprocess 직접 실행 후 결과 Discord로 반환
    if content.startswith("!run "):
        cmd = content[5:].strip()
        try:
            res = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=60, cwd=WORK_DIR
            )
            output = (res.stdout + res.stderr).strip()
            return f"💻 `{cmd}`\n{output[:1800] or '(출력 없음)'}"
        except subprocess.TimeoutExpired:
            return "⏰ 타임아웃 (60초)"
        except Exception as e:
            return f"❌ {str(e)}"

    # 일반 텍스트 → Claude pane에 직접 전달 (claude -p -c 불필요)
    if not content.startswith("!"):
        subprocess.run(['tmux', 'send-keys', '-t', CLAUDE_PANE, content, 'C-m'], check=False)
        return f"💬 Claude에게 전달했다냥!"

    return None

# 7. 워치독: Claude pane 감시
async def terminal_watchdog(session):
    permission_alerted = False
    yn_alerted = False
    print("🐾 애옹이 감시 모드 가동 중")

    while True:
        try:
            # A. 작업 완료 플래그
            if os.path.exists(FIN_FLAG):
                print("[FIN] 플래그 감지 → 알림 전송")
                await send_webhook_async(session, "✅ **버블리님, 작업이 끝났다냥! 🐾**")
                os.remove(FIN_FLAG)
                permission_alerted = False
                yn_alerted = False

            # B. Claude pane 캡처
            res = subprocess.run(
                ['tmux', 'capture-pane', '-p', '-t', CLAUDE_PANE, '-S', '-50'],
                capture_output=True, text=True
            )
            lines = [line[:100].rstrip() for line in res.stdout.split('\n')]
            current_content = '\n'.join(lines).strip()

            if not current_content:
                await asyncio.sleep(3)
                continue

            # C. Claude 권한 프롬프트 감지
            recent = '\n'.join(lines[-12:])
            has_numbered    = "1." in recent and "2." in recent
            has_approval_kw = any(kw in recent.lower() for kw in
                                  ["yes", "no", "proceed", "allow", "approve", "deny", "once", "always"])
            is_prompt = has_numbered and has_approval_kw
            recently_sent = (time.time() - _key_sent_at) < KEY_GRACE

            if is_prompt:
                if recently_sent:
                    permission_alerted = True
                elif not permission_alerted:
                    snippet = '\n'.join(lines[-10:])
                    await send_webhook_async(session, (
                        "⚠️ **버블리님! 승인 요청이 왔다냥!**\n"
                        "```\n" + snippet[-600:] + "\n```\n"
                        "👉 `1`(현재만) `2`(항상) `3`(거절) 또는 해당 번호 입력!"
                    ))
                    permission_alerted = True
            else:
                if not recently_sent:
                    permission_alerted = False

            # D. 일반 y/n 프롬프트
            if "(y/n)" in current_content.lower() or "password:" in current_content.lower():
                if not yn_alerted:
                    await send_webhook_async(session, "⚠️ **입력 대기 중이다냥!**\n```\n" + '\n'.join(lines[-5:]) + "\n```")
                    yn_alerted = True
            else:
                yn_alerted = False

        except Exception as e:
            print(f"Watchdog error: {e}")

        await asyncio.sleep(3)

# 8. 메인
async def main():
    acquire_pid_lock()
    print("🚀 애옹이 봇 기상 중... (Monitoring Start)")

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get("https://discord.com/api/v10/users/@me") as r:
            me = await r.json()
            bot_id = me.get("id")

        async with session.get(f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=1") as r:
            init_resp = await r.json()
            last_id = init_resp[0]["id"] if init_resp else None

        await send_webhook_async(session,
            "🟢 **애옹이 봇 부팅 완료했다냥!** (리팩토링 260408)\n"
            "이제 Claude pane에 직접 전달한다냥! 🐾"
        )

        asyncio.create_task(terminal_watchdog(session))

        while True:
            try:
                url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
                params = {"after": last_id} if last_id else {"limit": 1}

                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        msgs = await resp.json()
                        for msg in reversed(msgs):
                            if not msg.get("webhook_id") and msg["author"]["id"] != bot_id:
                                print(f"New message: {msg['content']}")
                                response = await handle_command(msg["content"])
                                if response:
                                    await send_webhook_async(session, response)
                            last_id = msg["id"]
            except Exception as e:
                print(f"Loop error: {e}")

            await asyncio.sleep(3)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🐾 애옹이 퇴근한다냥! 다음에 봐냥!")
    finally:
        release_pid_lock()
