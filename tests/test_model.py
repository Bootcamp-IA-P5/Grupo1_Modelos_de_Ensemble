"""
Test para el endpoint de información del modelo
EcoPrint AI - Sistema de Predicción de Riesgo de Incendios Forestales
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os
import json

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestModelEndpoint:
    """Test para el endpoint GET /model"""
    
    def test_model_info_success(self):
        """
        Test del endpoint /model cuando existe el archivo de metadata
        
        ¿Qué prueba?
        - Que la API responde correctamente
        - Que lee el archivo de metadata
        - Que devuelve la información del modelo
        """
        client = TestClient(app)
        
        # Hacer petición real
        response = client.get("/model")
        
        # Verificar que responde
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Obtener datos de respuesta
        data = response.json()
        
        # Verificar que tiene las secciones principales
        assert "model_info" in data, "Response should contain 'model_info' section"
        assert "performance" in data, "Response should contain 'performance' section"
        assert "usage" in data, "Response should contain 'usage' section"
        
        # Verificar campos en model_info
        model_info = data["model_info"]
        assert "algorithm" in model_info, "Model info should contain 'algorithm'"
        assert "accuracy" in model_info, "Model info should contain 'accuracy'"
        assert "version" in model_info, "Model info should contain 'version'"
        
        # Verificar campos en performance
        performance = data["performance"]
        assert "accuracy" in performance, "Performance should contain 'accuracy'"
        assert "features" in performance, "Performance should contain 'features'"
        assert "classes" in performance, "Performance should contain 'classes'"
        
        # Verificar campos en usage
        usage = data["usage"]
        assert "class_names" in usage, "Usage should contain 'class_names'"
        assert "input_shape" in usage, "Usage should contain 'input_shape'"
        
        # Verificar valores específicos
        assert performance["features"] == 54, f"Expected 54 features, got {performance['features']}"
        assert performance["classes"] == 7, f"Expected 7 classes, got {performance['classes']}"
        assert performance["accuracy"] > 0.9, f"Expected accuracy > 0.9, got {performance['accuracy']}"
        assert len(usage["class_names"]) == 7, f"Expected 7 class names, got {len(usage['class_names'])}"
        
        print("✅ Model info test PASSED - Model information is correct!")
    
    def test_model_info_structure(self):
        """
        Test de la estructura completa de respuesta del modelo
        """
        client = TestClient(app)
        response = client.get("/model")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar secciones principales
        expected_sections = ["model_info", "performance", "parameters", "preprocessing", "usage", "files"]
        
        for section in expected_sections:
            assert section in data, f"Missing section: {section}"
        
        # Verificar campos en model_info
        model_info_fields = ["name", "version", "algorithm", "accuracy", "created_date", "description"]
        for field in model_info_fields:
            assert field in data["model_info"], f"Missing field in model_info: {field}"
        
        # Verificar campos en performance
        performance_fields = ["accuracy", "accuracy_percentage", "dataset_size", "features", "classes", "training_time_minutes"]
        for field in performance_fields:
            assert field in data["performance"], f"Missing field in performance: {field}"
        
        # Verificar que las clases son las esperadas
        expected_classes = [
            "Spruce/Fir", "Lodgepole Pine", "Ponderosa Pine", 
            "Cottonwood/Willow", "Aspen", "Douglas-fir", "Krummholz"
        ]
        
        class_names = data["usage"]["class_names"]
        for expected_class in expected_classes:
            assert expected_class in class_names, f"Missing class: {expected_class}"
        
        print("✅ Model structure test PASSED - All fields and classes are present!")
    
    def test_model_info_values(self):
        """
        Test de los valores específicos del modelo
        """
        client = TestClient(app)
        response = client.get("/model")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar rangos de valores en performance
        performance = data["performance"]
        assert 0 <= performance["accuracy"] <= 1, f"Accuracy should be between 0 and 1, got {performance['accuracy']}"
        assert performance["features"] == 54, f"Features should be 54, got {performance['features']}"
        assert performance["classes"] == 7, f"Classes should be 7, got {performance['classes']}"
        assert performance["dataset_size"] > 0, f"Dataset size should be > 0, got {performance['dataset_size']}"
        
        # Verificar que la accuracy es alta (requisito del proyecto)
        assert performance["accuracy"] > 0.9, f"Accuracy should be > 90%, got {performance['accuracy']*100:.2f}%"
        
        # Verificar parámetros del modelo
        parameters = data["parameters"]
        assert parameters["learning_rate"] > 0, f"Learning rate should be > 0, got {parameters['learning_rate']}"
        assert parameters["max_depth"] > 0, f"Max depth should be > 0, got {parameters['max_depth']}"
        assert parameters["n_estimators"] > 0, f"N estimators should be > 0, got {parameters['n_estimators']}"
        
        print("✅ Model values test PASSED - All values are within expected ranges!")
