from sqlalchemy import Column,Integer,Text,Float,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class CallPacket(Base):
    __tablename__="call_packets"

    id=Column(Integer,primary_key=True)
    call_id=Column(UUID(as_uuid=True))
    sequence=Column(Integer)
    data=Column(Text)
    timestamp=Column(Float)

    __table_args__=(
        UniqueConstraint("call_id","sequence"),
    )