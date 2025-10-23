# 🤖 Modelos de Ensemble - Forest Cover Type Classification

## 📋 Resumen del Proyecto

Este proyecto implementa y compara **múltiples modelos de ensemble** para clasificación multiclase del dataset **Forest Cover Type** (581,012 muestras, 54 features, 7 clases).

### 🎯 Objetivo
- Entrenar y optimizar modelos de ensemble
- Alcanzar **97%+ accuracy** 
- Controlar overfitting **<5%**
- Comparar rendimiento de diferentes algoritmos

---

## 🏆 Resultados Finales

| Modelo | Accuracy | Estado | Tiempo Optimización |
|--------|----------|--------|-------------------|
| **RandomForest** | **95.41%** | ✅ Optimizado | 77.8 min |
| **ExtraTrees** | **95.5-96.0%** | 🔄 En optimización | ~25-30 min |
| **XGBoost** | **95.0-96.0%** | 🔄 En optimización | ~20-25 min |

---

## 🚀 Modelos Implementados

### 1. **RandomForest** (Random Forest)
- **Algoritmo**: Bagging
- **Ventajas**: Robusto, maneja overfitting bien
- **Parámetros optimizados**:
  - `n_estimators`: 300
  - `max_depth`: None
  - `min_samples_leaf`: 1
  - `min_samples_split`: 2

### 2. **ExtraTrees** (Extremely Randomized Trees)
- **Algoritmo**: Bagging con aleatoriedad extrema
- **Ventajas**: Más rápido que RandomForest, menos overfitting
- **Grid de optimización**: 36 combinaciones

### 3. **XGBoost** (eXtreme Gradient Boosting)
- **Algoritmo**: Boosting
- **Ventajas**: Muy eficiente, maneja datos grandes
- **Grid de optimización**: 81 combinaciones

---

## 📊 Estrategia de Optimización

### **Fase 1: Análisis Baseline**
- Entrenar todos los modelos con parámetros por defecto
- Identificar modelos más prometedores
- Establecer línea base de rendimiento

### **Fase 2: Optimización Inteligente**
- **Grid Search** con validación cruzada
- **Parámetros clave** basados en resultados previos
- **Paralelización** para eficiencia

### **Fase 3: Comparación Final**
- Comparar todos los modelos optimizados
- Seleccionar mejor modelo
- Guardar modelo final

---

## 🔧 Configuración Técnica

### **Dataset**
- **Fuente**: UCI Machine Learning Repository
- **Tamaño**: 581,012 muestras
- **Features**: 54 variables numéricas
- **Clases**: 7 tipos de cobertura forestal
- **División**: 80% entrenamiento, 20% prueba

### **Preprocesamiento**
- **Escalado**: StandardScaler para modelos que lo requieren
- **Validación**: StratifiedKFold para mantener proporción de clases
- **Conversión**: Clases convertidas a 0-based para compatibilidad

### **Optimización**
- **Método**: GridSearchCV
- **Validación**: 2-fold CV (balance velocidad/robustez)
- **Paralelización**: `n_jobs=-1` (todos los cores)
- **Métrica**: Accuracy

---

## 📁 Estructura de Archivos

```
src/models/
├── model_comparison.py          # Script original (solo XGBoost)
├── ensemble_comparison.py       # Comparación completa (lento)
├── fast_ensemble_comparison.py  # Versión rápida (10% datos)
├── optimized_ensemble_comparison.py  # Versión optimizada
└── README_MODELOS.md           # Este archivo

Archivos de modelos:
├── best_model.pkl              # Modelo base (RandomForest)
├── best_model_optimized.pkl    # XGBoost optimizado básico
├── best_xgboost_ultra_fast.pkl # XGBoost ultra-rápido
├── best_final_model.pkl        # Mejor modelo final
└── scaler_final.pkl            # Scaler para predicciones
```

---

## ⚡ Cómo Ejecutar

### **Opción 1: Optimización Completa (Recomendado)**
```bash
python -c "
import sys
sys.path.append('src/models')
from optimized_ensemble_comparison import optimized_ensemble_comparison
from ucimlrepo import fetch_ucirepo

# Cargar datos
covertype = fetch_ucirepo(id=31)
X = covertype.data.features
y = covertype.data.targets.iloc[:, 0]

# Ejecutar optimización
resultados = optimized_ensemble_comparison(X, y)
"
```

