from pydantic import (
    BaseModel,
    Field,
    ConfigDict    
)
from typing import Optional
from datetime import datetime
from uuid import UUID

from app.deal.models import CurrencyEnum, DealStatusEnum

    
class DealBase(BaseModel):
    title: str 
    description: Optional[str] = None
    amount: float = Field(..., gt=0)
    currency: CurrencyEnum = CurrencyEnum.RUB
    client_id: UUID
    user_id: UUID
    
class DealCreate(DealBase):
    pass

class DealUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[CurrencyEnum] = None
    status: Optional[DealStatusEnum] = None
    client_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    
class DealRead(DealBase):
    id: UUID 
    status: DealStatusEnum 
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)