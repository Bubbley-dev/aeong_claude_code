#!/bin/bash
# /상태확인 — 봇 상태 + 대기 업무 확인
cd "$(dirname "$(dirname "$(readlink -f "$0")")")"
python3 utils/work_automation.py status
