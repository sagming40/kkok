# app/main.py
# kkok-backend의 "가게 정문"
# uvicorn(건물 관리인)이 app/main.py 안의 app(가게)을 찾아서 문을 열어준다.

from fastapi import FastAPI

# FastAPI() = 가게를 하나 차린다.
# title과 version은 간판이다. /docs 화면 맨 위에 그대로 적힌다.
# version은 v0.1.0으로 맞춘다. (완료 기준)
app = FastAPI(
    title="콕 (kkok) API",
    version="0.1.0",
)

# 이제 막 차린 가게라 메뉴(router)가 하나도 없다.
# 추후 api/health.py를 만들어 메뉴판을 붙인다. ─ app.include_router
