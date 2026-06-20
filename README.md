# 🛒 Shopping List App

서버 없이 브라우저에서 바로 실행되는 쇼핑 리스트 웹앱입니다.

## 실행 방법

`index.html` 파일을 브라우저에서 열면 바로 실행됩니다. 별도 서버 불필요.

## 기능

- **추가** — 텍스트 입력 후 `+` 버튼 또는 `Enter`
- **체크** — 체크박스 클릭 시 취소선 처리
- **삭제** — 항목별 `✕` 버튼
- **완료 항목 일괄 삭제** — 하단 "완료 항목 삭제" 버튼
- **데이터 유지** — `localStorage` 저장으로 새로고침해도 목록 유지

## 자동 테스트

Playwright(Python)로 작성된 자동화 테스트가 포함되어 있습니다.

```bash
pip install playwright
python -m playwright install chromium
python test_app.py
```

### 테스트 항목 (16개)

| # | 항목 |
|---|------|
| 1 | 초기 빈 상태 메시지 표시 |
| 2 | 버튼 클릭으로 아이템 추가 |
| 3 | Enter 키로 아이템 추가 |
| 4 | 추가 후 입력창 자동 초기화 |
| 5 | 헤더 통계 업데이트 |
| 6 | 체크 시 done 클래스 + 취소선 |
| 7 | 완료 카운터 업데이트 |
| 8 | 체크 토글(해제) |
| 9 | 개별 삭제 버튼 |
| 10 | 완료 항목 일괄 삭제 |
| 11 | 새로고침 후 localStorage 유지 |
| 12 | 🔍 공백 입력 무시 |
| 13 | 🔍 빈 입력 무시 |
| 14 | 🔍 XSS 이스케이프 처리 |
| 15 | 🔍 전부 삭제 후 빈 상태 복귀 |

## 기술 스택

- **Frontend**: Vanilla HTML / CSS / JavaScript (프레임워크 없음)
- **데이터 저장**: localStorage
- **테스트**: Python + Playwright
