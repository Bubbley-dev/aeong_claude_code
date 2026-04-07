# 애옹이 Claude Code 자동화 시스템

Discord에서 명령을 받아 Claude Code를 원격 제어하는 자동화 봇 + 업무 관리 시스템.

---

## 컴퓨터 껐다 켰을 때 (일반 시작)

```bash
# 1. tmux 세션 시작
tmux new-session -d -s aeong

# 2. Claude Code 실행 (aeong 세션 안에서)
tmux send-keys -t aeong "cd /mnt/c/Users/ksh/Desktop/Claude && claude" C-m

# 3. 디스코드 봇 백그라운드 시작
cd /mnt/c/Users/ksh/Desktop/Claude/discord
nohup python3 discord_monitor.py > discord_monitor.log 2>&1 &

# 4. Discord에서 확인
# !출근 → 봇 응답 오면 정상
```

> tmux 세션 붙기: `tmux attach -t aeong`
> 봇 로그 확인: `tail -f /mnt/c/Users/ksh/Desktop/Claude/discord/discord_monitor.log`

---

## 처음 세팅 (새 컴퓨터)

### 1. 필수 패키지 설치

```bash
sudo apt update && sudo apt install -y tmux python3 python3-pip

pip3 install aiohttp requests google-api-python-client google-auth-oauthlib openpyxl --break-system-packages
```

### 2. Claude Code CLI 설치

```bash
npm install -g @anthropic-ai/claude-code
# 또는
curl -fsSL https://claude.ai/install.sh | sh
```

### 3. 레포 클론

```bash
cd /mnt/c/Users/ksh/Desktop
git clone https://github.com/Bubbley-dev/aeong_claude_code.git Claude
cd Claude
```

### 4. 민감 파일 복구 (Google Drive → Claude_secrets 폴더)

Drive 폴더 ID: `1cyQ6LRbY3OxPMyJ6s6Fx2QlrBcu2d58K`

| Drive 파일명 | 로컬 저장 경로 |
|---|---|
| `discord.env` | `discord/.env` |
| `notion.env` | `notion/.env` |
| `drive_token.json` | `drive/token.json` |
| `drive_oauth_client.json` | `drive/oauth_client.json` |

> Drive에서 수동으로 다운받아 해당 경로에 복사하면 됩니다.

### 5. htdocs 심볼릭 링크 생성 (MAMP 쓰는 경우)

```bash
ln -s /mnt/c/MAMP/htdocs /mnt/c/Users/ksh/Desktop/Claude/htdocs
```

### 6. CLI 함수 자동 로드 설정

```bash
echo 'source /mnt/c/Users/ksh/Desktop/Claude/.claude/cli-setup.sh' >> ~/.bashrc
source ~/.bashrc
```

### 7. Drive OAuth2 인증 (token.json 없을 때)

Drive `Claude_secrets`에서 복구해도 만료됐으면 재인증 필요:
- Windows에서 `drive/oauth_login.bat` 실행 → 브라우저 인증 → `drive/token.json` 생성

---

## 디스코드 봇 재시작 (봇이 죽었을 때)

```bash
cd /mnt/c/Users/ksh/Desktop/Claude/discord
kill $(cat discord_monitor.pid) 2>/dev/null
rm -f discord_monitor.pid
nohup python3 discord_monitor.py > discord_monitor.log 2>&1 &
```

---

## Discord 명령어 요약

| 명령어 | 설명 |
|---|---|
| `!출근` | 봇 온라인 상태 확인 |
| `!지시` | Notion 대기 업무 조회 |
| `!퇴근` | 퇴근 처리 |
| `!화면` | 현재 터미널 화면 캡처 |
| `!run <명령>` | 쉘 명령 직접 실행 |
| `!help` | 전체 명령어 목록 |
| `1` / `2` / `3` | Claude 권한 프롬프트 응답 (현재만/항상/거절) |
| 일반 텍스트 | Claude Code에 작업 요청 |

---

## 폴더 구조

```
Claude/
├── CLAUDE.md              # 애옹이 핵심 지침서
├── README.md              # 이 파일
├── .gitignore
├── discord/
│   ├── discord_monitor.py # 메인 봇 (채널 감시 + 터미널 제어)
│   └── .env               # ⚠️ git 제외 — Drive에서 복구
├── notion/
│   ├── notion_client.py   # Notion API 헬퍼
│   └── .env               # ⚠️ git 제외 — Drive에서 복구
├── drive/
│   ├── drive_client.py    # Drive 다운/업로드
│   ├── oauth_login.py     # OAuth2 인증
│   ├── token.json         # ⚠️ git 제외 — Drive에서 복구
│   └── oauth_client.json  # ⚠️ git 제외 — Drive에서 복구
├── utils/
│   └── work_automation.py # /작업 /완료 /상태확인 /일지 CLI
├── cmd/                   # 쉘 스크립트 래퍼
├── history/               # 작업 기록 (work-history.md)
└── works/                 # 작업 결과물 (git 제외)
```
