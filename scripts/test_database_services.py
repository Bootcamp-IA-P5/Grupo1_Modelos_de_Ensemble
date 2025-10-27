import os
import sys
import asyncio
from dotenv import load_dotenv

# ============================================================
#  Ajustar sys.path para poder importar módulos del proyecto
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
print(f"📂 Añadido al sys.path: {BASE_DIR}")

# ============================================================
#  Importaciones de servicios de base de datos
# ============================================================
from src.api.services.database import DatabaseService
from src.api.services.database_universal import DatabaseServiceUniversal


# ============================================================
#  Cargar configuración desde .env
# ============================================================
def load_env_config():
    env_file = ".env"
    if not os.path.exists(env_file):
        print("⚠️ No se encontró archivo .env en el directorio raíz del proyecto.")
    else:
        print(f"🔧 Cargando configuración desde {env_file}")
        load_dotenv(env_file)

    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    environment = os.getenv("ENVIRONMENT", "local").lower()

    print("\n📘 Variables de entorno detectadas:")
    print(f"  🌍 ENVIRONMENT = {environment}")
    print(f"  🔗 MONGO_URI = {mongo_uri}")
    print(f"  🧠 DB_NAME = {db_name}\n")

    return environment


# ============================================================
#  Función principal de pruebas sincrónicas
# ============================================================
def test_sync_service():
    print("🔹 Probando DatabaseService:")
    db_service = DatabaseService()
    db_service.connect()
    db_service.test_connection()


# ============================================================
#  Función principal de pruebas asíncronas (Motor)
# ============================================================
async def test_async_service():
    print("\n" + "=" * 80 + "\n")
    print("🔹 Probando DatabaseServiceUniversal:")
    db_universal = DatabaseServiceUniversal()
    await db_universal.connect()
    await db_universal.test_connection()


# ============================================================
#  Ejecución principal del script
# ============================================================
if __name__ == "__main__":
    print("🚀 Iniciando pruebas de conexión a MongoDB\n")
    environment = load_env_config()

    try:
        # Test sincrónico (pymongo)
        test_sync_service()

        # Test asíncrono (motor)
        asyncio.run(test_async_service())

        print("\n✅ Pruebas completadas correctamente.\n")

    except Exception as e:
        print("\n❌ Error durante las pruebas:")
        print(e)
