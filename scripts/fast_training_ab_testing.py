"""
Entrenamiento RÁPIDO para A/B Testing
Objetivo: Accuracy >95%, Overfitting <5%, Tiempo <10 minutos
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import joblib
import json
import time
from datetime import datetime

print("🚀 ENTRENAMIENTO RÁPIDO PARA A/B TESTING")
print("=" * 50)

# 1. CARGAR DATOS
print("📊 Cargando datos...")
from ucimlrepo import fetch_ucirepo
forest_cover = fetch_ucirepo(id=31)
X = forest_cover.data.features
y = forest_cover.data.targets

# Convertir a numpy arrays
X = X.values
y = y.values.ravel()

# Convertir clases a 0-based
y = y - 1

print(f"✅ Datos cargados: {X.shape[0]} muestras, {X.shape[1]} features")
print(f"✅ Clases: {sorted(np.unique(y))}")

# 2. DIVIDIR DATOS (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"📊 División: Train={X_train.shape[0]}, Test={X_test.shape[0]}")

# 3. CONFIGURACIONES OPTIMIZADAS PARA VELOCIDAD
print("\n🔧 Configuraciones optimizadas para velocidad...")

# Random Forest - Configuración rápida pero efectiva
rf_params = {
    'n_estimators': [100, 200],  # Menos árboles
    'max_depth': [15, 20],       # Profundidad limitada
    'min_samples_split': [5],    # Un solo valor
    'min_samples_leaf': [2],     # Un solo valor
    'max_features': ['sqrt'],    # Un solo valor
    'n_jobs': [-1]              # Paralelización
}

# Extra Trees - Configuración rápida
et_params = {
    'n_estimators': [100, 200],
    'max_depth': [15, 20],
    'min_samples_split': [5],
    'min_samples_leaf': [2],
    'max_features': ['sqrt'],
    'n_jobs': [-1]
}

# XGBoost - Configuración rápida
xgb_params = {
    'n_estimators': [100, 200],
    'max_depth': [6, 8],
    'learning_rate': [0.1, 0.2],
    'subsample': [0.8],
    'colsample_bytree': [0.8],
    'n_jobs': [-1]
}

# 4. ENTRENAR MODELOS
models = {}
results = []

# Random Forest
print("\n🌲 Entrenando Random Forest...")
start_time = time.time()
rf_grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    rf_params,
    cv=3,  # Solo 3-fold para velocidad
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)
rf_grid.fit(X_train, y_train)
rf_time = time.time() - start_time

rf_best = rf_grid.best_estimator_
rf_pred = rf_best.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)
rf_train_pred = rf_best.predict(X_train)
rf_train_accuracy = accuracy_score(y_train, rf_train_pred)
rf_overfitting = rf_train_accuracy - rf_accuracy

print(f"✅ Random Forest: {rf_accuracy:.4f} ({rf_accuracy:.2%}) - Overfitting: {rf_overfitting:.4f} ({rf_overfitting:.2%}) - Tiempo: {rf_time:.1f}s")

# Extra Trees
print("\n🌳 Entrenando Extra Trees...")
start_time = time.time()
et_grid = GridSearchCV(
    ExtraTreesClassifier(random_state=42),
    et_params,
    cv=3,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)
et_grid.fit(X_train, y_train)
et_time = time.time() - start_time

et_best = et_grid.best_estimator_
et_pred = et_best.predict(X_test)
et_accuracy = accuracy_score(y_test, et_pred)
et_train_pred = et_best.predict(X_train)
et_train_accuracy = accuracy_score(y_train, et_train_pred)
et_overfitting = et_train_accuracy - et_accuracy

print(f"✅ Extra Trees: {et_accuracy:.4f} ({et_accuracy:.2%}) - Overfitting: {et_overfitting:.4f} ({et_overfitting:.2%}) - Tiempo: {et_time:.1f}s")

# XGBoost
print("\n🚀 Entrenando XGBoost...")
start_time = time.time()
xgb_grid = GridSearchCV(
    xgb.XGBClassifier(random_state=42, eval_metric='logloss'),
    xgb_params,
    cv=3,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)
xgb_grid.fit(X_train, y_train)
xgb_time = time.time() - start_time

xgb_best = xgb_grid.best_estimator_
xgb_pred = xgb_best.predict(X_test)
xgb_accuracy = accuracy_score(y_test, xgb_pred)
xgb_train_pred = xgb_best.predict(X_train)
xgb_train_accuracy = accuracy_score(y_train, xgb_train_pred)
xgb_overfitting = xgb_train_accuracy - xgb_accuracy

print(f"✅ XGBoost: {xgb_accuracy:.4f} ({xgb_accuracy:.2%}) - Overfitting: {xgb_overfitting:.4f} ({xgb_overfitting:.2%}) - Tiempo: {xgb_time:.1f}s")

# 5. COMPARAR RESULTADOS
print("\n📊 COMPARACIÓN DE MODELOS:")
print("=" * 50)

comparison_data = {
    'Modelo': ['Random Forest', 'Extra Trees', 'XGBoost'],
    'Accuracy': [rf_accuracy, et_accuracy, xgb_accuracy],
    'Overfitting': [rf_overfitting, et_overfitting, xgb_overfitting],
    'Tiempo (s)': [rf_time, et_time, xgb_time],
    'Cumple Objetivos': [
        '✅' if rf_accuracy > 0.95 and rf_overfitting < 0.05 else '❌',
        '✅' if et_accuracy > 0.95 and et_overfitting < 0.05 else '❌',
        '✅' if xgb_accuracy > 0.95 and xgb_overfitting < 0.05 else '❌'
    ]
}

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))

# 6. GUARDAR MODELOS PARA A/B TESTING
print("\n💾 Guardando modelos para A/B Testing...")

# Crear metadata
metadata = {
    "training_info": {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dataset": "Forest Cover Type",
        "train_samples": X_train.shape[0],
        "test_samples": X_test.shape[0],
        "features": X_train.shape[1],
        "classes": len(np.unique(y))
    },
    "models": {
        "random_forest": {
            "accuracy": float(rf_accuracy),
            "overfitting": float(rf_overfitting),
            "training_time": float(rf_time),
            "best_params": rf_grid.best_params_
        },
        "extra_trees": {
            "accuracy": float(et_accuracy),
            "overfitting": float(et_overfitting),
            "training_time": float(et_time),
            "best_params": et_grid.best_params_
        },
        "xgboost": {
            "accuracy": float(xgb_accuracy),
            "overfitting": float(xgb_overfitting),
            "training_time": float(xgb_time),
            "best_params": xgb_grid.best_params_
        }
    }
}

# Guardar modelos
joblib.dump(rf_best, 'models/random_forest_ab.pkl')
joblib.dump(et_best, 'models/extra_trees_ab.pkl')
joblib.dump(xgb_best, 'models/xgboost_ab.pkl')

# Guardar metadata
with open('models/ab_testing_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("✅ Modelos guardados:")
print("   - models/random_forest_ab.pkl")
print("   - models/extra_trees_ab.pkl")
print("   - models/xgboost_ab.pkl")
print("   - models/ab_testing_metadata.json")

# 7. RESUMEN FINAL
print("\n🎯 RESUMEN FINAL:")
print("=" * 50)
total_time = rf_time + et_time + xgb_time
print(f"⏱️  Tiempo total: {total_time:.1f} segundos ({total_time/60:.1f} minutos)")

best_model = max([
    (rf_accuracy, 'Random Forest', rf_overfitting),
    (et_accuracy, 'Extra Trees', et_overfitting),
    (xgb_accuracy, 'XGBoost', xgb_overfitting)
], key=lambda x: x[0])

print(f"🏆 Mejor modelo: {best_model[1]}")
print(f"🎯 Accuracy: {best_model[0]:.4f} ({best_model[0]:.2%})")
print(f"📉 Overfitting: {best_model[2]:.4f} ({best_model[2]:.2%})")

print("\n🎉 ¡LISTO PARA A/B TESTING!")
