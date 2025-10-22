import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .base import BasePlatformIntegration
from app.models.enums import Platform, OrderStatus, ShippingType
from app.utils.status_mapper import StatusMapper
from app.utils.date_helpers import parse_iso_date

class MercadoLibreIntegration(BasePlatformIntegration):
    def __init__(self, access_token: str, user_id: str, base_url: str):
        super().__init__(Platform.MERCADOLIBRE)
        self.access_token = access_token
        self.user_id = user_id
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'x-format-new': 'true'
        }
    
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
        
        def _get_shipment(self, shipment_id: str) -> Optional[Dict]:
            """Obtiene detalles del shipment"""
            try:
                url = f"{self.base_url}/shipments/{shipment_id}"
                response = requests.get(url, headers=self.headers, timeout=15)
                response.raise_for_status()
                return response.json()
            except:
                return None
        
    def map_to_standard_order(self, raw_order: Dict) -> Dict:
        """Mapea orden de MercadoLibre al formato estándar"""
        
        shipment_data = raw_order.get('shipment_data', {})
        logistic = shipment_data.get('logistic', {})
        
        # Tipo de envío
        logistic_type = logistic.get('type', '').lower()
        if 'flex' in logistic_type:
            shipping_type = ShippingType.MELI_FLEX
        else:
            shipping_type = ShippingType.MELI_CENTRO_ENVIOS
        
        # Estado
        status = shipment_data.get('status', 'pending')
        substatus = shipment_data.get('substatus', '')
        
        if substatus == 'ready_to_print':
            current_status = OrderStatus.ETIQUETA_IMPRESA
        else:
            current_status = StatusMapper.map_status(Platform.MERCADOLIBRE, status)
        
        # Cliente
        buyer = raw_order.get('buyer', {})
        
        # Fechas
        date_created = parse_iso_date(raw_order.get('date_created'))
        
        # Límite de despacho
        lead_time = shipment_data.get('lead_time', {})
        limite_str = lead_time.get('estimated_schedule_limit', {}).get('date')
        limite_despacho = parse_iso_date(limite_str)
        
        if not limite_despacho and date_created:
            if shipping_type == ShippingType.MELI_FLEX:
                limite_despacho = date_created + timedelta(hours=24)
            else:
                limite_despacho = date_created + timedelta(days=2)
        
        # Dirección
        destination = shipment_data.get('destination', {})
        ship_addr = destination.get('shipping_address', {})
        address_parts = [
            ship_addr.get('street_name', ''),
            ship_addr.get('street_number', ''),
            ship_addr.get('zip_code', '')
        ]
        shipping_address = ', '.join(filter(None, [str(p) for p in address_parts]))
        
        city = ship_addr.get('city', {})
        if isinstance(city, dict):
            city = city.get('name')
        
        return {
            'platform': Platform.MERCADOLIBRE,
            'external_order_id': str(raw_order.get('id')),
            'order_number': str(raw_order.get('id')),
            'shipping_type': shipping_type,
            'current_status': current_status,
            'customer_name': f"{buyer.get('first_name', '')} {buyer.get('last_name', '')}".strip(),
            'customer_phone': buyer.get('phone', {}).get('number'),
            'customer_email': buyer.get('email'),
            'total_amount': float(raw_order.get('total_amount', 0)),
            'items_count': len(raw_order.get('order_items', [])),
            'shipping_address': shipping_address,
            'shipping_city': str(city) if city else None,
            'limite_despacho': limite_despacho,
            'promised_delivery': parse_iso_date(lead_time.get('estimated_delivery_time', {}).get('date')),
            'created_at': date_created,
            'raw_data': {'order': raw_order, 'shipment': shipment_data}
        }