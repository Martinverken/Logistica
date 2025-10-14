from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.services.ticket_service import TicketService
from app.models.ticket import Ticket, TicketCreate, TicketUpdate

router = APIRouter()

def get_ticket_service(db=Depends(get_db)):
    return TicketService(db)

@router.post("/", response_model=Ticket, status_code=201)
async def create_ticket(
    ticket: TicketCreate,
    service: TicketService = Depends(get_ticket_service)
):
    """
    Crea un ticket para gestión REACTIVA
    Usado cuando hay problemas que requieren atención inmediata
    """
    created_ticket = service.create_ticket(ticket)
    if not created_ticket:
        raise HTTPException(status_code=400, detail="Could not create ticket")
    return created_ticket

@router.get("/", response_model=List[Ticket])
async def get_open_tickets(service: TicketService = Depends(get_ticket_service)):
    """Obtiene todos los tickets abiertos"""
    return service.get_open_tickets()

@router.get("/order/{order_id}", response_model=List[Ticket])
async def get_tickets_by_order(
    order_id: UUID,
    service: TicketService = Depends(get_ticket_service)
):
    """Obtiene todos los tickets de una orden"""
    return service.get_tickets_by_order(order_id)

@router.patch("/{ticket_id}", response_model=Ticket)
async def update_ticket(
    ticket_id: UUID,
    update_data: TicketUpdate,
    service: TicketService = Depends(get_ticket_service)
):
    """Actualiza un ticket"""
    ticket = service.update_ticket(ticket_id, update_data)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
