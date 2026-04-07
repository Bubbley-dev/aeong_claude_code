# 작업 자동화 명령어

Claude Code의 최적화된 작업 워크플로우를 간편하게 실행합니다.

## 4가지 주요 명령어

### 1. `/작업` — 파일 다운로드 및 준비
```bash
./cmd/work.sh "https://drive.google.com/file/d/XXXXX/view"
```

**동작:**
- Google Drive에서 파일 다운로드
- `works/{타임스탐프}/` 폴더 자동 생성
- 파일을 작업 폴더에 복사

**출력:**
```
✅ 파일명 준비 완료
📁 작업 폴더: works/20260405_143000/
```

---

### 2. `/완료` — 작업 결과 기록
```bash
./cmd/done.sh "작업 설명" "결과파일.txt" "2.5"
```

**인자:**
- `[내용]` — 작업 내용 설명 (필수)
- `[결과파일]` — 수정된 파일 경로 (선택)
- `[시간]` — 소요 시간(시간) (선택, 기본값 0)

**동작:**
- 결과 파일 Google Drive에 업로드
- Notion 작업보고 DB에 행 추가
- work-history.md에 기록
- Discord에 자동 알림

**예:**
```bash
./cmd/done.sh "로그인 페이지 로직 수정" "works/20260405_143000/login.py" "2.5"
```

---

### 3. `/상태확인` — 봇 상태 및 대기 업무
```bash
./cmd/status.sh
```

**출력:**
```
**애옹이 상태**
봇: 🟢 온라인

**대기 업무**
1. 🔴 [긴급] 버그 수정
2. 🟡 [보통] 로그인 개선
```

---

### 4. `/일지` — 업무일지 동기화
```bash
./cmd/log.sh "😊 괜찮았어요"
```

**동작:**
- work-history.md 오늘 섹션 읽기
- Notion 업무일지 DB에 생성 또는 수정
- 작업 건수 자동 집계

**만족도 옵션:**
- `🚀 완벽했어요` — 최고조
- `😊 괜찮았어요` — 무난함 (기본값)
- `😐 그냥저냥` — 아쉬움

---

## 완전한 워크플로우 예시

```bash
# 1. 아침 출근
claude !출근  # Discord에서 입력

# 2. 대기 업무 확인
./cmd/status.sh

# 3. 첫 번째 작업 파일 준비
./cmd/work.sh "https://drive.google.com/file/d/ABC123/view"

# 4. 파일 수정 (로컬 에디터에서)
# vim works/20260405_143000/document.txt

# 5. 작업 완료 기록
./cmd/done.sh "문서 작성 및 검토" "works/20260405_143000/document.txt" "1.5"

# 6. 다음 작업 반복...

# 7. 퇴근 시 일지 저장
./cmd/log.sh "🚀 완벽했어요"

# 또는 Discord에서
claude !퇴근
```

---

## 기술 스택

- **Python:** `utils/work_automation.py` (자동화 로직)
- **Shell:** `cmd/*.sh` (CLI 래퍼)
- **Google Drive API:** 파일 다운로드/업로드
- **Notion API:** DB 기록
- **Discord API:** 알림

---

## 고급 사용

### 작업 폴더 직접 지정
```python
from utils.work_automation import download_work_file, complete_work

result = download_work_file("DRIVE_LINK")
# result['work_dir']로 작업 폴더 경로 확인

complete_work("작업 설명", "/custom/path/file.txt", 3.0)
```

### 자동 Discord 알림 비활성화
`utils/work_automation.py`의 `complete_work()` 함수에서 Webhook 호출 부분 주석 처리

---

## 문제 해결

**"Google Drive 서비스 초기화 실패"**
- `drive/drive-key.json` 파일 확인
- Notion 인증 확인

**"Notion 기록 실패"**
- `notion/.env` 토큰 확인
- 각 DB ID 정확성 확인

**파일 업로드 안 됨**
- `drive/drive-key.json`이 Google Drive 쓰기 권한 있는지 확인
