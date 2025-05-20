# tests/test_api.py
import io, json, pathlib, pandas as pd
import pytest, httpx, asyncio

BASE = "http://localhost:8000/api/v1"

@pytest.mark.asyncio
async def test_batch_limit():
    async with httpx.AsyncClient(base_url=BASE) as client:
        resp = await client.post("/employees/batch", json=[])
        assert resp.status_code == 400

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

async def upload_csv(client, target, df):
    buf = io.BytesIO()
    df.to_csv(buf, index=False, header=False)
    buf.seek(0)
    resp = await client.post(
        "/upload_csv",
        data={"target": target},
        files={"file": (f"{target}.csv", buf, "text/csv")},
    )
    return resp

@pytest.mark.asyncio
async def test_happy_path():
    deps = pd.DataFrame([[1, "Engineering"]], columns=["id", "department"])
    jobs = pd.DataFrame([[1, "Data Engineer"]], columns=["id", "job"])
    hires = pd.DataFrame(
        [[1, "Alice", "2021-03-15T10:00:00Z", 1, 1]],
        columns=["id", "name", "datetime", "department_id", "job_id"],
    )

    async with httpx.AsyncClient(base_url=BASE) as client:
        # Carga CSVs
        for tgt, df in [("departments", deps), ("jobs", jobs), ("hired_employees", hires)]:
            r = await upload_csv(client, tgt, df)
            assert r.status_code == 200
            assert r.json()["rows_inserted"] == len(df)

        # Métricas Q1-Q4
        r1 = await client.get("/metrics/hires-2021")
        assert r1.status_code == 200
        assert r1.json()[0]["q1"] == 1

        # Departamentos > promedio
        r2 = await client.get("/metrics/above-average-2021")
        assert r2.status_code == 200
        assert r2.json()[0]["department"] == "Engineering"