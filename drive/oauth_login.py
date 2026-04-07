#!/usr/bin/env python3
import os, sys

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CLIENT_FILE = os.path.join(BASE_DIR, "oauth_client.json")
TOKEN_FILE  = os.path.join(BASE_DIR, "token.json")
SCOPES      = ["https://www.googleapis.com/auth/drive"]

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, scopes=SCOPES)
            flow.redirect_uri = "http://localhost:9090"
            creds = flow.run_local_server(
                host="localhost",
                port=9090,
                open_browser=True,
                redirect_uri_trailing_slash=False
            )

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds

if __name__ == "__main__":
    get_credentials()
    print("✅ 인증 완료! token.json 저장됨")
