import uuid

from sqlalchemy import (
    Column,
    String,
    func,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.user.models import User

class Client(Base):
    __tablename__ = "client"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="clients")
    deals = relationship("Deal", back_populates="client")
   

