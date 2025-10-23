# 🍃 Configuración de MongoDB para EcoPrint

## 📋 Resumen

Este documento explica cómo configurar MongoDB Atlas para el proyecto EcoPrint. MongoDB nos permite almacenar predicciones, feedback de usuarios y métricas del modelo para análisis y mejora continua.

## 🎯 ¿Por qué MongoDB?

### **Problema sin base de datos:**
- ❌ No tenemos memoria de las predicciones hechas
- ❌ No podemos mejorar el modelo con datos reales
- ❌ No podemos detectar cuando el modelo se degrada
- ❌ No podemos hacer análisis de tendencias

### **Solución con MongoDB:**
- ✅ **Almacenar predicciones** para análisis histórico
- ✅ **Recoger feedback** de usuarios para mejorar
- ✅ **Monitorear rendimiento** del modelo en tiempo real
- ✅ **Detectar data drift** cuando los datos cambian
- ✅ **Cumplir requisitos** de nivel avanzado del proyecto

## 🔧 Configuración Paso a Paso

### **Paso 1: Configurar MongoDB Atlas**

1. **Crear cuenta en MongoDB Atlas:**
   - Ve a [MongoDB Atlas](https://cloud.mongodb.com/)
   - Crea una cuenta gratuita

2. **Crear cluster:**
   - Selecciona "Free Tier" (M0)
   - Elige una región cercana
   - Nombre del cluster: `Cluster0`

3. **Configurar acceso a la base de datos:**
   - Ve a "Database Access"
   - Crea un usuario con contraseña
   - Anota el usuario y contraseña

4. **Configurar acceso de red:**
   - Ve a "Network Access"
   - Agrega tu IP o usa `0.0.0.0/0` (menos seguro pero más fácil)

### **Paso 2: Obtener URL de conexión**

1. **Conectar a tu aplicación:**
   - Ve a "Database" → "Connect"
   - Selecciona "Connect your application"
   - Copia la URL de conexión

2. **Formato de la URL:**
   ```
   mongodb+srv://usuario:contraseña@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
   ```

### **Paso 3: Configurar variables de entorno**

1. **Editar archivo `.env`:**
   ```bash
   MONGO_URI=mongodb+srv://tu_usuario:tu_contraseña@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
   DB_NAME=ensemble_models
   ```

2. **Verificar configuración:**
   ```bash
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('MONGO_URI:', os.getenv('MONGO_URI')[:50] + '...')"
   ```

## 🧪 Probar la Conexión

### **Método 1: Endpoint de la API**
```bash
# Verificar estado
curl -X GET "http://localhost:8000/database/status"

# Probar conexión
curl -X POST "http://localhost:8000/database/test-connection"
```

### **Método 2: Python directo**
```python
from src.api.services.database import db_service
import asyncio

async def test():
    success = await db_service.connect()
    print("✅ Conectado" if success else "❌ Error")
    await db_service.disconnect()

asyncio.run(test())
```

## 📊 Estructura de la Base de Datos

### **Base de datos:** `ensemble_models`

### **Colecciones que se crearán:**

1. **`predictions`** - Predicciones del modelo
2. **`feedback`** - Feedback de usuarios
3. **`metrics`** - Métricas del modelo
4. **`data_drift`** - Detección de data drift

## 🚨 Solución de Problemas

### **Error: "authentication failed"**
- ✅ Verifica que el usuario y contraseña sean correctos
- ✅ Asegúrate de que el usuario tenga permisos de lectura/escritura
- ✅ Verifica que no haya espacios extra en la URL

### **Error: "network access denied"**
- ✅ Agrega tu IP a la lista blanca en "Network Access"
- ✅ O usa `0.0.0.0/0` para permitir todas las IPs (menos seguro)

### **Error: "connection timeout"**
- ✅ Verifica tu conexión a internet
- ✅ Asegúrate de que el cluster esté activo
- ✅ Verifica que la URL de conexión sea correcta

## 📈 Próximos Pasos

Una vez que la conexión funcione:

1. **Crear esquemas de datos** - Definir estructura de documentos
2. **Implementar guardado de predicciones** - Almacenar cada predicción
3. **Sistema de feedback** - Permitir que usuarios califiquen predicciones
4. **Monitoreo de métricas** - Seguir rendimiento del modelo

## 🔗 Enlaces Útiles

- [MongoDB Atlas](https://cloud.mongodb.com/)
- [Documentación de Motor (async MongoDB)](https://motor.readthedocs.io/)
- [FastAPI + MongoDB](https://fastapi.tiangolo.com/tutorial/sql-databases/)

---

**EcoPrint** - Sistema de Predicción de Riesgo de Incendios Forestales 🌲🔥
