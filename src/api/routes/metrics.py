from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

@router.get("/metrics")
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
