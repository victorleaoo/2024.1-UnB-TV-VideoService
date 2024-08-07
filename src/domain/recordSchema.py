from pydantic import BaseModel

class RecordBase(BaseModel):
    user_id: str
    videos: dict

class RecordCreate(RecordBase):
    pass

class RecordGet(BaseModel):
    user_id: str
