"""
Detector de Data Drift - VERSIÓN SIMPLE
Detecta cambios en la distribución de datos de entrada
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DriftDetector:
    """
    Detector simple de data drift
    """
    
    def __init__(self, threshold: float = 0.1):
        """
        Inicializar detector
        
        Args:
            threshold: Umbral para considerar drift (0.1 = 10%)
        """
        self.threshold = threshold
        self.baseline_data = None
        self.drift_history = []
    
    def set_baseline(self, data: List[List[float]]):
        """
        Establecer datos de referencia (baseline)
        
        Args:
            data: Lista de features de entrenamiento
        """
        self.baseline_data = np.array(data)
        logger.info(f" Baseline establecido con {len(data)} muestras")
    
    def detect_drift(self, new_data: List[List[float]]) -> Dict:
        """
        Detectar drift en datos nuevos
        
        Args:
            new_data: Datos nuevos a comparar
            
        Returns:
            Dict con información del drift
        """
        if self.baseline_data is None:
            return {"error": "No hay baseline establecido"}
        
        try:
            new_array = np.array(new_data)
            
            # Calcular estadísticas básicas
            baseline_mean = np.mean(self.baseline_data, axis=0)
            new_mean = np.mean(new_array, axis=0)
            
            # Calcular diferencia porcentual (evitar división por cero)
            mask = np.abs(baseline_mean) > 1e-8
            mean_diff = np.abs(new_mean - baseline_mean) / (np.abs(baseline_mean) + 1e-8)
            
            # Usar solo las features que tienen valores no cero en baseline
            if np.any(mask):
                max_diff = np.max(mean_diff[mask])
            else:
                max_diff = 0.0
            
            # Determinar si hay drift
            has_drift = bool(max_diff > self.threshold)
            
            drift_info = {
                "timestamp": datetime.now().isoformat(),
                "has_drift": has_drift,
                "max_difference": float(max_diff),
                "threshold": self.threshold,
                "baseline_samples": len(self.baseline_data),
                "new_samples": len(new_data),
                "drift_severity": "HIGH" if max_diff > 0.2 else "MEDIUM" if max_diff > 0.1 else "LOW"
            }
            
            # Guardar en historial
            self.drift_history.append(drift_info)
            
            logger.info(f" Drift detectado: {has_drift}, diferencia: {max_diff:.3f}")
            
            return drift_info
            
        except Exception as e:
            logger.error(f" Error detectando drift: {e}")
            return {"error": str(e)}
    
    def get_drift_history(self) -> List[Dict]:
        """
        Obtener historial de drift
        """
        return self.drift_history

# Instancia global del detector
drift_detector = DriftDetector()
