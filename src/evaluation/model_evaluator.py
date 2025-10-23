#!/usr/bin/env python3
"""
EcoPredict- Evaluación Completa del Modelo
Script para generar todas las métricas técnicas necesarias para la presentación
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    confusion_matrix, classification_report, 
    precision_recall_fscore_support, accuracy_score
)
from ucimlrepo import fetch_ucirepo
import warnings
warnings.filterwarnings('ignore')

def main():
    print("EcoPredict - Evaluación Completa del Modelo")
    print("=" * 60)
    
    # Configurar estilo de gráficos
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Cargar datos y modelo
    print("📊 Cargando Forest Cover Type Dataset...")
    covertype = fetch_ucirepo(id=31)
    X = covertype.data.features
    y = covertype.data.targets.iloc[:, 0]
    
    # Convertir clases de 1-7 a 0-6 para compatibilidad con el modelo entrenado
    print("🔄 Convirtiendo clases de 1-7 a 0-6...")
    y_original = y.copy()
    y = y - 1
    
    print("🤖 Cargando modelo optimizado...")
    model = joblib.load('models/best_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    
    # Nombres de las clases
    class_names = {
        0: "Spruce/Fir",
        1: "Lodgepole Pine", 
        2: "Ponderosa Pine",
        3: "Cottonwood/Willow",
        4: "Aspen",
        5: "Douglas-fir",
        6: "Krummholz"
    }
    
    print(f"✅ Datos: {X.shape[0]:,} muestras, {X.shape[1]} features")
    print(f"✅ Modelo: {type(model).__name__}")
    print(f"✅ Clases: {len(class_names)} tipos de bosque")
    
    # Preparar datos
    print("\n🔄 Preparando datos para evaluación...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Predicciones
    train_pred = model.predict(X_train_scaled)
    test_pred = model.predict(X_test_scaled)
    test_proba = model.predict_proba(X_test_scaled)
    
    # 1. MÉTRICAS GLOBALES
    print("\n🎯 MÉTRICAS GLOBALES DEL MODELO")
    print("=" * 50)
    
    train_acc = accuracy_score(y_train, train_pred)
    test_acc = accuracy_score(y_test, test_pred)
    overfitting = train_acc - test_acc
    
    print(f"📊 Training Accuracy:  {train_acc:.4f} ({train_acc*100:.2f}%)")
    print(f"📊 Test Accuracy:      {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"📊 Overfitting:        {overfitting:.4f} ({overfitting*100:.2f}%)")
    
    if overfitting < 0.05:
        print("✅ CUMPLE: Overfitting < 5%")
    else:
        print("❌ PROBLEMA: Overfitting >= 5%")
    
    print(f"🏆 RESULTADO: Modelo con {test_acc*100:.2f}% de precisión")
    print(f"🎯 OBJETIVO: {'✅ CUMPLIDO' if test_acc >= 0.97 else '❌ NO CUMPLIDO'} (97%+ accuracy)")
    
    # 2. MATRIZ DE CONFUSIÓN
    print("\n🔥 MATRIZ DE CONFUSIÓN")
    print("=" * 50)
    
    cm = confusion_matrix(y_test, test_pred)
    
    # Crear visualización
    plt.figure(figsize=(12, 10))
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    sns.heatmap(cm_normalized, 
                annot=True, 
                fmt='.3f', 
                cmap='Blues',
                xticklabels=[class_names[i] for i in range(7)],
                yticklabels=[class_names[i] for i in range(7)])
    
    plt.title('🔥 Matriz de Confusión Normalizada\n(FireRiskAI - XGBoost Optimizado)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Predicción', fontsize=12, fontweight='bold')
    plt.ylabel('Valor Real', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.figtext(0.02, 0.02, f'Accuracy: {test_acc:.3f} | Overfitting: {overfitting:.3f}', 
                fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig('data/processed/confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. MÉTRICAS POR CLASE
    print("\n📈 MÉTRICAS POR CLASE")
    print("=" * 50)
    
    precision, recall, f1, support = precision_recall_fscore_support(y_test, test_pred, average=None)
    
    metrics_df = pd.DataFrame({
        'Clase': [class_names[i] for i in range(7)],
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'Support': support
    })
    
    print(metrics_df.round(4))
    
    # Guardar métricas
    metrics_df.to_csv('data/processed/metrics_per_class.csv', index=False)
    print("\n💾 Métricas guardadas en: data/processed/metrics_per_class.csv")
    
    # 4. FEATURE IMPORTANCE
    print("\n🎯 FEATURE IMPORTANCE")
    print("=" * 50)
    
    if hasattr(model, 'feature_importances_'):
        feature_importance = model.feature_importances_
        
        # Nombres reales de las features del Forest Cover Type Dataset
        real_feature_names = [
            "Elevation", "Aspect", "Slope", "Horizontal_Distance_To_Hydrology",
            "Vertical_Distance_To_Hydrology", "Horizontal_Distance_To_Roadways",
            "Hillshade_9am", "Hillshade_Noon", "Hillshade_3pm", "Horizontal_Distance_To_Fire_Points",
            "Wilderness_Area1", "Soil_Type1", "Soil_Type2", "Soil_Type3", "Soil_Type4",
            "Soil_Type5", "Soil_Type6", "Soil_Type7", "Soil_Type8", "Soil_Type9",
            "Soil_Type10", "Soil_Type11", "Soil_Type12", "Soil_Type13", "Soil_Type14",
            "Soil_Type15", "Soil_Type16", "Soil_Type17", "Soil_Type18", "Soil_Type19",
            "Soil_Type20", "Soil_Type21", "Soil_Type22", "Soil_Type23", "Soil_Type24",
            "Soil_Type25", "Soil_Type26", "Soil_Type27", "Soil_Type28", "Soil_Type29",
            "Soil_Type30", "Soil_Type31", "Soil_Type32", "Soil_Type33", "Soil_Type34",
            "Soil_Type35", "Soil_Type36", "Soil_Type37", "Soil_Type38", "Soil_Type39",
            "Soil_Type40", "Wilderness_Area2", "Wilderness_Area3", "Wilderness_Area4"
        ]
        
        # Top 15 features más importantes
        importance_df = pd.DataFrame({
            'Feature': real_feature_names,
            'Importance': feature_importance
        }).sort_values('Importance', ascending=False).head(15)
        
        print("Top 15 Features más importantes:")
        print(importance_df.round(4))
        
        # Visualización
        plt.figure(figsize=(12, 8))
        sns.barplot(data=importance_df, x='Importance', y='Feature', palette='viridis')
        plt.title('🎯 Top 15 Features más Importantes\n(XGBoost Feature Importance)', 
                  fontsize=16, fontweight='bold')
        plt.xlabel('Importance Score', fontsize=12)
        plt.ylabel('Features', fontsize=12)
        plt.tight_layout()
        plt.savefig('data/processed/feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Guardar
        importance_df.to_csv('data/processed/feature_importance.csv', index=False)
        print("💾 Feature importance guardado en: data/processed/feature_importance.csv")
    
    # 5. ANÁLISIS DE ERRORES
    print("\n🔍 ANÁLISIS DE ERRORES")
    print("=" * 50)
    
    # Encontrar predicciones incorrectas
    incorrect_mask = y_test != test_pred
    incorrect_indices = np.where(incorrect_mask)[0]
    
    print(f"❌ Predicciones incorrectas: {len(incorrect_indices)} de {len(y_test)} ({len(incorrect_indices)/len(y_test)*100:.2f}%)")
    
    if len(incorrect_indices) > 0:
        # Análisis de confianza en errores
        error_confidences = np.max(test_proba[incorrect_indices], axis=1)
        print(f"📊 Confianza promedio en errores: {np.mean(error_confidences):.3f}")
        print(f"📊 Confianza mínima en errores: {np.min(error_confidences):.3f}")
        print(f"📊 Confianza máxima en errores: {np.max(error_confidences):.3f}")
        
        # Clases más confundidas
        error_pairs = list(zip(y_test[incorrect_indices], test_pred[incorrect_indices]))
        from collections import Counter
        error_counter = Counter(error_pairs)
        
        print("\n🔥 Pares de clases más confundidas:")
        for (true_class, pred_class), count in error_counter.most_common(5):
            print(f"  {class_names[true_class]} → {class_names[pred_class]}: {count} veces")
    
    # 6. REPORTE FINAL
    print("\n🏆 REPORTE FINAL")
    print("=" * 60)
    print(f"✅ Accuracy Global: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"✅ Overfitting: {overfitting:.4f} ({overfitting*100:.2f}%)")
    print(f"✅ F1-Score Promedio: {np.mean(f1):.4f}")
    print(f"✅ Errores: {len(incorrect_indices)} de {len(y_test)} ({len(incorrect_indices)/len(y_test)*100:.2f}%)")
    print("=" * 60)
    
    if test_acc >= 0.97 and overfitting < 0.05:
        print("🎉 ¡MODELO EXCELENTE! Cumple todos los objetivos:")
        print("   ✅ Accuracy >= 97%")
        print("   ✅ Overfitting < 5%")
        print("   ✅ Listo para producción")
    else:
        print("⚠️  Modelo necesita mejoras")
    
    print("\n📁 Archivos generados:")
    print("   📊 data/processed/confusion_matrix.png")
    print("   📊 data/processed/metrics_per_class.csv")
    print("   📊 data/processed/feature_importance.png")
    print("   📊 data/processed/feature_importance.csv")

if __name__ == "__main__":
    main()
