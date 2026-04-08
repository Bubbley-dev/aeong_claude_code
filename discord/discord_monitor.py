#!/usr/bin/env python3
import os
import sys
import subprocess
import asyncio
import aiohttp
from datetime import datetime

# 1. 경로 설정 및 notion_client 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, ".."))

try:
    from notion import notion_client
except ImportError:
    notion_client = None

# 2. .env 환경 변수 수동 로드
def load_env():
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()  # setdefault 대신 강제 덮어쓰기

load_env()

# 3. 주요 설정값 확보
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.environ.get("DISCORD_CHANNEL_ID")
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
WORK_DIR = os.environ.get("WORK_DIR", os.path.join(BASE_DIR, ".."))
HEADERS = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
PID_FILE = os.path.join(BASE_DIR, "discord_monitor.pid")
FIN_FLAG = "/tmp/aeong_fin"   # 작업 완료 신호 파일
import time
_key_sent_at = 0.0            # 1/2/3 키 전송 시각 (모듈 레벨, asyncio 단일 스레드라 안전)
KEY_GRACE = 10                # 키 전송 후 재알림 억제 시간(초)

# 4. 중복 실행 방지 로직
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

# 5. 디스코드 응답 전송 (비동기 방식)
# 웹훅은 Bot Authorization 헤더 없이 별도 세션으로 전송
async def send_webhook_async(session, content):
    if not content:
        return
    async with aiohttp.ClientSession() as wh_session:
        for i in range(0, len(content), 1990):
            chunk = content[i : i + 1990]
            async with wh_session.post(WEBHOOK_URL, json={"content": f"```\n{chunk}\n```"}) as resp:
                await resp.release()

