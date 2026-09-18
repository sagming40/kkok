# 콕 (kkok) DEVLOG

> 이 문서는 **날마다 · 마일스톤마다의 진행 기록**이다.
> "무엇을 왜 그렇게 했는지"를 담는 `MILESTONES.md`(계획)와 달리, 여기는 **실제로 무슨 일이 있었는지**를 담는다.
> 최신 기록이 맨 위로 오게 적는다.

---

## 쓰는 법

### 매일 쓰는 항목 (짧게, 5분)

작업을 마칠 때마다 아래 형식으로 한 칸씩 채운다. 길게 쓰려 하지 말고, **다음에 이어서 볼 내가 이해할 정도**면 충분하다.

```markdown
### 2026-09-21 (월) · M1

**한 일**
-

**막힌 것 · 해결**
-

**다음 할 일**
-
```

| 항목 | 채우는 기준 |
|---|---|
| 한 일 | 완료했거나 눈에 보이게 진전된 것. "공부함", "조금 함"처럼 애매하게 쓰지 않기 |
| 막힌 것 · 해결 | 30분 넘게 막혔던 것과, 어떻게 풀었는지 (또는 못 풀었으면 다음에 시도할 것) |
| 다음 할 일 | 다음번 세션 작업 시작 시 뭐부터 할지 1~3개. **이번 세션 감잡기** |

### 마일스톤 끝날 때 쓰는 항목 (길게)

`MILESTONES.md`의 완료 기준을 다 채웠을 때, 아래 회고를 채우고 `docs/retro/M{번호}.md`로 옮겨도 되고 이 파일에 남겨도 된다.

```markdown
## 회고 — M1 개발 환경과 뼈대

**기간**: 2026-09-21 ~ 09-30 (예상 09-21~10-04)

**만든 것**
-

**설계와 달라진 것**
(달라졌으면 `02_architecture.md` 등 설계 문서를 먼저 고치고, 여기엔 무엇을 왜 바꿨는지만 남긴다)
-

**가장 오래 막힌 문제**
-

**새로 이해한 개념**
-

**다음 마일스톤에서 조심할 것**
-
```

### 기록 습관 팁

- **거짓말하지 않기.** "잘 됐다"보다 "왜 안 됐는지"가 나중에 훨씬 값지다.
- 에러 메시지는 **원문 그대로** 한 줄 붙여두면 나중에 검색하기 좋다.
- 커밋하기 직전에 쓰면, 커밋 메시지랑 자연스럽게 맞아떨어진다.
- 하루에 여러 번 앉았다 떠나면, 그때마다 짧게 나눠 적어도 된다.
- 이 파일이 길어지면 분기 단위(`DEVLOG-2026-Q4.md`)로 나누고, 이 파일엔 최근 기록만 남긴다.

---

## 진행 요약

마일스톤이 끝날 때마다 한 줄씩 채운다. `MILESTONES.md`의 진행 현황표와 같이 본다.

| 마일스톤 | 시작 | 완료 | 실제 걸린 기간 | 비고 |
|---|---|---|---|---|
| M0 설계 | 2026-09-16 | 2026-09-17 | 2일 | 요구사항 → 아키텍처 → ERD → API 명세 → 화면 설계 |
| M1 개발 환경과 뼈대 | 2026-09-17 | - | - | - |

---

## 회고 모음

<!-- 마일스톤이 끝날 때마다 이 아래에 회고를 위에서부터 쌓는다 -->

---

## 일별 기록

<!-- 매일 여기에 위에서부터 쌓는다 -->

---

### 2026-09-17 (목/저녁~밤/집 PC) · M1

**한 일**
- README.md를 따라 집 PC에서 기기에 맞춰 개발 환경을 다시 세팅함
  - Docker Desktop 설치 (집 PC는 WSL2가 이미 활성화되어 있었음)
  - 저장소 클론(kkok) → .env 세팅 → DB 실행(`docker compose up -d`) PostgreSQL 컨테이너 정상 기동 확인 완료
  - 백엔드 실행 ─ Python 가상환경 `backend/.venv` 생성 → 의존성 패키지 설치(`backend/ pip install -r requirements-dev.txt`)
  - 서버 정상 작동 확인 완료 ─ `uvicorn app.main:app --reload` 
