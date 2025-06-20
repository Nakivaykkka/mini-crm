import pytest

@pytest.mark.asyncio
async def test_user_can_create_client(register_user, login_user, create_client):
    user = await register_user("user")
    token = await login_user(user["email"], "StrongPass123!321")
    client = await create_client(token, user["id"])
    assert client["user_id"] == user["id"]
