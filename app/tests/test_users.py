import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import UUID

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_user.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_user(client):
    # Регистрация
    response = client.post("/auth/register", json={
        "email": "usercheck@example.com",
        "full_name": "User Checker",
        "password": "checkpass"
    })
    assert response.status_code == 200
    user_data = response.json()
    user_id = user_data["id"]
    assert UUID(user_id)

    # Логин
    response = client.post("/auth/login", data={
        "username": "usercheck@example.com",
        "password": "checkpass"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token


