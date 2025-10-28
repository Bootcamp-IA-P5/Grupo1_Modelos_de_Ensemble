# 🔥 FireRiskAI - Sistema de Predicción de Riesgo de Incendios Forestales

## 📋 Descripción del Proyecto

FireRiskAI es una aplicación web impulsada por inteligencia artificial que combina **clasificación multiclase** y análisis predictivo para abordar un problema real: **la evaluación del riesgo de incendios forestales**. El sistema utiliza un modelo **XGBoost optimizado**, entrenado con el **Forest Cover Type Dataset** del UCI Machine Learning Repository, para **predecir el tipo de cobertura forestal y estimar el nivel de riesgo asociado**.

La visión de FireRiskAI se basa en una **estrategia de datos sólida**, fundamental para el desarrollo de un modelo de *machine learning* de alto rendimiento y confiabilidad, orientado a la toma de decisiones ambientales más precisas y sostenibles.

## 🎯 Características Principales

- **Clasificación de 7 tipos de bosque** con 97.07% de precisión
- **Evaluación de riesgo de incendio** basada en características de inflamabilidad
- **API REST** para predicciones en tiempo real
- **Dashboard Streamlit** interactivo para monitoreo
- **MLOps completo**: A/B Testing, Data Drift, Auto-Reemplazo de Modelos
- **Análisis de features** con nombres reales interpretables
- **Documentación completa** para desarrolladores

## 🚀 Resultados del Modelo

### 📊 Métricas de Rendimiento
| Métrica | Valor | Estado |
|---------|-------|--------|
| **Accuracy** | 97.07% | ✅ Objetivo cumplido (≥97%) |
| **F1-Score** | 96.6% | ✅ Excelente |
| **Recall** | 96.5% | ✅ Excelente |
| **Overfitting** | 2.92% | ✅ Controlado (<5%) |
| **Errores** | 2.93% | ✅ Mínimos |

### 🎯 Tipos de Bosque Clasificados
| Clase | Nombre | Nivel de Riesgo | Score |
|-------|--------|-----------------|-------|
| 0 | Spruce/Fir | LOW | 2 |
| 1 | Lodgepole Pine | HIGH | 8 |
| 2 | Ponderosa Pine | MEDIUM | 5 |
| 3 | Cottonwood/Willow | LOW | 1 |
| 4 | Aspen | MEDIUM | 4 |
| 5 | Douglas-fir | MEDIUM | 6 |
| 6 | Krummholz | HIGH | 9 |

### 🔍 Top 5 Features Más Importantes
1. **Elevation** (45%) - Elevación del terreno
2. **Horizontal_Distance_To_Hydrology** (12%) - Distancia horizontal al agua
3. **Hillshade_9am** (8%) - Sombreado matutino
4. **Wilderness_Area1** (4.2%) - Primera área silvestre
5. **Soil_Type** variados (35% colectivo) - Tipos de suelo

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.11+
- pip
- virtualenv (recomendado)
- MongoDB Atlas (para producción)

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/Bootcamp-IA-P5/Grupo1_Modelos_de_Ensemble.git
cd Grupo1_Modelos_de_Ensemble

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp env.example .env

# Configurar variables (editar .env)
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
DB_NAME=ensemble_models
WEATHER_API_KEY=tu_api_key_de_weatherapi
```

## 🚀 Uso del Sistema

### 1. Backend API (FastAPI)
```bash
# Iniciar servidor API
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Endpoints principales:**
- `GET /health` - Estado del sistema
- `POST /predict` - Predicción de tipo de vegetación
- `GET /model` - Información del modelo
- `GET /metrics` - Métricas de rendimiento
- `POST /feedback` - Feedback de predicciones
- `GET /ab-testing/stats` - Estadísticas de A/B Testing
- `GET /drift/status` - Estado de Data Drift

