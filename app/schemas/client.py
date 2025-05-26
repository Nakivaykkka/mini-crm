from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


class ClientBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    
class ClientCreate(ClientBase):
    password: str

class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class ClientRead(ClientBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
        
        

    