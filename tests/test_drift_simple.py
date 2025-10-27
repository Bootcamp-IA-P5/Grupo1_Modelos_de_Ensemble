"""Test simple del drift detector"""

from src.api.services.drift_detector import drift_detector

# 1. Establecer baseline
baseline = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
drift_detector.set_baseline(baseline)
print("✅ Baseline establecido")

# 2. Datos similares (sin drift)
new_data = [[1.5, 2.5, 3.5]]
result = drift_detector.detect_drift(new_data)
print(f"✅ Sin drift: {result}")

# 3. Datos muy diferentes (con drift)
very_different = [[100, 200, 300]]
result = drift_detector.detect_drift(very_different)
print(f"✅ Con drift: {result}")
