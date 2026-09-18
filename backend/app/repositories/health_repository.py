# 창고 담당: DB에 실제로 말을 걸어보는 일만 한다. ─ ⭐ 판단은 하지 않는다 ⭐
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def ping_database(session: AsyncSession) -> None:
    # "SELECT 1" = 창고 문을 똑똑 두드려보는 것
    # 아무 테이블도 건드리지 않고, DB가 정상적으로 응답만 하면 성공
    # 응답이 없으면(꺼짐, 비번 틀림 등) 예외가 터지고,
    # 그 예외를 어떻게 해석할지는 Service(주방장)가 정한다.
    await session.execute(text("SELECT 1"))
