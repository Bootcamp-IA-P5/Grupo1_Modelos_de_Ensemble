"""
Endpoints para probar la conexión a MongoDB
EcoPrint - Sistema de Predicción de Riesgo de Incendios Forestales
"""

from fastapi import APIRouter, HTTPException
from src.api.services.database import db_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/database/status")
async def database_status():
    """
    Verificar el estado de la conexión a MongoDB
    
    ¿Por qué este endpoint?
    - Permite verificar si la conexión funciona
    - Útil para debugging
    - Puede ser usado por el frontend para mostrar estado
    """
    try:
        # Verificar si tenemos cliente
        if not db_service.client:
            return {
                "status": "disconnected",
                "message": "Base de datos no conectada",
                "database": db_service.db_name
            }
        
        # Verificar conexión con ping
        await db_service.client.admin.command('ping')
        
        # Obtener información de la base de datos
        collections = await db_service.database.list_collection_names()
        
        return {
            "status": "connected",
            "message": "Base de datos conectada correctamente",
            "database": db_service.db_name,
            "collections": collections,
            "collections_count": len(collections)
        }
        
    except Exception as e:
        logger.error(f"Error verificando base de datos: {e}")
        return {
            "status": "error",
            "message": f"Error conectando a la base de datos: {str(e)}",
            "database": db_service.db_name
        }

@router.post("/database/test-connection")
async def test_connection():
    """
    Probar la conexión a MongoDB
    
    ¿Por qué este endpoint?
    - Permite probar la conexión manualmente
    - Útil para verificar configuración
    - Puede ser usado por scripts de testing
    """
    try:
        # Intentar conectar
        success = await db_service.connect()
        
        if success:
            return {
                "status": "success",
                "message": "Conexión a MongoDB exitosa",
                "database": db_service.db_name
            }
        else:
            return {
                "status": "error",
                "message": "No se pudo conectar a MongoDB",
                "database": db_service.db_name
            }
            
    except Exception as e:
        logger.error(f"Error en test de conexión: {e}")
        return {
            "status": "error",
            "message": f"Error en test de conexión: {str(e)}",
            "database": db_service.db_name
        }
