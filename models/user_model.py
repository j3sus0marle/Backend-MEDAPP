from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from datetime import datetime
from .campo_info_model import PyObjectId

class UserBase(BaseModel):
    email: EmailStr
    name: str
    google_sub: str
    role: str = "estudiante"  # Roles: estudiante, maestro, admin
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    google_sub: str
    role: str = "estudiante"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    last_login: Optional[datetime] = None

class UserDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True