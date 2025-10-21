# 🚀 **EcoPrint AI - Despliegue en Render**

## 📋 **INFORMACIÓN DEL PROYECTO**

**EcoPrint AI** es un sistema de predicción de riesgo de incendios forestales que utiliza modelos de machine learning para clasificar el tipo de vegetación y evaluar el riesgo de incendio.

## 🎯 **CARACTERÍSTICAS**

- ✅ **API Backend** - FastAPI con 7 endpoints
- ✅ **Modelo ML** - XGBoost con 97% accuracy
- ✅ **Base de Datos** - MongoDB Atlas
- ✅ **Dockerizado** - Listo para producción
- ✅ **Tests** - 23 tests unitarios pasando

## 🐳 **DOCKER**

Este proyecto está dockerizado y se despliega automáticamente en Render.

### **Dockerfile:**
- Multi-stage build optimizado
- Python 3.11 slim
- Usuario no-root para seguridad
- Health checks incluidos

### **docker-compose.yml:**
- Configuración para desarrollo y producción
- Variables de entorno
- Volúmenes persistentes

## 🌐 **ENDPOINTS DISPONIBLES**

### **Predicción de Riesgo**
```
POST /predict
Content-Type: application/json
{
  "features": [2000, 180, 15, 300, 50, 1000, 200, 220, 180, 2000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
```

### **Información del Modelo**
```
GET /model/info
```

### **Métricas en Tiempo Real**
```
GET /metrics
```

### **Sistema de Feedback**
```
POST /feedback
GET /feedback
```

### **Health Check**
```
GET /health
GET /database/status
```

### **Documentación API**
```
GET /docs
```

## 🔧 **VARIABLES DE ENTORNO**

### **Requeridas:**
- `MONGO_URI` - URI de conexión a MongoDB Atlas
- `DB_NAME` - Nombre de la base de datos (default: ensemble_models)

### **Opcionales:**
- `PYTHONPATH` - Path de Python (default: /app)
- `PYTHONUNBUFFERED` - Python unbuffered (default: 1)

## 📊 **ESTRUCTURA DE RESPUESTA**

### **Predicción:**
```json
{
  "prediction": 2,
  "class_name": "Ponderosa Pine",
  "confidence": 0.9876,
  "risk_level": "MEDIUM",
  "risk_score": 5,
  "processing_time_ms": 1521.7
}
```

### **Clases de Vegetación:**
- **0**: Spruce/Fir (LOW risk)
- **1**: Lodgepole Pine (HIGH risk)
- **2**: Ponderosa Pine (MEDIUM risk)
- **3**: Cottonwood/Willow (LOW risk)
- **4**: Aspen (MEDIUM risk)
- **5**: Douglas-fir (MEDIUM risk)
- **6**: Krummholz (HIGH risk)

## 🚀 **DESPLIEGUE**

### **Render.com:**
1. Conectar repositorio GitHub
2. Seleccionar branch `feature/dockerization`
3. Configurar variables de entorno
4. Deploy automático

### **Variables de entorno en Render:**
```
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
DB_NAME=ensemble_models
```

## 📈 **MONITOREO**

- **Health Check**: `/health`
- **Database Status**: `/database/status`
- **Métricas**: `/metrics`

## 🧪 **TESTING**

```bash
# Tests unitarios
python -m pytest tests/ -v

# Test de predicción
curl -X POST "https://tu-app.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [2000, 180, 15, 300, 50, 1000, 200, 220, 180, 2000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}'
```

## 📚 **DOCUMENTACIÓN**

- **API Docs**: `/docs` (Swagger UI)
- **Docker**: `docs/DOCKER_DEPLOYMENT.md`
- **Backend**: `docs/BACKEND_API_GUIDE.md`
- **Modelo**: `docs/MODEL_EVALUATION.md`

---

**EcoPrint AI** - Sistema de Predicción de Riesgo de Incendios Forestales 🌲🔥

*Desplegado en Render.com para máxima disponibilidad*
