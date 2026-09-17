# app/core/exceptions.py
# "가게 전용 에러 쪽지" 양식
# 앞으로 Service · Router에서 문제가 생기면 이 class로 throw exception 한다.

from fastapi import status


class AppError(Exception):
    """
    kkok API에서 의도적으로 던지는 모든 error의 부모 class
    
    비유: 손님께 건네드릴 "사과 쪽지"의 정형화된 양식
    ─ 항상 4단계로 사과하도록 강제한다.
    code(발생한 상황), message(손님께 건넬 쪽지),
    status_code(각 상황별 사과 멘트), details(발생한 상황의 세부 사항)
    """
    
    def __init__(self, code: str, message: str, 
                 status_code: int = status.HTTP_400_BAD_REQUEST, 
                 details: list | dict | None = None) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


# 자주 사용하는 error는 code·status_code를 매번 적지 않도록 미리 만들어둔다.
# 실제로 사용할 곳이 지속적으로 생길 예정이라 형태를 미리 잡아두어 바로바로 가져다 쓸 수 있게 한다.


class NotFoundError(AppError):
    """
    04_api-spec.md 3.3절: *NOT_FOUND 계열
    """ 
    
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code, message, status.HTTP_404_NOT_FOUND)


class ForbiddenError(AppError):
    """
    04_api-spec 3.3절: FORBIDDEN, INVITE_REQUIRED 등등
    """
    
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code, message, status.HTTP_403_FORBIDDEN)     
