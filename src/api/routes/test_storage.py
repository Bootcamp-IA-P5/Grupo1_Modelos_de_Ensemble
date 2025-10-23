"""
Endpoint simple para probar el guardado en MongoDB
EcoPrint - Sistema de Predicción de Riesgo de Incendios Forestales
"""

from fastapi import APIRouter
from src.api.services.database import db_service
from datetime import datetime
import json

router = APIRouter()

@router.post("/test/save-prediction")
async def test_save_prediction():
    """
    Probar guardando una predicción de ejemplo
    
    ¿Por qué este endpoint?
    - Es súper simple para probar que funciona
    - No necesita datos complejos
    - Podemos ver si se guarda correctamente
    """
    try:
        # Conectar a la base de datos si no está conectada
        if db_service.database is None:
            await db_service.connect()
        
        # Crear una predicción de ejemplo
        test_prediction = {
            "features": [2000.0, 180.0, 15.0] + [0.0] * 51,  # 54 features
            "prediction": 1,  # Lodgepole Pine
            "class_name": "Lodgepole Pine",
            "confidence": 0.95,
            "risk_level": "HIGH",
            "risk_score": 8,
            "timestamp": datetime.utcnow(),
            "model_version": "1.0.0",
            "test": True  # Marcar como prueba
        }
        
        # Guardar en MongoDB
        collection = db_service.get_collection("test_predictions")
        result = await collection.insert_one(test_prediction)
        
        return {
            "success": True,
            "message": "Predicción de prueba guardada correctamente",
            "prediction_id": str(result.inserted_id),
            "database": db_service.db_name,
            "collection": "test_predictions"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error guardando predicción: {str(e)}"
        }

@router.get("/test/list-predictions")
async def test_list_predictions():
    """
    Ver las predicciones de prueba guardadas
    
    ¿Por qué este endpoint?
    - Para verificar que se guardaron correctamente
    - Podemos ver qué datos tenemos
    """
    try:
        # Conectar a la base de datos si no está conectada
        if db_service.database is None:
            await db_service.connect()
            
        collection = db_service.get_collection("test_predictions")
        predictions = []
        
        async for pred in collection.find({"test": True}).limit(5):
            # Convertir ObjectId a string para JSON
            pred["_id"] = str(pred["_id"])
            predictions.append(pred)
        
        return {
            "success": True,
            "count": len(predictions),
            "predictions": predictions
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error listando predicciones: {str(e)}"
        }
