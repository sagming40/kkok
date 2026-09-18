# app/main.py
# kkok-backend의 "가게 정문"
# uvicorn(건물 관리인)이 app/main.py 안의 app(가게)을 찾아서 문을 열어준다.

from fastapi import FastAPI

from app.api import health
from app.core.error_handlers import register_error_handlers

# FastAPI() = 가게를 하나 차린다.
# title과 version은 간판이다. /docs 화면 맨 위에 그대로 적힌다.
# version은 v0.1.0으로 맞춘다. (완료 기준)
app = FastAPI(
    title="콕 (kkok) API",
    version="0.1.0",
)

# 예외 응대 매뉴얼을 가게 전체에 붙인다.
register_error_handlers(app)

# 메뉴판(router)을 가게에 붙인다.
# ⚠️ 순서 규칙: 새 메뉴판은 아래로 차곡차곡 쌓는다.
#    추후 구현할 redirect.router(/{code})는 "아무 주소나 다 받는" 메뉴라서
#    반드시 맨 마지막 줄이어야 한다. 위 쪽에 위치해 있으면 다른 주소를 전부 가로채 버린다.
app.include_router(health.router)
