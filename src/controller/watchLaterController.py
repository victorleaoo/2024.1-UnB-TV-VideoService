from fastaapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from model import watchLaterModel
from domain import watchLaterSchema
from database import get_db

router = APIRouter()

@router.post("/watch-later")
def add_to_watch_later(watch_later: watchLaterSchema.WatchLaterCreate, db: Session = Depends(get_db)):
    return watchLaterModel.create_watch_later(db = db, watch_later=watch_later)

@router.delete("/watch-later/{video_id}")
def remove_from_watch_later(video_id: str, user_id: str = Query(...), db: Session = Depends(get_db)):
    print(f"Attempting to remove video id={video_id} for user_id={user_id}")
    user_id = user_id.strip()
    video_id = video_id.strip()
    watchLaterModel.remove_watch_later(db=db, video_id = video_id, user_id = user_id)
    return {"message": "Removed from watch list"}

@router.get("watch-later/status/{video_id}")
def check_watch_later(video_id:str ,user_id: str = Query(...), db: Session = Depends(get_db))
    print(f"Checking watch later status for video_id={video_id}, user_id={user_id}")
    status = watchLaterModel.check_watch_later_status(db=db, video_id = video_id, user_id = user_id)
    print(f"status for video_id={video_id}, user_id={user_id} is {status}")
    return {"status": status}
    