from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime
from typing import Optional

class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    assignee_id: Optional[int] = None

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[int] = None

class IssueResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    reporter_id: int
    assignee_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    reporter_name: str
    assignee_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
