# conftest.py = 테스트들이 공용으로 사용하는 "준비물 창고"
# 파일이름이 정해져 있어서, pytest가 알아서 찾아 읽는다.
# fixture는 tests/ 내부 어느 테스트에서나 이름만 호출하면 사용가능하다.

import pytest
from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    TEST용 손님을 한 명 모집한다.
    
    ASGITransport = 실제로 server 켜지 않고 app에 직접 요청을 넣는 통로
    uvicorn을 띄우고 localhost:8000으로 요청을 하는 것이 아닌,
    가게 문을 열지 않고 주방에 바로 주문서를 건네는 셈이다.
    TEST가 훨씬 빠르고 port가 이미 사용 중이라도 상관이 없다.
    """    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
