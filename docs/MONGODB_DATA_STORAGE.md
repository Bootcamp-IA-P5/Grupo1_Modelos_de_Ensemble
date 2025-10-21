# 🍃 Sistema de Almacenamiento de Datos - EcoPrint

## 🤔 **¿QUÉ ES ESTO?**

Imagina que EcoPrint es como un **médico digital** que diagnostica el riesgo de incendio forestal. Necesitamos guardar cada "consulta" para poder:
- Ver si el médico funciona bien
- Detectar problemas
- Mejorar el diagnóstico
- **PERO NUNCA** dejar que aprenda de datos falsos

## 📊 **¿QUÉ GUARDAMOS?**

### **1. PREDICCIONES (Cada consulta)**
```json
{
  "features": [2000, 180, 15, ...],  // Características del terreno
  "prediction": 1,                   // Qué tipo de vegetación predijo
  "class_name": "Lodgepole Pine",    // Nombre de la vegetación
  "confidence": 0.95,                // Qué tan seguro está (0-1)
  "risk_level": "HIGH",              // Nivel de riesgo
  "risk_score": 8,                   // Puntuación de riesgo (1-10)
  "timestamp": "2025-10-21T16:41:35" // Cuándo se hizo
}
```

### **2. FEEDBACK (Calificaciones de usuarios)**
```json
{
  "prediction_id": "68f7b7bf60681c7097116062",
  "rating": "excellent",             // Calificación del usuario
  "comment": "Muy preciso",          // Comentario opcional
  "user_id": "usuario123"            // Quién calificó
}
```

## 🛡️ **¿CÓMO EVITAMOS DATOS FALSOS?**

### **PROBLEMA:**
- ¿Qué pasa si un usuario miente?
- ¿Qué pasa si dice que la predicción fue "mala" cuando era correcta?
- **Resultado:** El modelo podría aprender datos falsos y empeorar

### **SOLUCIÓN:**
```
📊 DATOS DE ENTRENAMIENTO (Originales)
├── Forest Cover Type Dataset
├── 100% verificados por expertos
├── Usados para entrenar el modelo
└── NUNCA se modifican

📝 DATOS DE MONITOREO (Separados)
├── Predicciones en producción
├── Feedback de usuarios
├── Usados solo para análisis
└── NUNCA para entrenar
```

## 🔍 **¿CÓMO FUNCIONA EL MONITOREO?**

### **1. DETECCIÓN DE PATRONES:**
```
Si 10+ predicciones seguidas dan el mismo resultado:
├── ¿Es normal? (ej: zona con mucha Lodgepole Pine)
├── ¿Es problema? (ej: modelo se "atascó")
└── Alerta a desarrolladores para investigar
```

### **2. ANÁLISIS DE FEEDBACK:**
```
Si muchos usuarios califican como "malo":
├── ¿Modelo empeoró?
├── ¿Datos cambiaron?
├── ¿Usuarios confiables?
└── Alerta para revisión manual
```

### **3. MÉTRICAS EN TIEMPO REAL:**
```
- Cuántas predicciones por hora
- Confianza promedio del modelo
- Tiempo de procesamiento
- Distribución de tipos de vegetación
- Alertas de calidad
```

## 🚫 **LO QUE NUNCA HACEMOS:**

### **❌ ENTRENAMIENTO AUTOMÁTICO:**
- NO reentrenamos el modelo automáticamente
- NO usamos feedback de usuarios para entrenar
- NO modificamos el modelo sin supervisión

### **❌ APRENDIZAJE DE DATOS FALSOS:**
- NO confiamos en un solo usuario
- NO usamos feedback no validado
- NO permitimos que bots arruinen el modelo

## ✅ **LO QUE SÍ HACEMOS:**

### **✅ MONITOREO INTELIGENTE:**
- Detectamos problemas rápidamente
- Alertamos cuando algo va mal
- Analizamos patrones de uso

