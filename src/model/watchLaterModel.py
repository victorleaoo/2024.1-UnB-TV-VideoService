import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import Session
from database import Base
from domain.watchLaterSchema import WatchLaterCreate
from fastapi import HTTPException  # Certifique-se de que HTTPException está importado


class WatchLater(Base):
   __tablename__ = 'watch_later'
   id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
   user_id = Column(String, index=True, nullable=False)
   video_id = Column(String, index=True, nullable=False)
   status = Column(Boolean, default=True) #assistir mais tarde
  


def create_watch_later(db: Session, watch_later: WatchLaterCreate):
   db_watch_later = WatchLater(
       user_id=watch_later.user_id.strip(),
       video_id=watch_later.video_id.strip(),
       status=True,
      
   )
   db.add(db_watch_later)
   db.commit()
   db.refresh(db_watch_later)
   print(f"Created WatchLater: user_id={db_watch_later.user_id}, video_id={db_watch_later.video_id}, id={db_watch_later.id}, status={db_watch_later.status}")
   return db_watch_later


def remove_watch_later(db: Session, video_id: str, user_id: str):
   video_id = video_id.strip()
   user_id = user_id.strip()
   print(f"Removing video_id={video_id} for user_id={user_id}")
   watch_later_entry = db.query(WatchLater).filter(
       WatchLater.video_id == video_id,
       WatchLater.user_id == user_id,
       WatchLater.status == True
   ).first()
   print(f"Query Result: {watch_later_entry}")
   if watch_later_entry:
       db.delete(watch_later_entry)
       db.commit()
       print(f"Removed WatchLater: user_id={user_id}, video_id={video_id}")
       return {"message": "Removed from watch later list"}
   else:
       raise HTTPException(status_code=404, detail="Video not found in watch later list")


def check_watch_later_status(db: Session, video_id: str, user_id: str) -> bool:
   video_id = video_id.strip()
   user_id = user_id.strip()
   print(f"Executing Query: video_id={video_id}, user_id={user_id}")
   watch_later_entry = db.query(WatchLater).filter(
       WatchLater.video_id == video_id,
       WatchLater.user_id == user_id,
       WatchLater.status == True
   ).first()
   print(f"Query Result: {watch_later_entry}")
   if watch_later_entry:
       print(f"Check Watch Later Status: video_id={video_id}, user_id={user_id}, status={watch_later_entry.status}")
       return watch_later_entry.status
   print(f"Check Watch Later Status: video_id={video_id}, user_id={user_id}, found=False")
   return False
