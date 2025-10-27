# 🚀 Entrenamiento de Modelos

## 📋 Scripts Disponibles

Los scripts de entrenamiento están en `src/models/` y se ejecutan localmente:

### 1. **01_baseline_comparison.py**
```bash
python src/models/01_baseline_comparison.py
```
- Comparación baseline de modelos
- Genera: `best_model_optimized.pkl`

### 2. **02_full_ensemble_comparison.py**
```bash
python src/models/02_full_ensemble_comparison.py
```
- Ensemble completo con optimización
- Genera: `best_ensemble_model.pkl`

### 3. **03_fast_comparison.py**
```bash
python src/models/03_fast_comparison.py
```
- Comparación rápida para A/B testing
- Genera: `best_fast_model.pkl`, `scaler.pkl`

### 4. **04_optimized_comparison.py**
```bash
python src/models/04_optimized_comparison.py
```
- Comparación optimizada sin GradientBoosting
- Genera: `best_optimized_model.pkl`, `scaler_optimized.pkl`

## 🎯 Para A/B Testing

Para generar los modelos de A/B testing:

```bash
python scripts/fast_training_ab_testing.py
```

Esto genera:
- `models/random_forest_ab.pkl`
- `models/extra_trees_ab.pkl` 
- `models/xgboost_ab.pkl`
- `models/ab_testing_metadata.json`

## 📁 Archivos Generados

Los archivos `.pkl` se generan en la carpeta `models/` pero **NO se suben al repositorio** por su tamaño.

## ⚠️ Importante

- Los modelos se entrenan **localmente**
- Los archivos `.pkl` se generan en `models/`
- Solo se suben los **scripts** y **metadata** al repositorio
- Para producción, ejecutar los scripts en el servidor
