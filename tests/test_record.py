
import pytest
import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, get_db
from src.main import app

# Crie um banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para usar o banco de dados de teste
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_add_to_record(setup_database):
    user_id = str(uuid.uuid4())
    video_id = str(uuid.uuid4())
    timestamp = "2024-08-14 12:00:00"
    
    response = client.post("/api/record/", json={"user_id": user_id, "videos": {video_id: timestamp}})
    assert response.status_code == 200
    
    # Verificar se o vídeo foi adicionado ao histórico
    response = client.get("/api/record/get_record/", params={"user_id": user_id})
    assert response.status_code == 200
    assert "videos" in response.json()
    assert response.json()["videos"] == {video_id: timestamp}

def test_toggle_tracking(setup_database):
    user_id = str(uuid.uuid4())

    # Desabilitar o rastreamento
    response = client.post("/api/record/toggle_tracking/", params={"user_id": user_id, "track": "false"})
    assert response.status_code == 200
    assert response.json()["message"] in [
        "Rastreamento desabilitado",
        "Rastreamento desabilitado e novo registro criado"
    ]
    
    # Verificar o status do rastreamento
    response = client.get("/api/record/get_tracking_status/", params={"user_id": user_id})
    assert response.status_code == 200
    assert response.json()["track_enabled"] is False

    # Habilitar o rastreamento novamente
    response = client.post("/api/record/toggle_tracking/", params={"user_id": user_id, "track": "true"})
    assert response.status_code == 200
    assert response.json()["message"] in [
        "Rastreamento habilitado",
        "Rastreamento habilitado e novo registro criado"
    ]
    
    # Verificar o status do rastreamento novamente
    response = client.get("/api/record/get_tracking_status/", params={"user_id": user_id})
    assert response.status_code == 200
    assert response.json()["track_enabled"] is True

def test_get_record_sorted(setup_database):
    user_id = str(uuid.uuid4())
    
    # Adicionar múltiplos vídeos ao registro com diferentes timestamps
    videos = {
        str(uuid.uuid4()): "2024-08-14 12:00:00",
        str(uuid.uuid4()): "2024-08-14 13:00:00",
        str(uuid.uuid4()): "2024-08-14 14:00:00"
    }
    for video_id, timestamp in videos.items():
        client.post("/api/record/", json={"user_id": user_id, "videos": {video_id: timestamp}})
    
    # Obter o registro ordenado de forma ascendente
    response = client.get("/api/record/get_record_sorted/", params={"user_id": user_id, "ascending": "true"})
    assert response.status_code == 200
    sorted_videos = response.json()["videos"]

    # Ordena os vídeos manualmente pelo timestamp para verificar se a API os ordenou corretamente
    expected_order = sorted(videos.items(), key=lambda x: x[1])
    sorted_keys = list(sorted_videos.keys())
    assert sorted_keys == [k for k, v in expected_order]  # Checa se está em ordem ascendente

    # Obter o registro ordenado de forma descendente
    response = client.get("/api/record/get_record_sorted/", params={"user_id": user_id, "ascending": "false"})
    assert response.status_code == 200
    sorted_videos = response.json()["videos"]

    # Inverte a ordem esperada para verificar a ordenação descendente
    expected_order = sorted(videos.items(), key=lambda x: x[1], reverse=True)
    sorted_keys = list(sorted_videos.keys())
    assert sorted_keys == [k for k, v in expected_order]  # Checa se está em ordem descendente
