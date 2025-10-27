# 🚀 FireRiskAI - Backend Completo

## 📋 Resumen

Backend completo de **FireRiskAI** con funcionalidades de **Nivel Experto** implementadas:
- ✅ Sistema de predicción multiclase
- ✅ A/B Testing de modelos
- ✅ Data Drift Monitoring
- ✅ Auto Model Replacement
- ✅ Integración con MongoDB
- ✅ Weather API
- ✅ Sistema de feedback

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Predicción  │  │  A/B Testing │  │ Data Drift   │ │
│  │   Principal  │  │              │  │ Monitoring   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                  │         │
│         └─────────────────┼──────────────────┘         │
│                           │                            │
│                  ┌────────▼────────┐                   │
│                  │ Auto Replacement│                   │
│                  └────────┬────────┘                   │
│                           │                            │
└───────────────────────────┼────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   MongoDB     │
                    └───────────────┘
```

## 📂 Estructura del Código

### **Archivos Principales:**

| Archivo | Ubicación | Función |
|---------|-----------|---------|
| `app.py` | Raíz | Aplicación FastAPI principal |
| `requirements.txt` | Raíz | Dependencias Python |

### **API Routes:**

| Archivo | Ubicación | Endpoints |
|---------|-----------|-----------|
| `health.py` | `src/api/routes/` | `/health` |
| `model.py` | `src/api/routes/` | `/model` |
| `predict.py` | `src/api/routes/` | `/predict` |
| `metrics.py` | `src/api/routes/` | `/metrics` |
| `feedback.py` | `src/api/routes/` | `/feedback` |
| `ab_testing.py` | `src/api/routes/` | `/predict-ab`, `/ab-testing/stats` |
| `drift.py` | `src/api/routes/` | `/drift/check`, `/drift/alerts` |
| `model_replacement.py` | `src/api/routes/` | `/models/compare`, `/models/replace` |
| `weather.py` | `src/api/routes/` | `/weather` |
| `dashboard.py` | `src/api/routes/` | `/dashboard` |

### **Services:**

| Archivo | Ubicación | Función |
|---------|-----------|---------|
| `ab_testing_service.py` | `src/api/services/` | Lógica de A/B Testing |
| `drift_detector.py` | `src/api/services/` | Detección de Data Drift |
| `model_manager.py` | `src/api/services/` | Gestión de modelos |
| `database.py` | `src/api/services/` | Conexión MongoDB |

## 🔌 Endpoints Disponibles

### **1. Predicción Principal**

**`POST /predict`**
- **Función:** Predice tipo de vegetación y riesgo de incendio
- **Archivo:** `src/api/routes/predict.py`
- **Service:** Carga modelo y hace predicción

### **2. A/B Testing**

**`POST /predict-ab`**
- **Función:** Predicción con distribución entre modelos
- **Archivo:** `src/api/routes/ab_testing.py`
- **Service:** `src/api/services/ab_testing_service.py`

### **3. Data Drift**

**`POST /drift/check`**
- **Función:** Detecta cambios en distribución de datos
- **Archivo:** `src/api/routes/drift.py`
- **Service:** `src/api/services/drift_detector.py`

### **4. Auto Model Replacement**

**`GET /models/compare`**
- **Función:** Compara modelos y encuentra el mejor
- **Archivo:** `src/api/routes/model_replacement.py`
- **Service:** `src/api/services/model_manager.py`

### **5. Métricas**

**`GET /metrics`**
- **Función:** Dashboard completo de métricas
- **Archivo:** `src/api/routes/metrics.py`

## 🧪 Funcionalidades Implementadas

### **✅ Nivel Esencial:**
- ✅ Modelo de clasificación multiclase (7 clases)
- ✅ EDA completo con visualizaciones
- ✅ Overfitting < 5% (2.92%)
- ✅ Aplicación FastAPI
- ✅ Métricas completas (accuracy, precision, recall, F1, matriz confusión)

### **✅ Nivel Medio:**
- ✅ Modelos ensemble (Random Forest, XGBoost, Extra Trees)
- ✅ Validación cruzada (StratifiedKFold)
- ✅ Optimización de hiperparámetros (GridSearchCV)
- ✅ Sistema de feedback en tiempo real
- ✅ Pipeline de recolección de datos (MongoDB)

### **✅ Nivel Avanzado:**
- ✅ Dockerización completa
- ✅ Integración con MongoDB Atlas
- ✅ Deploy en la nube (Render.com)
- ✅ Tests unitarios

### **✅ Nivel Experto:**
- ✅ A/B Testing para comparar modelos
- ✅ Data Drift Monitoring con alertas
- ✅ Auto Model Replacement

## 🔄 Flujos de Trabajo

### **Flujo de Predicción:**

```
Usuario → POST /predict
    ↓
