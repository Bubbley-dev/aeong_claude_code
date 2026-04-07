@echo off
:: 1. 현재 배치파일이 있는 윈도우 경로를 WSL용 경로로 자동 변환
:: %~dp0는 현재 파일의 드라이브+경로를 의미하며, 이를 리눅스용(/mnt/c/...)으로 바꿉니다.
for /f "tokens=*" %%i in ('wsl wslpath "%~dp0"') do set WSL_PATH=%%i

:: 마지막 슬래시 제거 (필요 시)
set WSL_PATH=%WSL_PATH:~0,-1%

echo [?? 애옹이 상대경로 부팅 중...]
echo 현재 위치: %WSL_PATH%

:: 2. 기존 프로세스 종료
wsl bash -c "cd %WSL_PATH% && kill -9 $(cat discord_monitor.pid) 2>/dev/null; rm discord_monitor.pid 2>/dev/null"

:: 3. 봇 실행 (상대경로 적용)
wsl bash -c "cd %WSL_PATH% && nohup python3 discord_monitor.py > discord_monitor.log 2>&1 &"

echo [? 재부팅 완료!]
pause