**Ejemplo de predicción:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"features": [2500, 180, 15, 200, 50, 1000, 220, 230, 140, 500, ...]}'
```

**Respuesta:**
```json
{
  "prediction": 1,
  "class_name": "Lodgepole Pine",
  "confidence": 0.982,
  "risk_level": "HIGH",
  "risk_score": 8,
  "processing_time_ms": 45.2
}
```

### 2. Dashboard Streamlit
```bash
# Iniciar dashboard interactivo
streamlit run streamlit_dashboard.py
```

**Funcionalidades del Dashboard:**
- 🏠 **Inicio**: Resumen del proyecto y métricas clave
- 🔮 **Predicción**: Interfaz para hacer predicciones manuales
- 📊 **EDA**: Análisis exploratorio de datos con visualizaciones
- 🤖 **Modelo**: Métricas detalladas, feature importance, matriz de confusión
- 🔄 **Reentrenamiento**: Monitoreo de datos y sistema de retraining
- 🧪 **A/B Testing**: Comparación de modelos en tiempo real
- 🔍 **Data Drift**: Monitoreo de cambios en distribuciones de datos
- 🤖 **Gestión Modelos**: Auto-reemplazo y comparación de modelos
- 📚 **Documentación**: Guías técnicas y arquitectura
- ℹ️ **Acerca**: Información del equipo y objetivos

### 3. Evaluación del Modelo
```bash
# Ejecutar evaluación completa
python src/evaluation/model_evaluator.py
```

**Archivos generados:**
- `data/processed/confusion_matrix.png` - Matriz de confusión
- `data/processed/metrics_per_class.csv` - Métricas por clase
- `data/processed/feature_importance.png` - Importancia de features

## 📊 Dataset y Features

### Forest Cover Type Dataset
- **Fuente:** UCI ML Repository (ID: 31)
- **Muestras:** 581,012
- **Features:** 54 (10 continuas + 44 categóricas)
- **Clases:** 7 tipos de cobertura forestal
- **División:** 80% entrenamiento, 20% prueba

### Features Principales
- **Elevation** - Elevación del terreno (0-4000m)
- **Aspect** - Orientación de la pendiente (0-360°)
- **Slope** - Inclinación de la pendiente (0-90°)
- **Horizontal_Distance_To_Hydrology** - Distancia horizontal al agua
- **Vertical_Distance_To_Hydrology** - Distancia vertical al agua
- **Horizontal_Distance_To_Roadways** - Distancia a carreteras
- **Hillshade_9am/Noon/3pm** - Sombreado en diferentes horas
- **Horizontal_Distance_To_Fire_Points** - Distancia a puntos de fuego
- **Wilderness_Area1-4** - Áreas silvestres (4 tipos)
- **Soil_Type1-40** - Tipos de suelo (40 tipos)

## 🔧 Desarrollo

### Entrenamiento de Modelos
```bash
# Comparación de modelos baseline
python src/models/01_baseline_comparison.py

# Optimización completa de ensembles
python src/models/02_full_ensemble_comparison.py

# Entrenamiento rápido para A/B Testing
python src/models/03_fast_comparison.py
```

### Tests
```bash
# Ejecutar tests unitarios
python -m pytest tests/

# Tests específicos
python -m pytest tests/test_predict.py
python -m pytest tests/test_metrics.py
python -m pytest tests/test_feedback.py
```

### Linting y Formato
```bash
# Verificar estilo de código
flake8 src/ tests/

