"""
<<<<<<< HEAD
API del clima - VERSIÓN SIMPLE
Solo obtiene temperatura y humedad
"""

from fastapi import APIRouter, HTTPException
=======
API del clima - VERSIÓN SÚPER SIMPLE
Solo obtiene temperatura y humedad
"""

from fastapi import APIRouter
>>>>>>> feature/external-apis
import requests
import os

router = APIRouter()

<<<<<<< HEAD
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
=======
@router.get("/weather")
def get_weather(lat: float, lon: float):
    """
    Obtener clima por coordenadas
    """
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        return {"error": "WEATHER_API_KEY no configurada"}
    
    try:
        # Weather API (weatherapi.com)
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}&aqi=no"
>>>>>>> feature/external-apis
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
<<<<<<< HEAD
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"]
=======
                "temperature": data["current"]["temp_c"],
                "humidity": data["current"]["humidity"],
                "description": data["current"]["condition"]["text"]
>>>>>>> feature/external-apis
            }
        else:
            return {"error": f"Error API: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
<<<<<<< HEAD

@router.get("/weather")
def weather_endpoint(lat: float, lon: float):
    """
    Endpoint simple para obtener clima
    """
    weather = get_weather(lat, lon)
    return weather
=======
>>>>>>> feature/external-apis
