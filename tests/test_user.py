import pytest

@pytest.mark.asyncio
async def test_admin_can_create_multiple_clients(register_user, login_user, create_client):
    admin = await register_user("admin")
    token = await login_user(admin["email"], "StrongPass123!321")
    clients = []
    for _ in range(3):
        client = await create_client(token, admin["id"])
        clients.append(client)
    assert len(clients) == 3
