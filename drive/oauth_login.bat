@echo off
cd /d "C:\Users\ksh\Desktop\Claude\drive"
pip install google-auth google-auth-oauthlib google-api-python-client -q
python oauth_login.py
echo.
echo 완료! 아무 키나 누르세요...
pause > nul
