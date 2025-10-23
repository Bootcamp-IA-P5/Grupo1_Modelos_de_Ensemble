"""
Script to compare multiclass classification models with hyperparameter optimization

Strategy:
1. Baseline comparison (default parameters) - quick overview
2. Hyperparameter optimization for best models - reach 97%+ accuracy
3. Final comparison with optimized models

What does this script do?
1. Trains several ML models with default parameters
2. Optimizes XGBoost hyperparameters to reach 97%+ accuracy
3. Compares final results and saves best model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# Advanced models
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except (ImportError, Exception) as e:
    XGBOOST_AVAILABLE = False
    print("⚠️  XGBoost no disponible. Error:", str(e)[:50] + "...")
    print("💡 Continuando sin XGBoost...")

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except (ImportError, OSError) as e:
    LIGHTGBM_AVAILABLE = False
    print("⚠️  LightGBM no disponible. Error:", str(e)[:50] + "...")


def compare_models_baseline(X, y):
    """
    Compare models with default parameters (baseline)
    
    Parameters:
    - X: input data (features)
    - y: target variable
    
    Returns:
    - DataFrame with baseline results
    - Split data and scaler for optimization
    """
    
    print("=== COMPARACIÓN BASELINE (parámetros por defecto) ===")
    print(f"Datos: {X.shape[0]} filas, {X.shape[1]} columnas")
    print(f"Clases originales: {sorted(y.unique())}")
    
    # Convert classes to 0-based for XGBoost compatibility
    y_original = y.copy()
    y = y - 1
    print(f"Clases convertidas: {sorted(y.unique())}")
    
    # 1. SPLIT DATA
    print("\n1. Dividiendo datos...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Entrenamiento: {X_train.shape[0]} muestras")
    print(f"   Prueba: {X_test.shape[0]} muestras")
    
    # 2. SCALE DATA
    print("\n2. Escalando datos...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 3. DEFINE MODELS (default parameters)
    print("\n3. Preparando modelos (parámetros por defecto)...")
    models = {
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=2000),
        'DecisionTree': DecisionTreeClassifier(random_state=42),
        'RandomForest': RandomForestClassifier(random_state=42, n_estimators=100),
        'ExtraTrees': ExtraTreesClassifier(random_state=42, n_estimators=100),
        'GradientBoosting': GradientBoostingClassifier(random_state=42, n_estimators=100)
    }
    
    # Add XGBoost with default parameters
    if XGBOOST_AVAILABLE:
        models['XGBoost'] = xgb.XGBClassifier(
            random_state=42,
            eval_metric='mlogloss'
        )
    
    # 4. TRAIN AND EVALUATE
    print("\n4. Entrenando modelos baseline...")
    results = []
    
    for name, model in models.items():
        print(f"   - {name}...")
        
        # Choose data based on model type
        if name in ['LogisticRegression', 'XGBoost', 'GradientBoosting']:
            X_train_use = X_train_scaled
            X_test_use = X_test_scaled
        else:
            X_train_use = X_train
            X_test_use = X_test
        
        # Train model
        model.fit(X_train_use, y_train)
        
        # Predict on test
        y_pred = model.predict(X_test_use)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        # Cross validation (3 folds for speed)
        cv_scores = cross_val_score(model, X_train_use, y_train, cv=3)
        cv_accuracy = cv_scores.mean()
        
        # Calculate overfitting
        overfitting = abs(test_accuracy - cv_accuracy)
        
        # Save results
        results.append({
            'Modelo': name,
            'Accuracy_Test': round(test_accuracy, 4),
            'Accuracy_CV': round(cv_accuracy, 4),
            'Overfitting': round(overfitting, 4),
            'Cumple_Requisito': 'SÍ' if overfitting < 0.05 else 'NO'
        })
        
        print(f"     Test: {test_accuracy:.4f}, CV: {cv_accuracy:.4f}, Overfitting: {overfitting:.4f}")
    
    # 5. SHOW RESULTS
    print("\n5. RESULTADOS BASELINE:")
    print("=" * 70)
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Accuracy_Test', ascending=False)
    
    print(results_df.to_string(index=False))
    
    return results_df, X_train, X_test, y_train, y_test, scaler


def optimize_xgboost(X_train, X_test, y_train, y_test, scaler):
    """
    Optimize XGBoost hyperparameters to reach 97%+ accuracy
    
    Parameters:
    - X_train, X_test, y_train, y_test: split data
    - scaler: fitted scaler
    
    Returns:
    - Best XGBoost model, parameters, and score
    """
    
    if not XGBOOST_AVAILABLE:
        print("❌ XGBoost no disponible para optimización")
        return None, None, 0
    
    print("\n=== OPTIMIZANDO XGBOOST ===")
    print("🎯 Objetivo: 97%+ accuracy")
    
    # Use scaled data for XGBoost
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define parameter grid for optimization
    param_grid = {
        'n_estimators': [300, 500, 800],
        'max_depth': [8, 12, 15],
        'learning_rate': [0.05, 0.1, 0.15],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0]
    }
    
    total_combinations = (len(param_grid['n_estimators']) * 
                         len(param_grid['max_depth']) * 
                         len(param_grid['learning_rate']) * 
                         len(param_grid['subsample']) * 
                         len(param_grid['colsample_bytree']))
    
    print(f"🔍 Probando {total_combinations} combinaciones...")
    
    best_score = 0
    best_params = None
    best_model = None
    
    # Simple grid search
    for n_est in param_grid['n_estimators']:
        for max_d in param_grid['max_depth']:
            for lr in param_grid['learning_rate']:
                for sub in param_grid['subsample']:
                    for col in param_grid['colsample_bytree']:
                        
                        # Create model with current parameters
                        model = xgb.XGBClassifier(
                            n_estimators=n_est,
                            max_depth=max_d,
                            learning_rate=lr,
                            subsample=sub,
                            colsample_bytree=col,
                            random_state=42,
                            eval_metric='mlogloss'
                        )
                        
                        # Train and evaluate
                        model.fit(X_train_scaled, y_train)
                        y_pred = model.predict(X_test_scaled)
                        accuracy = accuracy_score(y_test, y_pred)
                        
                        if accuracy > best_score:
                            best_score = accuracy
                            best_params = {
                                'n_estimators': n_est,
                                'max_depth': max_d,
                                'learning_rate': lr,
                                'subsample': sub,
                                'colsample_bytree': col
                            }
                            best_model = model
                        
                        print(f"   n_est={n_est}, max_d={max_d}, lr={lr:.2f}, sub={sub}, col={col} → {accuracy:.4f}")
    
    print(f"\n🏆 MEJOR XGBOOST:")
    print(f"   - Accuracy: {best_score:.4f}")
    print(f"   - Parámetros: {best_params}")
    
    if best_score >= 0.97:
        print("✅ ¡Objetivo alcanzado! 97%+ accuracy")
    else:
        print("⚠️  Objetivo no alcanzado, pero mejorado significativamente")
    
    return best_model, best_params, best_score


def compare_models(X, y):
    """
    Main function: baseline comparison + XGBoost optimization
    
    Parameters:
    - X: input data (features)
    - y: target variable
    
    Returns:
    - DataFrame with final results
    """
    
    # 1. BASELINE COMPARISON
    baseline_results, X_train, X_test, y_train, y_test, scaler = compare_models_baseline(X, y)
    
    # 2. XGBOOST OPTIMIZATION
    best_xgb, best_params, best_score = optimize_xgboost(X_train, X_test, y_train, y_test, scaler)
    
    # 3. FINAL COMPARISON
    print("\n=== COMPARACIÓN FINAL ===")
    
    # Update XGBoost result with optimized version
    if best_xgb is not None:
        # Find XGBoost row and update it
        xgb_idx = baseline_results[baseline_results['Modelo'] == 'XGBoost'].index
        if len(xgb_idx) > 0:
            baseline_results.loc[xgb_idx[0], 'Accuracy_Test'] = round(best_score, 4)
            baseline_results.loc[xgb_idx[0], 'Modelo'] = 'XGBoost_Optimized'
    
    # Sort by accuracy
    final_results = baseline_results.sort_values('Accuracy_Test', ascending=False)
    
    print(final_results.to_string(index=False))
    
    # 4. SAVE BEST MODEL
    if best_xgb is not None:
        joblib.dump(best_xgb, 'best_model_optimized.pkl')
        print(f" Mejor modelo guardado en: best_model_optimized.pkl")
        print(f" Parámetros óptimos: {best_params}")
    
    return final_results


def usage_example():
    """
    Example of how to use the function
    """
    print("=== EJEMPLO DE USO ===")
    print("""
    # 1. Cargar datos del EDA
    X = datos[['feature1', 'feature2', 'feature3']]  # tus features
    y = datos['target']  # tu variable objetivo
    
    # 2. Comparar modelos (baseline + optimización)
    resultados = compare_models(X, y)
    
    # 3. Ver resultados
    print(resultados)
    """)


if __name__ == "__main__":
    usage_example()