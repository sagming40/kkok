# GET /api/health 채점표
async def test_health_returns_ok(client):
    """
    DB가 켜져 있을 때 health가 200, ok를 돌려주는지 확인 한다.
    """
    # 문제를 낸다 (요청)
    response = await client.get("/api/health")
    
    # 정답과 대조한다 (assert = "맞는 응답인가? 틀렸다면 알려달라.")
    assert response.status_code == 200
    
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "ok"
