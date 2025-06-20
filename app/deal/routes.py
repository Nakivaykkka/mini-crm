from fastapi import(
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional

from app.core.database import get_async_session
from app.deal.schemas import(
    DealCreate,
    DealUpdate,
    DealRead
)
from app.deal.service import(
    deal_create,
    get_deal,
    get_deals,
    deal_update,
    deal_delete,
    deal_cancel
)
from app.security.dependencies import get_current_user, require_roles
from app.security.enums import UserRole

router = APIRouter(
    prefix="/deal",
    tags=["Deal"]
)

@router.post(
    "/",
    response_model=DealRead,
    status_code=status.HTTP_201_CREATED)
async def create_deal_route(
    deal_in: DealCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    try:
        deal = await deal_create(deal_in, db, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return deal

@router.get("/{deal_id}", response_model=DealRead)
async def get_deal_route(
    deal_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    deal = await get_deal(deal_id, db)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal id not found")
    return deal
    
@router.get("/", response_model=list[DealRead])
async def get_all_deals(
    user_id: Optional[UUID] = None,
    client_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session)
):
    deals = await get_deals(
        db, user_id=user_id,
        client_id=client_id,
        status=status
        )
    return deals

@router.put(
    "/{deal_id}",
    response_model=DealRead,
    dependencies=[
        Depends(
            require_roles([
            UserRole.manager,
            UserRole.admin,
            UserRole.superuser
            ]
                          )
            )
        ]
    )

async def update_deal_route(
    deal_id: UUID,
    deal_in: DealUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        deal = await deal_update(deal_id, deal_in, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return deal

@router.patch("/{deal_id}/cancel", response_model=DealRead)
async def cancel_deal_route(
    deal_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    try: 
        deal = await deal_cancel(deal_id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return deal 

@router.delete(
    "/{deal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_roles(
                [UserRole.admin, UserRole.superuser
                 ]
                )
            )
        ]
    )
async def delete_deal_route(
    deal_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        await deal_delete(deal_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return