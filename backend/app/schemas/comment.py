from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime

class CommentCreate(BaseModel):
    body: str

class CommentResponse(BaseModel):
    id: int
    issue_id: int
    author_id: int
    body: str
    created_at: datetime
    author_name: str
    
    model_config = ConfigDict(from_attributes=True)
