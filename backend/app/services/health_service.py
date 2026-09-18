# 주방장: 창고 담당의 보고를 받아서 "ok" / "error"로 판정한다.
# HTTP 상태 코드(503 등)는 절대 다루지 않는다.

import asyncio
import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import health_repository
from app.schemas.health import CheckStatus, HealthResponse

logger = logging.getLogger(__name__)

# 창고 문을 두드린 후 최대 몇 초까지 대기할지
# DB에서 응답이 없는데 연결도 끊기지 않는 상태일 때
# health 요청 자체가 한참을 멈춰버린다. 상태 확인이 멈추면 의미가 없다.
DB_CHECK_TIMEOUT_SECONDS = 2


async def check_health(session: AsyncSession) -> HealthResponse:
    # 부품별로 점검한 뒤, 전부 ok일 때만 가게 전체를 ok로 본다.
    database = await _check_database(session)
    overall: CheckStatus = "ok" if database == "ok" else "error"
    return HealthResponse(status=overall, database=database)


async def _check_database(session: AsyncSession) -> CheckStatus:
    try:
        # wait_for = Timer를 맞춰놓고 주문 넣기. 2초 안에 오지 않으면 포기
        await asyncio.wait_for(
            health_repository.ping_database(session),
            timeout=DB_CHECK_TIMEOUT_SECONDS,
        )
    except (SQLAlchemyError, OSError, TimeoutError) as exc:
        # SQLAlchemyError : DB가 거절함 (비밀번호 오류, DB 미존재)
        # OSError         : 연결 자체가 되지 않음 (컨테이너 꺼짐 → 연결 거부)
        # TimeoutError    : 2초 동안 응답 없음 
        #
        # ⚠️ log에는 예외 "종류 이름"만 남긴다.
        # 연결 관련 에러 메시지에는 접속 주소 같은 정보들이 섞여 있을 수 있어서,
        # DATABASE_URL 계열 정보가 log로 새어나가는 것을 막아야 한다.
        # TimeoutError는 사실 OSError의 하위 class라 중복이지만,
        # 아래 3가지 실패 유형을 눈으로 직접 구분짓기 위해 일부러 함께 적었다.
        logger.warning("DB 상태 확인 실패: %s", type(exc).__name__)
        return "error"
    return "ok"
