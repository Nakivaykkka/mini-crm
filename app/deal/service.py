
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.deal.models import (
    Deal,
    DealStatusEnum,
)
from app.deal.schemas import DealCreate, DealUpdate
from app.client.models import Client
from app.user.models import User

async def deal_create(
    deal_in: DealCreate,
    db: AsyncSession,
    user_id: Optional[UUID] = None
) -> Deal:
    client = await db.get(Client, deal_in.client_id)
    if not client:
        raise ValueError("Client not found")
    
    if user_id:
        user = await db.get(User, user_id)
        if not user:
            raise ValueError("User not found")
    
    if deal_in.amount <= 0:
        raise ValueError("Amount must be greater than zero")
    
    deal_data = deal_in.model_dump()
    deal_data["user_id"] = user_id
    
    new_deal = Deal(**deal_data)
    db.add(new_deal)
    await db.commit()
    await db.refresh(new_deal)
    return new_deal
    
async def get_deal(
    deal_id: UUID,
    db: AsyncSession
) -> Deal:
    result = await db.execute(
        select(Deal).where(Deal.id == deal_id)
    )
    deal = result.scalar_one_or_none()
    if not deal:
        raise ValueError("deal id not found")
    return deal 

async def get_deals(
    db: AsyncSession,
    user_id: Optional[UUID] = None,
    client_id: Optional[UUID] = None,
    status: Optional[str] = None
):
    query = select(Deal)
    if user_id:
        query = query.where(Deal.user_id == user_id)
    if client_id:
        query = query.where(Deal.client_id == client_id)
    if status:
        query = query.where(Deal.status == status)
    result = await db.execute(query)
    return result.scalars().all()

async def deal_update(
    deal_id: UUID,
    deal_in: DealUpdate,
    db: AsyncSession
) -> Deal:
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise ValueError("Deal not found")
    if deal.status in [DealStatusEnum.closed, DealStatusEnum.canceled]:
        raise ValueError("Cannot update closed or canceled deal ")
    update_data = deal_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(deal, field, value)
    await db.commit()
    await db.refresh(deal)
    return deal

async def deal_cancel(
    deal_id: UUID,
    db: AsyncSession
) -> Deal:
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise ValueError("Deal not found")
    if deal.status in [DealStatusEnum.closed, DealStatusEnum.canceled]:
        raise ValueError("Deal already closed or canceled")
    deal.status = DealStatusEnum.canceled
    await db.commit()
    await db.refresh(deal)
    return deal

async def deal_delete(
    deal_id: UUID,
    db: AsyncSession
) -> Deal:
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise ValueError("Deal not found")
    if deal.status in [DealStatusEnum.closed, DealStatusEnum.canceled]:
        raise ValueError("Cannot delete closed or canceled deal")
    await db.delete(deal)
    await db.commit()