import os
import gzip
import shutil
import pandas as pd
from pymongo import MongoClient

# === 1️⃣ Configuración de rutas ===
BASE_DIR = r"../Cover_type_Dataset"
GZ_FILE = os.path.join(BASE_DIR, "covtype.data.gz")
CSV_FILE = os.path.join(BASE_DIR, "covtype.csv")

# === 2️⃣ Descomprimir el archivo .gz ===
if not os.path.exists(CSV_FILE):
    print("Descomprimiendo archivo .gz ...")
    with gzip.open(GZ_FILE, "rb") as f_in:
        with open(CSV_FILE, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"✅ Archivo descomprimido en: {CSV_FILE}")
else:
    print(f"⚠️ Archivo ya descomprimido: {CSV_FILE}")

# === 3️⃣ Leer y añadir cabeceras ===
print("Cargando dataset y asignando cabeceras...")

columns = [
    "Elevation","Aspect","Slope","Horizontal_Distance_To_Hydrology",
    "Vertical_Distance_To_Hydrology","Horizontal_Distance_To_Roadways",
    "Hillshade_9am","Hillshade_Noon","Hillshade_3pm",
    "Horizontal_Distance_To_Fire_Points","Wilderness_Area1","Wilderness_Area2",
    "Wilderness_Area3","Wilderness_Area4","Soil_Type1","Soil_Type2","Soil_Type3",
    "Soil_Type4","Soil_Type5","Soil_Type6","Soil_Type7","Soil_Type8","Soil_Type9",
    "Soil_Type10","Soil_Type11","Soil_Type12","Soil_Type13","Soil_Type14",
    "Soil_Type15","Soil_Type16","Soil_Type17","Soil_Type18","Soil_Type19",
    "Soil_Type20","Soil_Type21","Soil_Type22","Soil_Type23","Soil_Type24",
    "Soil_Type25","Soil_Type26","Soil_Type27","Soil_Type28","Soil_Type29",
    "Soil_Type30","Soil_Type31","Soil_Type32","Soil_Type33","Soil_Type34",
    "Soil_Type35","Soil_Type36","Soil_Type37","Soil_Type38","Soil_Type39",
    "Soil_Type40","Cover_Type"
]

df = pd.read_csv(CSV_FILE, header=None, names=columns)
print(f"✅ Dataset cargado: {len(df):,} filas")

# === 4️⃣ Insertar en MongoDB ===
print("Conectando a MongoDB local...")
client = MongoClient("mongodb://localhost:27017/")
db = client["fireriskai_db"]
collection = db["forest_data"]

print("Insertando documentos (puede tardar unos minutos)...")
data = df.to_dict("records")
collection.insert_many(data)
print(f"✅ Insertados {len(data):,} documentos en fireriskai_db.forest_data")

# === 5️⃣ Verificar ===
doc = collection.find_one()
print("\nEjemplo de documento insertado:")
print(doc)

print("\n🚀 Base de datos 'fireriskai_db' creada correctamente en MongoDB local.")
