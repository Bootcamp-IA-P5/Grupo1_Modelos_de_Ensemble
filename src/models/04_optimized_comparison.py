"""
Script optimizado para comparar modelos de ensemble SIN GradientBoosting

Incluye:
- RandomForest (ya entrenado - 95.38%)
- ExtraTrees (ya entrenado - 95.27%) 
- XGBoost (optimizar)
- LightGBM (optimizar)
- CatBoost (optimizar)

Excluye:
- GradientBoosting (muy lento con datasets grandes)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, VotingClassifier
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


def optimized_ensemble_comparison(X, y, random_state=42):
    """
    Comparación optimizada de modelos de ensemble (sin GradientBoosting)
    
    Parameters:
    - X, y: datos completos
    - random_state: semilla para reproducibilidad
    
    Returns:
    - DataFrame con resultados
    - Mejor modelo entrenado
    """
    
    print(f"\n🚀 COMPARACIÓN OPTIMIZADA DE ENSEMBLES")
    print(f"📊 Dataset completo: {X.shape[0]:,} muestras")
    print("="*70)
    
    # Convertir clases a 0-based
    y_original = y.copy()
    y = y - 1
    print(f"Clases: {sorted(y.unique())}")
    
    # 1. DIVIDIR DATOS
    print("\n1. Dividiendo datos...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )
    print(f"   Entrenamiento: {X_train.shape[0]:,} muestras")
    print(f"   Prueba: {X_test.shape[0]:,} muestras")
    
    # 2. ESCALAR DATOS
    print("\n2. Escalando datos...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 3. RESULTADOS YA CONOCIDOS (del script anterior)
    print("\n3. Resultados ya obtenidos:")
    known_results = [
        {
            'Modelo': 'RandomForest',
            'Accuracy_Test': 0.9538,
            'Accuracy_CV': 0.9462,
            'Overfitting': 0.0076,
            'Tiempo_Entrenamiento': 710.34,
            'Estado': 'Ya entrenado'
        },
        {
            'Modelo': 'ExtraTrees',
            'Accuracy_Test': 0.9527,
            'Accuracy_CV': 0.9457,
            'Overfitting': 0.0069,
            'Tiempo_Entrenamiento': 256.36,
            'Estado': 'Ya entrenado'
        }
    ]
    
    for result in known_results:
        print(f"   - {result['Modelo']}: {result['Accuracy_Test']:.4f} (ya entrenado)")
    
    # 4. DEFINIR MODELOS A OPTIMIZAR
    print("\n4. Preparando modelos a optimizar...")
    models_to_optimize = {}
    
    # XGBoost
    if XGBOOST_AVAILABLE:
        models_to_optimize['XGBoost'] = xgb.XGBClassifier(
            random_state=random_state,
            eval_metric='mlogloss',
            verbosity=0,
            n_jobs=-1
        )
    
    # LightGBM
    if LIGHTGBM_AVAILABLE:
        models_to_optimize['LightGBM'] = lgb.LGBMClassifier(
            random_state=random_state,
            verbosity=-1,
            force_col_wise=True,
            n_jobs=-1
        )
    
    # CatBoost
    if CATBOOST_AVAILABLE:
        models_to_optimize['CatBoost'] = cb.CatBoostClassifier(
            random_state=random_state,
            verbose=False,
            thread_count=-1
        )
    
    print(f"   Modelos a optimizar: {list(models_to_optimize.keys())}")
    
    # 5. OPTIMIZAR MODELOS
    print("\n5. Optimizando modelos...")
    optimization_results = []
    
    # Grids de parámetros optimizados para velocidad
    param_grids = {
        'XGBoost': {
            'n_estimators': [200, 300, 500],
            'max_depth': [6, 8, 10],
            'learning_rate': [0.05, 0.1, 0.15],
            'subsample': [0.8, 0.9, 1.0]
        },
        'LightGBM': {
            'n_estimators': [200, 300, 500],
            'max_depth': [6, 8, 10],
            'learning_rate': [0.05, 0.1, 0.15],
            'subsample': [0.8, 0.9, 1.0]
        },
        'CatBoost': {
            'iterations': [200, 300, 500],
            'depth': [6, 8, 10],
            'learning_rate': [0.05, 0.1, 0.15]
        }
    }
    
    for model_name, model in models_to_optimize.items():
        print(f"\n   🔧 Optimizando {model_name}...")
        start_time = time.time()
        
        # Usar datos escalados
        X_train_use = X_train_scaled
        X_test_use = X_test_scaled
        
        # Grid Search (3 folds para balance velocidad/precisión)
        grid_search = GridSearchCV(
            model, 
            param_grids[model_name], 
            cv=3,
            scoring='accuracy',
            n_jobs=-1,
            verbose=0
        )
        
        grid_search.fit(X_train_use, y_train)
        
        # Evaluar mejor modelo
        best_model = grid_search.best_estimator_
        y_pred = best_model.predict(X_test_use)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        # Validación cruzada del mejor modelo
        cv_scores = cross_val_score(best_model, X_train_use, y_train, cv=3)
        cv_accuracy = cv_scores.mean()
        overfitting = abs(test_accuracy - cv_accuracy)
        
        optimization_time = time.time() - start_time
        
        print(f"     Mejor accuracy: {test_accuracy:.4f}")
        print(f"     CV accuracy: {cv_accuracy:.4f}")
        print(f"     Overfitting: {overfitting:.4f}")
        print(f"     Mejores parámetros: {grid_search.best_params_}")
        print(f"     Tiempo optimización: {optimization_time:.1f}s")
        
        optimization_results.append({
            'Modelo': f"{model_name}_Optimized",
            'Accuracy_Test': round(test_accuracy, 4),
            'Accuracy_CV': round(cv_accuracy, 4),
            'Overfitting': round(overfitting, 4),
            'Tiempo_Entrenamiento': round(optimization_time, 2),
            'Estado': 'Optimizado',
            'Mejores_Parámetros': str(grid_search.best_params_)
        })
    
    # 6. CREAR VOTING CLASSIFIER
    print("\n6. Creando VotingClassifier...")
    
    # Seleccionar los 3 mejores modelos
    all_results = known_results + optimization_results
    all_results_df = pd.DataFrame(all_results)
    all_results_df = all_results_df.sort_values('Accuracy_Test', ascending=False)
    
    top_3_models = all_results_df.head(3)['Modelo'].tolist()
    print(f"   Modelos seleccionados: {top_3_models}")
    
    # Crear VotingClassifier con los mejores modelos
    estimators = []
    
    # Agregar RandomForest y ExtraTrees (ya entrenados)
    if 'RandomForest' in top_3_models:
        rf_model = RandomForestClassifier(random_state=random_state, n_estimators=100)
        rf_model.fit(X_train, y_train)  # Re-entrenar rápidamente
        estimators.append(('RandomForest', rf_model))
    
    if 'ExtraTrees' in top_3_models:
        et_model = ExtraTreesClassifier(random_state=random_state, n_estimators=100)
        et_model.fit(X_train, y_train)  # Re-entrenar rápidamente
        estimators.append(('ExtraTrees', et_model))
    
    # Agregar modelos optimizados
    for result in optimization_results:
        model_name = result['Modelo'].replace('_Optimized', '')
        if result['Modelo'] in top_3_models:
            # Encontrar el modelo optimizado
            for name, model in models_to_optimize.items():
                if name == model_name:
                    estimators.append((name, model))
                    break
    
    if len(estimators) >= 2:
        voting_clf = VotingClassifier(
            estimators=estimators,
            voting='soft'
        )
        
        # Entrenar VotingClassifier
        print("   Entrenando VotingClassifier...")
        voting_clf.fit(X_train_scaled, y_train)
        
        # Evaluar VotingClassifier
        y_pred_voting = voting_clf.predict(X_test_scaled)
        voting_accuracy = accuracy_score(y_test, y_pred_voting)
        
        print(f"   VotingClassifier accuracy: {voting_accuracy:.4f}")
        
        optimization_results.append({
            'Modelo': 'VotingClassifier',
            'Accuracy_Test': round(voting_accuracy, 4),
            'Accuracy_CV': 'N/A',
            'Overfitting': 'N/A',
            'Tiempo_Entrenamiento': 'N/A',
            'Estado': 'Ensemble',
            'Mejores_Parámetros': f"Combinación de {len(estimators)} modelos"
        })
    
    # 7. RESULTADOS FINALES
    print("\n7. RESULTADOS FINALES:")
    print("="*70)
    
    # Combinar todos los resultados
    final_results = known_results + optimization_results
    final_df = pd.DataFrame(final_results)
    final_df = final_df.sort_values('Accuracy_Test', ascending=False)
    
    print(final_df.to_string(index=False))
    
    # 8. GUARDAR MEJOR MODELO
    best_model_name = final_df.iloc[0]['Modelo']
    best_accuracy = final_df.iloc[0]['Accuracy_Test']
    
    print(f"\n💾 MEJOR MODELO:")
    print(f"   - Modelo: {best_model_name}")
    print(f"   - Accuracy: {best_accuracy:.4f}")
    
    # Guardar el mejor modelo
    if best_model_name == 'VotingClassifier':
        joblib.dump(voting_clf, 'best_optimized_model.pkl')
        print("   - Archivo: best_optimized_model.pkl")
    elif best_model_name in ['RandomForest', 'ExtraTrees']:
        # Re-entrenar y guardar
        if best_model_name == 'RandomForest':
            best_model = RandomForestClassifier(random_state=random_state, n_estimators=100)
            best_model.fit(X_train, y_train)
        else:
            best_model = ExtraTreesClassifier(random_state=random_state, n_estimators=100)
            best_model.fit(X_train, y_train)
        
        joblib.dump(best_model, 'best_optimized_model.pkl')
        print("   - Archivo: best_optimized_model.pkl")
    else:
        # Guardar modelo optimizado
        model_name = best_model_name.replace('_Optimized', '')
        for name, model in models_to_optimize.items():
            if name == model_name:
                joblib.dump(model, 'best_optimized_model.pkl')
                print("   - Archivo: best_optimized_model.pkl")
                break
    
    joblib.dump(scaler, 'scaler_optimized.pkl')
    print("   - Scaler: scaler_optimized.pkl")
    
    return final_df


def usage_example():
    """
    Ejemplo de uso del script optimizado
    """
    print("=== EJEMPLO DE USO OPTIMIZADO ===")
    print("""
    # 1. Cargar datos
    from ucimlrepo import fetch_ucirepo
    covertype = fetch_ucirepo(id=31)
    X = covertype.data.features
    y = covertype.data.targets.iloc[:, 0]
    
    # 2. Comparación optimizada (sin GradientBoosting)
    resultados = optimized_ensemble_comparison(X, y)
    
    # 3. Ver resultados
    print(resultados)
    """)


if __name__ == "__main__":
    usage_example()
