from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str
    name: str
    last_name: str
    email: EmailStr
    role: UserRole = UserRole.USER
    
class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID
    created_at: datetime
    
    model_config =  ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None