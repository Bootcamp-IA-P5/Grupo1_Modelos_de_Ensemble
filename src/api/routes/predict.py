from fastapi import APIRouter, HTTPException
import joblib
import numpy as np
import pandas as pd
import os
import json
import time
from typing import Optional, List
from datetime import datetime
from src.api.schemas.predict import PredictRequest, PredictResponse
from src.api.schemas.prediction import PredictionData
from src.api.services.database import db_service
from src.api.services.metrics_service import metrics_service

router = APIRouter()

# Cargar modelo y scaler una sola vez
_model = None
_scaler = None
_metadata = None

def _load_artifacts():
    global _model, _scaler, _metadata
    if _model is None:
        model_path = os.path.join("models", "best_model.pkl")
        scaler_path = os.path.join("models", "scaler.pkl")
        metadata_path = os.path.join("models", "metadata.json")
        
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="best_model.pkl not found in models/")
        if not os.path.exists(scaler_path):
            raise HTTPException(status_code=404, detail="scaler.pkl not found in models/")
        
        try:
            _model = joblib.load(model_path)
            _scaler = joblib.load(scaler_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load model/scaler: {str(e)}")
        
        # metadata opcional
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    _metadata = json.load(f)
            except Exception:
                _metadata = None

# Mapeo de riesgo (clases 0-6 como las usa el modelo entrenado)
_risk_mapping = {
    0: {"level": "LOW", "score": 2, "name": "Spruce/Fir"},      # Spruce/Fir
    1: {"level": "HIGH", "score": 8, "name": "Lodgepole Pine"},   # Lodgepole Pine
    2: {"level": "MEDIUM", "score": 5, "name": "Ponderosa Pine"},# Ponderosa Pine
    3: {"level": "LOW", "score": 1, "name": "Cottonwood/Willow"},# Cottonwood/Willow
    4: {"level": "MEDIUM", "score": 4, "name": "Aspen"},        # Aspen
    5: {"level": "MEDIUM", "score": 6, "name": "Douglas-fir"},  # Douglas-fir
    6: {"level": "HIGH", "score": 9, "name": "Krummholz"},      # Krummholz
}

@router.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    """
    Endpoint principal de predicción con guardado automático en MongoDB
    
    ¿Qué hace este endpoint?
    - Hace la predicción como antes
    - Guarda automáticamente en MongoDB
    - Registra métricas de rendimiento
    - Mantiene compatibilidad con el frontend
    """
    start_time = time.time()
    _load_artifacts()
    
    features = np.array(req.features, dtype=float).reshape(1, -1)
    
    # Usar nombres de features reales del Forest Cover Type Dataset
    real_feature_names = [
        "Elevation", "Aspect", "Slope", "Horizontal_Distance_To_Hydrology",
        "Vertical_Distance_To_Hydrology", "Horizontal_Distance_To_Roadways",
        "Hillshade_9am", "Hillshade_Noon", "Hillshade_3pm", "Horizontal_Distance_To_Fire_Points",
        "Wilderness_Area1", "Soil_Type1", "Soil_Type2", "Soil_Type3", "Soil_Type4",
        "Soil_Type5", "Soil_Type6", "Soil_Type7", "Soil_Type8", "Soil_Type9",
        "Soil_Type10", "Soil_Type11", "Soil_Type12", "Soil_Type13", "Soil_Type14",
        "Soil_Type15", "Soil_Type16", "Soil_Type17", "Soil_Type18", "Soil_Type19",
        "Soil_Type20", "Soil_Type21", "Soil_Type22", "Soil_Type23", "Soil_Type24",
        "Soil_Type25", "Soil_Type26", "Soil_Type27", "Soil_Type28", "Soil_Type29",
        "Soil_Type30", "Soil_Type31", "Soil_Type32", "Soil_Type33", "Soil_Type34",
        "Soil_Type35", "Soil_Type36", "Soil_Type37", "Soil_Type38", "Soil_Type39",
        "Soil_Type40", "Wilderness_Area2", "Wilderness_Area3", "Wilderness_Area4"
    ]
    
    X_df = pd.DataFrame(features, columns=real_feature_names)
    
    try:
        X_scaled = _scaler.transform(X_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scale features: {str(e)}")
    
    try:
        proba = None
        if hasattr(_model, "predict_proba"):
            proba = _model.predict_proba(X_scaled)[0]
        y_pred = int(_model.predict(X_scaled)[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run prediction: {str(e)}")

    # Obtener nombre de clase y riesgo
    risk_info = _risk_mapping.get(y_pred, {"level": "UNKNOWN", "score": 0, "name": f"Class_{y_pred}"})
    class_name = risk_info["name"]

    confidence = float(max(proba)) if proba is not None else 1.0
    processing_time = (time.time() - start_time) * 1000  # en milisegundos

    # Crear respuesta
    response = PredictResponse(
        prediction=y_pred,
        class_name=class_name,
        confidence=confidence,
        risk_level=risk_info["level"],
        risk_score=risk_info["score"],
        processing_time_ms=processing_time
    )

    # Guardar en MongoDB (en segundo plano, no bloquea la respuesta)
    try:
        await _save_prediction_to_db(req, response, processing_time)
    except Exception as e:
        # No fallar la predicción si hay error guardando
        print(f"⚠️ Error guardando predicción en DB: {e}")

    return response

async def _save_prediction_to_db(req: PredictRequest, response: PredictResponse, processing_time: float):
    """
    Guardar predicción en MongoDB de forma asíncrona
    
    ¿Por qué esta función?
    - No bloquea la respuesta al usuario
    - Maneja errores sin afectar la predicción
    - Registra métricas para análisis
    """
    try:
        # Conectar a la base de datos si no está conectada
        if db_service.database is None:
            await db_service.connect()
        
        # Crear documento para MongoDB
        prediction_data = PredictionData(
            features=req.features,
            user_id=req.user_id,
            location=req.location,
            prediction=response.prediction,
            class_name=response.class_name,
            confidence=response.confidence,
            risk_level=response.risk_level,
            risk_score=response.risk_score,
            processing_time_ms=processing_time,
            timestamp=datetime.utcnow()
        )
        
        # Guardar en MongoDB
        collection = db_service.get_collection("predictions")
        result = await collection.insert_one(prediction_data.dict(by_alias=True))
        
        # Registrar métricas
        await metrics_service.record_prediction({
            "prediction": response.prediction,
            "confidence": response.confidence,
            "processing_time_ms": processing_time,
            "features": req.features  # Agregar features para el hash
        })
        
        print(f"✅ Predicción guardada: {result.inserted_id}")
        
    except Exception as e:
        print(f"❌ Error guardando predicción: {e}")
        # No re-lanzar el error para no afectar la respuesta

@router.get("/predictions/recent")
async def get_recent_predictions(limit: int = 10):
    """
    Obtener predicciones recientes guardadas en MongoDB
    
    ¿Para qué sirve?
    - Ver las últimas predicciones hechas
    - Verificar que se están guardando correctamente
    - Análisis de patrones de uso
    """
    try:
        # Conectar a la base de datos si no está conectada
        if db_service.database is None:
            await db_service.connect()
        
        collection = db_service.get_collection("predictions")
        predictions = []
        
        # Obtener predicciones recientes
        async for pred in collection.find().sort("timestamp", -1).limit(limit):
            # Convertir ObjectId a string para JSON
            pred["_id"] = str(pred["_id"])
            # Simplificar features para la respuesta (solo mostrar primeras 5)
            if "features" in pred and len(pred["features"]) > 5:
                pred["features_preview"] = pred["features"][:5]
                del pred["features"]  # Remover features completas para ahorrar espacio
            predictions.append(pred)
        
        return {
            "success": True,
            "count": len(predictions),
            "predictions": predictions,
            "database": db_service.db_name
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error obteniendo predicciones: {str(e)}"
        }

@router.get("/predictions/stats")
async def get_prediction_stats():
    """
    Obtener estadísticas de predicciones
    
    ¿Para qué sirve?
    - Ver métricas de rendimiento
    - Análisis de uso
    - Detectar patrones
    """
    try:
        # Obtener métricas del servicio
        performance = metrics_service.get_model_performance()
        feedback_analysis = metrics_service.get_feedback_analysis()
        
        return {
            "success": True,
            "performance": performance,
            "feedback_analysis": feedback_analysis,
            "database": db_service.db_name
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error obteniendo estadísticas: {str(e)}"
        }
