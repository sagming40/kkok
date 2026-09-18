# 점검표 양식: health 응답이 "어떤 칸에 어떤 값만" 들어갈 수 있는지 정해둔다.
from typing import Literal

from pydantic import BaseModel

# 각 칸에 적을 수 있는 도장은 딱 2개 뿐 ─ "ok" / "error"
# Literal = 객관식 문제. 보기 밖의 답("good", "fail" 등)을 사용하면 Pydantic이 바로 막아준다.
CheckStatus = Literal["ok", "error"]


class HealthResponse(BaseModel):
    # 가게 전체 상태: 모든 부품이 ok일 때만 ok
    status: CheckStatus
    # 창고(DB) 상태
    database: CheckStatus
    # redis 칸은 추후 Redis를 도입할 때 추가한다. (04_api-spec.md 4.2절)
