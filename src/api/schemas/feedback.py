"""
Esquemas para feedback de usuarios
EcoPrint - Sistema de Predicción de Riesgo de Incendios Forestales
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class FeedbackType(str, Enum):
    """Tipos de feedback"""
    ACCURACY = "accuracy"  # Precisión de la predicción
    USEFULNESS = "usefulness"  # Utilidad de la información
    INTERFACE = "interface"  # Calidad de la interfaz
    GENERAL = "general"  # Feedback general

class FeedbackRating(str, Enum):
    """Calificaciones de feedback"""
    VERY_POOR = "very_poor"
    POOR = "poor"
    AVERAGE = "average"
    GOOD = "good"
    EXCELLENT = "excellent"

class FeedbackRequest(BaseModel):
    """
    Esquema para solicitudes de feedback
    
    ¿Por qué este esquema?
    - Permite a los usuarios calificar las predicciones
    - Recoge información valiosa para mejorar el modelo
    - Incluye contexto sobre la predicción
    """
    prediction_id: str = Field(..., description="ID de la predicción a calificar")
    feedback_type: FeedbackType = Field(..., description="Tipo de feedback")
    rating: FeedbackRating = Field(..., description="Calificación del usuario")
    comment: Optional[str] = Field(None, description="Comentario adicional")
    user_id: Optional[str] = Field(None, description="ID del usuario")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FeedbackResponse(BaseModel):
    """
    Esquema para respuestas de feedback
    
    ¿Por qué este esquema?
    - Confirma que el feedback se guardó correctamente
    - Proporciona información útil al usuario
    """
    feedback_id: str = Field(..., description="ID del feedback guardado")
    message: str = Field(..., description="Mensaje de confirmación")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FeedbackData(BaseModel):
    """
    Esquema para almacenar feedback en MongoDB
    
    ¿Por qué este esquema?
    - Almacena feedback completo para análisis
    - Incluye metadata para estadísticas
    - Permite correlacionar con predicciones
    """
    # Datos del feedback
    prediction_id: str
    feedback_type: FeedbackType
    rating: FeedbackRating
    comment: Optional[str] = None
    
    # Metadata del usuario
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    
    # Metadata temporal
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    api_version: str = Field(default="1.0.0")
    
    # Para análisis
    is_helpful: Optional[bool] = Field(None, description="¿Fue útil el feedback?")
    processed: bool = Field(default=False, description="¿Se procesó el feedback?")
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat() + "Z"
        }
        use_enum_values = True