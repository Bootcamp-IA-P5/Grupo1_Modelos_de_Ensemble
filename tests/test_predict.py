"""
Test para el endpoint de predicción
EcoPrint AI - Sistema de Predicción de Riesgo de Incendios Forestales
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestPredictEndpoint:
    """Test para el endpoint POST /predict"""
    
    def test_predict_success(self):
        """
        Test del endpoint /predict con datos válidos
        
        ¿Qué prueba?
        - Que la API responde correctamente
        - Que devuelve una predicción válida
        - Que la estructura de respuesta es correcta
        """
        client = TestClient(app)
        
        # Datos de prueba (54 features del Forest Cover Type Dataset)
        test_data = {
            "features": [2000.0, 180.0, 15.0, 300.0, 50.0, 1000.0, 200.0, 220.0, 180.0, 2000.0] + [0.0] * 44,
            "user_id": "test_user_123",
            "location": {"lat": 40.7128, "lon": -74.0060}
        }
        
        # Hacer petición real
        response = client.post("/predict", json=test_data)
        
        # Verificar que responde
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Obtener datos de respuesta
        data = response.json()
        
        # Verificar estructura básica
        assert "prediction" in data, "Response should contain prediction"
        assert "class_name" in data, "Response should contain class_name"
        assert "confidence" in data, "Response should contain confidence"
        assert "risk_level" in data, "Response should contain risk_level"
        assert "risk_score" in data, "Response should contain risk_score"
        assert "processing_time_ms" in data, "Response should contain processing_time_ms"
        
        # Verificar tipos de datos
        assert isinstance(data["prediction"], int), "Prediction should be an integer"
        assert isinstance(data["class_name"], str), "Class name should be a string"
        assert isinstance(data["confidence"], (int, float)), "Confidence should be a number"
        assert isinstance(data["risk_level"], str), "Risk level should be a string"
        assert isinstance(data["risk_score"], int), "Risk score should be an integer"
        assert isinstance(data["processing_time_ms"], (int, float)), "Processing time should be a number"
        
        # Verificar rangos de valores
        assert 0 <= data["prediction"] <= 6, f"Prediction should be between 0 and 6, got {data['prediction']}"
        assert 0 <= data["confidence"] <= 1, f"Confidence should be between 0 and 1, got {data['confidence']}"
        assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH"], f"Risk level should be LOW/MEDIUM/HIGH, got {data['risk_level']}"
        assert 1 <= data["risk_score"] <= 9, f"Risk score should be between 1 and 9, got {data['risk_score']}"
        assert data["processing_time_ms"] > 0, f"Processing time should be > 0, got {data['processing_time_ms']}"
        
        print("✅ Predict success test PASSED - Prediction endpoint works correctly!")
    
    def test_predict_invalid_features_length(self):
        """
        Test con features de longitud incorrecta
        """
        client = TestClient(app)
        
        # Datos con features incorrectas (solo 3 en lugar de 54)
        invalid_data = {
            "features": [2000.0, 180.0, 15.0],
            "user_id": "test_user_123"
        }
        
        response = client.post("/predict", json=invalid_data)
        
        # Debería devolver error de validación
        assert response.status_code == 422, f"Expected 422 for invalid features, got {response.status_code}"
        
        print("✅ Predict invalid features test PASSED - Validation works correctly!")
    
    def test_predict_missing_features(self):
        """
        Test sin features
        """
        client = TestClient(app)
        
        # Datos sin features
        invalid_data = {
            "user_id": "test_user_123"
        }
        
        response = client.post("/predict", json=invalid_data)
        
        # Debería devolver error de validación
        assert response.status_code == 422, f"Expected 422 for missing features, got {response.status_code}"
        
        print("✅ Predict missing features test PASSED - Validation works correctly!")
    
    def test_predict_without_optional_fields(self):
        """
        Test con solo las features requeridas (sin user_id ni location)
        """
        client = TestClient(app)
        
        # Solo features requeridas
        minimal_data = {
            "features": [2000.0, 180.0, 15.0, 300.0, 50.0, 1000.0, 200.0, 220.0, 180.0, 2000.0] + [0.0] * 44
        }
        
        response = client.post("/predict", json=minimal_data)
        
        # Debería funcionar sin campos opcionales
        assert response.status_code == 200, f"Expected 200 for minimal data, got {response.status_code}"
        
        data = response.json()
        assert "prediction" in data, "Response should contain prediction"
        assert "class_name" in data, "Response should contain class_name"
        
        print("✅ Predict minimal data test PASSED - Works with required fields only!")
    
    def test_predict_class_names(self):
        """
        Test que verifica que los nombres de clase son correctos
        """
        client = TestClient(app)
        
        test_data = {
            "features": [2000.0, 180.0, 15.0, 300.0, 50.0, 1000.0, 200.0, 220.0, 180.0, 2000.0] + [0.0] * 44
        }
        
        response = client.post("/predict", json=test_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que el nombre de clase es válido
        valid_class_names = [
            "Spruce/Fir", "Lodgepole Pine", "Ponderosa Pine", 
            "Cottonwood/Willow", "Aspen", "Douglas-fir", "Krummholz"
        ]
        
        assert data["class_name"] in valid_class_names, f"Class name should be one of {valid_class_names}, got {data['class_name']}"
        
        print("✅ Predict class names test PASSED - Class names are valid!")
    
    def test_predict_risk_mapping(self):
        """
        Test que verifica que el mapeo de riesgo es consistente
        """
        client = TestClient(app)
        
        test_data = {
            "features": [2000.0, 180.0, 15.0, 300.0, 50.0, 1000.0, 200.0, 220.0, 180.0, 2000.0] + [0.0] * 44
        }
        
        response = client.post("/predict", json=test_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar consistencia entre risk_level y risk_score
        risk_level = data["risk_level"]
        risk_score = data["risk_score"]
        
        if risk_level == "LOW":
            assert risk_score <= 3, f"LOW risk should have score <= 3, got {risk_score}"
        elif risk_level == "MEDIUM":
            assert 4 <= risk_score <= 6, f"MEDIUM risk should have score 4-6, got {risk_score}"
        elif risk_level == "HIGH":
            assert risk_score >= 7, f"HIGH risk should have score >= 7, got {risk_score}"
        
        print("✅ Predict risk mapping test PASSED - Risk mapping is consistent!")