- `core/config.py` 작성 — `.env`(저장소 루트) 기반 설정 관리, `pydantic-settings`로 `DATABASE_URL` 로드 확인
- `core/db.py` 작성 — async Engine + `session_factory` + `get_db` 의존성, PostgreSQL 연결 확인 (`select pg_catalog.version()`)
- `core/exceptions.py`, `core/error_handlers.py` 작성 — `AppError` 및 3종 예외 처리기, `04_api-spec.md` 3.1절 형식으로 통일 확인

**막힌 것 · 해결**
- 학교 PC에서 만든 `.venv`는 Git에 추적되지 않으므로, 집 PC에서도 새로 생성함 → 기기마다 `.venv` 재생성 후 `requirements-dev.txt` 설치로 해결
- PowerShell의 `curl`(=`Invoke-WebRequest`)이 4xx/5xx 응답에서 본문 대신 예외를 던짐 → 브라우저로 실제 응답 재확인, 동작 자체는 정상이었음을 확인

**다음 할 일**
- `GET /api/health` 구현 (DB 연결 확인 포함, 3층 구조 중 첫 Router)
- `alembic init -t async` 마이그레이션 초기화
- pytest + async 플러그인 설정, health 테스트 1개

---

### 2026-09-18 (금/오전/학교 PC) · M1

**한 일**
- `GET /api/health` 구현 — Router → Service → Repository 3층 구조 첫 관통
  - `schemas/health.py` — `HealthResponse`, `CheckStatus`(Literal로 ok/error만 허용)
  - `repositories/health_repository.py` — `SELECT 1`로 DB 연결 확인, 예외는 잡지 않고 그대로 올림
  - `services/health_service.py` — 2초 타임아웃(`asyncio.wait_for`), 실패를 ok/error로 판정. 로그엔 예외 종류 이름만 남겨 접속 정보 노출 방지
  - `api/health.py` — 실패 시 `response.status_code`만 503으로 바꿔 `response_model` 검사 유지
- `core/db.py`에 `pool_pre_ping=True` 추가 — DB 재시작 후 끊긴 연결 재사용 방지
- 동작 확인 (`curl.exe -i`) — 정상 `200 {"status":"ok","database":"ok"}`, `docker compose stop` 후 `503 {"status":"error","database":"error"}`(5초 내), `start` 직후 첫 요청 바로 `200`
- `04_api-spec.md` 4.2절 보강 — 503 응답 예시, `status` 판정 규칙(모든 항목 ok일 때만 ok), 공통 에러 형식의 예외임을 명시, DB 확인 타임아웃 2초
- `alembic init -t async`로 마이그레이션 초기화
  - `alembic.ini`의 `sqlalchemy.url`은 비워두고 `env.py`가 `.env` → `config.py`를 통해 읽도록 구성 (비밀값 커밋 방지)
  - `file_template`에 날짜·rev 규칙 적용
  - `models/base.py`에 `DeclarativeBase` 기반 `Base` 추가, `target_metadata = Base.metadata` 연결
  - `compare_type=True`로 컬럼 타입 변경까지 감지
  - `alembic current` 정상 실행 확인 (`Context impl PostgresqlImpl.`)
- pytest 설정 및 health 테스트 1개 — `pytest.ini`(`asyncio_mode=auto`), `conftest.py`에 `ASGITransport` 기반 `AsyncClient` fixture, `1 passed in 0.07s`

