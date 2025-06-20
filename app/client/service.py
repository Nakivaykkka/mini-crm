from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.client.models import Client
from app.client.schemas import ClientCreate
from app.user.models import User


async def client_create(
    client_in: ClientCreate,
    db: AsyncSession
) -> Client:
    result = await db.execute(
        select(Client).where(Client.email == client_in.email)
    )
    if result.scalar_one_or_none():
        raise ValueError("Client already exists")
    user = await db.get(User, client_in.user_id)
    if not user:
        raise ValueError("User not found")
    new_client = Client(**client_in.model_dump())
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return new_client

async def get_client_by_id(
    client_id: UUID,
    db:AsyncSession
) -> Client:
    result = await db.execute(
        select(Client).where(Client.id == client_id)
    )
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client