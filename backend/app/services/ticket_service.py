from typing import List, Optional
from uuid import UUID
from datetime import datetime
from supabase import Client
from app.models.ticket import Ticket, TicketCreate, TicketUpdate
from app.models.enums import TicketStatus
import logging

logger = logging.getLogger(__name__)

class TicketService:
    def __init__(self, db: Client):
        self.db = db
    
    def create_ticket(self, ticket_data: TicketCreate) -> Optional[Ticket]:
        """Crea un ticket (REACTIVO)"""
        try:
            data = ticket_data.model_dump()
            data['order_id'] = str(data['order_id'])
            data['priority'] = data['priority'].value
            data['status'] = TicketStatus.OPEN.value
            
            result = self.db.table('tickets').insert(data).execute()
            
            if result.data:
                logger.info(f"Ticket created for order {ticket_data.order_id}")
                return Ticket(**result.data[0])
            return None
        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            return None
    
    def update_ticket(self, ticket_id: UUID, update_data: TicketUpdate) -> Optional[Ticket]:
        """Actualiza un ticket"""
        try:
            data = update_data.model_dump(exclude_none=True)
            
            if 'status' in data:
                data['status'] = data['status'].value
                if data['status'] in [TicketStatus.RESOLVED.value, TicketStatus.CLOSED.value]:
                    data['resolved_at'] = datetime.now().isoformat()
            
            if 'priority' in data:
                data['priority'] = data['priority'].value
            
            result = self.db.table('tickets').update(data).eq(
                'id', str(ticket_id)
            ).execute()
            
            if result.data:
                return Ticket(**result.data[0])
            return None
        except Exception as e:
            logger.error(f"Error updating ticket: {e}")
            return None
    
    def get_tickets_by_order(self, order_id: UUID) -> List[Ticket]:
        """Tickets de una orden"""
        try:
            result = self.db.table('tickets').select('*').eq(
                'order_id', str(order_id)
            ).order('created_at', desc=True).execute()
            
            return [Ticket(**t) for t in result.data] if result.data else []
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def get_open_tickets(self) -> List[Ticket]:
        """Todos los tickets abiertos"""
        try:
            result = self.db.table('tickets').select('*').in_(
                'status', [TicketStatus.OPEN.value, TicketStatus.IN_PROGRESS.value]
            ).order('priority', desc=True).execute()
            
            return [Ticket(**t) for t in result.data] if result.data else []
        except Exception as e:
            logger.error(f"Error: {e}")
            return []