# 🪟 Instrucciones para Ver la Base de Datos en Windows

## ⚠️ Problema Común en Windows

En Windows, es común tener problemas con certificados SSL al conectar a MongoDB Atlas. El código **ya está configurado** para manejar esto automáticamente.

## 🔍 Cómo Verificar que MongoDB Funciona

### **1. Verificar que el Backend está Funcionando**

Primero, inicia el backend:

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

Luego prueba estos endpoints:

### **2. Endpoint de Health (SIN MongoDB)**

```bash
curl http://localhost:8000/health
```

Debería responder:
```json
{"status": "ok"}
```

Si esto funciona, el backend está corriendo ✅

---

### **3. Endpoint que USA MongoDB**

#### **A. Hacer una Predicción (Guarda en MongoDB)**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      2500, 180, 15, 200, 50, 1000, 220, 230, 140, 500,
      1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
      0, 0, 0, 0
    ]
  }'
```

**Si responde con una predicción**, significa que:
- ✅ El modelo funciona
- ✅ La conexión SSL a MongoDB funciona
- ✅ Se guardó en la base de datos

**Si da error de SSL**, significa que necesitas la configuración especial de Windows.

---

#### **B. Ver Predicciones Guardadas (Lee de MongoDB)**

```bash
curl http://localhost:8000/predictions/recent?limit=5
```

**Si responde con predicciones**, significa que:
- ✅ MongoDB está conectado
- ✅ Puede leer la base de datos
- ✅ El SSL funciona correctamente

**Si da error**, ver siguiente sección.

---

## 🔧 Si Da Error de SSL en Windows

### **Opción 1: Verificar Variables de Entorno**

Crea un archivo `.env` en la raíz del proyecto:

```env
MONGO_URI=mongodb+srv://barbdeveloper11_db_user:<TU_PASSWORD>@cluster0.n7u5rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DB_NAME=ensemble_models
APP_PORT=8000
APP_HOST=0.0.0.0
LOG_LEVEL=INFO
```

**IMPORTANTE**: Reemplaza `<TU_PASSWORD>` con tu contraseña real de MongoDB Atlas.

---

### **Opción 2: Ver Logs del Backend**

Cuando inicies el backend, deberías ver estos logs:

```
🔧 DatabaseService inicializado para: ensemble_models en windows
🔌 Conectando a MongoDB Atlas...
✅ Conectado a MongoDB: ensemble_models
```

**Si ves "Error conectando a MongoDB"**, significa que hay un problema con la conexión SSL.

---

### **Opción 3: Probar Conexión Directa**

Puedes probar conectarte directamente a MongoDB desde Python:

```python
# test_mongo.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_connection():
    uri = "mongodb+srv://barbdeveloper11_db_user:<TU_PASSWORD>@cluster0.n7u5rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        # Configuración para Windows
        client = AsyncIOMotorClient(uri, 
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True,
            tlsInsecure=True,
            serverSelectionTimeoutMS=60000
        )
        
        # Probar ping
        await client.admin.command('ping')
        print("✅ Conexión exitosa!")
        
        # Listar bases de datos
        db_list = await client.list_database_names()
        print(f"📊 Bases de datos: {db_list}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

asyncio.run(test_connection())
```

Ejecuta:
```bash
python test_mongo.py
```

---

## 📊 Endpoints que Usan MongoDB

Estos son los endpoints que necesitan MongoDB para funcionar:

1. ✅ `POST /predict` - Guarda predicciones
2. ✅ `GET /predictions/recent` - Lee predicciones guardadas
3. ✅ `POST /feedback` - Guarda feedback
4. ✅ `GET /metrics` - Lee métricas
5. ✅ `GET /feedback/recent` - Lee feedback reciente
6. ✅ `POST /drift/check` - Detecta drift
7. ✅ `GET /drift/history` - Lee historial de drift

---

## 🎯 Prueba Rápida

1. Inicia el backend:
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8000
   ```

2. En otra terminal, haz una predicción:
   ```bash
   curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"features": [2500, 180, 15, 200, 50, 1000, 220, 230, 140, 500, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]}'
   ```

3. Verifica que se guardó:
   ```bash
   curl http://localhost:8000/predictions/recent?limit=1
   ```

**Si ambos funcionan** ✅, MongoDB está conectado correctamente.

---

## 🐛 Si Sigue Fallando

1. Verifica que el archivo `.env` tiene la contraseña correcta
2. Verifica que MongoDB Atlas permite conexiones desde tu IP
3. Revisa los logs del backend para ver el error exacto
4. Contacta a tu compañero de equipo para verificar las credenciales

---

**© 2025 Grupo 1 - FireRiskAI**

