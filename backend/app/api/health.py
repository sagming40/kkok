# 홀 직원: 요청을 받아 주방장에게 넘기고, 결과에 맞는 HTTP 응답을 돌려준다.
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.health import HealthResponse
from app.services import health_service

# prefix="/api" = 이 router의 모든 주소 앞에 /api를 붙인다.
router = APIRouter(prefix="/api", tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    # /docs 화면에 "상태 코드 503 시에도 같은 형식으로 온다"는 걸 보여주기 위한 설명서
    responses={503: {"model": HealthResponse, "description": "DB 연결 실패"}},
)
async def get_health(
    response: Response,
    # Depends(get_db) = 요청을 처리하는 동안 사용할 DB Session 하나 빌려오기
    # 요청이 끝나면 자동 반납 → get_db
    session: AsyncSession = Depends(get_db),
) -> HealthResponse:
    result = await health_service.check_health(session)
    
    # ok/error 판정은 주방장이 했고, 내린 판정을 HTTP 숫자로 변환하는 건 홀 직원의 몫
    # 본문 모양은 그대로 두고 상태 코드만 503으로 변환한다.
    if result.status != "ok":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    
    return result
