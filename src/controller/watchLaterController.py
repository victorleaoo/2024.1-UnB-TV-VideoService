from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from model import watchLaterModel
from domain import watchLaterSchema
from database import get_db


WatchLater = APIRouter(
 prefix="/watch-later"
)


@WatchLater.post("/")
def add_to_watch_later(watch_later: watchLaterSchema.WatchLaterCreate, db: Session = Depends(get_db)):
   return watchLaterModel.create_watch_later(db=db, watch_later=watch_later)


@WatchLater.delete("/{video_id}")
def remove_from_watch_later(video_id: str, user_id: str = Query(...), db: Session = Depends(get_db)):
   print(f"Attempting to remove video_id={video_id} for user_id={user_id}")
   user_id = user_id.strip()  # Certifique-se de que o `user_id` não contém espaços ou quebras de linha
   video_id = video_id.strip()  # Certifique-se de que o `video_id` não contém espaços ou quebras de linha
   watchLaterModel.remove_watch_later(db=db, video_id=video_id, user_id=user_id)
   return {"message": "Removed from watch later list"}


@WatchLater.get("/status/{video_id}")
def check_watch_later(video_id: str, user_id: str = Query(...), db: Session = Depends(get_db)):
   print(f"Checking watch later status for video_id={video_id}, user_id={user_id}")
   status = watchLaterModel.check_watch_later_status(db=db, video_id=video_id, user_id=user_id)
   print(f"Status for video_id={video_id}, user_id={user_id} is {status}")
   return {"status": status}
