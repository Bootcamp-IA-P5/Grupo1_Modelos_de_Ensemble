"""
Esquemas para predicciones
EcoPrint - Sistema de Predicción de Riesgo de Incendios Forestales
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    """Niveles de riesgo de incendio"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class PredictionRequest(BaseModel):
    """
    Esquema para solicitudes de predicción
    
    ¿Por qué este esquema?
    - Valida que los datos de entrada sean correctos
    - Asegura que tenemos exactamente 54 features
    - Permite metadata opcional (usuario, ubicación)
    """
    features: List[float] = Field(
        ..., 
        min_items=54, 
        max_items=54,
        description="Lista de 54 características del terreno"
    )
    user_id: Optional[str] = Field(None, description="ID del usuario (opcional)")
    location: Optional[Dict[str, float]] = Field(
        None, 
        description="Coordenadas geográficas (opcional)"
    )
    timestamp: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Momento de la solicitud"
    )

class PredictionResponse(BaseModel):
    """
    Esquema para respuestas de predicción
    
    ¿Por qué este esquema?
    - Estructura clara de la respuesta
    - Incluye información útil para el usuario
    - Permite análisis posterior
    """
    prediction: int = Field(..., description="Clase predicha (0-6)")
    class_name: str = Field(..., description="Nombre de la clase de vegetación")
    confidence: float = Field(..., description="Confianza de la predicción (0-1)")
    risk_level: RiskLevel = Field(..., description="Nivel de riesgo de incendio")
    risk_score: int = Field(..., description="Puntuación de riesgo (1-10)")
    processing_time_ms: Optional[float] = Field(None, description="Tiempo de procesamiento")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PredictionData(BaseModel):
    """
    Esquema para almacenar predicciones en MongoDB
    
    ¿Por qué este esquema?
    - Combina request + response para almacenamiento completo
    - Incluye metadata para análisis
    - Optimizado para consultas de base de datos
    """
    # Datos de entrada
    features: List[float]
    user_id: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    
    # Datos de salida
    prediction: int
    class_name: str
    confidence: float
    risk_level: RiskLevel
    risk_score: int
    processing_time_ms: Optional[float] = None
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_version: str = Field(default="1.0.0", description="Versión del modelo")
    api_version: str = Field(default="1.0.0", description="Versión de la API")
    
    # Para análisis
    session_id: Optional[str] = Field(None, description="ID de sesión del usuario")
    ip_address: Optional[str] = Field(None, description="IP del usuario")
    
    class Config:
        """Configuración de Pydantic"""
        json_encoders = {
            datetime: lambda dt: dt.isoformat() + "Z"
        }
        use_enum_values = True
