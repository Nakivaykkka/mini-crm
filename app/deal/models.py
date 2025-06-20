from sqlalchemy import (
    Column,
    String,
    func,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Numeric
import uuid

from app.core.database import Base

class CurrencyEnum(str, Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    
class DealStatusEnum(str, Enum):
    new = "new"
    in_progress = "in_progress"
    closed = "closed"
    canceled = "canceled"

class Deal(Base):
    __tablename__ = "deal"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    status = Column(SAEnum(DealStatusEnum), default=DealStatusEnum.new, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(SAEnum(CurrencyEnum), default=CurrencyEnum.RUB, nullable=False)
    
    client = relationship("Client", back_populates="deals")
    user = relationship("User", back_populates='deals')