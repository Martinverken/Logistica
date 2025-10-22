from abc import ABC, abstractmethod
from typing import List, Dict
from app.models.enums import Platform
import logging

logger = logging.getLogger(__name__)

class BasePlatformIntegration(ABC):
    """Clase base para todas las integraciones de plataformas"""
    
    def __init__(self, platform: Platform):
        self.platform = platform
        self.logger = logging.getLogger(f"{__name__}.{platform.value}")
    
    @abstractmethod
    def fetch_orders(self, **kwargs) -> List[Dict]:
        """Obtiene órdenes de la plataforma"""
        pass
    
    @abstractmethod
    def map_to_standard_order(self, raw_order: Dict) -> Dict:
        """Mapea la orden de la plataforma al formato estándar"""
        pass
    
    def get_orders_standardized(self, only_pending: bool = True, **kwargs) -> List[Dict]:
        """Obtiene y mapea órdenes al formato estándar"""
        try:
            raw_orders = self.fetch_orders(only_pending=only_pending, **kwargs)
            standardized = [
                self.map_to_standard_order(order) 
                for order in raw_orders
            ]
            self.logger.info(f"Fetched {len(standardized)} orders from {self.platform.value}")
            return standardized
        except Exception as e:
            self.logger.error(f"Error fetching orders: {e}")
            raise