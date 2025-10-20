# 🌲 Forest Cover Type Classification

> **Modelo de Machine Learning para clasificación de tipos de cobertura forestal con 97.07% de accuracy**

## 📊 Resumen

Este proyecto implementa un **clasificador XGBoost optimizado** que predice el tipo de cobertura forestal basándose en 54 variables geográficas y climáticas. El modelo alcanza una **precisión del 97.07%** en el dataset Forest Cover Type de UCI.

### 🎯 Características Principales
- **Accuracy**: 97.07%
- **Algoritmo**: XGBoost optimizado
- **Dataset**: 581,012 muestras, 54 features, 7 clases
- **Tiempo de entrenamiento**: ~45 minutos
- **Overfitting**: <3% (excelente generalización)

## 🚀 Uso Rápido

### Instalación
```bash
pip install -r requirements.txt
```

### Predicción Simple
```python
from src.predict import ForestCoverPredictor

# Inicializar predictor
predictor = ForestCoverPredictor()

# Hacer predicción (54 features)
features = [1.2, 3.4, 5.6, ...]  # 54 valores
result = predictor.predict(features)

print(f"Tipo de bosque: {result['class_name']}")
print(f"Confianza: {result['confidence']:.3f}")
```

### Ejecutar Demo
```bash
python src/predict.py
```

### API (FastAPI)
```bash
# arrancar la API (hot-reload)
uvicorn src.api.app:app --reload

# comprobar salud
curl http://127.0.0.1:8000/health

# documentación interactiva
# abrir en el navegador: http://127.0.0.1:8000/docs
```

#### Endpoints disponibles

- GET `/health`
  - Propósito: Comprobar que el servicio está vivo.
  - Respuesta de ejemplo:
  ```json
  {"status": "ok", "service": "FireRiskAI"}
  ```
  - Probar:
  ```bash
  curl http://127.0.0.1:8000/health
  ```

- GET `/model`
  - Propósito: Devolver metadatos del modelo desde `models/metadata.json`.
  - Respuesta: JSON con nombre, versión, accuracy, algoritmo, parámetros, clases, etc.
  - Códigos de error:
    - 404 si no existe `models/metadata.json`.
    - 500 si hay error al leer/parsear el archivo.
  - Probar:
  ```bash
  curl http://127.0.0.1:8000/model
  ```

## 📁 Estructura del Proyecto

```
├── README.md                    # Este archivo
├── README_MODELOS.md           # Documentación técnica detallada
├── requirements.txt            # Dependencias
├── models/                     # Modelos entrenados
│   ├── best_model.pkl         # Modelo final (XGBoost)
│   ├── scaler.pkl             # Scaler para preprocesamiento
│   └── metadata.json          # Información del modelo
├── src/                       # Código fuente
│   ├── predict.py             # Script principal de predicción
│   ├── models/                # Scripts de entrenamiento
│   ├── api/                   # API endpoints (próximamente)
│   └── utils/                 # Utilidades
├── notebooks/                 # Jupyter notebooks
│   ├── 01_EDA.ipynb          # Análisis exploratorio
│   └── 02_Model_Training.ipynb # Entrenamiento de modelos
└── data/                      # Datos
    ├── raw/                   # Datos originales
    ├── processed/             # Datos procesados
    └── external/              # Datos externos
```

## 🎯 Tipos de Bosque Clasificados

| ID | Nombre | Descripción |
|----|--------|-------------|
| 0 | Spruce/Fir | Abeto/Pícea |
| 1 | Lodgepole Pine | Pino Lodgepole |
| 2 | Ponderosa Pine | Pino Ponderosa |
| 3 | Cottonwood/Willow | Álamo/Sauce |
| 4 | Aspen | Álamo temblón |
| 5 | Douglas-fir | Abeto de Douglas |
| 6 | Krummholz | Vegetación alpina |

## 📈 Rendimiento del Modelo

### Métricas Principales
- **Accuracy**: 97.07%
- **Precision**: 96.8% (promedio)
- **Recall**: 96.5% (promedio)
- **F1-Score**: 96.6% (promedio)

### Comparación de Modelos
| Modelo | Accuracy | Tiempo Entrenamiento |
|--------|----------|---------------------|
| **XGBoost** | **97.07%** | 45 min |
| RandomForest | 95.41% | 78 min |
| ExtraTrees | 95.27% | 65 min |

## 🔧 Parámetros del Modelo

```python
{
    "learning_rate": 0.2,
    "max_depth": 10,
    "n_estimators": 500,
    "subsample": 0.9,
    "random_state": 42
}
```

## 📚 Documentación

- **[README_MODELOS.md](README_MODELOS.md)**: Documentación técnica completa
- **[Notebooks](notebooks/)**: Análisis exploratorio y entrenamiento
- **[Modelos](src/models/)**: Scripts de entrenamiento y comparación

## 🚀 Próximos Pasos

- [ ] **API REST** con FastAPI
- [ ] **Interfaz web** para predicciones
- [ ] **Deploy en la nube**
- [ ] **Monitoreo de rendimiento**

## 👥 Equipo

**Grupo 1 - Modelos de Ensemble**
- Ingeniero/a de Modelos: Optimización y comparación
- Ingeniero/a de Datos: Preprocesamiento y EDA  
- Ingeniero/a de Software: API y deployment

## 📄 Licencia

Este proyecto es parte del bootcamp de IA y está destinado a fines educativos.

---

**¿Necesitas ayuda?** Revisa la [documentación técnica](README_MODELOS.md) o ejecuta `python src/predict.py` para ver un ejemplo.