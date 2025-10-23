"""
Test REAL para el endpoint de health
EcoPrint AI - Sistema de Predicción de Riesgo de Incendios Forestales
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestHealthReal:
    """Test REAL para el endpoint GET /health"""
    
    def test_health_check_real(self):
        """
        Test REAL del health check
        
        ¿Qué prueba?
        - Que la API responde
        - Que el endpoint /health funciona
        - Que devuelve la estructura correcta
        """
        # Crear cliente de prueba
        client = TestClient(app)
        
        # Hacer petición real
        response = client.get("/health")
        
        # Verificar que responde
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Obtener datos de respuesta
        data = response.json()
        
        # Verificar estructura básica
        assert "status" in data, "Response should contain 'status' field"
        assert "service" in data, "Response should contain 'service' field"
        
        # Verificar valores
        assert data["status"] == "ok", f"Expected 'ok', got '{data['status']}'"
        assert data["service"] == "FireRiskAI", f"Expected 'FireRiskAI', got '{data['service']}'"
        
        print("✅ Health check test PASSED - API is working!")
    
    def test_health_check_structure(self):
        """
        Test de la estructura de respuesta del health check
        """
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que tiene los campos esperados
        expected_fields = ["status", "service"]
        for field in expected_fields:
            assert field in data, f"Missing field: {field}"
        
        # Verificar tipos de datos
        assert isinstance(data["status"], str), "Status should be a string"
        assert isinstance(data["service"], str), "Service should be a string"
        
        print("✅ Health check structure test PASSED - Response format is correct!")
