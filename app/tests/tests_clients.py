# app/tests/test_clients.py
import pytest
from fastapi.testclient import TestClient
from uuid import UUID

created_client_id = None  # глобальная переменная

def test_create_and_list_clients(client):
    global created_client_id

    payload = {
        "email": "test@example.com",
        "full_name": "Test Client",
        "password": "secure123",
        "phone": "1234567890"
    }

    # Регистрация пользователя
    client.post("/auth/register", json={
        "email": "admin@example.com",
        "full_name": "Admin User",
        "password": "adminpass"
    })

    # Логин
    login_response = client.post("/auth/login", data={
        "username": "admin@example.com",
        "password": "adminpass"
    })
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    
    create_resp = client.post("/clients/", json=payload, headers=headers)
    assert create_resp.status_code == 200
    created_client_id = create_resp.json()["id"]  # Сохраняем строку, не UUID

    # Получение всех клиентов
    list_resp = client.get("/clients/", headers=headers)
    assert list_resp.status_code == 200
    data = list_resp.json()

    assert any(c["id"] == created_client_id for c in data)  # Сравнение строк

def test_get_client_by_id(client):
    global created_client_id

    # Авторизация
    login_response = client.post("/auth/login", data={
        "username": "admin@example.com",
        "password": "adminpass"
    })
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Получение клиента по ID
    response = client.get(f"/clients/{created_client_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_client_id
    assert data["email"] == "test@example.com"

def test_update_client(client):
    # Авторизация
    client.post("/auth/register", json={
        "email": "admin@example.com",
        "full_name": "Admin",
        "password": "adminpass"
    })

    login_response = client.post("/auth/login", data={
        "username": "admin@example.com",
        "password": "adminpass"
    })
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Создание клиента
    create_resp = client.post("/clients/", json={
        "email": "patchme@example.com",
        "full_name": "Old Name",
        "password": "secure123",
        "phone": "1234567890"
    }, headers=headers)
    assert create_resp.status_code == 200
    client_id = create_resp.json()["id"]

    # Обновление
    update_data = {"full_name": "Updated Name"}
    patch_resp = client.patch(f"/clients/{client_id}", json=update_data, headers=headers)

    # Проверка
    assert patch_resp.status_code == 200
    assert patch_resp.json()["full_name"] == "Updated Name"
    assert patch_resp.json()["id"] == client_id
    
def test_delete_client(client):
    client.post("/auth/register", json={
        "email": "admin@example.com",
        "full_name": "Admin",
        "password": "adminpass"
    })

    login_response = client.post("/auth/login", data={
        "username": "admin@example.com",
        "password": "adminpass"
    })
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Создание клиента
    create_resp = client.post("/clients/", json={
        "email": "delete_me@example.com",
        "full_name": "To Be Deleted",
        "password": "secure123",
        "phone": "9999999999"
    }, headers=headers)

    assert create_resp.status_code == 200
    client_id = create_resp.json()["id"]

    # Удаление
    delete_resp = client.delete(f"/clients/{client_id}", headers=headers)
    assert delete_resp.status_code == 204

    # Проверка отсутствия
    get_resp = client.get(f"/clients/{client_id}", headers=headers)
    assert get_resp.status_code == 404

def test_unauthorized_access_rejected(client):
    response = client.get("/clients/")
    assert response.status_code == 401
    
    
    
        
        
    






    
    