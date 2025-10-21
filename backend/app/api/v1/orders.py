from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.services.order_service import OrderService
from app.models.order import Order
from app.models.enums import OrderStatus

router = APIRouter()

def get_order_service(db=Depends(get_db)):
    return OrderService(db)

@router.get("/", response_model=List[dict])
async def get_all_orders(
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    service: OrderService = Depends(get_order_service)
):
    """Obtiene todas las órdenes"""
    return service.get_all_orders(limit=limit, offset=offset)

@router.get("/today", response_model=List[dict])
async def get_orders_today(service: OrderService = Depends(get_order_service)):
    """Órdenes del día - Vista PREVENTIVA"""
    return service.get_orders_today()

@router.get("/delayed", response_model=List[dict])
async def get_delayed_orders(service: OrderService = Depends(get_order_service)):
    """Órdenes atrasadas - Vista REACTIVA"""
    return service.get_delayed_orders()

@router.get("/at-risk", response_model=List[dict])
async def get_orders_at_risk(service: OrderService = Depends(get_order_service)):
    """Órdenes en riesgo (cerca del límite) - PREVENTIVO"""
    return service.get_orders_at_risk()

@router.get("/to-ship", response_model=List[dict])
async def get_orders_to_ship(service: OrderService = Depends(get_order_service)):
    """Órdenes por enviar - Vista unificada con todas las pendientes"""
    return service.get_orders_to_ship()

@router.get("/{order_id}")
async def get_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service)
):
    """Obtiene una orden por ID"""
    order = service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/delivered", response_model=List[dict])
async def get_delivered_orders(service: OrderService = Depends(get_order_service)):
    """Órdenes entregadas"""
    return service.get_delivered_orders()


