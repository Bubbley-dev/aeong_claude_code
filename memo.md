### 디스코드 재부팅
```
! cd /mnt/c/Users/ksh/Desktop/Claude/discord && kill -9 $(cat discord_monitor.pid 2>/dev/null) 2>/dev/null; rm discord_monitor.pid 2>/dev/null; nohup python3 discord_monitor.py > discord_monitor.log 2>&1 &
```