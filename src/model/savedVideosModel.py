import uuid
from sqlalchemy import Column, String, Boolean
from database import Base

class WatchLater(Base):
   __tablename__ = 'watch_later'
   id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
   user_id = Column(String, index=True, nullable=False)
   video_id = Column(String, index=True, nullable=False)
   status = Column(Boolean, default=False) #assistir mais tarde
   statusfavorite = Column(Boolean, default=False) # favoritos
  