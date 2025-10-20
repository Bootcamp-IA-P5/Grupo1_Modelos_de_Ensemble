from fastapi import FastAPI, HTTPException
import json
import os

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
