# app\core\error_handlers.py ─ "예외 응대 매뉴얼"
# 어떤 예외가 날아오든 04_api-spec.md 3.1절 형식으로 통일하여 내보낸다.

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError

# log 담당자 ─ print 대신 logging을 사용한다.
# "언제(몇 시), 어디에서(파일), 얼마나 심각한" 문제가 터졌는지 형식이 갖춰 나온다.
logger = logging.getLogger("kkok")


def _error_body(code: str, message: str, details=None) -> dict:
    """
    04_api-spec.md 3.1절 형식으로 쪽지를 접는다
    함수로 뺀 이유 ─ 세 군데에서 똑같이 사용해야 한다.
    """
    return {"error": {"code": code, "message": message, "details": details}}


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """
    직접 raise AppError(...)를 던진 경우
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(exc.code, exc.message, exc.details),
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    요청 형식이 맞지 않을 때 FastAPI가 자동으로 던지는 예외 (예: 필수 값 누락 등)
    exc.errors()는 FastAPI 고유 형식이기 때문에 직접 만든 형식(field, reason)으로 바꿔 담는다.
    """    
    details = [
        {
            # loc 예: ("body", "password") → 맨 뒤 조각이 실제 field 명이다
            "field": str(err["loc"][-1]) if err["loc"] else "body",
            "reason": err["msg"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_error_body("VALIDATION_ERROR", "입력값을 확인해 주세요.", details),
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    예상치 못한 "진짜" 버그
    
    비유: 가게에서 처음 겪어본 사고가 생겼을 때 꺼내는 최후의 안전망
    사용자에게는 세세한 Python error message(비밀번호 값이 섞여 들어갈 수도 있음)를
    그대로 노출시키면 안되므로 server log에만 자세히 남기고 사용자에게는 뭉뚱그려 답한다. 
    """
    logger.exception("처리되지 않은 예외 발생")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_error_body("INTERNAL_ERROR", "서버 문제가 발생했습니다."),
    )


def register_error_handlers(app: FastAPI) -> None:
    """
    main.py에서 이 함수 하나만 호출하면 위 세 매뉴얼이 전부 등록된다.
    """
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
