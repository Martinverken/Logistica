
# =====================================================
# backend/app/services/order_service.py
# =====================================================
from typing import List, Optional, Dict
from datetime import datetime
from uuid import UUID
from supabase import Client
from app.models.order import Order, OrderCreate
from app.models.enums import OrderStatus
from app.utils.date_helpers import is_delayed
import logging

logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, db: Client):
        self.db = db
    
    def create_or_update_order(self, order_data: OrderCreate) -> Optional[Order]:
        """Crea o actualiza una orden"""
        try:
            data = order_data.model_dump(exclude_none=True)
            data['platform'] = data['platform'].value
            data['shipping_type'] = data['shipping_type'].value
            data['current_status'] = data['current_status'].value
            
            # Convertir datetimes a ISO string
            for field in ['limite_despacho', 'promised_delivery', 'created_at']:
                if field in data and isinstance(data[field], datetime):
                    data[field] = data[field].isoformat()
            
            # Verificar si está atrasada
            if 'limite_despacho' in data:
                limite = datetime.fromisoformat(data['limite_despacho'].replace('Z', '+00:00'))
                data['is_delayed'] = is_delayed(limite)
                if data['is_delayed'] and 'delay_detected_at' not in data:
                    data['delay_detected_at'] = datetime.now().isoformat()
            
            result = self.db.table('orders').upsert(
                data,
                on_conflict='platform,external_order_id'
            ).execute()
            
            if result.data:
                logger.info(f"Order {order_data.order_number} saved")
                return Order(**result.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error saving order: {e}")
            return None
    
    def get_order_by_id(self, order_id: UUID) -> Optional[Order]:
        """Obtiene una orden por ID"""
        try:
            result = self.db.table('orders').select('*').eq('id', str(order_id)).execute()
            if result.data:
                return Order(**result.data[0])
            return None
        except Exception as e:
            logger.error(f"Error fetching order: {e}")
            return None
    
    def get_orders_today(self) -> List[Dict]:
        """Órdenes del día"""
        try:
            result = self.db.table('orders_today').select('*').execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def get_delayed_orders(self) -> List[Dict]:
        """Órdenes atrasadas"""
        try:
            result = self.db.table('orders_delayed').select('*').execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def get_orders_at_risk(self) -> List[Dict]:
        """Órdenes en riesgo (PREVENTIVO)"""
        try:
            result = self.db.table('orders_at_risk').select('*').execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def get_all_orders(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Todas las órdenes"""
        try:
            result = self.db.table('orders').select('*').order(
                'created_at', desc=True
            ).range(offset, offset + limit - 1).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def get_orders_to_ship(self) -> List[Dict]:
        """Órdenes por enviar (todas las pendientes)"""
        try:
            result = self.db.table('orders_to_ship').select('*').execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
        
    def get_delivered_orders(self) -> List[Dict]:
        """Órdenes entregadas"""
        try:
            result = self.db.table('orders').select('*').eq(
                'current_status', 'entregado'
            ).order('updated_at', desc=True).limit(100).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error: {e}")
            return []