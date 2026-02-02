from sqlalchemy import Column,Text,Integer,String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class CallAnalysis(Base):
    __tablename__="call_analysis"

    call_id=Column(UUID(as_uuid=True),primary_key=True)
    transcript=Column(Text)
    sentiment=Column(String)
    attempts=Column(Integer)