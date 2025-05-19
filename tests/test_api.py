# tests/test_api.py
import httpx, asyncio, pytest

BASE = "http://localhost:8000/api/v1"

@pytest.mark.asyncio
async def test_batch_limit():
    async with httpx.AsyncClient(base_url=BASE) as client:
        resp = await client.post("/employees/batch", json=[])
        assert resp.status_code == 400
