"""
Endpoints para A/B Testing de modelos
"""

from fastapi import APIRouter, HTTPException
from src.api.schemas.predict import PredictRequest, PredictResponse
from src.api.services.ab_testing_service import ab_testing_service
import time
import numpy as np

router = APIRouter()

@router.post("/predict-ab", response_model=PredictResponse)
async def predict_ab(request: PredictRequest):
    """
    Predicción con A/B testing automático
    Selecciona modelo automáticamente basado en pesos configurados
    """
    start_time = time.time()
    
    try:
        # Seleccionar modelo para A/B testing
        model_name = ab_testing_service.select_model(request.user_id)
        
        # Preparar features
        features = np.array(request.features, dtype=float).reshape(1, -1)
        
        # Hacer predicción
        prediction = ab_testing_service.predict(features, model_name)
        
        if prediction is None:
            raise HTTPException(status_code=500, detail="Error en predicción A/B")
        
        prediction = int(prediction[0])
        
        # Mapeo de riesgo (igual que en predict.py)
        risk_mapping = {
            0: {"level": "LOW", "score": 2, "name": "Spruce/Fir"},
            1: {"level": "HIGH", "score": 8, "name": "Lodgepole Pine"},
            2: {"level": "MEDIUM", "score": 5, "name": "Ponderosa Pine"},
            3: {"level": "LOW", "score": 1, "name": "Cottonwood/Willow"},
            4: {"level": "MEDIUM", "score": 4, "name": "Aspen"},
            5: {"level": "MEDIUM", "score": 6, "name": "Douglas-fir"},
            6: {"level": "HIGH", "score": 9, "name": "Krummholz"},
        }
        
        risk_info = risk_mapping.get(prediction, {"level": "UNKNOWN", "score": 0, "name": f"Class_{prediction}"})
        
        # Calcular confianza (simplificado)
        confidence = 0.95  # Placeholder - en un sistema real se calcularía
        
        processing_time = (time.time() - start_time) * 1000
        
        # Registrar resultado para análisis
        ab_testing_service.record_prediction_result(
            model_name, prediction, confidence, processing_time
        )
        
        response = PredictResponse(
            prediction=prediction,
            class_name=risk_info["name"],
            confidence=confidence,
            risk_level=risk_info["level"],
            risk_score=risk_info["score"],
            processing_time_ms=processing_time
        )
        
        # Añadir metadata de A/B testing
        response_dict = response.dict()
        response_dict["ab_testing"] = {
            "model_used": model_name,
            "ab_testing_enabled": True
        }
        
        return response_dict
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en A/B testing: {str(e)}")

@router.get("/ab-testing/stats")
async def get_ab_testing_stats():
    """
    Obtener estadísticas de A/B testing
    """
    try:
        stats = ab_testing_service.get_model_stats()
        return {
            "success": True,
            "ab_testing_stats": stats,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo stats: {str(e)}")

@router.post("/ab-testing/weights")
async def update_model_weights(weights: dict):
    """
    Actualizar pesos de distribución de modelos
    
    Ejemplo:
    {
        "random_forest": 0.4,
        "extra_trees": 0.3,
        "xgboost": 0.3
    }
    """
    try:
        ab_testing_service.update_model_weights(weights)
        return {
            "success": True,
            "message": "Pesos actualizados correctamente",
            "new_weights": ab_testing_service.model_weights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando pesos: {str(e)}")

@router.get("/ab-testing/models")
async def get_available_models():
    """
    Obtener lista de modelos disponibles para A/B testing
    """
    try:
        stats = ab_testing_service.get_model_stats()
        return {
            "success": True,
            "available_models": stats['models_loaded'],
            "model_weights": stats['model_weights'],
            "total_models": stats['total_models']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo modelos: {str(e)}")
