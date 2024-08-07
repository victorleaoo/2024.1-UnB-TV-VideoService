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
def check_record(record: recordSchema.RecordGet, db: Session = Depends(get_db)):
   videos = recordRepository.get_record(db=db, record=record)
   return {"videos": videos}
