import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .base import BasePlatformIntegration
from app.models.enums import Platform, ShippingType
from app.utils.status_mapper import StatusMapper
from app.utils.date_helpers import parse_iso_date

class FalabellaIntegration(BasePlatformIntegration):
    def __init__(self, api_key: str, user_id: str, base_url: str):
        super().__init__(Platform.FALABELLA)
        self.api_key = api_key
        self.user_id = user_id
        self.base_url = base_url
    
    def fetch_orders(
        self, 
        created_after: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """Obtiene órdenes de Falabella"""
        params = {
            'UserID': self.user_id,
            'Version': '1.0',
            'Action': 'GetOrders',
            'Format': 'JSON',
            'Timestamp': datetime.utcnow().isoformat() + 'Z',
            'Limit': limit,
            'Offset': offset,
            'Signature': self.api_key
        }
        
        if created_after:
            params['CreatedAfter'] = created_after
        
        try:
            response = requests.get(
                f"{self.base_url}/orders",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            orders = data.get('Body', {}).get('Orders', {}).get('Order', [])
            if isinstance(orders, dict):
                orders = [orders]
            
            self.logger.info(f"Fetched {len(orders)} orders from Falabella")
            return orders
            
        except Exception as e:
            self.logger.error(f"Error fetching Falabella orders: {e}")
            return []
    
    def map_to_standard_order(self, raw_order: Dict) -> Dict:
        """Mapea orden de Falabella al formato estándar"""
        
        # Tipo de envío
        delivery_info = raw_order.get('DeliveryInfo', '')
        if 'Directo' in delivery_info or 'directo' in delivery_info.lower():
            shipping_type = ShippingType.FALABELLA_DIRECTO
        else:
            shipping_type = ShippingType.FALABELLA_NORMAL
        
        # Estado
        statuses = raw_order.get('Statuses', [])
        if isinstance(statuses, list) and len(statuses) > 0:
            raw_status = statuses[0]
        else:
            raw_status = str(statuses)
        
        current_status = StatusMapper.map_status(Platform.FALABELLA, raw_status)
        
        # Fechas
        created_at = parse_iso_date(raw_order.get('CreatedAt'))
        promised_shipping = parse_iso_date(raw_order.get('PromisedShippingTimes'))
        
        if not promised_shipping and created_at:
            promised_shipping = created_at + timedelta(days=2)
        
        # Dirección
        addr_ship = raw_order.get('AddressShipping', {})
        address_parts = [
            addr_ship.get('Address1', ''),
            addr_ship.get('City', ''),
            addr_ship.get('PostCode', '')
        ]
        shipping_address = ', '.join(filter(None, address_parts))
        
        return {
            'platform': Platform.FALABELLA,
            'external_order_id': str(raw_order.get('OrderId')),
            'order_number': str(raw_order.get('OrderNumber')),
            'shipping_type': shipping_type,
            'current_status': current_status,
            'customer_name': f"{raw_order.get('CustomerFirstName', '')} {raw_order.get('CustomerLastName', '')}".strip(),
            'customer_phone': addr_ship.get('Phone'),
            'total_amount': float(raw_order.get('Price', 0)),
            'items_count': int(raw_order.get('ItemsCount', 1)),
            'shipping_address': shipping_address,
            'shipping_city': addr_ship.get('City'),
            'limite_despacho': promised_shipping,
            'promised_delivery': promised_shipping,
            'created_at': created_at,
            'raw_data': raw_order
        }
