"""
VERSIÓN RÁPIDA - Comparación de modelos de ensemble optimizada para velocidad

Características:
- Usa submuestra de datos (10% del dataset)
- Grid de parámetros reducido
- Menos folds en validación cruzada
- Resultados en ~5-10 minutos

Modelos incluidos:
1. RandomForest (sklearn)
2. ExtraTrees (sklearn) 
3. GradientBoosting (sklearn)
4. XGBoost
5. LightGBM
6. CatBoost
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib
import time

# Modelos avanzados
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

try:
    import catboost as cb
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False


def fast_ensemble_comparison(X, y, sample_size=0.1, random_state=42):
    """
    Comparación rápida de modelos de ensemble
    
    Parameters:
    - X, y: datos completos
    - sample_size: fracción del dataset a usar (0.1 = 10%)
    - random_state: semilla para reproducibilidad
    
    Returns:
    - DataFrame con resultados
    - Mejor modelo entrenado
    """
    
    print(f"\n🚀 COMPARACIÓN RÁPIDA DE ENSEMBLES")
    print(f"📊 Usando {sample_size*100:.0f}% del dataset ({int(len(X)*sample_size):,} muestras)")
    print("="*70)
    
    # 1. SUBSAMPLE DE DATOS
    print("1. Creando submuestra de datos...")
    if sample_size < 1.0:
        X_sample, _, y_sample, _ = train_test_split(
            X, y, train_size=sample_size, random_state=random_state, stratify=y
        )
    else:
        X_sample, y_sample = X, y
    
    print(f"   Datos originales: {X.shape[0]:,} muestras")
    print(f"   Datos de muestra: {X_sample.shape[0]:,} muestras")
    print(f"   Clases: {sorted(y_sample.unique())}")
    
    # Convertir clases a 0-based
    y_original = y_sample.copy()
    y_sample = y_sample - 1
    print(f"   Clases convertidas: {sorted(y_sample.unique())}")
    
    # 2. DIVIDIR DATOS
    print("\n2. Dividiendo datos...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_sample, y_sample, test_size=0.2, random_state=random_state, stratify=y_sample
    )
    print(f"   Entrenamiento: {X_train.shape[0]:,} muestras")
    print(f"   Prueba: {X_test.shape[0]:,} muestras")
    
    # 3. ESCALAR DATOS
    print("\n3. Escalando datos...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 4. DEFINIR MODELOS CON PARÁMETROS RÁPIDOS
    print("\n4. Preparando modelos (parámetros optimizados para velocidad)...")
    models = {}
    
    # Modelos básicos con parámetros reducidos
    models['RandomForest'] = RandomForestClassifier(
        random_state=random_state, 
        n_estimators=50,  # Reducido de 100
        max_depth=10,     # Limitado para velocidad
        n_jobs=-1
    )
    
    models['ExtraTrees'] = ExtraTreesClassifier(
        random_state=random_state, 
        n_estimators=50,  # Reducido de 100
        max_depth=10,     # Limitado para velocidad
        n_jobs=-1
    )
    
    models['GradientBoosting'] = GradientBoostingClassifier(
        random_state=random_state, 
        n_estimators=50,  # Reducido de 100
        max_depth=5,      # Reducido para velocidad
        learning_rate=0.1
    )
    
    # XGBoost con parámetros rápidos
    if XGBOOST_AVAILABLE:
        models['XGBoost'] = xgb.XGBClassifier(
            random_state=random_state,
            eval_metric='mlogloss',
            verbosity=0,
            n_estimators=50,  # Reducido
            max_depth=6,      # Reducido
            n_jobs=-1
        )
    
    # LightGBM con parámetros rápidos
    if LIGHTGBM_AVAILABLE:
        models['LightGBM'] = lgb.LGBMClassifier(
            random_state=random_state,
            verbosity=-1,
            force_col_wise=True,
            n_estimators=50,  # Reducido
            max_depth=6,      # Reducido
            n_jobs=-1
        )
    
    # CatBoost con parámetros rápidos
    if CATBOOST_AVAILABLE:
        models['CatBoost'] = cb.CatBoostClassifier(
            random_state=random_state,
            verbose=False,
            iterations=50,    # Reducido
            depth=6,          # Reducido
            thread_count=-1
        )
    
    print(f"   Total de modelos: {len(models)}")
    for name in models.keys():
        print(f"   - {name}")
    
    # 5. ENTRENAR Y EVALUAR (BASELINE)
    print("\n5. Entrenando modelos baseline...")
    baseline_results = []
    
    for name, model in models.items():
        print(f"   - {name}...")
        start_time = time.time()
        
        # Elegir datos según el tipo de modelo
        if name in ['XGBoost', 'LightGBM', 'CatBoost', 'GradientBoosting']:
            X_train_use = X_train_scaled
            X_test_use = X_test_scaled
        else:
            X_train_use = X_train
            X_test_use = X_test
        
        # Entrenar modelo
        model.fit(X_train_use, y_train)
        
        # Predecir en test
        y_pred = model.predict(X_test_use)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        # Validación cruzada rápida (2 folds)
        cv_scores = cross_val_score(model, X_train_use, y_train, cv=2)
        cv_accuracy = cv_scores.mean()
        
        # Calcular overfitting
        overfitting = abs(test_accuracy - cv_accuracy)
        
        # Tiempo de entrenamiento
        training_time = time.time() - start_time
        
        # Guardar resultados
        baseline_results.append({
            'Modelo': name,
            'Accuracy_Test': round(test_accuracy, 4),
            'Accuracy_CV': round(cv_accuracy, 4),
            'Overfitting': round(overfitting, 4),
            'Tiempo_Entrenamiento': round(training_time, 2),
            'Cumple_Requisito': 'SÍ' if overfitting < 0.05 else 'NO'
        })
        
        print(f"     Test: {test_accuracy:.4f}, CV: {cv_accuracy:.4f}, Overfitting: {overfitting:.4f}, Tiempo: {training_time:.1f}s")
    
    # 6. OPTIMIZACIÓN RÁPIDA DE LOS 3 MEJORES MODELOS
    print("\n6. Optimizando los 3 mejores modelos...")
    
    # Ordenar por accuracy y tomar los 3 mejores
    baseline_df = pd.DataFrame(baseline_results)
    baseline_df = baseline_df.sort_values('Accuracy_Test', ascending=False)
    top_3_models = baseline_df.head(3)['Modelo'].tolist()
    
    print(f"   Modelos a optimizar: {top_3_models}")
    
    # Grids de parámetros reducidos para optimización rápida
    param_grids = {
        'RandomForest': {
            'n_estimators': [50, 100],
            'max_depth': [10, 15, None],
            'min_samples_split': [2, 5]
        },
        'ExtraTrees': {
            'n_estimators': [50, 100],
            'max_depth': [10, 15, None],
            'min_samples_split': [2, 5]
        },
        'GradientBoosting': {
            'n_estimators': [50, 100],
            'learning_rate': [0.05, 0.1, 0.15],
            'max_depth': [3, 5]
        },
        'XGBoost': {
            'n_estimators': [50, 100],
            'max_depth': [6, 8],
            'learning_rate': [0.05, 0.1, 0.15]
        },
        'LightGBM': {
            'n_estimators': [50, 100],
            'max_depth': [6, 8],
            'learning_rate': [0.05, 0.1, 0.15]
        },
        'CatBoost': {
            'iterations': [50, 100],
            'depth': [6, 8],
            'learning_rate': [0.05, 0.1, 0.15]
        }
    }
    
    optimization_results = []
    
    for model_name in top_3_models:
        if model_name not in models:
            continue
            
        print(f"\n   🔧 Optimizando {model_name}...")
        start_time = time.time()
        
        # Crear modelo base
        base_model = models[model_name]
        
        # Usar datos escalados si es necesario
        if model_name in ['XGBoost', 'LightGBM', 'CatBoost', 'GradientBoosting']:
            X_train_use = X_train_scaled
            X_test_use = X_test_scaled
        else:
            X_train_use = X_train
            X_test_use = X_test
        
        # Grid Search rápido (2 folds)
        grid_search = GridSearchCV(
            base_model, 
            param_grids[model_name], 
            cv=2,  # Solo 2 folds
            scoring='accuracy',
            n_jobs=-1,
            verbose=0
        )
        
        grid_search.fit(X_train_use, y_train)
        
        # Evaluar mejor modelo
        best_model = grid_search.best_estimator_
        y_pred = best_model.predict(X_test_use)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        optimization_time = time.time() - start_time
        
        print(f"     Mejor accuracy: {test_accuracy:.4f}")
        print(f"     Mejores parámetros: {grid_search.best_params_}")
        print(f"     Tiempo optimización: {optimization_time:.1f}s")
        
        optimization_results.append({
            'Modelo': f"{model_name}_Optimized",
            'Accuracy_Test': round(test_accuracy, 4),
            'Mejores_Parámetros': str(grid_search.best_params_),
            'Tiempo_Optimización': round(optimization_time, 2)
        })
    
    # 7. RESULTADOS FINALES
    print("\n7. RESULTADOS FINALES:")
    print("="*70)
    
    # Combinar resultados
    final_results = []
    
    # Agregar baseline
    for _, row in baseline_df.iterrows():
        final_results.append({
            'Modelo': row['Modelo'],
            'Accuracy_Test': row['Accuracy_Test'],
            'Accuracy_CV': row['Accuracy_CV'],
            'Overfitting': row['Overfitting'],
            'Tiempo_Entrenamiento': row['Tiempo_Entrenamiento'],
            'Estado': 'Baseline'
        })
    
    # Agregar optimizados
    for result in optimization_results:
        final_results.append({
            'Modelo': result['Modelo'],
            'Accuracy_Test': result['Accuracy_Test'],
            'Accuracy_CV': 'N/A',
            'Overfitting': 'N/A',
            'Tiempo_Entrenamiento': result['Tiempo_Optimización'],
            'Estado': 'Optimizado'
        })
    
    final_df = pd.DataFrame(final_results)
    final_df = final_df.sort_values('Accuracy_Test', ascending=False)
    
    print(final_df.to_string(index=False))
    
    # 8. GUARDAR MEJOR MODELO
    best_model_name = final_df.iloc[0]['Modelo']
    best_accuracy = final_df.iloc[0]['Accuracy_Test']
    
    print(f"\n💾 MEJOR MODELO:")
    print(f"   - Modelo: {best_model_name}")
    print(f"   - Accuracy: {best_accuracy:.4f}")
    
    # Guardar el mejor modelo baseline (más simple)
    best_baseline = baseline_df.iloc[0]
    best_baseline_model = models[best_baseline['Modelo']]
    
    # Re-entrenar con datos escalados si es necesario
    if best_baseline['Modelo'] in ['XGBoost', 'LightGBM', 'CatBoost', 'GradientBoosting']:
        best_baseline_model.fit(X_train_scaled, y_train)
    else:
        best_baseline_model.fit(X_train, y_train)
    
    joblib.dump(best_baseline_model, 'best_fast_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print(f"   - Archivo: best_fast_model.pkl")
    print(f"   - Scaler: scaler.pkl")
    
    return final_df, best_baseline_model, scaler


def usage_example():
    """
    Ejemplo de uso del script rápido
    """
    print("=== EJEMPLO DE USO RÁPIDO ===")
    print("""
    # 1. Cargar datos
    from ucimlrepo import fetch_ucirepo
    covertype = fetch_ucirepo(id=31)
    X = covertype.data.features
    y = covertype.data.targets.iloc[:, 0]
    
    # 2. Comparación rápida (10% de datos, ~5-10 minutos)
    resultados, mejor_modelo, scaler = fast_ensemble_comparison(X, y, sample_size=0.1)
    
    # 3. Ver resultados
    print(resultados)
    
    # 4. Usar modelo para predicciones
    predicciones = mejor_modelo.predict(X_test)
    """)


if __name__ == "__main__":
    usage_example()
