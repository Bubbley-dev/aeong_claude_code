import os
import requests
from dotenv import load_dotenv

# 설정 로드
load_dotenv('discord/.env')
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_notification():
    payload = {
        "content": "🔔 **애옹이 토큰 충전 완료!** \n시간 토큰이 초기화되었습니다. 이제 다시 명령을 내리셔도 좋아요! 🐱💻"
    }
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_notification()
