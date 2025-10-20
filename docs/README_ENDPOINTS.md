# 🔥 FireRiskAI - Guía de Endpoints API

## 📋 **Endpoints Esenciales (MVP)**

### **1. Health Check**
```http
GET /health
```
**Propósito**: Verificar que la API esté funcionando
**Respuesta**: `{"status": "ok", "service": "FireRiskAI"}`

### **2. Información del Modelo**
```http
GET /model
```
**Propósito**: Obtener metadata del modelo actual
**Respuesta**: Información del modelo, versión, métricas

### **3. Predicción Principal**
```http
POST /predict
```
**Body**:
```json
{
  "features": [2500, 15, 270, 1200, 800, 1, 2, 3, ...]
}
```
**Respuesta**:
```json
{
  "prediction": 1,
  "class_name": "Lodgepole Pine",
  "confidence": 0.92,
  "risk_level": "HIGH",
  "risk_score": 8
}
```

### **4. Métricas de Riesgo**
```http
GET /metrics
```
**Propósito**: Obtener mapeo de tipos de bosque a niveles de riesgo
**Respuesta**: Configuración de riesgo por tipo de bosque

## 🎯 **Endpoints Opcionales (Mejoras)**

### **5. Feedback del Usuario**
```http
POST /feedback
```
**Body**:
```json
{
  "request_id": "abc123",
  "predicted_class": 1,
  "correct_class": 2,
  "notes": "Predicción incorrecta"
}
```

### **6. Métricas de Rendimiento**
```http
POST /metrics
```
**Body**:
```json
{
  "request_id": "abc123",
  "timestamp": "2024-01-15T10:30:00Z",
  "model_version": "v1.0",
  "latency_ms": 150,
  "status": "success",
  "input": {...},
  "output": {...}
}
```

## 🚫 **Endpoints NO Necesarios (Complejidad Innecesaria)**

### **❌ Endpoints Geográficos**
- `POST /predict/geo` - Demasiado complejo para MVP
- `GET /risk-summary` - No aporta valor real

### **❌ Endpoints de Reentrenamiento**
- `POST /model/retrain` - Complejidad MLOps innecesaria
- `GET /model/version` - Ya está en `/model`

### **❌ Endpoints de Historial**
- `GET /history` - No es crítico para MVP
- `GET /feature-importance` - Se puede calcular en frontend

## 🏗️ **Arquitectura Recomendada**

### **Frontend Simple**
```javascript
// Solo necesita estos endpoints:
const api = {
  health: () => fetch('/health'),
  model: () => fetch('/model'),
  predict: (features) => fetch('/predict', { method: 'POST', body: JSON.stringify({features}) }),
  metrics: () => fetch('/metrics')
}
```

### **Backend Mínimo**
```python
# Solo estos endpoints en app.py:
@app.get("/health")
@app.get("/model") 
@app.get("/metrics")
@app.post("/predict")
@app.post("/feedback")  # Opcional
@app.post("/metrics")   # Opcional
```

## 💡 **Ventajas de Esta Simplificación**

1. **Menos complejidad**: Fácil de implementar y mantener
2. **Mejor UX**: El frontend se enfoca en lo esencial
3. **Escalable**: Se pueden añadir endpoints después
4. **Enfoque**: Concentrarse en la predicción, no en features secundarias

## 🎯 **Recomendación Final**

**Implementar solo los 4 endpoints esenciales** para el MVP. Los demás se pueden añadir después si son realmente necesarios.

El frontend React se puede construir perfectamente con solo estos endpoints básicos.
