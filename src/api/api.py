"""
API simple para desarrollo inicial
"""

from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear aplicación FastAPI
app = FastAPI(title="ML Project API", version="1.0.0")

# Configuración de MongoDB
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('MONGODB_DATABASE', 'grupo1_modelos_de_ensemble')

# Cliente de MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {"message": "API funcionando", "status": "ok"}

@app.get("/health")
async def health():
    """Verificar estado"""
    try:
        client.admin.command('ping')
        return {"status": "healthy", "mongodb": "connected"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
