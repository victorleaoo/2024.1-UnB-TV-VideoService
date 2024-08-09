from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from domain import savedVideosSchema
from database import get_db
from repository import savedVideosRepository
from starlette.responses import JSONResponse

WatchLater = APIRouter(
 prefix="/watch-later"
)

@WatchLater.post("/")
def add_to_watch_later(watch_later: savedVideosSchema.WatchLaterCreate, db: Session = Depends(get_db)):
   return savedVideosRepository.create_watch_later(db=db, watch_later=watch_later)


@WatchLater.delete("/{video_id}")
def remove_from_watch_later(video_id: str, user_id: str = Query(...), db: Session = Depends(get_db)):
   user_id = user_id.strip()  
   video_id = video_id.strip()
   savedVideosRepository.remove_watch_later(db=db, video_id=video_id, user_id=user_id)
   return {"message": "Removed from watch later list"}


@WatchLater.get("/status/{video_id}")
def check_watch_later(video_id: str, user_id: str = Query(...), db: Session = Depends(get_db)):
   status = savedVideosRepository.check_watch_later_status(db=db, video_id=video_id, user_id=user_id)
   return {"status": status}


@WatchLater.get("/")
def get_watch_later_videos(user_id: str = Query(...), db: Session = Depends(get_db)):
    videos = savedVideosRepository.get_watch_later_videos(db=db, user_id=user_id)
    return {"videoList": videos}

# início das requisições do favorite

favorite = APIRouter(
  prefix="/favorite"
)

@favorite.post("/")
def add_to_favorite(favorite: savedVideosSchema.FavoriteCreate, db: Session = Depends(get_db)):
  return savedVideosRepository.create_favorite(db=db, favorite=favorite)
  
@favorite.get("/status/{video_id}")
def check_favorite(video_id: str, user_id: str = Query(...), db: Session = Depends(get_db)):
    status = savedVideosRepository.check_favorite_status(db=db, video_id=video_id, user_id=user_id)
    return status

@favorite.delete("/{video_id}")
def remove_from_favorites(video_id: str, user_id: str = Query(...), db: Session = Depends(get_db)):
   user_id = user_id.strip() 
   video_id = video_id.strip() 
   savedVideosRepository.remove_favorite(db=db, video_id=video_id, user_id=user_id)
   return {"message": "Removed from favorites"}

@favorite.get("/")
def get_favorite_videos(user_id: str = Query(...), db: Session = Depends(get_db)):
   videos = savedVideosRepository.get_favorite_videos(db=db, user_id=user_id)
   return {"videoList": videos}