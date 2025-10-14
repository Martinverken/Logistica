from app.models.enums import OrderStatus, ShippingType, Platform

class StatusMapper:
    """Mapea estados de diferentes plataformas al formato unificado"""
    
    FALABELLA_STATUS_MAP = {
        "ready_to_ship": OrderStatus.LISTO_DESPACHAR,
        "shipped": OrderStatus.ENVIADO,
        "delivered": OrderStatus.ENTREGADO,
        "canceled": OrderStatus.CANCELADO,
    }
    
    MELI_STATUS_MAP = {
        "ready_to_ship": OrderStatus.LISTO_DESPACHAR,
        "shipped": OrderStatus.ENVIADO,
        "delivered": OrderStatus.ENTREGADO,
        "cancelled": OrderStatus.CANCELADO,
    }
    
    @classmethod
    def map_status(cls, platform: Platform, raw_status: str) -> OrderStatus:
        if platform == Platform.FALABELLA:
            return cls.FALABELLA_STATUS_MAP.get(
                raw_status.lower(), 
                OrderStatus.LISTO_DESPACHAR
            )
        elif platform == Platform.MERCADOLIBRE:
            return cls.MELI_STATUS_MAP.get(
                raw_status.lower(),
                OrderStatus.LISTO_DESPACHAR
            )
        return OrderStatus.LISTO_DESPACHAR