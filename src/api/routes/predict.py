from fastapi import APIRouter, HTTPException
import joblib
import numpy as np
import pandas as pd
import os
import json
from typing import Optional, List
from src.api.schemas.predict import PredictRequest, PredictResponse

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
def predict(req: PredictRequest):
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

    return PredictResponse(
        prediction=y_pred,
        class_name=class_name,
        confidence=confidence,
        risk_level=risk_info["level"],
        risk_score=risk_info["score"],
    )
