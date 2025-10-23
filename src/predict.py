"""
Script principal para hacer predicciones con el modelo final
"""

import joblib
import numpy as np
import json
from pathlib import Path

class ForestCoverPredictor:
    """
    Clasificador de tipos de cobertura forestal usando XGBoost optimizado
    """
    
    def __init__(self, model_path="models/best_model.pkl", scaler_path="models/scaler.pkl"):
        """
        Inicializar el predictor
        
        Args:
            model_path: Ruta al modelo entrenado
            scaler_path: Ruta al scaler entrenado
        """
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.metadata = None
        
        # Cargar modelo y metadatos
        self._load_model()
        self._load_metadata()
    
    def _load_model(self):
        """Cargar modelo y scaler"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            print("✅ Modelo y scaler cargados correctamente")
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise
    
    def _load_metadata(self):
        """Cargar metadatos del modelo"""
        try:
            metadata_path = Path(self.model_path).parent / "metadata.json"
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            print("✅ Metadatos cargados correctamente")
        except Exception as e:
            print(f"⚠️  No se pudieron cargar metadatos: {e}")
            self.metadata = None
    
    def predict(self, features):
        """
        Hacer predicción para una muestra
        
        Args:
            features: Lista o array de 54 features
            
        Returns:
            dict: Predicción con información detallada
        """
        if len(features) != 54:
            raise ValueError(f"Se esperan 54 features, se recibieron {len(features)}")
        
        # Convertir a numpy array y escalar
        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features_array)
        
        # Hacer predicción
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = probabilities.max()
        
        # Obtener nombre de la clase
        class_name = self._get_class_name(prediction)
        
        return {
            "prediction": int(prediction),
            "class_name": class_name,
            "confidence": float(confidence),
            "probabilities": {
                f"class_{i}": float(prob) for i, prob in enumerate(probabilities)
            }
        }
    
    def _get_class_name(self, class_id):
        """Obtener nombre de la clase"""
        if self.metadata and "usage" in self.metadata:
            class_names = self.metadata["usage"]["class_names"]
            if 0 <= class_id < len(class_names):
                return class_names[class_id]
        
        # Nombres por defecto
        default_names = [
            "Spruce/Fir", "Lodgepole Pine", "Ponderosa Pine",
            "Cottonwood/Willow", "Aspen", "Douglas-fir", "Krummholz"
        ]
        return default_names[class_id] if 0 <= class_id < len(default_names) else f"Class {class_id}"
    
    def get_model_info(self):
        """Obtener información del modelo"""
        if self.metadata:
            return {
                "name": self.metadata["model_info"]["name"],
                "version": self.metadata["model_info"]["version"],
                "accuracy": self.metadata["performance"]["accuracy_percentage"],
                "algorithm": self.metadata["model_info"]["algorithm"]
            }
        return {"name": "XGBoost Forest Cover Classifier", "accuracy": "97.07%"}


def main():
    """Función principal para probar el predictor"""
    print("🌲 FOREST COVER TYPE PREDICTOR")
    print("="*40)
    
    # Inicializar predictor
    predictor = ForestCoverPredictor()
    
    # Mostrar información del modelo
    model_info = predictor.get_model_info()
    print(f"Modelo: {model_info['name']}")
    print(f"Versión: {model_info['version']}")
    print(f"Accuracy: {model_info['accuracy']}")
    print(f"Algoritmo: {model_info['algorithm']}")
    
    # Ejemplo de predicción (features aleatorias)
    print("\n🔍 Ejemplo de predicción:")
    print("Generando features aleatorias...")
    
    # Generar features aleatorias (en un rango realista)
    np.random.seed(42)
    sample_features = np.random.uniform(0, 10, 54).tolist()
    
    try:
        result = predictor.predict(sample_features)
        print(f"Predicción: {result['prediction']}")
        print(f"Tipo de bosque: {result['class_name']}")
        print(f"Confianza: {result['confidence']:.3f}")
        print(f"Probabilidades por clase:")
        for class_id, prob in result['probabilities'].items():
            print(f"  {class_id}: {prob:.3f}")
    except Exception as e:
        print(f"❌ Error en predicción: {e}")


if __name__ == "__main__":
    main()
