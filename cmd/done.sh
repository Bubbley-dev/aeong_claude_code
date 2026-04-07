#!/bin/bash
# /완료 [내용] [결과파일] [시간] — 작업 완료 기록 (Notion + work-history)
cd "$(dirname "$(dirname "$(readlink -f "$0")")")"
python3 utils/work_automation.py complete "$1" "$2" "$3"
