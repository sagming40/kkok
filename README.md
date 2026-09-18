<div align="center">

# 👆 콕 (kkok)

**긴 주소를 콕, 짧게.**
누가, 언제, 어디서 눌렀는지도 한눈에.

단축 URL + 클릭 분석 서비스

</div>

---

## 소개

콕은 긴 URL을 짧은 주소로 바꿔주고, 그 링크가 **언제 · 어떤 기기로 · 어디서 들어와** 눌렸는지 대시보드로 보여주는 서비스입니다.

기술 스택을 하나씩 깊게 익히기 위한 **자기계발 프로젝트**로, 기한 없이 단계별로 기능을 쌓아 올립니다.
초대 코드를 받은 사람만 링크를 만들 수 있는 **초대제**로 운영합니다.

## 주요 기능

| 기능 | 설명 | 단계 |
|---|---|:-:|
| 🔗 짧은 링크 | 긴 주소를 7자 무작위 코드로 단축 | 1 |
| ↪️ 리다이렉트 | 짧은 주소 접속 시 원래 주소로 이동 | 1 |
| 🔐 로그인 | 이메일 · 비밀번호, GitHub 로그인 | 2 |
| 🎟 초대제 | 초대 코드로 회원 승격, 관리자 코드 발급 | 2 |
| 📋 링크 관리 | 검색 · 켜기/끄기 · 삭제 | 2 |
| 👣 클릭 기록 | 시각 · 기기 · 브라우저 · 유입 경로 (IP 미저장) | 2 |
| 📊 통계 | 클릭 추이, 기기 · 유입 경로 비율, 요일×시간 히트맵 | 3 |
| ⚡ 캐싱 | Redis로 리다이렉트 가속 | 3 |
| ✨ 확장 | 커스텀 주소, 만료일, 링크 미리보기, 메일 인증 | 4 |

## 기술 스택

| 구분 | 기술 |
|---|---|
| **Frontend** | Vue 3 · TypeScript · Vite · Tailwind CSS · shadcn-vue · Pinia · Vue Router · Motion · ECharts |
| **Backend** | Python · FastAPI · Pydantic · SQLAlchemy (async) · Alembic · httpx · pytest |
| **Auth** | JWT (httpOnly 쿠키) · OAuth 2.0 (GitHub) |
| **Database** | PostgreSQL · Redis |
| **Infra** | Docker Compose · Nginx · Uvicorn · GitHub Actions |
| **Docs** | OpenAPI / Swagger UI · Mermaid |

## 아키텍처

```mermaid
flowchart LR
    User["브라우저"] --> Nginx
    Nginx -->|화면 경로| Vue["Vue 빌드 파일"]
    Nginx -->|/api/*| API["FastAPI"]
    Nginx -->|/짧은코드| API
    API --> PG[("PostgreSQL")]
    API --> Redis[("Redis")]
    API -->|OAuth| GitHub["GitHub"]
```

- 짧은 링크를 누르면 **Redis 캐시 → PostgreSQL** 순으로 원래 주소를 찾아 **302**로 이동시킵니다.
- 클릭 기록은 응답을 보낸 뒤 백그라운드에서 저장해, 기록이 실패해도 이동은 정상 동작합니다.
- 백엔드는 **Router → Service → Repository** 3층 구조입니다.

자세한 내용은 [아키텍처 설계서](docs/02_architecture.md)를 참고하세요.

## 문서

| 문서 | 내용 |
|---|---|
| [요구사항 정의서](docs/01_requirements.md) | 기능 · 비기능 요구사항, 범위 |
| [아키텍처 설계서](docs/02_architecture.md) | 시스템 구성, 핵심 흐름, 폴더 구조 |
| [ERD 설계서](docs/03_erd.md) | 테이블 · 인덱스 · Redis 키 · 인증 토큰 규칙 |
| [API 명세서](docs/04_api-spec.md) | 엔드포인트, 요청 · 응답, 에러 코드 |
| [화면 설계서](docs/05_uiux-design.md) | 유즈케이스, 화면 흐름, 화면별 상세 |
| [MILESTONES](MILESTONES.md) | 마일스톤 · 완료 기준 · 예상 일정 |
| [DEVLOG](DEVLOG.md) | 개발 일지 · 회고 |

## 프로젝트 구조

