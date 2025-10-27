# 🧪 A/B Testing System - Guía Completa

## 🎯 **¿QUÉ ES ESTO?**

Este sistema permite probar **3 modelos diferentes** de Machine Learning al mismo tiempo para ver cuál funciona mejor en producción. Es como tener 3 cocineros diferentes preparando el mismo plato y ver cuál lo hace mejor.

## 🤖 **LOS 3 MODELOS:**

| Modelo | Accuracy | Overfitting | Velocidad | Tamaño |
|--------|----------|-------------|-----------|--------|
| **Random Forest** | 88.65% | 2.64% | ~60ms | 512MB |
| **Extra Trees** | 80.78% | 1.10% | ~50ms | 363MB |
| **XGBoost** | 93.30% | 2.09% | ~4ms | 10MB |

## 🚀 **CÓMO USAR EL SISTEMA:**

### **1. HACER UNA PREDICCIÓN (A/B Testing Automático)**
```bash
POST /predict-ab
{
  "features": [2596, 51, 3, 258, 0, 510, ...],  # 54 números
  "user_id": "mi_usuario_123"  # Opcional
}
```

**Respuesta:**
```json
{
  "prediction": 4,
  "class_name": "Aspen",
  "confidence": 0.95,
  "risk_level": "MEDIUM",
  "risk_score": 4,
  "processing_time_ms": 45.8,
  "ab_testing": {
    "model_used": "random_forest",
    "ab_testing_enabled": true
  }
}
```

### **2. VER ESTADÍSTICAS EN TIEMPO REAL**
```bash
GET /ab-testing/stats
```

**Respuesta:**
```json
{
  "success": true,
  "ab_testing_stats": {
    "models_loaded": ["random_forest", "extra_trees", "xgboost"],
    "model_weights": {
      "random_forest": 0.5,    # 50% del tráfico
      "extra_trees": 0.3,      # 30% del tráfico
      "xgboost": 0.2           # 20% del tráfico
    },
    "model_performance": {
      "random_forest": {
        "total_predictions": 10,
        "avg_confidence": 0.95,
        "avg_processing_time": 59.3
      }
    }
  }
}
```

### **3. CAMBIAR DISTRIBUCIÓN DE TRÁFICO**
```bash
POST /ab-testing/weights
{
  "random_forest": 0.6,    # 60% del tráfico
  "extra_trees": 0.2,      # 20% del tráfico
  "xgboost": 0.2           # 20% del tráfico
}
```

### **4. VER MODELOS DISPONIBLES**
```bash
GET /ab-testing/models
```

## 🔧 **CONFIGURACIÓN INICIAL:**

### **1. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### **2. Configurar variables de entorno (.env):**
```env
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
DB_NAME=ensemble_models
WEATHER_API_KEY=tu_api_key_de_weatherapi
```

### **3. Iniciar servidor:**
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 **CÓMO INTERPRETAR LOS RESULTADOS:**

### **Métricas Importantes:**
- **`total_predictions`**: Cuántas veces se usó cada modelo
- **`avg_confidence`**: Confianza promedio (más alto = mejor)
- **`avg_processing_time`**: Velocidad promedio (más bajo = mejor)
- **`predictions_by_class`**: Qué tipos de vegetación predice cada modelo

### **Ejemplo de Análisis:**
```json
"model_performance": {
  "random_forest": {
    "total_predictions": 50,      # Se usó 50 veces
    "avg_confidence": 0.92,       # 92% de confianza promedio
    "avg_processing_time": 45.2,  # 45ms promedio
    "predictions_by_class": {
      "1": 20,  # 20 predicciones de Lodgepole Pine
      "4": 30   # 30 predicciones de Aspen
    }
  }
}
```

## 🎯 **ESTRATEGIAS DE A/B TESTING:**

### **1. Distribución Uniforme (Inicial):**
```json
{
  "random_forest": 0.33,
  "extra_trees": 0.33,
  "xgboost": 0.34
}
```

### **2. Favorito al Mejor Modelo:**
```json
{
  "random_forest": 0.1,
  "extra_trees": 0.1,
  "xgboost": 0.8
}
```

### **3. Test A/B Clásico (50/50):**
```json
{
  "random_forest": 0.5,
  "xgboost": 0.5
}
```

## 🚨 **SOLUCIÓN DE PROBLEMAS:**

### **Error: "Modelo no encontrado"**
- Verificar que los archivos `.pkl` estén en la carpeta `models/`
- Reiniciar el servidor

### **Error: "WEATHER_API_KEY no configurada"**
- Añadir la API key al archivo `.env`
- Reiniciar el servidor

### **Error de conexión a MongoDB**
- Verificar que `MONGO_URI` sea correcta
- Verificar conexión a internet

## 📈 **CASOS DE USO REALES:**

### **1. Comparar Modelos en Producción**
- Usar distribución uniforme inicialmente
- Monitorear métricas por 1 semana
- Ajustar pesos según rendimiento

### **2. Lanzar Nuevo Modelo**
- Empezar con 10% del tráfico
- Aumentar gradualmente si funciona bien
- Reducir si hay problemas

### **3. Optimizar por Velocidad vs Precisión**
- XGBoost: Más rápido, menos preciso
- Random Forest: Más lento, más preciso
- Ajustar según necesidades del negocio

## 🔍 **MONITOREO RECOMENDADO:**

### **Métricas a Revisar Diariamente:**
1. **Tiempo de respuesta promedio** por modelo
2. **Confianza promedio** por modelo
3. **Distribución de predicciones** por clase
4. **Errores** por modelo

### **Alertas a Configurar:**
- Tiempo de respuesta > 100ms
- Confianza promedio < 0.8
- Errores > 5% del tráfico

## 🎉 **¡LISTO PARA USAR!**

El sistema está configurado y funcionando. Solo necesitas:
1. **Configurar las variables de entorno**
2. **Iniciar el servidor**
3. **Hacer predicciones** y **monitorear resultados**

¿Tienes dudas? ¡Pregunta al equipo! 🤝
