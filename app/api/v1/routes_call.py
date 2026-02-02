from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.schemas.packet import PacketSchema
from app.models.call import Call, CallState
from app.models.packet import CallPacket
from app.core.database import get_session
from app.utils.logger import logger

router = APIRouter()

@router.post("/v1/call/stream/{call_id}", status_code=202)
async def ingest_packet(
    call_id: UUID,
    packet: PacketSchema,   # 👈 COMMA IS REQUIRED
    session: AsyncSession = Depends(get_session)
):
    async with session.begin():
        result = await session.execute(
            select(Call).where(Call.id == call_id).with_for_update()
        )
    call = result.scalar_one_or_none()

    if not call:
        call = Call(
            id=call_id,
            state=CallState.IN_PROGRESS,
            last_sequence=0
        )
        session.add(call)

        expected = (call.last_sequence or 0) + 1
        if packet.sequence != expected:
            logger.warning(
                f"Missing packet for call {call_id}: expected {expected}, got {packet.sequence}"
            )

        try:
            session.add(CallPacket(
                call_id=call_id,
                sequence=packet.sequence,
                data=packet.data,
                timestamp=packet.timestamp
            ))
            call.last_sequence = max(call.last_sequence, packet.sequence)
        except Exception:
            pass  # duplicate packet

    return {"status": "accepted"}
