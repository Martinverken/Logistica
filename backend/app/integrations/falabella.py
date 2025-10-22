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
    
    def fetch_orders(self, offset: int = 0, limit: int = 50, only_pending: bool = True) -> List[Dict]:
        """Obtiene órdenes de MercadoLibre"""
        try:
            url = f"{self.base_url}/orders/search"
            params = {
                'seller': self.user_id,
                'offset': offset,
                'limit': limit,
                'sort': 'date_desc'
            }
            
            # FILTRO: Solo órdenes pendientes por defecto
            if only_pending:
                params['shipping.status'] = 'ready_to_ship'
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            orders = data.get('results', [])
            
            # Enriquecer con shipments
            enriched_orders = []
            for order in orders:
                shipment_id = order.get('shipping', {}).get('id')
                if shipment_id:
                    shipment_data = self._get_shipment(shipment_id)
                    order['shipment_data'] = shipment_data
                enriched_orders.append(order)
            
            self.logger.info(f"Fetched {len(enriched_orders)} orders from MercadoLibre")
            return enriched_orders
            
        except Exception as e:
            self.logger.error(f"Error fetching ML orders: {e}")
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
