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

def create_watch_later(db: Session, watch_later: WatchLaterCreate):
    db_watchl_later = WatchLater(video_id = watch_later.video_id.strip() , user_id =watch_later.user_id.strip(), status =True)
    db.add(db_watch_later)
    db.commit()
    db.refresh(db_watch_later)
    return db_watch_later

def remove_watch_later(db: Session, video_id : str, user_id : str):
    video_id = video_id.strip()
    user_id = user_id.strip()
    watch_later_entry = db.query(WatchLater).filter(WatchLater.video_id == video_id, WatchLater.user_id == user_id, WatchLater.status == True).first()

    if watch_later_entry:
        db.delete(watch_later_entry)
        db.commit()
        return {"messege": "Removed from watch later list"}
    else:
        raise HTTPException(status_code= 404, detail= "Video not found in watch later list")
    
def check_watch_later_status(db: Session, video_id: str, user_id: str)->bool:
    video_id= video_id.strip()
    user_id = user_id.strip()

    watch_later_entry = db.query(WatchLater).filter( WatchLater.video_id == video_id, WatchLater.user_id ==user_id, WatchLater.status ==True)

    if watch_later_entry :
        return watch_later_entry.status
    
    return False