from enum import Enum

class Platform(str, Enum):
    FALABELLA = "falabella"
    MERCADOLIBRE = "mercadolibre"

class ShippingType(str, Enum):
    FALABELLA_DIRECTO = "falabella_directo"
    FALABELLA_NORMAL = "falabella_normal"
    MELI_FLEX = "meli_flex"
    MELI_CENTRO_ENVIOS = "meli_centro_envios"

class OrderStatus(str, Enum):
    LISTO_DESPACHAR = "listo_despachar"
    ETIQUETA_IMPRESA = "etiqueta_impresa"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

class AlertLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    CRITICAL = "critical"

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"