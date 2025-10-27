# 📊 Diagrama ER - FireRiskAI Database

## 🗄️ Base de Datos: MongoDB Atlas

### **Base de Datos**: `ensemble_models`

---

## 📋 Colecciones

### **1. Colección: `predictions`**
Almacena todas las predicciones realizadas por el modelo.

#### Campos:
```javascript
{
  _id: ObjectId,                    // ID único generado por MongoDB
  timestamp: DateTime,              // Fecha y hora de la predicción
  features: Array[54],              // Features normalizadas usadas
  prediction: Number,                // Clase predicha (0-6)
  class_name: String,               // Nombre de la clase (e.g., "Lodgepole Pine")
  confidence: Number,               // Confianza de la predicción (0-1)
  risk_level: String,               // Nivel de riesgo: "LOW", "MEDIUM", "HIGH"
  risk_score: Number,               // Score de riesgo (1-10)
  processing_time_ms: Number,       // Tiempo de procesamiento en milisegundos
  model_version: String,             // Versión del modelo usado
  user_id: String                   // ID del usuario (opcional)
}
```

#### Índices:
- `timestamp`: Para búsquedas por fecha
- `prediction`: Para búsquedas por clase
- `risk_level`: Para filtros por nivel de riesgo

---

### **2. Colección: `feedback`**
Almacena el feedback de los usuarios sobre las predicciones.

#### Campos:
```javascript
{
  _id: ObjectId,                    // ID único generado por MongoDB
  prediction_id: String,            // Referencia a prediction_id
  feedback_type: String,             // "positive" o "negative"
  rating: Number,                   // Rating (1-5)
  comment: String,                  // Comentario del usuario
  user_id: String,                  // ID del usuario
  timestamp: DateTime,              // Fecha y hora del feedback
  is_validated: Boolean             // Si el feedback es válido
}
```

#### Índices:
- `prediction_id`: Para conectar con predictions
- `timestamp`: Para búsquedas por fecha
- `feedback_type`: Para filtrar por tipo de feedback

---

### **3. Colección: `metrics`**
Almacena métricas agregadas del rendimiento del modelo.

#### Campos:
```javascript
{
  _id: ObjectId,                    // ID único generado por MongoDB
  timestamp: DateTime,              // Fecha y hora de la métrica
  total_predictions: Number,         // Total de predicciones
  accuracy: Number,                 // Accuracy del modelo
  avg_confidence: Number,           // Confianza promedio
  predictions_by_class: Object,     // {class_0: count, class_1: count, ...}
  avg_processing_time: Number,      // Tiempo promedio de procesamiento
  feedback_accuracy: Number         // Accuracy basada en feedback
}
```

#### Índices:
- `timestamp`: Para búsquedas por fecha

---

### **4. Colección: `drift_detections`**
Almacena detecciones de Data Drift.

#### Campos:
```javascript
{
  _id: ObjectId,                    // ID único generado por MongoDB
  timestamp: DateTime,              // Fecha y hora de la detección
  has_drift: Boolean,               // Si se detectó drift
  max_difference: Number,           // Máxima diferencia encontrada
  threshold: Number,                 // Umbral usado (0.1 = 10%)
  baseline_samples: Number,         // Número de muestras en baseline
  new_samples: Number,              // Número de muestras nuevas
  drift_severity: String            // "LOW", "MEDIUM", "HIGH"
}
```

#### Índices:
- `timestamp`: Para búsquedas por fecha
- `has_drift`: Para filtrar detecciones activas
- `drift_severity`: Para alertas por severidad

---

## 🔗 Relaciones

```
predictions (1) ──────── (N) feedback
     │                          │
     │                          │
     └──────────┬────────────────┘
                │
                ▼
            metrics (agregación)
            
drift_detections (independiente)
```

### **Descripción de Relaciones:**

1. **predictions ↔ feedback (1:N)**
   - Una predicción puede tener múltiples feedbacks
   - Relación referenciada por `prediction_id`
   - Feedback es opcional (no todas las predicciones tienen feedback)

2. **predictions → metrics**
   - Las métricas se calculan agregando datos de `predictions`
   - Se actualiza periódicamente (no es una relación estricta)

3. **drift_detections**
   - Independiente de las otras colecciones
   - Se actualiza cuando se detecta drift en los datos

---

## 📈 Diagrama Visual

```
┌─────────────────────────────────────────────────────────┐
│                   MONGODB ATLAS                        │
│              Base de Datos: ensemble_models             │
└─────────────────────────────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        ┌───────────┐   ┌───────────┐   ┌───────────┐
        │predictions│──▶│ feedback  │   │  metrics  │
        └───────────┘   └───────────┘   └───────────┘
                │              │              │
                │              │              │
                └──────────────┼──────────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │drift_detections  │
                      └──────────────────┘
```

---

## 🎯 Casos de Uso

### **1. Guardar una Predicción**
```javascript
// Colección: predictions
{
  timestamp: ISODate("2025-01-20T10:30:00Z"),
  prediction: 1,
  class_name: "Lodgepole Pine",
  confidence: 0.95,
  risk_level: "HIGH",
  risk_score: 8,
  processing_time_ms: 42.5
}
```

### **2. Agregar Feedback a una Predicción**
```javascript
// Colección: feedback
{
  prediction_id: "prediction_123",
  feedback_type: "positive",
  rating: 5,
  comment: "La predicción fue correcta",
  user_id: "user_456",
  timestamp: ISODate("2025-01-20T10:35:00Z"),
  is_validated: true
}
```

### **3. Registrar Detección de Drift**
```javascript
// Colección: drift_detections
{
  timestamp: ISODate("2025-01-20T11:00:00Z"),
  has_drift: true,
  max_difference: 0.15,
  threshold: 0.1,
  baseline_samples: 581012,
  new_samples: 100,
  drift_severity: "MEDIUM"
}
```

---

## 📊 Estadísticas Estimadas

### **Volumen de Datos Esperado:**

- **predictions**: ~10,000-50,000 documentos/mes
- **feedback**: ~1,000-5,000 documentos/mes (10% de predictions)
- **metrics**: ~100-500 documentos/mes (agregación diaria)
- **drift_detections**: ~10-50 documentos/mes (chequeo periódico)

### **Tamaño Estimado:**
- Por documento: ~1-2 KB
- Total: ~100-500 MB (1 año de operación)

---

## 🔧 Configuración en el Código

### **Ejemplo de Uso:**

```python
# Guardar predicción
collection = db_service.get_collection("predictions")
await collection.insert_one(prediction_data)

# Guardar feedback
collection = db_service.get_collection("feedback")
await collection.insert_one(feedback_data)

# Guardar detección de drift
collection = db_service.get_collection("drift_detections")
await collection.insert_one(drift_data)
```

---

## ✅ Ventajas de esta Estructura

1. **Flexibilidad**: MongoDB permite agregar campos sin alterar el esquema
2. **Escalabilidad**: Índices optimizan consultas frecuentes
3. **Separación de Concerns**: Cada colección tiene un propósito claro
4. **Relaciones Lógicas**: Feedback vinculado a predictions por ID
5. **Monitoreo**: Drift detection independiente para alertas

---

**© 2025 Grupo 1 - FireRiskAI**

