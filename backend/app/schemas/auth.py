from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from datetime import datetime


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    
    # Pydantic v2 config to read from ORM objects
    model_config = ConfigDict(from_attributes=True)
