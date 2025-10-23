"""
API del clima - VERSIÓN SÚPER SIMPLE
Solo obtiene temperatura y humedad
"""

from fastapi import APIRouter
import requests
import os

router = APIRouter()

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
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": data["current"]["temp_c"],
                "humidity": data["current"]["humidity"],
                "description": data["current"]["condition"]["text"]
            }
        else:
            return {"error": f"Error API: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
