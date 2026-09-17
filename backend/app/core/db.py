# app/core/db.py
# DB 창고로 가는 "도로"와, 그 도로를 타고 다니는 "트럭 대여소"를 만든다.

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

# Engine = 창고로 가는 도로. App이 켜져 있는 동안 딱 하나만 만들어서 계속 사용한다.
# echo=True로 주게 되면 실제 SQL 문장이 Terminal에 그대로 찍힌다.
# 지금은 "도로가 제대로 뚫렸는지" 직관적으로 확인하기 위해 켜둔다. ─ 추후 log가 불어나면 False로 끈다.
engine = create_async_engine(settings.database_url, echo=True)

# async_sessionmaker = "트럭 대여소"
# "트럭 한 대" 요청을 보내면(session_factory()) 새 트럭을 보내준다.
# expire_on_commit=False:
# 본래는 commit(짐 배달 완료 도장) 직후 트럭에 실었던 데이터를 믿지 못하게 만드는데,
# 응답을 생성할 때 그 데이터를 계속 사용해야 하는 경우가 많기 때문에 꺼둔다.
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI가 요청마다 호출하는 '트럭 대여 창구'
    
    yield 앞: 트럭을 빌려서 건네준다. (Router·Service가 이 트럭으로 업무를 본다)
    yield 뒤: 업무가 끝나면(성공/에러 상관없이) 반드시 트럭을 반납한다.
    
    async with ─ 트럭을 반납(close)하지 못했더라도 알아서(Python) 처리해준다.
    빌린 물건을 사용하고 나면 자동으로 제자리에 놓이는 셈이다.
    """
    async with session_factory() as session:
        yield session
