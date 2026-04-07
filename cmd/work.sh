#!/bin/bash
# /작업 [드라이브링크] — 파일 다운로드 및 작업 폴더 생성
cd "$(dirname "$(dirname "$(readlink -f "$0")")")"
python3 utils/work_automation.py download "$1"
