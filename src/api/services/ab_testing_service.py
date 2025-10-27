"""
Servicio de A/B Testing para modelos
Permite alternar entre diferentes modelos para comparar rendimiento
"""

import os
import joblib
import random
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ABTestingService:
    """
    Servicio para manejar A/B testing entre modelos
    """
    
    def __init__(self):
        self.models = {}
        self.model_weights = {}  # Pesos para distribución de tráfico
        self.model_performance = {}  # Métricas de rendimiento
        self.load_models()
    
    def load_models(self):
        """Cargar modelos para A/B testing"""
        try:
            # Cargar modelos
            self.models = {
                'random_forest': joblib.load('models/random_forest_ab.pkl'),
                'extra_trees': joblib.load('models/extra_trees_ab.pkl'),
                'xgboost': joblib.load('models/xgboost_ab.pkl')
            }
            
            # Configurar pesos iniciales (distribución uniforme)
            self.model_weights = {
                'random_forest': 0.33,
                'extra_trees': 0.33,
                'xgboost': 0.34
            }
            
            logger.info("✅ Modelos de A/B testing cargados")
            
        except Exception as e:
            logger.error(f"❌ Error cargando modelos: {e}")
            self.models = {}
    
    def select_model(self, user_id: Optional[str] = None) -> str:
        """
        Seleccionar modelo para A/B testing
        
        Args:
            user_id: ID del usuario (para consistencia)
            
        Returns:
            Nombre del modelo seleccionado
        """
        if not self.models:
            return 'xgboost'  # Fallback al mejor modelo
        
        # Usar user_id para consistencia (mismo usuario = mismo modelo)
        if user_id:
            random.seed(hash(user_id) % 1000)
        
        # Seleccionar modelo basado en pesos
        rand = random.random()
        cumulative = 0
        
        for model_name, weight in self.model_weights.items():
            cumulative += weight
            if rand <= cumulative:
                return model_name
        
        # Fallback
        return 'xgboost'
    
    def predict(self, features, model_name: str = None):
        """
        Hacer predicción con modelo específico
        
        Args:
            features: Features de entrada
            model_name: Nombre del modelo (si no se especifica, se selecciona automáticamente)
            
        Returns:
            Predicción del modelo
        """
        if model_name is None:
            model_name = self.select_model()
        
        if model_name not in self.models:
            logger.error(f"❌ Modelo {model_name} no encontrado")
            return None
        
        try:
            model = self.models[model_name]
            prediction = model.predict(features)
            return prediction
        except Exception as e:
            logger.error(f"❌ Error en predicción con {model_name}: {e}")
            return None
    
    def update_model_weights(self, new_weights: Dict[str, float]):
        """
        Actualizar pesos de distribución de modelos
        
        Args:
            new_weights: Nuevos pesos para cada modelo
        """
        # Validar que los pesos sumen 1.0
        total_weight = sum(new_weights.values())
        if abs(total_weight - 1.0) > 0.01:
            logger.warning("⚠️ Los pesos no suman 1.0, normalizando...")
            total_weight = sum(new_weights.values())
            new_weights = {k: v/total_weight for k, v in new_weights.items()}
        
        self.model_weights = new_weights
        logger.info(f"✅ Pesos actualizados: {self.model_weights}")
    
    def get_model_stats(self) -> Dict:
        """
        Obtener estadísticas de los modelos
        
        Returns:
            Diccionario con estadísticas de cada modelo
        """
        return {
            'models_loaded': list(self.models.keys()),
            'model_weights': self.model_weights,
            'model_performance': self.model_performance,
            'total_models': len(self.models)
        }
    
    def record_prediction_result(self, model_name: str, prediction: int, 
                               confidence: float, processing_time: float):
        """
        Registrar resultado de predicción para análisis
        
        Args:
            model_name: Nombre del modelo usado
            prediction: Predicción realizada
            confidence: Confianza de la predicción
            processing_time: Tiempo de procesamiento
        """
        if model_name not in self.model_performance:
            self.model_performance[model_name] = {
                'total_predictions': 0,
                'avg_confidence': 0.0,
                'avg_processing_time': 0.0,
                'predictions_by_class': {}
            }
        
        stats = self.model_performance[model_name]
        stats['total_predictions'] += 1
        
        # Actualizar promedio de confianza
        total_conf = stats['avg_confidence'] * (stats['total_predictions'] - 1)
        stats['avg_confidence'] = (total_conf + confidence) / stats['total_predictions']
        
        # Actualizar promedio de tiempo
        total_time = stats['avg_processing_time'] * (stats['total_predictions'] - 1)
        stats['avg_processing_time'] = (total_time + processing_time) / stats['total_predictions']
        
        # Contar predicciones por clase
        if prediction not in stats['predictions_by_class']:
            stats['predictions_by_class'][prediction] = 0
        stats['predictions_by_class'][prediction] += 1

# Instancia global del servicio
ab_testing_service = ABTestingService()
