from sqlalchemy.orm import Session

from domain import savedVideosSchema
from model import savedVideosModel
from fastapi import HTTPException 

def create_watch_later(db: Session, watch_later: savedVideosSchema.WatchLaterCreate):
   db_watch_later = savedVideosModel.WatchLater(
       user_id=watch_later.user_id.strip(),
       video_id=watch_later.video_id.strip(),
       status=True
   )
   db.add(db_watch_later)
   db.commit()
   db.refresh(db_watch_later)
   print(f"Created watchLater: user_id={db_watch_later.user_id}, video_id={db_watch_later.video_id}, id={db_watch_later.id}, status={db_watch_later.status}")
   return db_watch_later


def remove_watch_later(db: Session, video_id: str, user_id: str):
   video_id = video_id.strip()
   user_id = user_id.strip()
   print(f"Removing video_id={video_id} for user_id={user_id}")
   watch_later_entry = db.query(savedVideosModel.WatchLater).filter(
       savedVideosModel.WatchLater.video_id == video_id,
       savedVideosModel.WatchLater.user_id == user_id,
       savedVideosModel.WatchLater.status == True
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
   watch_later_entry = db.query(savedVideosModel.WatchLater).filter(
       savedVideosModel.WatchLater.video_id == video_id,
       savedVideosModel.WatchLater.user_id == user_id,
       savedVideosModel.WatchLater.status == True
   ).first()
   print(f"Query Result: {watch_later_entry}")
   if watch_later_entry:
       print(f"Check Watch Later Status: video_id={video_id}, user_id={user_id}, status={watch_later_entry.status}")
       return watch_later_entry.status
   print(f"Check Watch Later Status: video_id={video_id}, user_id={user_id}, found=False")
   return False


def get_watch_later_videos(db: Session, user_id: str):
    user_id = user_id.strip()
    watch_later_entries = db.query(savedVideosModel.WatchLater).filter(
        savedVideosModel.WatchLater.user_id == user_id,
        savedVideosModel.WatchLater.status == True
    ).all()
    return watch_later_entries


# início dos métodos do favorite
    
def create_favorite(db: Session, favorite: savedVideosSchema.FavoriteCreate):
    db_favorite = savedVideosModel.WatchLater(
        user_id = favorite.user_id.strip(),
        video_id = favorite.video_id.strip(),
        statusfavorite = True
    )
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite
    
def check_favorite_status(db: Session, video_id: str, user_id: str) -> dict:
    video_id = video_id.strip()
    user_id = user_id.strip()
    favorite_entry = db.query(savedVideosModel.WatchLater).filter(
        savedVideosModel.WatchLater.user_id == user_id,
        savedVideosModel.WatchLater.video_id == video_id,
        savedVideosModel.WatchLater.statusfavorite == True
    ).first()
    if favorite_entry:
        return {
            "statusfavorite": favorite_entry.statusfavorite
        }
    return {
        "statusfavorite": False
    }
    
def remove_favorite(db: Session, video_id: str, user_id: str):
   video_id = video_id.strip()
   user_id = user_id.strip()
   print(f"Removing favorite video_id={video_id} for user_id={user_id}")
   favorite_entry = db.query(savedVideosModel.WatchLater).filter(
       savedVideosModel.WatchLater.video_id == video_id,
       savedVideosModel.WatchLater.user_id == user_id,
       savedVideosModel.WatchLater.statusfavorite == True
   ).first()
   print(f"Query Result: {favorite_entry}")
   if favorite_entry:
       db.delete(favorite_entry)
       db.commit()
       print(f"Removed Favorite: user_id={user_id}, video_id={video_id}")
       return {"message": "Removed from favorites"}
   else:
       raise HTTPException(status_code=404, detail="Video not found in favorites")

def get_favorite_videos(db: Session, user_id: str):
    user_id = user_id.strip()
    favorite_entries = db.query(savedVideosModel.WatchLater).filter(
        savedVideosModel.WatchLater.user_id == user_id,
        savedVideosModel.WatchLater.statusfavorite == True
    ).all()
    return favorite_entries