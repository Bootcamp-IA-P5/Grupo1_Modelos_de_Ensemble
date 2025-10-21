"""
Test para el endpoint de feedback
EcoPrint AI - Sistema de Predicción de Riesgo de Incendios Forestales
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestFeedbackEndpoint:
    """Test para los endpoints de feedback"""
    
    def test_submit_feedback_success(self):
        """
        Test del endpoint POST /feedback con datos válidos
        
        ¿Qué prueba?
        - Que la API responde correctamente
        - Que devuelve una respuesta de feedback válida
        - Que la estructura de respuesta es correcta
        """
        client = TestClient(app)
        
        # Datos de feedback válidos
        feedback_data = {
            "prediction_id": "test_prediction_123",
            "feedback_type": "accuracy",
            "rating": "excellent",
            "comment": "Muy preciso, la predicción fue correcta",
            "user_id": "test_user_123"
        }
        
        # Hacer petición real
        response = client.post("/feedback", json=feedback_data)
        
        # Verificar que responde
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Obtener datos de respuesta
        data = response.json()
        
        # Verificar estructura básica
        assert "feedback_id" in data, "Response should contain feedback_id"
        assert "message" in data, "Response should contain message"
        assert "timestamp" in data, "Response should contain timestamp"
        
        # Verificar tipos de datos
        assert isinstance(data["feedback_id"], str), "Feedback ID should be a string"
        assert isinstance(data["message"], str), "Message should be a string"
        assert isinstance(data["timestamp"], str), "Timestamp should be a string"
        
        # Verificar que el ID no está vacío
        assert len(data["feedback_id"]) > 0, "Feedback ID should not be empty"
        
        print("✅ Feedback submit test PASSED - Feedback endpoint works correctly!")
    
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
        Test con todos los ratings válidos
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
            
            # Todos los ratings válidos deberían funcionar
            assert response.status_code == 200, f"Expected 200 for rating '{rating}', got {response.status_code}"
            
            data = response.json()
            assert "feedback_id" in data, f"Response should contain feedback_id for rating '{rating}'"
        
        print("✅ Feedback valid ratings test PASSED - All valid ratings work!")
    
    def test_get_feedback_dashboard(self):
        """
        Test del endpoint GET /feedback (dashboard)
        
        ¿Qué prueba?
        - Que la API responde correctamente
        - Que devuelve la estructura del dashboard
        - Que los datos son consistentes
        """
        client = TestClient(app)
        
        # Hacer petición real
        response = client.get("/feedback")
        
        # Verificar que responde
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Obtener datos de respuesta
        data = response.json()
        
        # Verificar estructura básica
        assert "success" in data, "Response should contain success"
        assert "feedback_stats" in data, "Response should contain feedback_stats"
        assert "recent_feedback" in data, "Response should contain recent_feedback"
        assert "prediction_quality" in data, "Response should contain prediction_quality"
        
        # Verificar tipos de datos
        assert isinstance(data["success"], bool), "Success should be a boolean"
        assert isinstance(data["feedback_stats"], dict), "Feedback stats should be a dict"
        assert isinstance(data["recent_feedback"], list), "Recent feedback should be a list"
        assert isinstance(data["prediction_quality"], dict), "Prediction quality should be a dict"
        
        print("✅ Feedback dashboard test PASSED - Dashboard endpoint works correctly!")
    
    def test_feedback_stats_structure(self):
        """
        Test específico para la estructura de feedback_stats
        """
        client = TestClient(app)
        response = client.get("/feedback")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar estructura de feedback_stats
        stats = data["feedback_stats"]
        assert "total_feedback" in stats, "Feedback stats should contain total_feedback"
        assert "average_rating" in stats, "Feedback stats should contain average_rating"
        assert "rating_distribution" in stats, "Feedback stats should contain rating_distribution"
        assert "quality_score" in stats, "Feedback stats should contain quality_score"
        
        # Verificar tipos de datos
        assert isinstance(stats["total_feedback"], int), "Total feedback should be an integer"
        assert isinstance(stats["average_rating"], (int, float)), "Average rating should be a number"
        assert isinstance(stats["rating_distribution"], dict), "Rating distribution should be a dict"
        assert isinstance(stats["quality_score"], (int, float)), "Quality score should be a number"
        
        # Verificar rangos de valores
        assert stats["total_feedback"] >= 0, f"Total feedback should be >= 0, got {stats['total_feedback']}"
        assert 0 <= stats["average_rating"] <= 5, f"Average rating should be between 0 and 5, got {stats['average_rating']}"
        assert 0 <= stats["quality_score"] <= 1, f"Quality score should be between 0 and 1, got {stats['quality_score']}"
        
        print("✅ Feedback stats structure test PASSED - Stats structure is valid!")
    
    def test_feedback_with_limit_parameter(self):
        """
        Test del dashboard con parámetro limit
        """
        client = TestClient(app)
        
        # Probar con diferentes límites
        for limit in [1, 5, 10]:
            response = client.get(f"/feedback?limit={limit}")
            
            assert response.status_code == 200, f"Expected 200 for limit {limit}, got {response.status_code}"
            
            data = response.json()
            assert "success" in data, f"Response should contain success for limit {limit}"
            assert "recent_feedback" in data, f"Response should contain recent_feedback for limit {limit}"
            
            # El número de feedback reciente no debería exceder el límite
            recent_feedback = data["recent_feedback"]
            assert len(recent_feedback) <= limit, f"Recent feedback should not exceed limit {limit}, got {len(recent_feedback)}"
        
        print("✅ Feedback limit parameter test PASSED - Limit parameter works correctly!")