async def handle_command(content):
    content = content.strip()
    if not content: return None

    if content == "!help":
        return (
            "**사용 가능한 명령어:**\n"
            "- `<텍스트>` : Claude 작업 요청\n"
            "- `!run <명령>` : 쉘 명령 직접 실행\n"
            "- `!입력 <값>` : 터미널 대기 시 값 전달\n"
            "- `1` / `2` / `3` : 권한 프롬프트 빠른 응답\n"
            "- `!화면` : 현재 터미널 화면 캡처\n"
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
                if not tasks: return "📋 대기 중인 업무가 없다냥."
                msg = "📋 **대기 중인 업무 목록:**\n"
                for i, t in enumerate(tasks, 1):
                    msg += f"{i}. [{t.get('priority','보통')}] {t['title']}\n"
                return msg
            except Exception as e: return f"Error: {str(e)}"
        return "Error: notion_client 설정 누락이다냥."

    # [권한 프롬프트 빠른 응답]
    # Claude Code ink UI: 숫자 키 직접 전송 후 Enter
    if content in ["1", "2", "3"]:
        global _key_sent_at
        labels = {"1": "현재만 승인", "2": "항상 승인", "3": "거절"}
        subprocess.run(['tmux', 'send-keys', '-t', 'aeong', content, ''], check=False)
        subprocess.run(['tmux', 'send-keys', '-t', 'aeong', 'Enter', ''], check=False)
        _key_sent_at = time.time()  # 타임스탬프 기록 → watchdog 억제
        print(f"[KEY] {content} → 숫자+Enter 전송")
        return f"⌨️ `{content}` ({labels[content]}) 전달했다냥!"

    if content.startswith("!입력 "):
        val = content[4:].strip()
        subprocess.run(['tmux', 'send-keys', '-t', 'aeong', val, 'C-m'], check=False)
        return f"⌨️ 터미널에 `{val}` 입력 완료!"

    if content == "!화면":
        res = subprocess.run(['tmux', 'capture-pane', '-p', '-t', 'aeong'], capture_output=True, text=True)
        trimmed = [line[:100].rstrip() for line in res.stdout.split('\n')]
        return f"📺 **현재 화면:**\n" + "\n".join(trimmed[-30:])

    # [실행 명령]
    target_cmd = None
    if content.startswith("!run "):
        target_cmd = content[5:].strip()
    elif not content.startswith("!"):
        # 작은따옴표 이스케이프 처리
        escaped = content.replace("'", "'\\''")
        target_cmd = f"claude -p -c '{escaped}' --output-format text"

    if target_cmd:
        try:
            full_cmd = f"(cd {WORK_DIR} && {target_cmd}); touch {FIN_FLAG}"
            # shell=True 없이 리스트 형태로 전달 → 쉘 파싱 에러 원천 차단
            subprocess.run(['tmux', 'send-keys', '-t', 'aeong', full_cmd, 'C-m'], check=True)
            return f"🚀 작업을 시작한다냥! 완료 알림을 기다려달라냥.\n명령: `{content[:80]}`"
        except Exception as e:
            return f"❌ 실행 에러: {str(e)}"
    return None

# 7. [핵심] 터미널 감시 워치독 (파일 기반 완료 감지 + 1회 알림 플래그)
async def terminal_watchdog(session):
    permission_alerted = False
    yn_alerted = False
    print("🐾 애옹이 감시 모드 가동 중")

    while True:
        try:
            # A. 작업 완료 — 파일 기반 감지 (TUI에 묻혀도 확실히 동작)
            if os.path.exists(FIN_FLAG):
                print(f"[FIN] 플래그 감지 → 알림 전송")
                await send_webhook_async(session, "✅ **버블리님, 요청하신 작업이 모두 끝났다냥! 🐾**")
                os.remove(FIN_FLAG)
                print(f"[FIN] 플래그 삭제 완료")
                permission_alerted = False
                yn_alerted = False

            # 터미널 캡처 (권한 프롬프트 감지용) — 줄당 100자 잘라서 펭귄 제거
            res = subprocess.run(['tmux', 'capture-pane', '-p', '-t', 'aeong', '-S', '-50'], capture_output=True, text=True)
            lines = [line[:100].rstrip() for line in res.stdout.split('\n')]
            current_content = '\n'.join(lines).strip()

            if not current_content:
                await asyncio.sleep(3)
                continue

            # B. Claude 권한 프롬프트 — 선택지 개수 무관하게 감지
            recent = '\n'.join(lines[-12:])
            has_numbered = "1." in recent and "2." in recent
            has_approval_kw = any(kw in recent.lower() for kw in ["yes", "no", "proceed", "allow", "approve", "deny", "once", "always"])
            is_prompt = has_numbered and has_approval_kw

            recently_sent = (time.time() - _key_sent_at) < KEY_GRACE

            if is_prompt:
                if recently_sent:
                    permission_alerted = True  # 키 전송 직후 → 재알림 억제
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
                    permission_alerted = False  # 유예 기간 지나야 리셋

            # C. 일반 y/n 프롬프트
            if "(y/n)" in current_content.lower() or "password:" in current_content.lower():
                if not yn_alerted:
                    await send_webhook_async(session, "⚠️ **입력 대기 중이다냥!**\n```\n" + '\n'.join(lines[-5:]) + "\n```")
                    yn_alerted = True
            else:
                yn_alerted = False

        except Exception as e:
            print(f"Watchdog error: {e}")

        await asyncio.sleep(3)

# 8. 메인 실행 루프 (비동기)
async def main():
    acquire_pid_lock()
    print("🚀 애옹이 봇 기상 중... (Monitoring Start)")
    
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        # 내 정보 확인
        async with session.get("https://discord.com/api/v10/users/@me") as r:
            me = await r.json()
            bot_id = me.get("id")

        # 마지막 메시지 ID 초기화
        async with session.get(f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=1") as r:
            init_resp = await r.json()
            last_id = init_resp[0]["id"] if init_resp else None
        
        # 부팅메시지 (버전출력)
        boot_msg = f"🟢 **애옹이 봇 부팅 완료했다냥!**\n애옹이는 260408 23:00 수정됐다냥\n오늘도 열심히 감시하겠다냥! 🐾"
        await send_webhook_async(session, boot_msg)

        # [병렬 실행] 터미널 감시 워치독 시작
        asyncio.create_task(terminal_watchdog(session))

        while True:
            try:
                url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
                params = {"after": last_id} if last_id else {"limit": 1}
                
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        msgs = await resp.json()
                        for msg in reversed(msgs):
                            # 내가 보낸 메시지나 웹훅 제외
                            if not msg.get("webhook_id") and msg["author"]["id"] != bot_id:
                                print(f"New message: {msg['content']}")
                                response = await handle_command(msg["content"])
                                if response:
                                    await send_webhook_async(session, response)
                            last_id = msg["id"]
            except Exception as e:
                print(f"Loop error: {e}")
            
            await asyncio.sleep(3) # 메시지 폴링 간격

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🐾 애옹이 퇴근한다냥! 다음에 봐냥!")
    finally:
        release_pid_lock()
