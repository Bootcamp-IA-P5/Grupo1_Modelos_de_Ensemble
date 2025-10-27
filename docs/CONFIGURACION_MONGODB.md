# 🔧 Configuración de MongoDB para el Proyecto

## 📋 Pasos para Configurar MongoDB

### **1. Acceder a MongoDB Atlas**

1. Ve a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Inicia sesión con las credenciales del equipo
3. Accede al cluster `Cluster0`

### **2. Obtener la Connection String**

#### **Opción A: Usar el Connection String Existente**

Si ya existe un usuario configurado, solo necesitas la contraseña:

1. Ve a **Database Access** → Busca usuario `barbdeveloper11_db_user`
2. Si necesitas resetear la contraseña, haz clic en "Edit" → "Edit Password"

#### **Opción B: Crear un Nuevo Usuario para tu Compañero**

1. Ve a **Database Access** → "Add New Database User"
2. Crea un usuario nuevo (ej: `developer2`)
3. Genera una contraseña segura
4. Ve a **Network Access** → "Add IP Address" → "Allow Access from Anywhere" (0.0.0.0/0)
5. Ve a **Database** → "Connect" → "Connect your application"
6. Copia el connection string

### **3. Configurar el Archivo `.env` Local**

#### **Para el Compañero de Equipo:**

```bash
# En el directorio del proyecto
cp env.example .env
```

Luego editar `.env`:

```env
# Base de datos MongoDB
MONGO_URI=mongodb+srv://barbdeveloper11_db_user:TU_PASSWORD_AQUI@cluster0.n7u5rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DB_NAME=ensemble_models

# Aplicación
APP_PORT=8000
APP_HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO

# APIs Externas
WEATHER_API_KEY=tu_api_key_de_weatherapi
```

### **4. Verificar la Conexión**

```bash
# En la raíz del proyecto
python -c "from src.api.services.database import db_service; import asyncio; asyncio.run(db_service.connect()); print('✅ Conexión exitosa')"
```

O usar el script de prueba:

```bash
python test_mongo_simple.py
```

### **5. Problemas Comunes**

#### **Error: "authentication failed"**
- Verifica que la contraseña en `.env` sea correcta
- Asegúrate de reemplazar caracteres especiales con URL encoding:
  - `@` → `%40`
  - `:` → `%3A`
  - `/` → `%2F`

#### **Error: "connection timeout"**
- Verifica que tu IP esté en la whitelist de MongoDB Atlas
- Ve a **Network Access** → "Add IP Address" → "Allow Access from Anywhere"

#### **Error: "SSL handshake failed" (Windows)**
- El sistema ya está configurado para Windows
- Verifica que `database.py` use la configuración SSL correcta
- Ejecuta: `python test_mongo_universal.py`

### **6. Compartir Credenciales de Forma Segura**

**NO hacer:**
- ❌ Subir `.env` a GitHub
- ❌ Compartir credenciales por WhatsApp/Slack

**SÍ hacer:**
- ✅ Usar variables de entorno del equipo
- ✅ Compartir credenciales por método seguro (1Password, etc.)
- ✅ Cada miembro tiene su propia contraseña

---

## 🔐 Acceso a MongoDB Atlas

### **Credenciales del Equipo:**

**Cluster:** Cluster0
**Base de datos:** ensemble_models
**Usuario:** barbdeveloper11_db_user
**Contraseña:** [Compartir de forma segura]

### **URL de Conexión:**

```
mongodb+srv://barbdeveloper11_db_user:<password>@cluster0.n7u5rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

**Nota:** Reemplazar `<password>` con la contraseña real.

---

## 📊 Colecciones en MongoDB

### **1. predictions**
Almacena todas las predicciones del modelo.

### **2. feedback**
Almacena feedback de usuarios sobre predicciones.

### **3. metrics**
Almacena métricas agregadas del modelo.

### **4. drift_detections**
Almacena detecciones de drift en datos.

Ver diagrama completo en: `docs/diagramas/database_schema.md`

---

## 🧪 Verificar que MongoDB Funciona

### **1. Desde Python:**

```python
from src.api.services.database import db_service
import asyncio

async def test():
    await db_service.connect()
    if db_service.database:
        print("✅ MongoDB conectado")
        collection = db_service.get_collection("predictions")
        count = await collection.count_documents({})
        print(f"📊 Total predicciones: {count}")
    else:
        print("❌ Error conectando")

asyncio.run(test())
```

### **2. Desde la API:**

```bash
# Iniciar servidor
python -m uvicorn app:app --reload

# En otra terminal
curl http://localhost:8000/health
```

### **3. Desde Streamlit:**

```bash
streamlit run streamlit_dashboard.py
```

Ve a la página "Inicio" → Debería mostrar "✅ Backend conectado y funcionando"

---

## 🆘 Solución de Problemas

### **Problema: No puede conectar desde su máquina**

1. Verificar que `.env` existe y tiene `MONGO_URI` correcto
2. Verificar que su IP está en la whitelist de MongoDB Atlas
3. Verificar firewall de Windows/Mac
4. Probar con `test_mongo_universal.py`

### **Problema: "Module not found: motor"**

```bash
pip install -r requirements.txt
```

### **Problema: "connection refused"**

Verificar que MongoDB Atlas esté activo:
1. Ve a MongoDB Atlas dashboard
2. Verifica que el cluster esté "Active"
3. Si está pausado, despiértalo

---

## 📝 Checklist de Configuración

- [ ] Crear archivo `.env` desde `env.example`
- [ ] Obtener contraseña de MongoDB Atlas
- [ ] Configurar `MONGO_URI` en `.env`
- [ ] Verificar IP en whitelist de MongoDB
- [ ] Probar conexión con script de prueba
- [ ] Verificar que se pueden insertar datos
- [ ] Verificar que se pueden leer datos

---

**© 2025 Grupo 1 - FireRiskAI**

