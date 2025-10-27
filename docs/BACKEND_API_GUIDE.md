# 🚀 **EcoPrint AI - Guía Completa del Backend**



**EcoPrint AI** es un sistema de predicción de riesgo de incendios forestales que utiliza modelos de machine learning para clasificar el tipo de vegetación y evaluar el riesgo de incendio. El backend está construido con **FastAPI** y **MongoDB**.

---

## 🎯 **FLUJO PRINCIPAL DE LA APLICACIÓN**

```mermaid
graph TD
    A[Usuario Frontend] --> B[POST /predict]
    B --> C[Modelo ML]
    C --> D[Predicción + Confianza]
    D --> E[Guardar en MongoDB]
    E --> F[Respuesta al Frontend]
    
    G[Usuario Frontend] --> H[POST /feedback]
    H --> I[Validar Feedback]
    I --> J[Guardar en MongoDB]
    J --> K[Actualizar Métricas]
    
    L[Frontend Dashboard] --> M[GET /metrics]
    M --> N[Calcular Métricas en Tiempo Real]
    N --> O[Devolver Dashboard Completo]
```

---

## 🔌 **ENDPOINTS DISPONIBLES**

### **1. 🎯 PREDICCIÓN PRINCIPAL**

#### **`POST /predict`**
**¿Qué hace?** Predice el tipo de vegetación y riesgo de incendio

**Request:**
```json
{
  "features": [2000, 180, 15, 300, 50, 1000, 200, 220, 180, 2000, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "user_id": "usuario123",
  "location": {"lat": 40.7128, "lon": -74.0060}
}
```

**Response:**
```json
{
  "prediction": 1,
  "class_name": "Lodgepole Pine",
  "confidence": 0.95,
  "risk_level": "HIGH",
  "risk_score": 8,
  "processing_time_ms": 45.2
}
```

**¿Qué se guarda automáticamente?**
- ✅ Predicción completa en MongoDB
- ✅ Métricas de rendimiento
- ✅ Tiempo de procesamiento
- ✅ Metadata del usuario

---

### **2. 📊 DASHBOARD DE MÉTRICAS**

#### **`GET /metrics`**
**¿Qué hace?** Devuelve un dashboard completo de métricas en tiempo real

**Response:**
```json
{
  "success": true,
  "timestamp": "2025-10-21T17:53:31.417895",
  "model_performance": {
    "accuracy": 0.9707,
    "precision": 0.968,
    "recall": 0.965,
    "f1_score": 0.966,
    "overfitting": 0.0292,
    "model_type": "XGBoost Ensemble",
    "training_date": "2025-10-21"
  },
  "production_metrics": {
    "total_predictions": 9,
    "successful_predictions": 9,
    "success_rate": 1.0,
    "error_rate": 0.0,
    "average_processing_time_ms": 1264.56
  },
  "confidence_analysis": {
    "average_confidence": 0.775,
    "high_confidence_predictions": 4,
    "low_confidence_predictions": 1,
    "confidence_distribution": {
      "very_high": 3,
      "high": 1,
      "medium": 3,
      "low": 2,
      "very_low": 0
    }
  },
  "data_drift_alerts": [],
  "performance_trends": {
    "last_24h": {"predictions": 9, "period": "24 hours"},
    "last_7d": {"predictions": 9, "period": "7 days"},
    "last_30d": {"predictions": 9, "period": "30 days"}
  },
  "system_health": {
    "database_status": "connected",
    "model_status": "active",
    "last_prediction": "2025-10-21T17:25:05.049000",
    "api_status": "running"
  }
}
```

**¿Cómo usar en el frontend?**
- 📈 **Gráficos de rendimiento**: `model_performance.accuracy`
- 📊 **Estadísticas de uso**: `production_metrics.total_predictions`
- 🎯 **Análisis de confianza**: `confidence_analysis.confidence_distribution`
- ⚠️ **Alertas del sistema**: `data_drift_alerts`
- 📈 **Tendencias**: `performance_trends.last_24h`

---

### **3. 💬 SISTEMA DE FEEDBACK**

#### **`POST /feedback`**
**¿Qué hace?** Permite a los usuarios calificar las predicciones

**Request:**
```json
{
  "prediction_id": "68f7c1f158eb669b80a5df4d",
  "feedback_type": "accuracy",
  "rating": "excellent",
  "comment": "Muy preciso, la predicción fue correcta",
  "user_id": "usuario123"
}
```

**Response:**
```json
{
  "feedback_id": "68f7c4a571bdc2fc4f715737",
  "message": "Feedback enviado correctamente",
  "timestamp": "2025-10-21T17:36:37.993444"
}
```

#### **`GET /feedback`**
**¿Qué hace?** Dashboard completo de feedback

