from sqlalchemy import (
    Column,
    String,
    func,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.deal.models import Deal
from app.core.database import Base
from app.security.enums import UserRole
import uuid

class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    clients = relationship("Client", back_populates="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(String, default=UserRole.user.value, nullable=False)
    deals = relationship("Deal", back_populates="user")