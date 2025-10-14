from fastapi import APIRouter, Depends
from app.core.database import get_db
from supabase import Client

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(db: Client = Depends(get_db)):
    """Obtiene estadísticas del dashboard"""
    try:
        result = db.table('dashboard_stats').select('*').execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        return {
            "orders_today": 0,
            "orders_delayed": 0,
            "orders_ready_to_ship": 0,
            "orders_shipped": 0,
            "orders_delivered_today": 0,
            "avg_delay_hours": 0
        }
    except Exception as e:
        return {
            "error": str(e),
            "orders_today": 0,
            "orders_delayed": 0
        }

