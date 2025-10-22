from typing import Dict
from datetime import datetime, timedelta
from supabase import Client
from app.integrations.falabella import FalabellaIntegration
from app.integrations.mercadolibre import MercadoLibreIntegration
from app.services.order_service import OrderService
from app.models.order import OrderCreate
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)

class SyncService:
    def __init__(self, db: Client):
        self.db = db
        self.order_service = OrderService(db)
        self.settings = get_settings()
        
        self.falabella = FalabellaIntegration(
            api_key=self.settings.FALABELLA_API_KEY,
            user_id=self.settings.FALABELLA_USER_ID,
            base_url=self.settings.FALABELLA_BASE_URL
        )
        
        self.mercadolibre = MercadoLibreIntegration(
            access_token=self.settings.MELI_ACCESS_TOKEN,
            user_id=self.settings.MELI_USER_ID,
            base_url=self.settings.MELI_BASE_URL
        )
    
    def sync_all_platforms(self, only_pending: bool = True) -> Dict:
        """Sincroniza todas las plataformas"""
        start_time = datetime.now()
        results = {
            'falabella': None,
            'mercadolibre': None,
            'total_synced': 0,
            'errors': [],
            'sync_type': 'pending_only' if only_pending else 'full'
        }
        
        # Falabella
        try:
            fb_result = self.sync_falabella(only_pending=only_pending)
            results['falabella'] = fb_result
            results['total_synced'] += fb_result.get('orders_synced', 0)
        except Exception as e:
            logger.error(f"Error syncing Falabella: {e}")
            results['errors'].append(f"Falabella: {str(e)}")
        
        # MercadoLibre
        try:
            ml_result = self.sync_mercadolibre(only_pending=only_pending)
            results['mercadolibre'] = ml_result
            results['total_synced'] += ml_result.get('orders_synced', 0)
        except Exception as e:
            logger.error(f"Error syncing MercadoLibre: {e}")
            results['errors'].append(f"MercadoLibre: {str(e)}")
        
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        results['execution_time_ms'] = execution_time
        
        logger.info(f"Sync completed: {results['total_synced']} orders in {execution_time}ms (type: {results['sync_type']})")
        return results
    
    def sync_falabella(self, only_pending: bool = True) -> Dict:
        """Sincroniza Falabella"""
        created_after = (datetime.now() - timedelta(days=7)).isoformat()
        orders = self.falabella.get_orders_standardized(
            only_pending=only_pending,
            created_after=created_after, 
            limit=100
        )
        
        synced = 0
        for order_data in orders:
            try:
                order_create = OrderCreate(**order_data)
                self.order_service.create_or_update_order(order_create)
                synced += 1
            except Exception as e:
                logger.error(f"Error syncing Falabella order: {e}")
        
        return {
            'platform': 'falabella',
            'orders_synced': synced,
            'orders_fetched': len(orders),
            'only_pending': only_pending
        }
    
    def sync_mercadolibre(self, only_pending: bool = True) -> Dict:
        """Sincroniza MercadoLibre"""
        orders = self.mercadolibre.get_orders_standardized(
            only_pending=only_pending, 
            limit=50
        )
        
        synced = 0
        for order_data in orders:
            try:
                order_create = OrderCreate(**order_data)
                self.order_service.create_or_update_order(order_create)
                synced += 1
            except Exception as e:
                logger.error(f"Error syncing ML order: {e}")
        
        return {
            'platform': 'mercadolibre',
            'orders_synced': synced,
            'orders_fetched': len(orders),
            'only_pending': only_pending
        }