import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "grupo1_modelos_de_ensemble")
MONGODB_COLLECTION_METRICS = os.getenv("MONGODB_COLLECTION_METRICS", "metrics")

# Configuración de archivos
MODEL_PATH = os.path.join("models", "best_model.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")
METADATA_PATH = os.path.join("models", "metadata.json")
RISK_METRICS_PATH = os.path.join("src", "utils", "fire_risk_metrics.json")
