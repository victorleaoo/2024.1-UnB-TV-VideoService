from pydantic import BaseModel
from typing import Dict

class RecordBase(BaseModel):
    user_id: str
    videos: Dict[str, str]

class RecordCreate(RecordBase):
    pass

class RecordGet(BaseModel):
    user_id: str
