import pytest
import asyncio
import time 
from uuid import uuid4
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_race_condition():
    call_id=uuid4()

    payload={
        "sequence":1,
        "data":"audio",
        "timestamp":time.time()
    }
    async with AsyncClient(app=app,base_url="http://test") as client:
        async def send():
            return await client.post(
                f"/v1/call/stream/{call_id}",
                json=payload
            )
        r1,r2=await asyncio.gather(send(),send())

        assert r1.status_code==202
        assert r2.status_code==202