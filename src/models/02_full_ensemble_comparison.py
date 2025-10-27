"""
Script para comparar y optimizar TODOS los modelos de ensemble disponibles

Modelos incluidos:
1. RandomForest (sklearn)
2. ExtraTrees (sklearn) 
3. GradientBoosting (sklearn)
4. XGBoost
5. LightGBM
6. CatBoost
7. VotingClassifier (combinación de los mejores)

Estrategia:
1. Comparación baseline (parámetros por defecto)
2. Optimización individual de cada modelo de ensemble
3. Comparación final con todos los modelos optimizados
4. Creación de VotingClassifier con los mejores modelos
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import time

# Modelos avanzados
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
    print("✅ XGBoost disponible")
except ImportError as e:
    XGBOOST_AVAILABLE = False
    print("❌ XGBoost no disponible:", str(e))

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
    print("✅ LightGBM disponible")
except ImportError as e:
    LIGHTGBM_AVAILABLE = False
    print("❌ LightGBM no disponible:", str(e))

try:
    import catboost as cb
    CATBOOST_AVAILABLE = True
    print("✅ CatBoost disponible")
except ImportError as e:
    CATBOOST_AVAILABLE = False
    print("❌ CatBoost no disponible:", str(e))


def compare_ensemble_models_baseline(X, y):
    """
    Comparar todos los modelos de ensemble con parámetros por defecto
    
    Returns:
    - DataFrame con resultados baseline
    - Datos divididos y scaler para optimización
    """
    
    print("\n" + "="*80)
    print("🔍 COMPARACIÓN BASELINE - TODOS LOS MODELOS DE ENSEMBLE")
    print("="*80)
    print(f"Datos: {X.shape[0]} filas, {X.shape[1]} columnas")
    print(f"Clases: {sorted(y.unique())}")
    
    # Convertir clases a 0-based para compatibilidad
    y_original = y.copy()
    y = y - 1
    print(f"Clases convertidas: {sorted(y.unique())}")
    
    # 1. DIVIDIR DATOS
    print("\n1. Dividiendo datos...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Entrenamiento: {X_train.shape[0]} muestras")
    print(f"   Prueba: {X_test.shape[0]} muestras")
    
    # 2. ESCALAR DATOS
    print("\n2. Escalando datos...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 3. DEFINIR TODOS LOS MODELOS
    print("\n3. Preparando modelos de ensemble...")
    models = {}
    
    # Modelos básicos de sklearn
    models['RandomForest'] = RandomForestClassifier(random_state=42, n_estimators=100)
    models['ExtraTrees'] = ExtraTreesClassifier(random_state=42, n_estimators=100)
    models['GradientBoosting'] = GradientBoostingClassifier(random_state=42, n_estimators=100)
    
    # XGBoost
    if XGBOOST_AVAILABLE:
        models['XGBoost'] = xgb.XGBClassifier(
            random_state=42,
            eval_metric='mlogloss',
            verbosity=0
        )
    
    # LightGBM
    if LIGHTGBM_AVAILABLE:
        models['LightGBM'] = lgb.LGBMClassifier(
            random_state=42,
            verbosity=-1,
            force_col_wise=True
        )
    
    # CatBoost
    if CATBOOST_AVAILABLE:
        models['CatBoost'] = cb.CatBoostClassifier(
            random_state=42,
            verbose=False
        )
    
    print(f"   Total de modelos: {len(models)}")
    for name in models.keys():
        print(f"   - {name}")
    
    # 4. ENTRENAR Y EVALUAR
    print("\n4. Entrenando modelos baseline...")
    results = []
    
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
        
        # Validación cruzada (3 folds para velocidad)
        cv_scores = cross_val_score(model, X_train_use, y_train, cv=3)
        cv_accuracy = cv_scores.mean()
        
        # Calcular overfitting
        overfitting = abs(test_accuracy - cv_accuracy)
        
        # Tiempo de entrenamiento
        training_time = time.time() - start_time
        
        # Guardar resultados
        results.append({
            'Modelo': name,
            'Accuracy_Test': round(test_accuracy, 4),
            'Accuracy_CV': round(cv_accuracy, 4),
            'Overfitting': round(overfitting, 4),
            'Tiempo_Entrenamiento': round(training_time, 2),
            'Cumple_Requisito': 'SÍ' if overfitting < 0.05 else 'NO'
        })
        
        print(f"     Test: {test_accuracy:.4f}, CV: {cv_accuracy:.4f}, Overfitting: {overfitting:.4f}, Tiempo: {training_time:.2f}s")
    
    # 5. MOSTRAR RESULTADOS
    print("\n5. RESULTADOS BASELINE:")
    print("="*80)
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Accuracy_Test', ascending=False)
    
    print(results_df.to_string(index=False))
    
    return results_df, X_train, X_test, y_train, y_test, scaler


def optimize_ensemble_model(model_name, model, X_train, X_test, y_train, y_test, scaler):
    """
    Optimizar hiperparámetros de un modelo de ensemble específico
    
    Parameters:
    - model_name: nombre del modelo
    - model: instancia del modelo
    - X_train, X_test, y_train, y_test: datos divididos
    - scaler: scaler ajustado
    
    Returns:
    - Mejor modelo, mejores parámetros, mejor score
    """
    
    print(f"\n🔧 OPTIMIZANDO {model_name.upper()}")
    print("-" * 50)
    
    # Usar datos escalados para modelos que lo necesiten
    if model_name in ['XGBoost', 'LightGBM', 'CatBoost', 'GradientBoosting']:
        X_train_use = scaler.transform(X_train)
        X_test_use = scaler.transform(X_test)
    else:
        X_train_use = X_train
        X_test_use = X_test
    
    # Definir grids de parámetros específicos para cada modelo
    param_grids = {
        'RandomForest': {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        },
        'ExtraTrees': {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        },
        'GradientBoosting': {
            'n_estimators': [100, 200, 300],
            'learning_rate': [0.05, 0.1, 0.15],
            'max_depth': [3, 5, 7],
            'subsample': [0.8, 0.9, 1.0]
        },
        'XGBoost': {
            'n_estimators': [200, 300, 500],
            'max_depth': [6, 8, 10],
            'learning_rate': [0.05, 0.1, 0.15],
            'subsample': [0.8, 0.9, 1.0],
            'colsample_bytree': [0.8, 0.9, 1.0]
        },
        'LightGBM': {
            'n_estimators': [200, 300, 500],
            'max_depth': [6, 8, 10],
            'learning_rate': [0.05, 0.1, 0.15],
            'subsample': [0.8, 0.9, 1.0],
            'colsample_bytree': [0.8, 0.9, 1.0]
        },
        'CatBoost': {
            'iterations': [200, 300, 500],
            'depth': [6, 8, 10],
            'learning_rate': [0.05, 0.1, 0.15],
            'subsample': [0.8, 0.9, 1.0]
        }
    }
    
    if model_name not in param_grids:
        print(f"❌ No hay grid de parámetros definido para {model_name}")
        return None, None, 0
    
    param_grid = param_grids[model_name]
    
    # Calcular total de combinaciones
    total_combinations = 1
    for param, values in param_grid.items():
        total_combinations *= len(values)
    
    print(f"🔍 Probando {total_combinations} combinaciones de parámetros...")
    
    # Grid Search con validación cruzada
    grid_search = GridSearchCV(
        model, 
        param_grid, 
        cv=3, 
        scoring='accuracy',
        n_jobs=-1,
        verbose=0
    )
    
    start_time = time.time()
    grid_search.fit(X_train_use, y_train)
    optimization_time = time.time() - start_time
    
    # Obtener mejores resultados
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_
    
    # Evaluar en test
    y_pred = best_model.predict(X_test_use)
    test_accuracy = accuracy_score(y_test, y_pred)
    
    print(f"🏆 MEJOR {model_name.upper()}:")
    print(f"   - CV Score: {best_score:.4f}")
    print(f"   - Test Score: {test_accuracy:.4f}")
    print(f"   - Parámetros: {best_params}")
    print(f"   - Tiempo optimización: {optimization_time:.2f}s")
    
    return best_model, best_params, test_accuracy


def create_voting_classifier(optimized_models):
    """
    Crear VotingClassifier con los mejores modelos optimizados
    
    Parameters:
    - optimized_models: diccionario con modelos optimizados
    
    Returns:
    - VotingClassifier entrenado
    """
    
    print("\n🗳️ CREANDO VOTING CLASSIFIER")
    print("-" * 50)
    
    # Seleccionar los 3 mejores modelos (o todos si son menos de 3)
    model_names = list(optimized_models.keys())
    if len(model_names) >= 3:
        # Ordenar por accuracy y tomar los 3 mejores
        model_scores = [(name, optimized_models[name]['score']) for name in model_names]
        model_scores.sort(key=lambda x: x[1], reverse=True)
        best_models = [name for name, _ in model_scores[:3]]
    else:
        best_models = model_names
    
    print(f"Modelos seleccionados para VotingClassifier: {best_models}")
    
    # Crear lista de estimadores para VotingClassifier
    estimators = []
    for name in best_models:
        model = optimized_models[name]['model']
        estimators.append((name, model))
    
    # Crear VotingClassifier
    voting_clf = VotingClassifier(
        estimators=estimators,
        voting='soft'  # Usar probabilidades para votación suave
    )
    
    return voting_clf


def compare_all_ensemble_models(X, y):
    """
    Función principal: comparar y optimizar TODOS los modelos de ensemble
    
    Parameters:
    - X: datos de entrada (features)
    - y: variable objetivo
    
    Returns:
    - DataFrame con resultados finales
    - Diccionario con modelos optimizados
    """
    
    print("\n" + "="*80)
    print("🚀 COMPARACIÓN COMPLETA DE MODELOS DE ENSEMBLE")
    print("="*80)
    
    # 1. COMPARACIÓN BASELINE
    baseline_results, X_train, X_test, y_train, y_test, scaler = compare_ensemble_models_baseline(X, y)
    
    # 2. OPTIMIZAR CADA MODELO DE ENSEMBLE
    print("\n" + "="*80)
    print("🔧 OPTIMIZACIÓN DE HIPERPARÁMETROS")
    print("="*80)
    
    optimized_models = {}
    optimization_results = []
    
    # Modelos a optimizar
    models_to_optimize = {
        'RandomForest': RandomForestClassifier(random_state=42),
        'ExtraTrees': ExtraTreesClassifier(random_state=42),
        'GradientBoosting': GradientBoostingClassifier(random_state=42)
    }
    
    if XGBOOST_AVAILABLE:
        models_to_optimize['XGBoost'] = xgb.XGBClassifier(random_state=42, eval_metric='mlogloss', verbosity=0)
    
    if LIGHTGBM_AVAILABLE:
        models_to_optimize['LightGBM'] = lgb.LGBMClassifier(random_state=42, verbosity=-1, force_col_wise=True)
    
    if CATBOOST_AVAILABLE:
        models_to_optimize['CatBoost'] = cb.CatBoostClassifier(random_state=42, verbose=False)
    
    # Optimizar cada modelo
    for model_name, model in models_to_optimize.items():
        best_model, best_params, best_score = optimize_ensemble_model(
            model_name, model, X_train, X_test, y_train, y_test, scaler
        )
        
        if best_model is not None:
            optimized_models[model_name] = {
                'model': best_model,
                'params': best_params,
                'score': best_score
            }
            
            optimization_results.append({
                'Modelo': f"{model_name}_Optimized",
                'Accuracy_Test': round(best_score, 4),
                'Parámetros': str(best_params)[:100] + "..." if len(str(best_params)) > 100 else str(best_params)
            })
    
    # 3. CREAR VOTING CLASSIFIER
    if len(optimized_models) >= 2:
        voting_clf = create_voting_classifier(optimized_models)
        
        # Entrenar VotingClassifier
        print("\nEntrenando VotingClassifier...")
        if any(name in ['XGBoost', 'LightGBM', 'CatBoost', 'GradientBoosting'] for name in optimized_models.keys()):
            X_train_use = scaler.transform(X_train)
            X_test_use = scaler.transform(X_test)
        else:
            X_train_use = X_train
            X_test_use = X_test
        
        voting_clf.fit(X_train_use, y_train)
        
        # Evaluar VotingClassifier
        y_pred_voting = voting_clf.predict(X_test_use)
        voting_accuracy = accuracy_score(y_test, y_pred_voting)
        
        print(f"🏆 VOTING CLASSIFIER - Accuracy: {voting_accuracy:.4f}")
        
        optimization_results.append({
            'Modelo': 'VotingClassifier',
            'Accuracy_Test': round(voting_accuracy, 4),
            'Parámetros': f"Combinación de {len(optimized_models)} modelos"
        })
    
    # 4. COMPARACIÓN FINAL
    print("\n" + "="*80)
    print("📊 COMPARACIÓN FINAL - TODOS LOS MODELOS OPTIMIZADOS")
    print("="*80)
    
    # Combinar resultados baseline y optimizados
    final_results = []
    
    # Agregar resultados baseline (sin optimizar)
    for _, row in baseline_results.iterrows():
        final_results.append({
            'Modelo': row['Modelo'],
            'Accuracy_Test': row['Accuracy_Test'],
            'Accuracy_CV': row['Accuracy_CV'],
            'Overfitting': row['Overfitting'],
            'Tiempo_Entrenamiento': row['Tiempo_Entrenamiento'],
            'Estado': 'Baseline'
        })
    
    # Agregar resultados optimizados
    for result in optimization_results:
        final_results.append({
            'Modelo': result['Modelo'],
            'Accuracy_Test': result['Accuracy_Test'],
            'Accuracy_CV': 'N/A',
            'Overfitting': 'N/A',
            'Tiempo_Entrenamiento': 'N/A',
            'Estado': 'Optimizado'
        })
    
    final_df = pd.DataFrame(final_results)
    final_df = final_df.sort_values('Accuracy_Test', ascending=False)
    
    print(final_df.to_string(index=False))
    
    # 5. GUARDAR MEJOR MODELO
    if optimization_results:
        best_model_name = final_df.iloc[0]['Modelo']
        best_accuracy = final_df.iloc[0]['Accuracy_Test']
        
        print(f"\n💾 GUARDANDO MEJOR MODELO:")
        print(f"   - Modelo: {best_model_name}")
        print(f"   - Accuracy: {best_accuracy:.4f}")
        
        if best_model_name == 'VotingClassifier':
            joblib.dump(voting_clf, 'best_ensemble_model.pkl')
            print("   - Archivo: best_ensemble_model.pkl")
        else:
            # Encontrar el modelo en optimized_models
            base_name = best_model_name.replace('_Optimized', '')
            if base_name in optimized_models:
                joblib.dump(optimized_models[base_name]['model'], 'best_ensemble_model.pkl')
                print("   - Archivo: best_ensemble_model.pkl")
                print(f"   - Parámetros: {optimized_models[base_name]['params']}")
    
    return final_df, optimized_models


def usage_example():
    """
    Ejemplo de uso del script
    """
    print("=== EJEMPLO DE USO ===")
    print("""
    # 1. Cargar datos
    from ucimlrepo import fetch_ucirepo
    covertype = fetch_ucirepo(id=31)
    X = covertype.data.features
    y = covertype.data.targets.iloc[:, 0]
    
    # 2. Comparar TODOS los modelos de ensemble
    resultados, modelos_optimizados = compare_all_ensemble_models(X, y)
    
    # 3. Ver resultados
    print(resultados)
    """)


if __name__ == "__main__":
    usage_example()
