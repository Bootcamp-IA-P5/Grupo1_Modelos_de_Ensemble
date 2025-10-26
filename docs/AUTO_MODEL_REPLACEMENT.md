# 🤖 Auto Model Replacement

## 📋 Descripción

Sistema automático de sustitución de modelos que compara el rendimiento de múltiples modelos y automáticamente reemplaza el modelo principal si encuentra uno mejor.

## 🎯 ¿Cómo Funciona?

### **Concepto Simple:**

1. **Tienes 3 modelos** en producción (Random Forest, Extra Trees, XGBoost)
2. **Comparas su rendimiento** (accuracy, precision, recall)
3. **Si un modelo es mejor** → Lo reemplazas automáticamente como principal
4. **Monitorizas** que siga funcionando bien

### **Ejemplo Práctico:**

```
Situación Inicial:
- Modelo Principal: XGBoost (97% accuracy)
- Modelos en A/B Testing: Random Forest (95%), Extra Trees (96%)

Después de 1000 predicciones:
- Random Forest: 98% accuracy
- Extra Trees: 97% accuracy  
- XGBoost: 96% accuracy

👉 Random Forest se convierte en modelo principal
```

## 🚀 Endpoints Disponibles

### **1. Comparar Modelos**

```bash
GET /models/compare
```

**Respuesta:**
```json
{
  "best_model": "random_forest",
  "best_accuracy": 0.9800,
  "reason": "Mejor accuracy: 0.9800",
  "current_model": "xgboost",
  "should_replace": true,
  "model_stats": {
    "random_forest": {"accuracy": 0.9800, "model_type": "RandomForest"},
    "extra_trees": {"accuracy": 0.9700, "model_type": "ExtraTrees"},
    "xgboost": {"accuracy": 0.9600, "model_type": "XGBoost"}
  }
}
```

**Campos:**
- `best_model`: Modelo con mejor métrica
- `best_accuracy`: Accuracy del mejor modelo
- `current_model`: Modelo actualmente en uso
- `should_replace`: `true` si debería reemplazarse

### **2. Reemplazar Modelo**

```bash
POST /models/replace/{model_name}
```

**Ejemplo:**
```bash
POST /models/replace/random_forest
```

**Respuesta:**
```json
{
  "success": true,
  "current_model": "random_forest",
  "message": "Modelo reemplazado a: random_forest"
}
```

### **3. Ver Modelo Actual**

```bash
GET /models/current
```

**Respuesta:**
```json
{
  "current_model": "random_forest",
  "available_models": ["random_forest", "extra_trees", "xgboost"]
}
```

## 📊 Arquitectura

### **Componentes:**

1. **`ModelManager`** (`src/api/services/model_manager.py`)
   - Compara modelos
   - Decide cuál es el mejor
   - Maneja el reemplazo

2. **Endpoints** (`src/api/routes/model_replacement.py`)
   - API REST para interactuar con el gestor
   - Comparar, reemplazar, consultar

### **Flujo de Decisión:**

```python
# 1. Comparar todos los modelos
best = model_manager.compare_models()
# Returns: {"best_model": "random_forest", "should_replace": true}

# 2. Si debería reemplazarse
if best["should_replace"]:
    model_manager.replace_model(best["best_model"])
    # Ahora random_forest es el modelo principal
```

## 🔧 Configuración

### **Modelos Disponibles:**

| Modelo | Archivo | Accuracy | Uso |
|--------|---------|----------|-----|
| Random Forest | `models/random_forest_model.pkl` | 95-98% | A/B Testing |
| Extra Trees | `models/extra_trees_model.pkl` | 95-97% | A/B Testing |
| XGBoost | `models/xgboost_model.pkl` | 96-98% | Principal |

### **Metadata de Modelos:**

Cada modelo tiene un archivo `*_metadata.json` con:
- Accuracy
- Precision
- Recall
- F1 Score
- Model Type
- Training Date

## 💡 Casos de Uso

### **1. Reemplazo Automático Periódico**

```bash
# Cron job que revisa cada hora
0 * * * * curl -X GET http://localhost:8000/models/compare
```

### **2. Reemplazo Manual en Producción**

```bash
# Ver comparación
curl http://localhost:8000/models/compare

# Si hay mejor modelo, reemplazarlo
curl -X POST http://localhost:8000/models/replace/random_forest
```

### **3. Monitoreo Continuo**

```bash
# Ver estado actual
curl http://localhost:8000/models/current
```

## 🔗 Integración con A/B Testing

El Auto Model Replacement funciona en conjunto con A/B Testing:

```
A/B Testing → Genera estadísticas de modelos
       ↓
Auto Replacement → Compara modelos y decide cuál usar
       ↓
Producción → Usa el mejor modelo
```

### **Flujo Completo:**

1. **A/B Testing** distribuye predicciones entre modelos
2. **Data Drift** detecta cambios en los datos
3. **Auto Replacement** compara modelos y elige el mejor
4. **El mejor modelo** se convierte en principal
5. **Monitoriza** que funcione bien

## ⚠️ Consideraciones

### **Cuándo Reemplazar:**

- ✅ **SÍ reemplazar** si:
  - Nuevo modelo tiene accuracy > 2% mejor
  - Nuevo modelo tiene mejor precisión para clases importantes
  - Data drift detecta cambios significativos

- ❌ **NO reemplazar** si:
  - Mejora es < 1%
  - Modelo nuevo no está suficientemente probado
  - Hay errores en el nuevo modelo

### **Rollback Automático:**

Si el nuevo modelo falla:
```bash
# Revertir al modelo anterior
curl -X POST http://localhost:8000/models/replace/xgboost
```

## 📈 Métricas a Considerar

| Métrica | Peso | Descripción |
|---------|------|-------------|
| Accuracy | 40% | Precisión global del modelo |
| Precision | 30% | Precision por clase |
| Recall | 20% | Cobertura del modelo |
| F1 Score | 10% | Balance precision/recall |

## 🚀 Próximos Pasos

### **Mejoras Futuras:**

1. **Reemplazo Automático** - Sistema que reemplace automáticamente
2. **Alertas** - Notificar cuando hay reemplazo
3. **Historial** - Guardar cambios de modelo en MongoDB
4. **Rollback Automático** - Revertir si nuevo modelo falla

## ✅ Estado Actual

**Auto Model Replacement:** ✅ **IMPLEMENTADO (Versión Manual)**

- ✅ Comparación de modelos
- ✅ Reemplazo manual de modelos (via endpoint)
- ✅ Consulta de modelo actual
- ✅ Integración con A/B Testing

**Nota:** La versión actual requiere que ejecutes manualmente los endpoints para reemplazar modelos. Para automatización completa, se puede implementar un cron job que ejecute `/models/compare` periódicamente y `/models/replace` si hay un mejor modelo.