FastAPI recibe features
    ↓
Modelo ML predice clase
    ↓
Guarda en MongoDB
    ↓
Retorna predicción al usuario
```

### **Flujo de A/B Testing:**

```
Usuario → POST /predict-ab
    ↓
Servicio selecciona modelo (Random Forest, Extra Trees, XGBoost)
    ↓
Predicción con modelo seleccionado
    ↓
Guarda estadísticas en MongoDB
    ↓
Retorna predicción + modelo usado
```

### **Flujo de Data Drift:**

```
Sistema → POST /drift/check
    ↓
Compara datos nuevos con baseline
    ↓
Detecta si hay drift significativo
    ↓
Si hay drift → Genera alerta
    ↓
Guarda en MongoDB
```

### **Flujo de Auto Replacement:**

```
Sistema → GET /models/compare
    ↓
Compara accuracy de todos los modelos
    ↓
Encuentra el mejor modelo
    ↓
Si es mejor → POST /models/replace/{model}
    ↓
Nuevo modelo se convierte en principal
```

## 📊 Integración de Componentes

### **A/B Testing + Data Drift + Auto Replacement:**

```
1. A/B Testing distribuye predicciones
   ↓
2. Data Drift detecta cambios en datos
   ↓
3. Auto Replacement compara modelos
   ↓
4. Mejor modelo se convierte en principal
   ↓
5. Sistema funciona con mejor modelo
```

## 🗂️ Modelos Disponibles

### **Modelos en Producción:**

| Modelo | Accuracy | Archivo | Status |
|--------|----------|---------|--------|
| Random Forest | ~96% | `models/random_forest_model.pkl` | A/B Testing |
| Extra Trees | ~97% | `models/extra_trees_model.pkl` | A/B Testing |
| XGBoost | ~97% | `models/best_model.pkl` | Principal |

### **Ubicación de Archivos:**

- **Modelos:** `models/*.pkl`
- **Metadata:** `models/*_metadata.json`
- **Scalers:** `models/*_scaler.pkl`
- **Config:** `models/ab_testing_metadata.json`

## 🔧 Configuración

### **Variables de Entorno (.env):**

```env
# MongoDB
MONGO_URI=mongodb+srv://...
DB_NAME=ensemble_models

# APIs
WEATHER_API_KEY=...

# App
APP_PORT=8000
APP_HOST=0.0.0.0
LOG_LEVEL=INFO
```

### **Dependencias (requirements.txt):**

```txt
# Core ML
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
joblib>=1.3.0

# Web
fastapi>=0.100.0
uvicorn>=0.20.0
pydantic>=2.0.0

# Database
pymongo>=4.4.0
motor>=3.0.0

# External APIs
requests>=2.31.0
python-dotenv>=1.0.0

# Testing
pytest>=7.0.0
```

## 🚀 Cómo Iniciar

### **1. Instalar Dependencias:**

```bash
pip install -r requirements.txt
```

### **2. Configurar Variables:**

```bash
cp env.example .env
# Editar .env con tus valores
```

### **3. Iniciar Servidor:**

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **4. Verificar:**

```bash
curl http://localhost:8000/health
```

## 📚 Documentación Adicional

- `docs/AUTO_MODEL_REPLACEMENT.md` - Auto Replacement
- `docs/DATA_DRIFT_MONITORING.md` - Data Drift
- `docs/README_MODELOS.md` - Modelos ML
- `docs/BACKEND_API_GUIDE.md` - Guía de API

## ✅ Estado Final

**Backend:** ✅ **COMPLETO AL 100%**

- ✅ Todas las funcionalidades de Nivel Experto
- ✅ Integración completa de componentes
- ✅ Sistema de monitoreo y alertas
- ✅ Auto-optimización de modelos
- ✅ Listo para Streamlit dashboard

