from pydantic import BaseModel
from pydantic import ConfigDict
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
    
    model_config = ConfigDict(from_attributes=True)

class AddMemberRequest(BaseModel):
    email: str
    role: str = "member"

class MemberResponse(BaseModel):
    id: int
    user_id: int
    role: str
    user_name: str
    user_email: str
    
    model_config = ConfigDict(from_attributes=True)
