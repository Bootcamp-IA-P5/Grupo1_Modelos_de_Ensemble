"""
Gestor de Modelos - VERSIÓN SIMPLE
Compara modelos del A/B testing y decide cuál usar como principal
"""

import os
import joblib
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Gestor simple de modelos para auto-replacement
    """
    
    def __init__(self):
        self.current_model = "xgboost"  # Modelo por defecto
        self.available_models = ["random_forest", "extra_trees", "xgboost"]
        self.model_stats = {}
    
    def load_model_metadata(self, model_name: str) -> Optional[Dict]:
        """
        Cargar metadata de un modelo
        
        Args:
            model_name: Nombre del modelo (random_forest, extra_trees, xgboost)
            
        Returns:
            Dict con metadata o None
        """
        try:
            metadata_path = f"models/{model_name}_metadata.json"
            if os.path.exists(metadata_path):
                import json
                with open(metadata_path, "r") as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Error cargando metadata de {model_name}: {e}")
            return None
    
    def compare_models(self) -> Dict:
        """
        Comparar todos los modelos y devolver el mejor
        
        Returns:
            Dict con el mejor modelo y razón
        """
        best_model = None
        best_score = 0.0
        reason = ""
        
        for model_name in self.available_models:
            metadata = self.load_model_metadata(model_name)
            
            if metadata:
                accuracy = metadata.get("accuracy", 0.0)
                
                # Guardar stats
                self.model_stats[model_name] = {
                    "accuracy": accuracy,
                    "model_type": metadata.get("model_type", model_name)
                }
                
                # Actualizar mejor modelo
                if accuracy > best_score:
                    best_score = accuracy
                    best_model = model_name
                    reason = f"Mejor accuracy: {accuracy:.4f}"
        
        return {
            "best_model": best_model,
            "best_accuracy": best_score,
            "reason": reason,
            "current_model": self.current_model,
            "should_replace": best_model != self.current_model,
            "model_stats": self.model_stats
        }
    
    def replace_model(self, new_model: str) -> bool:
        """
        Reemplazar modelo actual
        
        Args:
            new_model: Nombre del nuevo modelo a usar
            
        Returns:
            True si reemplazo exitoso
        """
        if new_model in self.available_models:
            self.current_model = new_model
            logger.info(f"✅ Modelo reemplazado a: {new_model}")
            return True
        return False
    
    def get_current_model(self) -> str:
        """Obtener modelo actual"""
        return self.current_model

# Instancia global del gestor
model_manager = ModelManager()
