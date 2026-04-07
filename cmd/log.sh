#!/bin/bash
# /일지 [만족도] — work-history → Notion 업무일지 동기화
cd "$(dirname "$(dirname "$(readlink -f "$0")")")"
python3 utils/work_automation.py sync "$1"
