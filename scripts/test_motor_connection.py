import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

async def test_connection():
    uri = os.getenv("MONGO_URI")
    print(f"🔍 Usando URI: {uri}")

    # Si no hay URI definida, fallar explícitamente
    if not uri:
        raise ValueError("❌ No se ha definido MONGO_URI en el archivo .env")

    try:
        # Crear cliente asíncrono
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)

        # Forzar conexión real con el servidor (esto lanza excepción si no conecta)
        await client.server_info()

        # Acceder a la base concreta (usa el nombre que tengas en tu URI o el tuyo local)
        db = client["fireriskai_db"]

        # Listar colecciones como prueba de lectura
        collections = await db.list_collection_names()

        print("✅ Conectado correctamente a MongoDB")
        print(f"📂 Colecciones disponibles: {collections}")

    except Exception as e:
        print("❌ Error conectando a MongoDB:")
        print(e)

# Ejecutar
if __name__ == "__main__":
    asyncio.run(test_connection())
