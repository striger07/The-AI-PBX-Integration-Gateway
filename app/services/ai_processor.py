import asyncio
from app.services.ai_mock import flaky_transcription
from app.core.database import AsyncSessionLocal
from app.models.call import Call,CallState
from app.models.analysis import CallAnalysis

async def process_call_ai(call_id):
    delay=1
    max_retries=5

    for attempt in range(max_retries):
        try:
            async with AsyncSessionLocal() as session:
                call=await session.get(Call,call_id)
                call.state=CallState.PROCESSING_AI
                await session.commit()

            transcript=await flaky_transcription("merged packets")
            sentiment="POSITIVE"

            async with AsyncSessionLocal() as session:
                session.add(CallAnalysis(
                   call_id=call_id,
                   transcript=transcript,
                   sentiment=sentiment
                   attempts=attempt+1
            ))
                call=await session.get(Call,call_id)
                call.state=CallState.ARCHIVED
                await session.commit()
            return
        
        except Exception:
           await asyncio.sleep(delay)
           delay *=2
    
    async with AsyncSessionLocal() as session:
       call=await session.get(Call,call_id)
       call.state=CallState.FAILED
       await session.commit()

