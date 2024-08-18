from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from domain import recordSchema
from database import get_db
from repository import recordRepository
from model import recordModel

Record = APIRouter(
 prefix="/record"
)

@Record.post("/")
def add_to_record(record: recordSchema.RecordCreate, db: Session = Depends(get_db)):
    # Verifique o estado de rastreamento do usuário usando o campo track_enabled da model Record
    record_entry = db.query(recordModel.Record).filter(recordModel.Record.user_id == record.user_id).first()

    if record_entry and not record_entry.track_enabled:
        # Se o rastreamento estiver desabilitado, não adicionar ao histórico
        return JSONResponse(status_code=403, content={"message": "Rastreamento desabilitado, vídeo não adicionado ao histórico"})

    # Se o rastreamento estiver habilitado ou não houver registro, continue com a adição ao histórico
    if record_entry:
        return recordRepository.create_record(db=db, record=record, is_create=False)
    
    # Se não houver registro, criar um novo com o estado de rastreamento padrão
    new_record = recordModel.Record(
        user_id=record.user_id,
        videos=record.videos,
        track_enabled=True
    )
    db.add(new_record)
    db.commit()
    return new_record

@Record.get("/get_record")
def check_record(user_id: str = Query(...), db: Session = Depends(get_db)):
    record = db.query(recordModel.Record).filter(recordModel.Record.user_id == user_id).first()
    if record:
        return {"videos": record.videos}
    return {"videos": {}}  # Retorna um dicionário vazio se não houver registro

@Record.get("/get_tracking_status/")
def get_tracking_status(user_id: str = Query(...), db: Session = Depends(get_db)):
    record = db.query(recordModel.Record).filter(recordModel.Record.user_id == user_id).first()
    if record:
        return {"track_enabled": record.track_enabled}
    return {"track_enabled": True}  # Padrão para True se não houver histórico
