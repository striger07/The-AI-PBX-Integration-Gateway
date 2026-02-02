import enum
from sqlalchemy import Column,String,Integer,Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import uuid
from app.core.database import Base

class CallState(str,enum.Enum):
    IN_PROGRESS="IN_PROGRESS"
    COMPLETED="COMPLETED"
    PROCESSING_AI="PROCESSING_AI"
    FAILED="FAILED"
    ARCHIVED="ARCHIVED"

class Call(Base):
    __tablename__="calls"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    state=Column(
        Enum(CallState, native_enum=False),
        nullable=False,
        default=CallState.IN_PROGRESS

    )
    last_sequence=Column(Integer,default=0)
    created_at=Column(DateTime,server_default=func.now())
    updated_at=Column(DateTime,onupdate=func.now())