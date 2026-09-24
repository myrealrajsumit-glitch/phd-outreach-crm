from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    target_field: Optional[str] = "Computer Science & AI"
    current_degree: Optional[str] = "M.S. in Computer Science"
    research_interests: Optional[str] = None
    cv_summary: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    target_field: Optional[str] = None
    current_degree: Optional[str] = None
    research_interests: Optional[str] = None
    cv_summary: Optional[str] = None

class SMTPSettingsUpdate(BaseModel):
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    smtp_from_name: Optional[str] = None
    smtp_use_tls: bool = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    smtp_configured: bool = False
    smtp_host: Optional[str] = "smtp.gmail.com"
    smtp_port: Optional[int] = 587
    smtp_user: Optional[str] = None
    smtp_from_name: Optional[str] = None
    smtp_use_tls: Optional[bool] = True

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
