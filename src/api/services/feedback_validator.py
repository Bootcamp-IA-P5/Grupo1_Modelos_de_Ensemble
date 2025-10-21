"""
Validador de feedback para evitar datos falsos
EcoPrint - Sistema de Predicción de Riesgo de Incendios Forestales
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class FeedbackValidator:
    """
    Valida feedback de usuarios para evitar datos falsos
    
    ¿Por qué este validador?
    - Evita que usuarios maliciosos arruinen el modelo
    - Detecta patrones sospechosos
    - Mantiene la calidad de los datos
    """
    
    def __init__(self):
        self.suspicious_patterns = []
        self.user_reputation = {}  # Reputación de usuarios
    
    def validate_feedback(self, feedback_data: Dict) -> Dict:
        """
        Validar feedback de usuario
        
        ¿Qué validamos?
        - Consistencia con predicciones anteriores
        - Patrones sospechosos del usuario
        - Lógica del feedback
        """
        validation_result = {
            "is_valid": True,
            "confidence": 1.0,
            "warnings": [],
            "action": "accept"
        }
        
        # 1. Validar consistencia básica
        if not self._validate_basic_consistency(feedback_data):
            validation_result["is_valid"] = False
            validation_result["action"] = "reject"
            validation_result["warnings"].append("Feedback inconsistente con datos básicos")
            return validation_result
        
        # 2. Verificar reputación del usuario
        user_id = feedback_data.get("user_id")
        if user_id:
            user_rep = self._get_user_reputation(user_id)
            if user_rep < 0.3:  # Usuario con baja reputación
                validation_result["confidence"] *= 0.5
                validation_result["warnings"].append("Usuario con baja reputación")
        
        # 3. Detectar patrones sospechosos
        if self._detect_suspicious_patterns(feedback_data):
            validation_result["confidence"] *= 0.3
            validation_result["warnings"].append("Patrón sospechoso detectado")
        
        # 4. Determinar acción final
        if validation_result["confidence"] < 0.5:
            validation_result["action"] = "review"
        elif validation_result["confidence"] < 0.3:
            validation_result["action"] = "reject"
        
        return validation_result
    
    def _validate_basic_consistency(self, feedback_data: Dict) -> bool:
        """Validar consistencia básica del feedback"""
        # Verificar que el feedback tenga sentido
        rating = feedback_data.get("rating")
        feedback_type = feedback_data.get("feedback_type")
        
        # Validaciones básicas
        if not rating or not feedback_type:
            return False
        
        # Verificar que el rating sea válido
        valid_ratings = ["very_poor", "poor", "average", "good", "excellent"]
        if rating not in valid_ratings:
            return False
        
        return True
    
    def _get_user_reputation(self, user_id: str) -> float:
        """Obtener reputación del usuario (0-1)"""
        # Por ahora, todos los usuarios tienen reputación neutral
        # En el futuro, esto se calcularía basado en:
        # - Historial de feedback
        # - Consistencia con otros usuarios
        # - Validación por expertos
        return self.user_reputation.get(user_id, 0.5)
    
    def _detect_suspicious_patterns(self, feedback_data: Dict) -> bool:
        """Detectar patrones sospechosos"""
        # Por ahora, no detectamos patrones sospechosos
        # En el futuro, esto detectaría:
        # - Múltiples feedbacks negativos del mismo usuario
        # - Feedback muy rápido (bot)
        # - Patrones de calificación extraños
        return False
    
    def update_user_reputation(self, user_id: str, feedback_quality: float):
        """Actualizar reputación del usuario basada en calidad del feedback"""
        current_rep = self.user_reputation.get(user_id, 0.5)
        # Promedio ponderado: 70% reputación actual + 30% nueva calidad
        new_rep = current_rep * 0.7 + feedback_quality * 0.3
        self.user_reputation[user_id] = max(0.0, min(1.0, new_rep))
        
        logger.info(f"Reputación actualizada para {user_id}: {new_rep:.2f}")

# Instancia global del validador
feedback_validator = FeedbackValidator()
