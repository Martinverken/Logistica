from fastapi import APIRouter, Depends, BackgroundTasks
from app.core.database import get_db
from app.services.sync_service import SyncService
from supabase import Client

router = APIRouter()

@router.post("/all")
async def sync_all_platforms(
    background_tasks: BackgroundTasks,
    db: Client = Depends(get_db)
):
    """Sincroniza todas las plataformas"""
    sync_service = SyncService(db)
    
    # Ejecutar en background para no bloquear
    def sync_task():
        return sync_service.sync_all_platforms()
    
    result = sync_task()
    
    return {
        "message": "Sync completed",
        "result": result
    }

@router.post("/falabella")
async def sync_falabella(db: Client = Depends(get_db)):
    """Sincroniza solo Falabella"""
    sync_service = SyncService(db)
    result = sync_service.sync_falabella()
    return {
        "message": "Falabella sync completed",
        "result": result
    }

@router.post("/mercadolibre")
async def sync_mercadolibre(db: Client = Depends(get_db)):
    """Sincroniza solo MercadoLibre"""
    sync_service = SyncService(db)
    result = sync_service.sync_mercadolibre()
    return {
        "message": "MercadoLibre sync completed",
        "result": result
    }

