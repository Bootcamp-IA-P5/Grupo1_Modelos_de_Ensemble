from fastapi import FastAPI, HTTPException
import json
import os
import joblib
import numpy as np
import pandas as pd
from typing import Optional, List
from .schemas.predict import PredictRequest, PredictResponse

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "service": "FireRiskAI"}

@app.get("/model")
def model_info():
    metadata_path = os.path.join("models", "metadata.json")
    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="metadata.json not found in models/")
    try:
        with open(metadata_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read metadata.json: {str(e)}")

@app.get("/metrics")
def risk_metrics():
    metrics_path = os.path.join("src", "utils", "fire_risk_metrics.json")
    if not os.path.exists(metrics_path):
        raise HTTPException(status_code=404, detail="fire_risk_metrics.json not found in src/utils/")
    try:
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read fire_risk_metrics.json: {str(e)}")


# ==========================
# POST /predict
# ==========================

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


# cover_type id (0..6) -> riesgo
_risk_mapping = {
    0: {"level": "LOW", "score": 2},   # Spruce/Fir
    1: {"level": "HIGH", "score": 8},  # Lodgepole Pine
    2: {"level": "MEDIUM", "score": 5},# Ponderosa Pine
    3: {"level": "LOW", "score": 1},   # Cottonwood/Willow
    4: {"level": "MEDIUM", "score": 4},# Aspen
    5: {"level": "MEDIUM", "score": 6},# Douglas-fir
    6: {"level": "HIGH", "score": 9},  # Krummholz
}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    _load_artifacts()
    features = np.array(req.features, dtype=float).reshape(1, -1)
    # si hay nombres de features en metadata, úsalos para evitar warnings
    columns: Optional[List[str]] = None
    if _metadata and isinstance(_metadata.get("features"), list) and len(_metadata["features"]) == 54:
        columns = _metadata["features"]
    X_df = pd.DataFrame(features, columns=columns if columns else [f"f{i}" for i in range(54)])
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

    # nombre de clase desde metadata si existe
    class_name = str(y_pred)
    if _metadata and isinstance(_metadata.get("target_classes"), dict):
        class_name = _metadata["target_classes"].get(str(y_pred), class_name)

    confidence = float(max(proba)) if proba is not None else 1.0
    risk = _risk_mapping.get(y_pred, {"level": "UNKNOWN", "score": 0})

    return PredictResponse(
        prediction=y_pred,
        class_name=class_name,
        confidence=confidence,
        risk_level=risk["level"],
        risk_score=risk["score"],
    )
