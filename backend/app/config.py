# =====================================================
# backend/app/config.py
# =====================================================
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Sistema Logística Unificado"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    FALABELLA_API_KEY: str
    FALABELLA_USER_ID: str
    FALABELLA_BASE_URL: str = "https://sellercenter-api.falabella.com"
    
    MELI_ACCESS_TOKEN: str
    MELI_USER_ID: str
    MELI_BASE_URL: str = "https://api.mercadolibre.com"
    
    SYNC_INTERVAL_HOURS: int = 2
    RISK_HOURS_THRESHOLD: int = 6
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()


# =====================================================
# backend/app/core/database.py
# =====================================================
from supabase import create_client, Client
from app.config import get_settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            settings = get_settings()
            cls._instance = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            logger.info("Supabase client initialized")
        return cls._instance

def get_db() -> Client:
    return SupabaseClient.get_client()