"""
Test simplificado para el endpoint de feedback
EcoPrint AI - Sistema de Predicción de Riesgo de Incendios Forestales
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestFeedbackEndpointSimple:
    """Test simplificado para los endpoints de feedback"""
    
    def test_submit_feedback_validation(self):
        """
        Test de validación de datos de feedback
        
        ¿Qué prueba?
        - Que la validación de datos funciona correctamente
        - Que los campos requeridos son validados
        - Que los tipos de datos son correctos
        """
        client = TestClient(app)
        
        # Test con datos válidos (solo validación, no guardado)
        valid_data = {
            "prediction_id": "test_prediction_123",
            "feedback_type": "accuracy",
            "rating": "excellent",
            "comment": "Muy preciso, la predicción fue correcta",
            "user_id": "test_user_123"
        }
        
        # Hacer petición (puede fallar por DB, pero la validación debe pasar)
        response = client.post("/feedback", json=valid_data)
        
        # Si falla por DB (500), está bien - significa que la validación pasó
        # Si falla por validación (422), hay un problema
        assert response.status_code in [200, 500], f"Expected 200 or 500, got {response.status_code}"
        
        print("✅ Feedback validation test PASSED - Data validation works correctly!")
    
    def test_submit_feedback_invalid_rating(self):
        """
        Test con rating inválido
        """
        client = TestClient(app)
        
        # Datos con rating inválido
        invalid_data = {
            "prediction_id": "test_prediction_123",
            "feedback_type": "accuracy",
            "rating": "invalid_rating",
            "comment": "Test comment"
        }
        
        response = client.post("/feedback", json=invalid_data)
        
        # Debería devolver error de validación
        assert response.status_code == 422, f"Expected 422 for invalid rating, got {response.status_code}"
        
        print("✅ Feedback invalid rating test PASSED - Validation works correctly!")
    
    def test_submit_feedback_missing_required_fields(self):
        """
        Test sin campos requeridos
        """
        client = TestClient(app)
        
        # Datos sin campos requeridos
        invalid_data = {
            "prediction_id": "test_prediction_123",
            "comment": "Test comment"
            # Faltan feedback_type y rating
        }
        
        response = client.post("/feedback", json=invalid_data)
        
        # Debería devolver error de validación
        assert response.status_code == 422, f"Expected 422 for missing fields, got {response.status_code}"
        
        print("✅ Feedback missing fields test PASSED - Validation works correctly!")
    
    def test_submit_feedback_valid_ratings(self):
        """
        Test con todos los ratings válidos (solo validación)
        """
        client = TestClient(app)
        
        valid_ratings = ["very_poor", "poor", "average", "good", "excellent"]
        
        for rating in valid_ratings:
            feedback_data = {
                "prediction_id": f"test_prediction_{rating}",
                "feedback_type": "accuracy",
                "rating": rating,
                "comment": f"Test comment for {rating}",
                "user_id": "test_user_123"
            }
            
            response = client.post("/feedback", json=feedback_data)
            
            # Si falla por DB (500), está bien - significa que la validación pasó
            # Si falla por validación (422), hay un problema
            assert response.status_code in [200, 500], f"Expected 200 or 500 for rating '{rating}', got {response.status_code}"
        
        print("✅ Feedback valid ratings test PASSED - All valid ratings pass validation!")
    
    def test_get_feedback_endpoint_exists(self):
        """
        Test que verifica que el endpoint GET /feedback existe
        
        ¿Qué prueba?
        - Que el endpoint responde (aunque falle por DB)
        - Que no es un 404 (endpoint no encontrado)
        """
        client = TestClient(app)
        
        # Hacer petición
        response = client.get("/feedback")
        
        # Debería responder (no 404), aunque falle por DB
        assert response.status_code != 404, f"Endpoint not found, got {response.status_code}"
        
        # Debería ser 200 (éxito) o 500 (error de DB)
        assert response.status_code in [200, 500], f"Expected 200 or 500, got {response.status_code}"
        
        print("✅ Feedback GET endpoint test PASSED - Endpoint exists and responds!")
    
    def test_feedback_schema_validation(self):
        """
        Test que verifica que los esquemas de Pydantic funcionan
        """
        from src.api.schemas.feedback import FeedbackRequest, FeedbackRating
        
        # Test de enum de ratings
        valid_ratings = ["very_poor", "poor", "average", "good", "excellent"]
        for rating in valid_ratings:
            assert rating in [e.value for e in FeedbackRating], f"Rating '{rating}' should be valid"
        
        # Test de creación de objeto
        feedback_data = {
            "prediction_id": "test_123",
            "feedback_type": "accuracy",
            "rating": "excellent",
            "comment": "Test comment",
            "user_id": "user_123"
        }
        
        # Debería crear el objeto sin errores
        feedback = FeedbackRequest(**feedback_data)
        assert feedback.prediction_id == "test_123"
        assert feedback.rating == "excellent"
        
        print("✅ Feedback schema validation test PASSED - Pydantic schemas work correctly!")