### **✅ VALIDACIÓN DE FEEDBACK:**
- Múltiples usuarios deben coincidir
- Detectamos usuarios sospechosos
- Validamos antes de usar

### **✅ CONTROL MANUAL:**
- Solo desarrolladores pueden reentrenar
- Validación exhaustiva antes de cambios
- Testing completo antes de deploy

## 🎯 **BENEFICIOS PARA EL PROYECTO:**

### **1. CUMPLIR REQUISITOS:**
- ✅ **Nivel Avanzado:** Base de datos integrada
- ✅ **Nivel Experto:** Monitoreo de data drift
- ✅ **MLOps:** Alertas y métricas en tiempo real

### **2. MEJORAR EL MODELO:**
- Datos reales para análisis
- Detección de problemas
- Base para futuras mejoras

### **3. EXPERIENCIA DE USUARIO:**
- Feedback para mejorar interfaz
- Alertas de calidad
- Monitoreo de rendimiento

## 🔧 **TECNOLOGÍAS USADAS:**

- **MongoDB Atlas:** Base de datos en la nube
- **FastAPI:** API para guardar y consultar datos
- **Pydantic:** Validación de datos
- **Motor:** Conexión asíncrona a MongoDB

## ✅ **FUNCIONALIDADES IMPLEMENTADAS:**

### **1. GUARDADO AUTOMÁTICO:**
- ✅ **Endpoint `/predict`** guarda automáticamente cada predicción
- ✅ **Metadata completa** (usuario, ubicación, timestamp, confianza)
- ✅ **No bloquea** la respuesta al usuario
- ✅ **Manejo de errores** sin afectar la predicción
- ✅ **Sin errores en consola** - Sistema completamente funcional

### **2. ENDPOINTS DE CONSULTA:**
- ✅ **`/predictions/recent`** - Ver predicciones recientes
- ✅ **`/predictions/stats`** - Estadísticas de rendimiento
- ✅ **`/database/status`** - Estado de la conexión

### **3. MÉTRICAS EN TIEMPO REAL:**
- ✅ **Tiempo de procesamiento** de cada predicción
- ✅ **Confianza promedio** del modelo
- ✅ **Distribución de predicciones** por tipo
- ✅ **Conteo de predicciones** por período
- ✅ **Hash de features** para detectar duplicados
- ✅ **Registro de métricas** sin errores

## 📈 **PRÓXIMOS PASOS:**

1. **Sistema de feedback** - Que usuarios califiquen predicciones
2. **Dashboard de monitoreo** - Ver métricas en tiempo real (frontend)
3. **Sistema de alertas** - Notificar problemas
4. **Análisis de data drift** - Detectar cambios en los datos

## 🚀 **CÓMO USAR:**

### **Ver estado de la base de datos:**
```bash
curl -X GET "http://localhost:8000/database/status"
```

### **Hacer predicción (se guarda automáticamente):**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [2000, 180, 15, 300, 50, 1000, 200, 220, 180, 2000, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "user_id": "usuario123",
    "location": {"lat": 40.7128, "lon": -74.0060}
  }'
```

### **Ver predicciones guardadas:**
```bash
curl -X GET "http://localhost:8000/predictions/recent?limit=5"
```

### **Ver estadísticas:**
```bash
curl -X GET "http://localhost:8000/predictions/stats"
```

### **Probar guardado (endpoint de prueba):**
```bash
curl -X POST "http://localhost:8000/test/save-prediction"
```

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Error: "Error guardando predicción: 'features'"**
- ✅ **SOLUCIONADO** - Era causado por el servicio de métricas
- ✅ **Causa:** Faltaban las features en el diccionario de métricas
- ✅ **Solución:** Agregar `"features": req.features` en `metrics_service.record_prediction()`
- ✅ **Estado:** Sistema completamente funcional sin errores

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

---

**EcoPrint** - Sistema de Predicción de Riesgo de Incendios Forestales 🌲🔥

*"Monitoreamos para mejorar, pero nunca corrompemos el modelo con datos falsos"*