**막힌 것 · 해결**
- `alembic current` 실행 시 `UnicodeDecodeError: 'cp949' codec can't decode byte 0xec in position 3586: illegal multibyte sequence` → alembic이 `alembic.ini`를 `encoding="locale"`(한글 윈도우 기본값 cp949)로 읽는데 주석은 UTF-8 한글이라 충돌. **`.ini` 설정 파일엔 한글 주석을 쓰지 않는다**로 정리하고 영문으로 교체해 해결
- `api/health.py`에서 `responses`를 `response`로 오타 → `TypeError: APIRouter.get() got an unexpected keyword argument 'response'`. 데코레이터의 `responses`(문서용)와 함수 인자 `response`(실제 응답 객체)가 한 블록에 같이 있어 헷갈리기 쉬움
- `env.py`에서 `settings = get_settings`로 괄호 누락 → 함수 자체를 변수에 담아 `AttributeError` 발생 예정이었음. 실행 전 검수에서 발견

**다음 할 일**
- `feat/backend-skeleton` PR 생성 · `main` 병합
- 프론트엔드 시작: Vite + Vue 3 + TypeScript 프로젝트 생성, Tailwind + shadcn-vue 설치
- 화면에 health 결과 표시(연결 확인용 임시 화면)까지 가면 M1 완료 기준 충족

---

### 2026-09-17 (목/오후/학교 PC) · M1

**한 일**
- Docker Desktop 설치 (WSL2 활성화 포함), 도구 버전 확인 (Git 2.53, Python 3.13.9, Node 24.16, Docker 29.8.0)
- `.gitignore`, `.env.example`, `docker-compose.yml` 작성 (postgres:16, 포트 5433, 볼륨 영속화, healthcheck)
- `docker compose up -d`로 PostgreSQL 컨테이너 정상 기동 확인
- `chore/dev-env` 브랜치 PR #1 병합 (`main`에 반영)
- `MILESTONES.md` M1 체크박스 세분화 및 완료 항목 체크
- `backend/` 폴더 구성, Python 가상환경(`.venv`) 생성
- 의존성을 `requirements.txt`(운영) / `requirements-dev.txt`(개발)로 분리, 버전 고정
- `app/` 폴더 뼈대 구성 (`api/`, `services/`, `repositories/`, `models/`, `schemas/`, `core/`), `app/main.py` 작성 및 `/docs` 정상 기동 확인

**막힌 것 · 해결**
- 학교 PC에 Docker 미설치 확인 (`docker : 'docker' 용어가... 인식되지 않습니다`) → Docker Desktop 설치로 해결
- 집 PC·노트북에 로컬 PostgreSQL이 이미 설치돼 있어 기본 포트(5432) 충돌 가능성 발견 → 컨테이너 포트를 5433으로 통일해 세 기기 어디서든 동일하게 동작하도록 결정
- 브랜치를 안 파고 `main`에서 작업 시작 → 커밋 전 상태라 `git checkout -b`로 바로 전환, 문제없이 해결
- PR 병합 커밋의 `Close #1` 문구가 GitHub 자동 종료 키워드(`Closes`)와 다름을 발견 → `Closes #1`로 수정

**다음 할 일**
- `frontend/`, `backend/` 폴더 생성
- FastAPI 뼈대 작업 시작 (`feat/backend-skeleton` 브랜치)

---

### 2026-09-17 (목/오전/학교 PC) · M0

**한 일**
- 프로젝트 컨셉 확정: 단축 URL + 클릭 분석 서비스, 이름 "콕(kkok)"
- 요구사항 정의서, 아키텍처 설계서, ERD 설계서, API 명세서, 화면 설계서 작성 완료
- 주요 결정: 짧은 코드 무작위 7자 · httpOnly 쿠키 + DB Refresh Token 인증 · 코랄 오렌지(`#FF6B4A`) + Pretendard · ECharts
- `MILESTONES.md` 작성, 대략의 예상 일정(09-21 시작) 반영

**막힌 것 · 해결**
- 해당 없음 (설계 단계)

**다음 할 일**
- M1 시작: GitHub 저장소 생성, `frontend/` · `backend/` 폴더 구성

---
