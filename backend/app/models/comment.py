from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CommentCreate(BaseModel):
    order_id: UUID
    comment: str
    user_name: str = "Sistema"

class Comment(BaseModel):
    id: UUID
    order_id: UUID
    comment: str
    user_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True