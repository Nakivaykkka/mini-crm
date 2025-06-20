from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.client.schemas import  ClientRead, ClientCreate
from app.client.service import client_create, get_client_by_id
from app.core.database import get_async_session

router = APIRouter(prefix="/clients", tags=["Client"])

@router.post("/", response_model=ClientRead, status_code=201)
async def create_client(
    client: ClientCreate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        return await client_create(client, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/clients/{client_id}", response_model=ClientRead)
async def get_client(
    client_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    client = await get_client_by_id(client_id, db)
    return client