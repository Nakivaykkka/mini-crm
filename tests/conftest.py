from httpx import AsyncClient, ASGITransport

from app.main import app

 
import uuid
import pytest_asyncio

@pytest_asyncio.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

        
@pytest_asyncio.fixture(scope="function")
async def register_user(async_client):
    async def _register_user(role="user"):
        email = f"user_{uuid.uuid4().hex[:8]}@test.com"
        payload = {
            "name": "Test User",
            "email": email,
            "password": "StrongPass123!321",
            "role": role
        }
        resp = await async_client.post("/users/create", json=payload)
        assert resp.status_code == 201
        return resp.json()
    return _register_user

@pytest_asyncio.fixture(scope="function")
async def login_user(async_client):
    async def _login_user(email, password):
        resp = await async_client.post(
    "/users/login/",
    json={"email": email, "password": password}
)
        assert resp.status_code == 200
        return resp.json()["access_token"]
    return _login_user

@pytest_asyncio.fixture(scope="function")
async def create_client(async_client):
    async def _create_client(token, user_id):
        payload = {
            "name": f"Client_{uuid.uuid4().hex[:6]}",
            "email": f"client_{uuid.uuid4().hex[:8]}@test.com",
            "user_id": user_id
        }
        headers = {"Authorization": f"Bearer {token}"}
        resp = await async_client.post("/clients/", json=payload, headers=headers)
        assert resp.status_code == 201
        return resp.json()
    return _create_client