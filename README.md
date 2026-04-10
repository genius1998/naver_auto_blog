# Naver Auto Blog

엑셀 기반 Python 자동화 스크립트를 Spring Boot + React 웹 서비스 형태로 옮기는 작업용 저장소입니다.

## 현재 구조

- `backend/`
  - Spring Boot API
  - `POST /api/publish-jobs` 로 발행 요청 수신
- `frontend/`
  - React UI
  - `blogId`, `naverUserId`, `cookiesRaw`, `keyword` 직접 입력 후 발행 요청
- `publisher_core.py`
  - Gemini 텍스트 생성
  - 로컬 네이버 발행 클라이언트 호출
- `publisher_cli.py`
  - Spring Boot가 subprocess로 호출하는 Python 진입점

## 로컬 전용 파일

- `naver_blog_client_local.py`
  - 실제 네이버 블로그 내부 API 호출 구현
  - `.gitignore`에 포함되어 repo에 올라가지 않음
- `naver_blog_client_template.py`
  - 인터페이스/구조 참고용 템플릿

## 실행

### Backend

```powershell
cd backend
.\gradlew.bat bootRun
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

## 환경 변수

기본 Gemini 키는 코드에 들어 있지만, 필요하면 환경 변수로 덮어쓸 수 있습니다.

```powershell
$env:GEMINI_API_KEY="..."
```

## 주의

- 실제 네이버 발행 로직과 세션 쿠키가 들어간 파일은 커밋 대상에서 제외했습니다.
- 레거시 테스트 스크립트 중 민감정보가 섞인 파일도 `.gitignore`로 제외했습니다.
