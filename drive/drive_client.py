#!/usr/bin/env python3
"""
Google Drive API 클라이언트
- 드라이브 링크에서 파일 ID 추출
- 파일 다운로드
- 파일 업로드
"""

import os
import json
import re
from typing import Optional, Tuple
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from io import BytesIO

# 인증 키 경로
KEY_PATH = os.path.join(os.path.dirname(__file__), "drive-key.json")

# Google Drive API 인증
SCOPES = ['https://www.googleapis.com/auth/drive']


def get_drive_service():
    """Google Drive 서비스 객체 생성"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            KEY_PATH, scopes=SCOPES
        )
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        print(f"[Drive] 인증 실패: {e}")
        return None


def extract_file_id(link: str) -> Optional[str]:
    """
    구글 드라이브 링크에서 파일 ID 추출

    지원 형식:
    - https://drive.google.com/file/d/{FILE_ID}/view
    - https://drive.google.com/open?id={FILE_ID}
    - {FILE_ID} (직접 입력)
    """
    # 패턴 1: /file/d/{ID}/view
    match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', link)
    if match:
        return match.group(1)

    # 패턴 2: ?id={ID}
    match = re.search(r'[?&]id=([a-zA-Z0-9-_]+)', link)
    if match:
        return match.group(1)

    # 패턴 3: 직접 ID
    if re.match(r'^[a-zA-Z0-9-_]+$', link):
        return link

    return None


def download_file(file_link: str, save_path: Optional[str] = None) -> Tuple[bool, str]:
    """
    Google Drive 파일 다운로드

    Args:
        file_link: 파일 링크 또는 파일 ID
        save_path: 저장할 경로 (None이면 파일명으로 자동 저장)

    Returns:
        (성공 여부, 저장된 경로 또는 오류 메시지)
    """
    try:
        service = get_drive_service()
        if not service:
            return False, "Google Drive 서비스 초기화 실패"

        file_id = extract_file_id(file_link)
        if not file_id:
            return False, "유효한 파일 링크가 아닙니다"

        # 파일 메타데이터 조회
        try:
            file_metadata = service.files().get(fileId=file_id, fields='name').execute()
            file_name = file_metadata.get('name', f'download_{file_id}')
        except Exception as e:
            return False, f"파일 조회 실패: {e}"

        # 저장 경로 결정
        if save_path is None:
            save_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "downloads",
                file_name
            )

        # downloads 폴더 생성
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 파일 다운로드
        request = service.files().get_media(fileId=file_id)
        with open(save_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

        return True, save_path

    except Exception as e:
        return False, f"다운로드 오류: {str(e)}"


def upload_file(local_path: str, folder_id: Optional[str] = None) -> Tuple[bool, str]:
    """
    로컬 파일을 Google Drive에 업로드

    Args:
        local_path: 로컬 파일 경로
        folder_id: 업로드할 폴더 ID (None이면 루트)

    Returns:
        (성공 여부, 파일 ID 또는 오류 메시지)
    """
    try:
        if not os.path.exists(local_path):
            return False, f"파일을 찾을 수 없습니다: {local_path}"

        service = get_drive_service()
        if not service:
            return False, "Google Drive 서비스 초기화 실패"

        file_name = os.path.basename(local_path)

        # 메타데이터
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        # 업로드
        media = MediaFileUpload(local_path, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink',
            supportsAllDrives=True
        ).execute()

        file_id = file.get('id')
        file_link = file.get('webViewLink')

        return True, f"업로드 완료: {file_link}"

    except Exception as e:
        return False, f"업로드 오류: {str(e)}"


def get_file_info(file_link: str) -> Tuple[bool, dict]:
    """
    Google Drive 파일 정보 조회

    Returns:
        (성공 여부, 파일 정보 딕셔너리)
    """
    try:
        service = get_drive_service()
        if not service:
            return False, {}

        file_id = extract_file_id(file_link)
        if not file_id:
            return False, {}

        file = service.files().get(
            fileId=file_id,
            fields='id, name, mimeType, size, modifiedTime, owners'
        ).execute()

        return True, file

    except Exception as e:
        print(f"[Drive] 파일 정보 조회 오류: {e}")
        return False, {}
