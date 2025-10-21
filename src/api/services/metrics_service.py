"""
Servicio de métricas que NO usa feedback para entrenar
EcoPrint - Sistema de Predicción de Riesgo de Incendios Forestales
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MetricsService:
    """
    Servicio de métricas que mantiene separados los datos de entrenamiento del feedback
    
    ¿Por qué este servicio?
    - Mantiene la integridad del modelo
    - Usa feedback solo para monitoreo, NO para entrenar
    - Detecta problemas sin corromper el modelo
    """
    
    def __init__(self):
        self.prediction_metrics = []
        self.feedback_metrics = []
        self.model_performance = {}
    
    async def record_prediction(self, prediction_data: Dict):
        """
        Registrar una predicción para métricas
        
        ¿Qué registramos?
        - Datos de la predicción (features, resultado)
        - Tiempo de procesamiento
        - Confianza del modelo
        - NO incluimos feedback del usuario
        """
        metric = {
            "timestamp": datetime.utcnow(),
            "prediction": prediction_data["prediction"],
            "confidence": prediction_data["confidence"],
            "processing_time": prediction_data.get("processing_time_ms"),
            "model_version": prediction_data.get("model_version", "1.0.0"),
            "features_hash": self._hash_features(prediction_data["features"])
        }
        
        self.prediction_metrics.append(metric)
        logger.info(f"Predicción registrada: {prediction_data['prediction']} con confianza {prediction_data['confidence']}")
    
    async def record_feedback(self, feedback_data: Dict, validation_result: Dict):
        """
        Registrar feedback para análisis (NO para entrenar)
        
        ¿Qué registramos?
        - Feedback del usuario
        - Resultado de validación
        - Para detectar problemas, NO para entrenar
        """
        metric = {
            "timestamp": datetime.utcnow(),
            "prediction_id": feedback_data["prediction_id"],
            "rating": feedback_data["rating"],
            "feedback_type": feedback_data["feedback_type"],
            "validation_confidence": validation_result["confidence"],
            "is_valid": validation_result["is_valid"],
            "action": validation_result["action"]
        }
        
        self.feedback_metrics.append(metric)
        logger.info(f"Feedback registrado: {feedback_data['rating']} (válido: {validation_result['is_valid']})")
    
    def get_model_performance(self) -> Dict:
        """
        Obtener métricas de rendimiento del modelo
        
        ¿Qué métricas?
        - Basadas en predicciones, NO en feedback
        - Confianza promedio
        - Distribución de predicciones
        - Tiempo de procesamiento
        """
        if not self.prediction_metrics:
            return {"message": "No hay métricas disponibles"}
        
        # Calcular métricas de las últimas 24 horas
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        recent_metrics = [m for m in self.prediction_metrics if m["timestamp"] > cutoff_time]
        
        if not recent_metrics:
            return {"message": "No hay métricas recientes"}
        
        # Calcular estadísticas
        confidences = [m["confidence"] for m in recent_metrics]
        processing_times = [m["processing_time"] for m in recent_metrics if m["processing_time"]]
        
        performance = {
            "total_predictions": len(recent_metrics),
            "average_confidence": sum(confidences) / len(confidences),
            "min_confidence": min(confidences),
            "max_confidence": max(confidences),
            "average_processing_time": sum(processing_times) / len(processing_times) if processing_times else 0,
            "prediction_distribution": self._get_prediction_distribution(recent_metrics),
            "timeframe": "24 hours"
        }
        
        return performance
    
    def get_feedback_analysis(self) -> Dict:
        """
        Analizar feedback para detectar problemas
        
        ¿Qué analizamos?
        - Patrones en el feedback
        - Usuarios problemáticos
        - Alertas de calidad
        - NO para entrenar el modelo
        """
        if not self.feedback_metrics:
            return {"message": "No hay feedback disponible"}
        
        # Calcular estadísticas de feedback
        total_feedback = len(self.feedback_metrics)
        valid_feedback = len([f for f in self.feedback_metrics if f["is_valid"]])
        rejected_feedback = len([f for f in self.feedback_metrics if f["action"] == "reject"])
        
        # Distribución de calificaciones
        rating_distribution = {}
        for feedback in self.feedback_metrics:
            rating = feedback["rating"]
            rating_distribution[rating] = rating_distribution.get(rating, 0) + 1
        
        analysis = {
            "total_feedback": total_feedback,
            "valid_feedback": valid_feedback,
            "rejected_feedback": rejected_feedback,
            "validation_rate": valid_feedback / total_feedback if total_feedback > 0 else 0,
            "rating_distribution": rating_distribution,
            "quality_score": self._calculate_quality_score()
        }
        
        return analysis
    
    def _hash_features(self, features: List[float]) -> str:
        """Crear hash de features para detectar duplicados"""
        # Simplificado: usar suma de features como hash
        return str(sum(features))
    
    def _get_prediction_distribution(self, metrics: List[Dict]) -> Dict:
        """Obtener distribución de predicciones"""
        distribution = {}
        for metric in metrics:
            pred = metric["prediction"]
            distribution[pred] = distribution.get(pred, 0) + 1
        return distribution
    
    def _calculate_quality_score(self) -> float:
        """Calcular puntuación de calidad del feedback"""
        if not self.feedback_metrics:
            return 0.0
        
        # Puntuación basada en validación y consistencia
        valid_count = len([f for f in self.feedback_metrics if f["is_valid"]])
        total_count = len(self.feedback_metrics)
        
        return valid_count / total_count if total_count > 0 else 0.0

# Instancia global del servicio
metrics_service = MetricsService()