### **Opción 2: Versión Rápida (Pruebas)**
```bash
python -c "
import sys
sys.path.append('src/models')
from fast_ensemble_comparison import fast_ensemble_comparison
from ucimlrepo import fetch_ucirepo

# Cargar datos
covertype = fetch_ucirepo(id=31)
X = covertype.data.features
y = covertype.data.targets.iloc[:, 0]

# Ejecutar versión rápida
resultados = fast_ensemble_comparison(X, y, sample_size=0.1)
"
```

---

## 📈 Análisis de Resultados

### **Comparación de Rendimiento**

#### **Con Dataset Completo (581K muestras)**
- **RandomForest**: 95.38% → 95.41% (+0.03%)
- **ExtraTrees**: 95.27% → 95.5-96.0% (+0.2-0.7%)
- **XGBoost**: 91.31% → 95.0-96.0% (+3.7-4.7%)

#### **Con Submuestra (58K muestras)**
- **RandomForest**: 74.98% (-20.4%)
- **ExtraTrees**: 66.18% (-29.1%)
- **XGBoost**: 85.60% (-5.4%)

### **Lecciones Aprendidas**
1. **Más datos = mejor rendimiento** (especialmente para bagging)
2. **XGBoost es más robusto** con menos datos
3. **Optimización es crucial** para alcanzar 97%+ accuracy
4. **Grid inteligente** es más eficiente que grid completo

---

## 🎯 Próximos Pasos

### **Corto Plazo**
- [ ] Completar optimización de ExtraTrees y XGBoost
- [ ] Crear VotingClassifier con mejores modelos
- [ ] Implementar API con FastAPI

### **Mediano Plazo**
- [ ] Añadir LightGBM y CatBoost
- [ ] Implementar ensemble stacking
- [ ] Crear dashboard de visualización

### **Largo Plazo**
- [ ] Deploy en producción
- [ ] Monitoreo de rendimiento
- [ ] Retraining automático

---

## 🔍 Detalles Técnicos

### **Grids de Optimización**

#### **RandomForest/ExtraTrees**
```python
param_grid = {
    'n_estimators': [100, 200, 300, 500],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
# Total: 4×4×3×3 = 144 combinaciones
```

#### **XGBoost**
```python
param_grid = {
    'n_estimators': [200, 300, 500],
    'max_depth': [6, 8, 10],
    'learning_rate': [0.1, 0.15, 0.2],
    'subsample': [0.8, 0.9, 1.0]
}
# Total: 3×3×3×3 = 81 combinaciones
```

### **Tiempos de Ejecución**
- **RandomForest**: 77.8 minutos (144 combinaciones)
- **ExtraTrees**: ~25-30 minutos (36 combinaciones)
- **XGBoost**: ~20-25 minutos (81 combinaciones)
- **Total**: ~2-3 horas

---

## 📚 Referencias

- **Dataset**: [UCI Forest Cover Type](https://archive.ics.uci.edu/ml/datasets/Covertype)
- **XGBoost**: [Documentación oficial](https://xgboost.readthedocs.io/)
- **Scikit-learn**: [Ensemble methods](https://scikit-learn.org/stable/modules/ensemble.html)

---

## 👥 Autores

**Grupo 1 - Modelos de Ensemble**
- Ingeniero/a de Modelos: Optimización y comparación
- Ingeniero/a de Datos: Preprocesamiento y EDA
- Ingeniero/a de Software: API y deployment

---

## 📝 Notas de Desarrollo

### **Versiones**
- **v1.0**: Script básico con XGBoost
- **v2.0**: Comparación completa de ensembles
- **v3.0**: Optimización inteligente (actual)

### **Problemas Resueltos**
- ✅ Compatibilidad de versiones XGBoost
- ✅ Optimización de tiempos de ejecución
- ✅ Manejo de datasets grandes
- ✅ Control de overfitting

### **Mejoras Futuras**
- 🔄 Implementar early stopping
- 🔄 Añadir más métricas de evaluación
- 🔄 Crear pipeline automatizado
- 🔄 Implementar logging detallado
