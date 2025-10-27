"""
Endpoint simple para Data Drift Monitoring
"""

from fastapi import APIRouter, HTTPException
from src.api.services.drift_detector import drift_detector
from src.api.services.database import db_service
from pydantic import BaseModel
from typing import List
import asyncio

router = APIRouter()

class DriftRequest(BaseModel):
    features: List[List[float]]

class BaselineRequest(BaseModel):
    baseline_data: List[List[float]]

@router.post("/drift/check")
async def check_drift(request: DriftRequest):
    """
    Verificar si hay drift en datos nuevos y guardarlo en MongoDB
    """
    try:
        result = drift_detector.detect_drift(request.features)
        
        # Guardar en MongoDB
        try:
            collection = db_service.get_collection("drift_detections")
            await collection.insert_one(result)
        except Exception as db_error:
            # No fallar si MongoDB no está disponible
            pass
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/drift/baseline")
def set_baseline(request: BaselineRequest):
    """
    Establecer datos de referencia (baseline)
    """
    try:
        drift_detector.set_baseline(request.baseline_data)
        return {"success": True, "message": "Baseline establecido correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/drift/history")
async def get_drift_history():
    """
    Obtener historial de detecciones de drift desde MongoDB
    """
    try:
        # Intentar obtener de MongoDB
        try:
            collection = db_service.get_collection("drift_detections")
            cursor = collection.find().sort("timestamp", -1).limit(100)
            history = await cursor.to_list(length=100)
            return {"history": history}
        except Exception:
            # Fallback a historial en memoria
            history = drift_detector.get_drift_history()
            return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/drift/status")
async def get_drift_status():
    """
    Obtener estado actual del drift
    """
    try:
        if drift_detector.baseline_data is None:
            return {
                "has_baseline": False,
                "message": "No hay baseline establecido"
            }
        
        latest_drift = drift_detector.drift_history[-1] if drift_detector.drift_history else None
        
        return {
            "has_baseline": True,
            "baseline_samples": len(drift_detector.baseline_data),
            "total_detections": len(drift_detector.drift_history),
            "latest_drift": latest_drift,
            "threshold": drift_detector.threshold
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/drift/alerts")
async def get_drift_alerts():
    """
    Obtener alertas de drift activas
    """
    try:
        alerts = []
        
        # Obtener última detección
        if drift_detector.drift_history:
            latest = drift_detector.drift_history[-1]
            
            if latest.get("has_drift"):
                alerts.append({
                    "type": "DRIFT_DETECTED",
                    "severity": latest.get("drift_severity", "MEDIUM"),
                    "message": f"Drift detectado con severidad {latest.get('drift_severity')}",
                    "timestamp": latest.get("timestamp"),
                    "max_difference": latest.get("max_difference")
                })
        
        return {
            "alerts": alerts,
            "total_alerts": len(alerts),
            "has_active_alerts": len(alerts) > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
