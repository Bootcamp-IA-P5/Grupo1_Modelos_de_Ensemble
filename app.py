from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.api.routes import (
    health_router,
    model_router, 
    metrics_router,
    predict_router,
    feedback_router,
    database_router,
    test_storage_router
)
from src.api.routes.weather import router as weather_router
from src.api.routes.predict_with_weather import router as predict_weather_router

# Crear app FastAPI
app = FastAPI(
    title="FireRiskAI API",
    description="API para predicción de riesgo de incendios forestales",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios del front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar variables de entorno
load_dotenv()

# Incluir todas las rutas
app.include_router(health_router)
app.include_router(model_router)
app.include_router(metrics_router)
app.include_router(predict_router)
app.include_router(feedback_router)
app.include_router(database_router)
app.include_router(test_storage_router)
app.include_router(weather_router)
app.include_router(predict_weather_router)