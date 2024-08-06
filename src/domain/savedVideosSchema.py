from pydantic import BaseModel

class WatchLaterBase(BaseModel):
    user_id: str
    video_id: str

class WatchLaterCreate(WatchLaterBase):
    pass

class WatchLaterStatus(WatchLaterBase):
    staus: bool
    
class FavoriteBase(BaseModel):
    user_id: str
    video_id: str
    
class FavoriteCreate(FavoriteBase):
    pass

class FavoriteStatus(FavoriteBase):
    status: bool