# Formatear código
black src/ tests/
```

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico
- **Backend**: FastAPI + Python 3.11
- **Frontend**: Streamlit Dashboard
- **ML**: XGBoost + Scikit-learn
- **Database**: MongoDB Atlas
- **Deployment**: Render.com
- **CI/CD**: GitHub Actions

### MLOps Implementado
- ✅ **A/B Testing**: Comparación de modelos en producción
- ✅ **Data Drift**: Monitoreo de cambios en distribuciones
- ✅ **Auto Model Replacement**: Reemplazo automático de modelos
- ✅ **Feedback Loop**: Recolección de feedback de usuarios
- ✅ **Métricas**: Monitoreo continuo de performance
- ✅ **CI/CD**: Pipeline automatizado de despliegue

## 📈 Análisis de Rendimiento

### Matriz de Confusión
El modelo muestra excelente rendimiento en todas las clases:
- **Spruce/Fir:** 97.35% precisión
- **Lodgepole Pine:** 97.19% precisión
- **Ponderosa Pine:** 96.52% precisión
- **Cottonwood/Willow:** 90.82% precisión (clase minoritaria)
- **Aspen:** 94.06% precisión (clase minoritaria)
- **Douglas-fir:** 94.69% precisión
- **Krummholz:** 97.57% precisión

### Análisis de Errores
- **Total de errores:** 3,406 de 116,203 (2.93%)
- **Confianza promedio en errores:** 74.4%
- **Clases más confundidas:** Cottonwood/Willow y Aspen (clases minoritarias)

## 🎯 Aplicaciones

### Gestión Forestal
- **Identificación de tipos de bosque** para inventarios forestales
- **Evaluación de riesgo de incendio** para planificación preventiva
- **Análisis de vulnerabilidad** de diferentes ecosistemas

### Investigación
- **Estudios ecológicos** sobre distribución de especies
- **Análisis de biodiversidad** en diferentes tipos de suelo
- **Modelado de ecosistemas** forestales

### MLOps y Producción
- **Monitoreo de modelos** en tiempo real
- **Detección de degradación** de performance
- **Gestión automática** de versiones de modelos

## 📚 Documentación Completa

### Documentación Técnica
- [📊 Conclusiones del Proyecto](docs/PROYECTO_CONCLUSIONES.md) - Análisis completo de datos y modelos
- [🤖 Guía de Modelos](docs/README_MODELOS.md) - Comparación de ensembles
- [📈 Evaluación del Modelo](docs/MODEL_EVALUATION.md) - Métricas detalladas
- [🏗️ Arquitectura del Backend](docs/BACKEND_COMPLETE.md) - Guía completa de la API
- [🔌 Guía de Endpoints](docs/BACKEND_API_GUIDE.md) - Documentación de la API REST

### MLOps y Producción
- [🧪 A/B Testing](docs/AUTO_MODEL_REPLACEMENT.md) - Sistema de comparación de modelos
- [🔍 Data Drift](docs/DATA_DRIFT_MONITORING.md) - Monitoreo de cambios en datos
- [🗄️ MongoDB](docs/MONGODB_DATA_STORAGE.md) - Configuración de base de datos
- [🎓 Entrenamiento](docs/MODEL_TRAINING.md) - Guía de entrenamiento de modelos

### Presentación y Evaluación
- [📋 Guía de Presentación](docs/PRESENTATION_GUIDE.md) - Cómo presentar el proyecto
- [✅ Checklist Rúbrica](docs/RUBRICA_CHECKLIST.md) - Evaluación del proyecto
- [🗺️ Diagramas](docs/diagramas/) - Esquemas de arquitectura y base de datos

## 🚀 Despliegue en Producción

### Render.com (Recomendado)
1. **Backend FastAPI:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Variables: `MONGO_URI`, `DB_NAME`, `WEATHER_API_KEY`

2. **Dashboard Streamlit:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run streamlit_dashboard.py --server.port $PORT --server.address 0.0.0.0`
   - Variables: `BASE_URL=https://tu-backend-url.onrender.com`

### URLs de Producción
- **Backend API**: https://grupo1-modelos-de-ensemble-fireriskai.onrender.com
- **Dashboard**: https://tu-dashboard-url.onrender.com
- **Documentación API**: https://grupo1-modelos-de-ensemble-fireriskai.onrender.com/docs

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Equipo

| Nombre | GitHub | LinkedIn | Rol |
|--------|--------|----------|-----|
| **Alfonso Bermúdez Torres** | [@GHalfbbt](https://github.com/GHalfbbt) | [LinkedIn](https://www.linkedin.com/in/alfonsobermudeztorres/) | Análisis Exploratorio de Datos (EDA) |
| **Bárbara Sánchez Urbano** | [@Barbarasanchez11](https://github.com/Barbarasanchez11) | [LinkedIn](https://github.com/Barbarasanchez11) | Ingeniera de Modelos |
| **Bunty Nanwani** | [LinkedIn](https://www.linkedin.com/in/buntynanwani/) | [LinkedIn](https://www.linkedin.com/in/buntynanwani/) | Análisis de Riesgo de Incendios |
| **Aroa Mateo Gómez** | [@Arowi95](https://github.com/Arowi95) | [LinkedIn](https://www.linkedin.com/in/aroamateogomez/) | Evaluación de Modelos |

## 📞 Contacto

Para preguntas o sugerencias, por favor contacta al equipo de desarrollo.

---

<div align="center">

*Desarrollado con ❤️ usando Python, FastAPI y Streamlit*

**🔥 FireRiskAI - Clasificación Inteligente de Vegetación Forestal 🔥**

</div>