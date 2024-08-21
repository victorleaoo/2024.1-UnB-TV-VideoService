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

@Record.post("/toggle_tracking")
def toggle_tracking(track: bool, user_id: str = Query(...), db: Session = Depends(get_db)):
    record_entry = db.query(recordModel.Record).filter(recordModel.Record.user_id == user_id).first()
   
    if record_entry:
        # Atualiza o estado de track_enabled
        record_entry.track_enabled = track


        if not track:
            # Limpa os vídeos do histórico, mas mantém o registro
            record_entry.videos = {}


        db.commit()
        return JSONResponse(status_code=200, content={"message": f"Rastreamento {'habilitado' if track else 'desabilitado'}"})
    else:
        # Se não houver registro anterior, criar um novo com o estado de rastreamento definido
        new_record = recordModel.Record(
            user_id=user_id,
            videos={},
            track_enabled=track
        )
        db.add(new_record)
        db.commit()
        return JSONResponse(status_code=200, content={"message": f"Rastreamento {'habilitado' if track else 'desabilitado'} e novo registro criado"})


@Record.get("/get_record_sorted")
def get_record_sorted(user_id: str = Query(...), ascending: bool = Query(True), db: Session = Depends(get_db)):
    records = db.query(recordModel.Record).filter(recordModel.Record.user_id == user_id).all()
   
    # Agregando todos os vídeos em um único dicionário
    aggregated_videos = {}
    for record in records:
        aggregated_videos.update(record.videos)
   
    if aggregated_videos:
        sorted_videos = dict(sorted(aggregated_videos.items(), key=lambda item: item[1], reverse=not ascending))
        return {"videos": sorted_videos}
    return {"videos": []}
