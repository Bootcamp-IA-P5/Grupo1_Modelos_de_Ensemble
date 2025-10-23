"""
API del clima - VERSIÓN SIMPLE
Solo obtiene temperatura y humedad
"""

from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

def get_weather(lat: float, lon: float):
    """
    Obtener clima simple
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key or api_key == "test_key_123":
        # Datos mock para pruebas
        return {
            "temperature": 25.5,
            "humidity": 60,
            "description": "clear sky",
            "note": "Datos de prueba - configura API key real para datos reales"
        }
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"]
            }
        else:
            return {"error": f"Error API: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/weather")
def weather_endpoint(lat: float, lon: float):
    """
    Endpoint simple para obtener clima
    """
    weather = get_weather(lat, lon)
    return weather
