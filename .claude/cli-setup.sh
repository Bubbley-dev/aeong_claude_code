#!/bin/bash
# Claude Code 작업 자동화 CLI 설정
# 사용법: source ~/.claude/cli-setup.sh

PROJECT_ROOT="/mnt/c/Users/ksh/Desktop/Claude"

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수 정의 (alias는 특수문자 미지원)
function 작업() {
    $PROJECT_ROOT/cmd/work.sh "$1"
}

function 완료() {
    $PROJECT_ROOT/cmd/done.sh "$1" "$2" "$3"
}

function 상태확인() {
    $PROJECT_ROOT/cmd/status.sh
}

function 일지() {
    $PROJECT_ROOT/cmd/log.sh "$1"
}

# 출근/퇴근 조회용 헬퍼 함수
function 출근() {
    echo "🔍 애옹이 상태 확인 중..."
    curl -s https://api.discord.com/api/v10/users/@me \
        -H "Authorization: Bot $(grep DISCORD_BOT_TOKEN $PROJECT_ROOT/discord/.env | cut -d= -f2)" \
        > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 애옹이 온라인${NC}"
    else
        echo -e "${YELLOW}⚠️  봇 확인 중...${NC}"
        $PROJECT_ROOT/cmd/status.sh
    fi
}

function 퇴근() {
    echo "📝 업무일지 저장 중..."
    $PROJECT_ROOT/cmd/log.sh "${1:-😊 괜찮았어요}"
}

# 도움말
function 작업도움말() {
    cat << 'EOF'

╔═══════════════════════════════════════════════════════════════╗
║          Claude Code 작업 자동화 CLI v1.0                    ║
╚═══════════════════════════════════════════════════════════════╝

📋 4가지 주요 명령어
─────────────────────────────────────────────────────────────

  작업 [드라이브링크]
    파일 다운로드 → works/ 폴더 생성
    예: 작업 https://drive.google.com/file/d/XXXXX/view

  완료 [내용] [결과파일] [시간]
    작업 완료 기록 → Notion + work-history + Discord
    예: 완료 "로그인 수정" "works/20260405_143000/file.txt" "2.5"

  상태확인
    봇 상태 + 대기 업무 조회
    예: 상태확인

  일지 [만족도]
    work-history → Notion 업무일지 동기화
    예: 일지 "🚀 완벽했어요"

🔧 추가 헬퍼 함수
─────────────────────────────────────────────────────────────

  출근
    애옹이 봇 상태 확인

  퇴근 [만족도]
    업무일지 저장 (기본값: 😊 괜찮았어요)
    예: 퇴근 "🚀 완벽했어요"

  작업도움말
    이 도움말 표시

🚀 빠른 사용 예시
─────────────────────────────────────────────────────────────

  # 아침 출근
  출근

  # 업무 확인
  상태확인

  # 파일 준비
  작업 https://drive.google.com/file/d/ABC123/view

  # 파일 수정 (로컬 에디터)
  vim works/20260405_143000/document.txt

  # 작업 완료
  완료 "문서 작성" "works/20260405_143000/document.txt" "1.5"

  # 반복...

  # 퇴근
  퇴근 "🚀 완벽했어요"

💡 팁
─────────────────────────────────────────────────────────────

• alias 영구 저장: ~/.bashrc 또는 ~/.zshrc에 추가
  echo 'source /mnt/c/Users/ksh/Desktop/Claude/.claude/cli-setup.sh' >> ~/.bashrc

• 작업 폴더 빠르게 접근
  cd $(ls -td works/* | head -1)

• Discord 명령어
  !출근   — 봇 상태 확인
  !지시   — 대기 업무 조회
  !퇴근   — 일지 저장 (Discord에서)

EOF
}

# 자동 출력 (처음 한 번만)
if [ -z "$CLAUDE_CLI_LOADED" ]; then
    export CLAUDE_CLI_LOADED=1
    echo -e "${GREEN}✅ Claude Code 자동화 CLI 로드 완료${NC}"
    echo -e "${BLUE}💡 도움말: 작업도움말${NC}"
fi
