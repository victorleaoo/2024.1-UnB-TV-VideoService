import uuid
from sqlalchemy import Boolean, Column, String 
from sqlalchemy.orm import Session
from database import Base
from domain.watchLaterSchema import WatchLaterCreate
from fastapi import HTTPException

class WatchLater(Base):
    __tablename__ = 'watch_later'
    id =  Column(String, primary_key = True, index = True, default = lambda: str(uuid.uuid4()))
    user_id =Column(String, index= True, nullable = False)
    video_id = Column(String, index= True, nullable = False)
    status = Column(Boolean, default = True)

    