from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
from .enums import TicketStatus, TicketPriority

class TicketCreate(BaseModel):
    order_id: UUID
    title: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM
    category: Optional[str] = None
    created_by: str = "Sistema"

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None

class Ticket(BaseModel):
    id: UUID
    order_id: UUID
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    category: Optional[str] = None
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    created_by: str
    
    class Config:
        from_attributes = True