from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    name: str
    key: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    key: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class AddMemberRequest(BaseModel):
    email: str
    role: str = "member"

class MemberResponse(BaseModel):
    id: int
    user_id: int
    role: str
    user_name: str
    user_email: str
    
    class Config:
        from_attributes = True