**Response:**
```json
{
  "success": true,
  "feedback_stats": {
    "total_feedback": 2,
    "average_rating": 4.5,
    "rating_distribution": {
      "good": 1,
      "excellent": 1
    },
    "quality_score": 1.0
  },
  "recent_feedback": [
    {
      "_id": "68f7c528233f3214ca2d05b1",
      "prediction_id": "68f7c0b0b3116f4f7e399322",
      "rating": "good",
      "comment": "Útil pero podría ser más rápido",
      "user_id": "usuario_test_002",
      "timestamp": "2025-10-21T17:38:48.388000"
    }
  ],
  "prediction_quality": {
    "total_predictions": 9,
    "high_confidence_predictions": 4,
    "low_confidence_predictions": 1,
    "average_confidence": 0.775
  }
}
```

---

### **4. 🔍 ENDPOINTS DE CONSULTA**

#### **`GET /predictions/recent`**
**¿Qué hace?** Obtiene predicciones recientes

**Query Parameters:**
- `limit` (opcional): Número de predicciones (default: 10)

**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "id": "68f7c1f158eb669b80a5df4d",
      "prediction": 1,
      "class_name": "Lodgepole Pine",
      "confidence": 0.95,
      "risk_level": "HIGH",
      "timestamp": "2025-10-21T17:25:05.049000",
      "user_id": "usuario123"
    }
  ],
  "total": 9
}
```

#### **`GET /database/status`**
**¿Qué hace?** Verifica el estado de la base de datos

**Response:**
```json
{
  "status": "connected",
  "message": "Base de datos conectada correctamente",
  "database": "ensemble_models",
  "collections": ["predictions", "feedback", "test_predictions"],
  "collections_count": 3
}
```

---

## 🗄️ **BASE DE DATOS MONGODB**

### **Colecciones:**

1. **`predictions`** - Predicciones guardadas
2. **`feedback`** - Feedback de usuarios
3. **`test_predictions`** - Predicciones de prueba

### **¿Qué se guarda automáticamente?**
- ✅ **Cada predicción** se guarda en `predictions`
- ✅ **Cada feedback** se guarda en `feedback`
- ✅ **Métricas** se calculan en tiempo real (NO se guardan)

---

## 🎨 **CÓMO USAR EN EL FRONTEND**

### **1. Dashboard Principal**
```javascript
// Obtener métricas completas
const response = await fetch('http://localhost:8000/metrics');
const metrics = await response.json();

// Mostrar en gráficos
const accuracy = metrics.model_performance.accuracy;
const totalPredictions = metrics.production_metrics.total_predictions;
const confidence = metrics.confidence_analysis.confidence_distribution;
```

### **2. Hacer Predicción**
```javascript
// Enviar datos para predicción
const prediction = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    features: [2000, 180, 15, ...], // 54 features
    user_id: 'usuario123',
    location: {lat: 40.7128, lon: -74.0060}
  })
});
```

### **3. Enviar Feedback**
```javascript
// Enviar feedback
const feedback = await fetch('http://localhost:8000/feedback', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    prediction_id: '68f7c1f158eb669b80a5df4d',
    rating: 'excellent',
    comment: 'Muy preciso'
  })
});
```

### **4. Dashboard de Feedback**
```javascript
// Obtener feedback
const feedback = await fetch('http://localhost:8000/feedback');
const feedbackData = await feedback.json();

// Mostrar estadísticas
const totalFeedback = feedbackData.feedback_stats.total_feedback;
const averageRating = feedbackData.feedback_stats.average_rating;
```

---

## 🔧 **CONFIGURACIÓN TÉCNICA**

### **Variables de Entorno (.env):**
```env
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
DB_NAME=ensemble_models
```

### **Puerto:**
- **API**: `http://localhost:8000`
- **Documentación**: `http://localhost:8000/docs`

### **Dependencias Principales:**
- FastAPI
- MongoDB (Motor)
- Scikit-learn
- Pandas/NumPy
- Pydantic

---

## 🚀 **ESTADO ACTUAL DEL PROYECTO**

### **✅ COMPLETADO:**
- ✅ Modelo ML funcional (97.07% accuracy)
- ✅ API REST completa
- ✅ Base de datos MongoDB
- ✅ Sistema de feedback
- ✅ Métricas en tiempo real
- ✅ Validación de datos

### **🔄 EN PROGRESO:**
- 🔄 Tests unitarios
- 🔄 Dockerización
- 🔄 Documentación

### **📋 PENDIENTE:**
- 📋 A/B Testing
- 📋 Data Drift Detection avanzado
- 📋 Despliegue en la nube

---

## 🎯 **PRÓXIMOS PASOS PARA EL FRONTEND**

1. **Crear dashboard principal** con métricas de `/metrics`
2. **Implementar formulario de predicción** con `/predict`
3. **Añadir sistema de feedback** con `/feedback`
4. **Mostrar predicciones recientes** con `/predictions/recent`
5. **Implementar alertas** basadas en `system_health`

---

**EcoPrint AI** - Sistema de Predicción de Riesgo de Incendios Forestales 🌲🔥

*"Datos en tiempo real, predicciones precisas, feedback continuo"*
