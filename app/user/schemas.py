from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from datetime import datetime

from app.security.enums import UserRole

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None
    role: UserRole = UserRole.user
    
class UserRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: str | None = None
    created_at: datetime
    role: UserRole 
    
    model_config = ConfigDict(from_attributes=True)
    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str