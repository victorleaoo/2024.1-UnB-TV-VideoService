import uuid
from sqlalchemy import Column, String, JSON, Boolean
from database import Base

class Record(Base):
   __tablename__ = 'record'
   id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
   user_id = Column(String, index=True, nullable=False)
   videos = Column(JSON, nullable=False)
   track_enabled = Column(Boolean, default=True)
  