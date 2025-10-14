from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
from .enums import Platform, ShippingType, OrderStatus

class OrderBase(BaseModel):
    platform: Platform
    external_order_id: str
    order_number: Optional[str] = None
    shipping_type: ShippingType
    current_status: OrderStatus
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    total_amount: Optional[float] = None
    items_count: int = 1
    shipping_address: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_region: Optional[str] = None
    limite_despacho: datetime
    promised_delivery: Optional[datetime] = None

class OrderCreate(OrderBase):
    raw_data: Optional[dict] = None

class OrderUpdate(BaseModel):
    current_status: Optional[OrderStatus] = None
    actual_delivery: Optional[datetime] = None
    is_delayed: Optional[bool] = None

class Order(OrderBase):
    id: UUID
    is_delayed: bool = False
    delay_detected_at: Optional[datetime] = None
    delay_resolved_at: Optional[datetime] = None
    hours_delayed: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True