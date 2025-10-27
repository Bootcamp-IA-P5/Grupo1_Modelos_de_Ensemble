import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")
print(f"🔍 Usando URI: {uri}")

if not uri:
    raise ValueError("❌ No se ha definido MONGO_URI en el archivo .env")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    print("👉 Dirección efectiva:", client.address)
    client.server_info()
    db = client["fireriskai_db"]
    print("✅ Conectado correctamente a MongoDB")
    print(f"📂 Colecciones disponibles: {db.list_collection_names()}")
except Exception as e:
    print("❌ Error al conectar con MongoDB:")
    print(e)

