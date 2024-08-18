import pytest, sys, os, uuid

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

'''    
def test_check_record(setup_database):
    user_id = str(uuid.uuid4())
    video_id = str(uuid.uuid4())
    timestamp = "2024-08-14 12:00:00"
    response = client.get("/api/record/get_record/", params={"user_id": user_id})
    assert response.status_code == 200
    assert "videos" in response.json()
    assert response.json()["videos"] == {video_id: timestamp}
'''
