from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from domain import recordSchema
from database import get_db
from repository import recordRepository
from starlette.responses import JSONResponse

Record = APIRouter(
 prefix="/record"
)

@Record.post("/")
def add_to_record(record: recordSchema.RecordCreate, db: Session = Depends(get_db)):
   return recordRepository.create_record(db=db, record=record)

@Record.get("/get_record")
def check_record(user_id: str =Query(...) , db: Session = Depends(get_db)):
   record = recordSchema.RecordGet(user_id =user_id)
   videos = recordRepository.get_record(db=db, record=record)
   return {"videos": videos}
