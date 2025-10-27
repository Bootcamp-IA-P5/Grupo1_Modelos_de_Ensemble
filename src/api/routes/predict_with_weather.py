"""
Predicción + Clima - VERSIÓN SIMPLE
Combina predicción básica con datos del clima
"""

from fastapi import APIRouter, HTTPException
from src.api.schemas.predict import PredictRequest, PredictResponse
from src.api.routes.predict import predict as basic_predict
from src.api.routes.weather import get_weather
import time

router = APIRouter()

@router.post("/predict-with-weather")
async def predict_with_weather(request: PredictRequest):
    """
    Predicción básica + datos del clima
    """
    start_time = time.time()
    
    # 1. Hacer predicción básica
    basic_response = await basic_predict(request)
    
    # 2. Obtener clima si hay coordenadas
    weather_data = None
    if request.location:
        weather_data = get_weather(
            request.location["lat"], 
            request.location["lon"]
        )
    
    # 3. Crear respuesta simple
    response = {
        "prediction": basic_response.prediction,
        "class_name": basic_response.class_name,
        "confidence": basic_response.confidence,
        "risk_level": basic_response.risk_level,
        "risk_score": basic_response.risk_score,
        "processing_time_ms": (time.time() - start_time) * 1000,
        "weather": weather_data
    }
    
    return response
