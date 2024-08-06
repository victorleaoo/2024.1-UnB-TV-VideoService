import pytest, sys, os


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


def test_add_to_watch_later(setup_database):
    response = client.post("/api/watch-later/", json={"user_id": "user123", "video_id": "video123"})
    assert response.status_code == 200
    assert response.json()["user_id"] == "user123"
    assert response.json()["video_id"] == "video123"
    assert response.json()["status"] is True
    


def test_check_watch_later_status(setup_database):
    response = client.get("/api/watch-later/status/video123?user_id=user123")
    assert response.status_code == 200
    assert response.json()["status"] is True


def test_remove_from_watch_later(setup_database):
    response = client.delete("/api/watch-later/video123?user_id=user123")
    assert response.status_code == 200
    assert response.json()["message"] == "Removed from watch later list"


    # Check status again to ensure it's removed
    response = client.get("/api/watch-later/status/video123?user_id=user123")
    assert response.status_code == 200
    assert response.json()["status"] is False
