"""
Aplicación principal del proyecto de clasificación multiclase
"""

from src.api.api import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando aplicación de clasificación multiclase...")
    print("📊 API disponible en: http://localhost:8000")
    print("📚 Documentación en: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
