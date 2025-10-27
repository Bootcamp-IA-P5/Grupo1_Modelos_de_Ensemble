# 🔍 Data Drift Monitoring

## 📋 Descripción

Sistema simple para detectar **Data Drift** (cambios en la distribución de datos) en el sistema de predicción de riesgo de incendios.

## 🎯 ¿Qué es Data Drift?

**Data Drift** ocurre cuando los datos de entrada cambian significativamente con el tiempo, lo que puede hacer que nuestro modelo no funcione correctamente.

### Ejemplo:
- **Entrenamos** el modelo con datos de 2020-2023
- **En producción** llegan datos de 2024
- **Si los datos de 2024 son muy diferentes** → **DRIFT DETECTADO** ⚠️

## 🚀 Endpoints Disponibles

### 1. Establecer Baseline (Datos de Referencia)

```bash
POST /drift/baseline
```

**Body:**
```json
{
  "baseline_data": [
    [2500, 180, 15, 200, 50, 1000, 220, 230, 140, 500, ...],
    [2600, 190, 16, 210, 55, 1100, 225, 235, 145, 510, ...]
  ]
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Baseline establecido correctamente"
}
```

### 2. Verificar Drift en Datos Nuevos

```bash
POST /drift/check
```

**Body:**
```json
{
  "features": [
    [2550, 185, 15, 205, 52, 1050, 222, 232, 142, 505, ...]
  ]
}
```

**Respuesta:**
```json
{
  "timestamp": "2025-10-26T18:19:08.885366",
  "has_drift": false,
  "max_difference": 0.05,
  "threshold": 0.1,
  "baseline_samples": 3,
  "new_samples": 1,
  "drift_severity": "LOW"
}
```

**Campos:**
- `has_drift`: `true` si hay drift, `false` si no
- `max_difference`: Diferencia máxima detectada (0.05 = 5%)
- `threshold`: Umbral configurado (0.1 = 10%)
- `drift_severity`: `LOW`, `MEDIUM`, o `HIGH`

### 3. Obtener Historial de Drift

```bash
GET /drift/history
```

**Respuesta:**
```json
{
  "history": [
    {
      "timestamp": "2025-10-26T18:19:08.885366",
      "has_drift": false,
      "max_difference": 0.05,
      ...
    },
    ...
  ]
}
```

### 4. Estado del Detector

```bash
GET /drift/status
```

**Respuesta:**
```json
{
  "has_baseline": true,
  "baseline_samples": 3,
  "total_detections": 2,
  "latest_drift": {...},
  "threshold": 0.1
}
```

## 📊 Cómo Funciona

### Lógica Simple:

1. **Estableces datos de referencia** (baseline) con datos de entrenamiento
2. **Comparas datos nuevos** con el baseline
3. **Si la diferencia es > 10%** → DRIFT DETECTADO
4. **Se guarda en MongoDB** para análisis posterior

### Métrica de Drift:

```python
# Compara promedios de features
baseline_mean = promedio_de_datos_entrenamiento
new_mean = promedio_de_datos_nuevos
diferencia = |new_mean - baseline_mean| / |baseline_mean|

# Si diferencia > 10% → DRIFT
```

## 💾 Persistencia en MongoDB

Las detecciones de drift se guardan automáticamente en MongoDB:

- **Colección:** `drift_detections`
- **Datos:** Cada detección con timestamp, diferencias, severidad
- **Fallback:** Si MongoDB no está disponible, se usa memoria

## 🎯 Casos de Uso

### 1. Monitoreo Continuo

Ejecutar cada vez que se hace una predicción para detectar cambios en tiempo real.

### 2. Alertas Automáticas

Configurar alertas cuando `has_drift: true` y `severity: "HIGH"`.

### 3. Análisis de Tendencias

Revisar el historial para entender cómo cambian los datos con el tiempo.

## 🔧 Configuración

### Umbral (Threshold)

Por defecto es `0.1` (10% de diferencia).

Para cambiar:
```python
drift_detector = DriftDetector(threshold=0.15)  # 15%
```

## 📈 Interpretación de Resultados

### `drift_severity: "LOW"`
- Diferencia < 10%
- Normal, no requiere acción

### `drift_severity: "MEDIUM"`
- Diferencia 10-20%
- Monitorear de cerca

### `drift_severity: "HIGH"`
- Diferencia > 20%
- **REENTRENAR MODELO** ⚠️

## 🚨 ¿Qué Hacer cuando Detectamos Drift?

1. **Analizar** el historial de drift
2. **Revisar** qué features cambiaron
3. **Decidir:**
   - Si el cambio es esperado → Continuar
   - Si el cambio es significativo → **Reentrenar modelo**
4. **Reentrenar** con nuevos datos
5. **Actualizar** el baseline

## 📝 Ejemplo Completo

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Establecer baseline
baseline = {
    "baseline_data": [[2500, 180, 15, 200, 50, 1000, 220, 230, 140, 500] + [0]*44]
}
requests.post(f"{BASE_URL}/drift/baseline", json=baseline)

# 2. Verificar drift en datos nuevos
new_data = {
    "features": [[5000, 300, 30, 400, 100, 2000, 240, 250, 160, 1000] + [0]*44]
}
result = requests.post(f"{BASE_URL}/drift/check", json=new_data)

if result.json()["has_drift"]:
    print("⚠️ DRIFT DETECTADO!")
    print(f"Severidad: {result.json()['drift_severity']}")
    print("👉 Considerar reentrenar el modelo")
```

## 🔗 Integración con A/B Testing

El Data Drift puede usarse junto con A/B Testing:

1. **Detectas drift** → Los datos cambian
2. **A/B testing** → Comparar modelos con nuevos datos
3. **Reemplazo automático** → Cambiar al mejor modelo

## 📚 Archivos Relacionados

- `src/api/services/drift_detector.py` - Lógica de detección
- `src/api/routes/drift.py` - Endpoints REST
- `docs/` - Documentación del proyecto

## ✅ Estado del Sistema

**Nivel Experto - Data Drift Monitoring:** ✅ **COMPLETO**

- ✅ Detección automática de drift
- ✅ Alertas configurables
- ✅ Historial persistente en MongoDB
- ✅ Dashboard de monitoreo
- ✅ Integración con predicciones

