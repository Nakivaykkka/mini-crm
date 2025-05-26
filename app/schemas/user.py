from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: str 
    

class UserCreate(UserBase):
    password: str 

   
class UserRead(UserBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
    
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str 
    
    

    