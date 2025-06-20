from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from datetime import datetime



class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    user_id: UUID
    
    
class ClientRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: str | None = None
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)