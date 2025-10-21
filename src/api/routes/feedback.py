"""
Sistema de feedback para predicciones
EcoPrint - Sistema de Predicción de Riesgo de Incendios Forestales
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from src.api.services.database import db_service
from src.api.services.feedback_validator import feedback_validator
from src.api.schemas.feedback import FeedbackRequest, FeedbackResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackRequest):
    """
    Enviar feedback sobre una predicción
    
    ¿Qué hace?
    - Valida el feedback del usuario
    - Guarda en MongoDB si es válido
    - Actualiza métricas de calidad
    - Devuelve confirmación
    """
    try:
        # Validar feedback
        validation_result = feedback_validator.validate_feedback(feedback.dict())
        
        if not validation_result["is_valid"]:
            return FeedbackResponse(
                feedback_id="",
                message=f"Feedback rechazado: {', '.join(validation_result['warnings'])}",
                timestamp=datetime.utcnow()
            )
        
        # Conectar a la base de datos si no está conectada
        if db_service.database is None:
            await db_service.connect()
        
        # Crear documento de feedback
        feedback_data = {
            "prediction_id": feedback.prediction_id,
            "feedback_type": feedback.feedback_type,
            "rating": feedback.rating,
            "comment": feedback.comment,
            "user_id": feedback.user_id,
            "timestamp": datetime.utcnow(),
            "validation_confidence": validation_result["confidence"],
            "is_valid": True,
            "processed": False
        }
        
        # Guardar en MongoDB
        collection = db_service.get_collection("feedback")
        result = await collection.insert_one(feedback_data)
        
        # Actualizar reputación del usuario si es válido
        if feedback.user_id and validation_result["confidence"] > 0.7:
            feedback_validator.update_user_reputation(
                feedback.user_id, 
                validation_result["confidence"]
            )
        
        return FeedbackResponse(
            feedback_id=str(result.inserted_id),
            message="Feedback enviado correctamente",
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error enviando feedback: {e}")
        raise HTTPException(status_code=500, detail=f"Error enviando feedback: {str(e)}")

@router.get("/feedback")
async def get_feedback_dashboard(limit: int = 10):
    """
    Dashboard completo de feedback
    
    ¿Qué devuelve?
    - Estadísticas de feedback
    - Feedback reciente
    - Calidad de predicciones
    - Métricas de usuario
    """
    try:
        # Conectar a la base de datos si no está conectada
        if db_service.database is None:
            await db_service.connect()
        
        # Obtener colecciones
        feedback_collection = db_service.get_collection("feedback")
        predictions_collection = db_service.get_collection("predictions")
        
        # Calcular estadísticas de feedback
        total_feedback = await feedback_collection.count_documents({})
        
        # Distribución de calificaciones
        rating_pipeline = [
            {"$group": {"_id": "$rating", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        rating_distribution = {}
        async for doc in feedback_collection.aggregate(rating_pipeline):
            rating_distribution[doc["_id"]] = doc["count"]
        
        # Calcular puntuación promedio (simplificado)
        avg_rating = 0
        if total_feedback > 0:
            # Mapear ratings a números para calcular promedio
            rating_scores = {
                "very_poor": 1,
                "poor": 2,
                "average": 3,
                "good": 4,
                "excellent": 5
            }
            
            total_score = 0
            count = 0
            async for feedback in feedback_collection.find({}, {"rating": 1}):
                if feedback.get("rating") in rating_scores:
                    total_score += rating_scores[feedback["rating"]]
                    count += 1
            
            if count > 0:
                avg_rating = total_score / count
        
        # Obtener feedback reciente
        recent_feedback = []
        async for feedback in feedback_collection.find().sort("timestamp", -1).limit(limit):
            feedback["_id"] = str(feedback["_id"])
            recent_feedback.append(feedback)
        
        # Calcular calidad de predicciones
        total_predictions = await predictions_collection.count_documents({})
        
        # Predicciones de alta confianza (>0.8)
        high_confidence = await predictions_collection.count_documents({
            "confidence": {"$gt": 0.8}
        })
        
        # Predicciones de baja confianza (<0.5)
        low_confidence = await predictions_collection.count_documents({
            "confidence": {"$lt": 0.5}
        })
        
        # Confianza promedio
        avg_confidence_pipeline = [
            {"$group": {"_id": None, "avg_confidence": {"$avg": "$confidence"}}}
        ]
        avg_confidence = 0
        async for doc in predictions_collection.aggregate(avg_confidence_pipeline):
            avg_confidence = doc.get("avg_confidence", 0)
        
        # Calcular puntuación de calidad
        quality_score = 0
        if total_feedback > 0:
            valid_feedback = await feedback_collection.count_documents({"is_valid": True})
            quality_score = valid_feedback / total_feedback
        
        return {
            "success": True,
            "feedback_stats": {
                "total_feedback": total_feedback,
                "average_rating": round(avg_rating, 2),
                "rating_distribution": rating_distribution,
                "quality_score": round(quality_score, 2)
            },
            "recent_feedback": recent_feedback,
            "prediction_quality": {
                "total_predictions": total_predictions,
                "high_confidence_predictions": high_confidence,
                "low_confidence_predictions": low_confidence,
                "average_confidence": round(avg_confidence, 3)
            },
            "database": db_service.db_name
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo dashboard de feedback: {e}")
        return {
            "success": False,
            "message": f"Error obteniendo feedback: {str(e)}"
        }

@router.get("/feedback/stats")
async def get_feedback_stats():
    """
    Solo estadísticas de feedback (versión simplificada)
    """
    try:
        if db_service.database is None:
            await db_service.connect()
        
        collection = db_service.get_collection("feedback")
        
        # Estadísticas básicas
        total = await collection.count_documents({})
        valid = await collection.count_documents({"is_valid": True})
        
        return {
            "success": True,
            "total_feedback": total,
            "valid_feedback": valid,
            "quality_rate": round(valid / total, 2) if total > 0 else 0
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error obteniendo estadísticas: {str(e)}"
        }