```
kkok/
├─ frontend/                # Vue 3 + Vite
│  └─ src/
│     ├─ pages/             # 화면
│     ├─ components/        # UI 부품
│     ├─ stores/            # Pinia
│     ├─ router/            # 라우터 + 가드
│     └─ api/               # 백엔드 호출
├─ backend/                 # FastAPI
│  ├─ app/
│  │  ├─ api/               # Router
│  │  ├─ services/          # Service
│  │  ├─ repositories/      # Repository
│  │  ├─ models/            # SQLAlchemy
│  │  ├─ schemas/           # Pydantic
│  │  ├─ core/              # 설정 · 보안 · 연결
│  │  └─ main.py
│  ├─ alembic/
│  └─ tests/
├─ docs/                    # 설계 문서 5종
├─ .env.example             # .env 예시
├─ .gitignore
├─ DEVLOG.md                # 개발 일지
├─ docker-compose.yml
├─ MILESTONES.md            # 마일스톤 · 개발 로드맵
├─ README.md
└─ .github/workflows/
```

## 시작하기

> ⚠️ 아래 내용은 **M1 완료 시 확정**됩니다. 현재는 예정된 실행 방법입니다.

### 준비물

- Docker / Docker Compose
- Python 3.12 이상
- Node.js (LTS)

### 1. 저장소 받기

```bash
git clone https://github.com/<your-id>/kkok.git
cd kkok
cp .env.example .env
```

### 2. DB · Redis 실행

```bash
docker compose up -d
```

### 3. 백엔드 실행

```PowerShell
cd backend
python -m venv .venv
# Windows cmd: .venv\Scripts\activate
# macOS / Linux: source .venv/bin/activate
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

- API 문서: http://localhost:8000/docs

### 4. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

- 화면: http://localhost:5173

### 5. 테스트

```bash
cd backend
pytest
```

### 환경변수

| 이름 | 설명 | 예시 |
|---|---|---|
| `DATABASE_URL` | PostgreSQL 연결 주소 (async) | `postgresql+asyncpg://kkok:kkok@localhost:5433/kkok` |
| `REDIS_URL` | Redis 연결 주소 | `redis://localhost:6379/0` |
| `BASE_URL` | 짧은 주소 앞부분 | `http://localhost:8000` |
| `JWT_SECRET` | JWT 서명 키 | 충분히 긴 무작위 문자열 |
| `COOKIE_SECURE` | 쿠키 `Secure` 옵션 | 개발 `false` / 운영 `true` |
| `GITHUB_CLIENT_ID` | GitHub OAuth 앱 ID | M5부터 사용 |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth 앱 비밀값 | M5부터 사용 |

> `.env`는 절대 커밋하지 않습니다. `.env.example`만 저장소에 포함합니다.

## 로드맵

| 마일스톤 | 내용 | 예상 기간 | 상태 |
|:-:|---|---|:-:|
| M0 | 설계 | ~ 2026-09-17 | ✅ |
| M1 | 개발 환경과 뼈대 | 2026-09 ~ 10 | 🟨 |
| M2 | 줄이고 이동하기 | 2026-10 | ⬜ |
| M3 | 로그인 | 2026-10 ~ 11 | ⬜ |
| M4 | 초대제와 관리자 | 2026-11 | ⬜ |
| M5 | 링크 관리 · 클릭 기록 · GitHub | 2026-12 ~ 2027-01 | ⬜ |
| M6 | 통계 · 대시보드 · 캐싱 | 2027-01 ~ 02 | ⬜ |
| M8 | 배포 (`v1.0.0`) | 2027-02 | ⬜ |
| M7 | 확장 기능 (`v1.1.0`) | 2027-03 | ⬜ |

자세한 작업 목록과 완료 기준은 [MILESTONES](MILESTONES.md)를 참고하세요.

## 개발 규칙

**브랜치**
- `main` + 작업별 브랜치 (`feat/…`, `fix/…`)
- 혼자 작업하더라도 Pull Request로 병합

**커밋 메시지**

| 접두어 | 용도 |
|---|---|
| `feat:` | 기능 추가 |
| `fix:` | 버그 수정 |
| `docs:` | 문서 |
| `test:` | 테스트 |
| `refactor:` | 구조 개선 |
| `chore:` | 설정 · 빌드 |

**원칙**
- 설계와 다르게 구현하면 **설계 문서를 먼저** 고친다.
- 마일스톤 완료 시 태그(`v0.x.0`)를 붙인다.

## 디자인

| 항목 | 값 |
|---|---|
| 포인트 컬러 | 코랄 오렌지 `#FF6B4A` (다크 `#FF8B6B`) |
| 폰트 | Pretendard |
| UI 기반 | shadcn-vue 기본 테마 |
| 모드 | 라이트 · 다크 · 시스템 |

## 라이선스

미정

---

<div align="center">

Made by [sagming40](https://github.com/sagming40) · 👆 콕

</div>
