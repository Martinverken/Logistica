from datetime import datetime, timezone
from typing import Optional

def parse_iso_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parsea fecha ISO string a datetime"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return None

def is_delayed(limite_despacho: datetime) -> bool:
    """Verifica si una orden está atrasada"""
    now = datetime.now(timezone.utc)
    return now > limite_despacho

def hours_until_deadline(limite_despacho: datetime) -> float:
    """Calcula horas hasta el límite de despacho"""
    now = datetime.now(timezone.utc)
    delta = limite_despacho - now
    return delta.total_seconds() / 3600

def is_at_risk(limite_despacho: datetime, threshold_hours: int = 6) -> bool:
    """Verifica si una orden está en riesgo"""
    hours = hours_until_deadline(limite_despacho)
    return 0 < hours < threshold_hours