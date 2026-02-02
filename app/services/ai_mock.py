import random
import asyncio
from fastapi import HTTPException

async def flaky_transcription(text:str)->str:
    await asyncio.sleep(random.uniform(1,3))

    if random.random()<0.25:
        raise HTTPException(status_code=503,detail="AI Unavailable")
    
    return f"Transcipt for :{text}"