"""
Configuración global para tests
EcoPrint AI - Sistema de Predicción de Riesgo de Incendios Forestales
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
import os
from unittest.mock import AsyncMock, MagicMock

# Configurar variables de entorno para tests
os.environ["MONGO_URI"] = "mongodb://localhost:27017/test_ecoprint"
os.environ["DB_NAME"] = "test_ecoprint"

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

@pytest.fixture(scope="session")
def event_loop():
    """Crear event loop para tests async"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """Cliente de prueba para FastAPI"""
    return TestClient(app)

@pytest.fixture
def mock_database():
    """Mock de la base de datos para tests unitarios"""
    mock_db = AsyncMock()
    mock_collection = AsyncMock()
    
    # Configurar mocks
    mock_collection.count_documents.return_value = 0
    mock_collection.find.return_value = []
    mock_collection.find_one.return_value = None
    mock_collection.insert_one.return_value = MagicMock(inserted_id="test_id")
    mock_collection.aggregate.return_value = []
    
    mock_db.__getitem__.return_value = mock_collection
    mock_db.list_collection_names.return_value = ["predictions", "feedback"]
    
    return mock_db

@pytest.fixture
def sample_prediction_data():
    """Datos de ejemplo para predicciones"""
    return {
        "features": [2000.0, 180.0, 15.0] + [0.0] * 51,  # 54 features
        "user_id": "test_user_123",
        "location": {"lat": 40.7128, "lon": -74.0060}
    }

@pytest.fixture
def sample_feedback_data():
    """Datos de ejemplo para feedback"""
    return {
        "prediction_id": "test_prediction_123",
        "feedback_type": "accuracy",
        "rating": "excellent",
        "comment": "Muy preciso",
        "user_id": "test_user_123"
    }

@pytest.fixture
def sample_metrics_response():
    """Respuesta de ejemplo para métricas"""
    return {
        "success": True,
        "model_performance": {
            "accuracy": 0.9707,
            "precision": 0.968,
            "recall": 0.965,
            "f1_score": 0.966
        },
        "production_metrics": {
            "total_predictions": 10,
            "success_rate": 1.0,
            "average_processing_time_ms": 50.0
        },
        "system_health": {
            "database_status": "connected",
            "model_status": "active",
            "api_status": "running"
        }
    }
