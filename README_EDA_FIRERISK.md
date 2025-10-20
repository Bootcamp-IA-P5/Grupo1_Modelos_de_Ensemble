# 🔥 FireRiskAI — EDA específico de riesgo de incendios

Este EDA analiza el dataset Forest Cover Type (UCI) desde la perspectiva de prevención de incendios. Se mapea cada tipo de cobertura forestal a un nivel de riesgo y se estudian relaciones con variables geográficas.

## 📦 Dataset
- Muestras: 581,012
- Features: 54 (10 continuas + 44 binarias)
- Clases (7): Spruce/Fir, Lodgepole Pine, Ponderosa Pine, Cottonwood/Willow, Aspen, Douglas-fir, Krummholz

## 🔁 Mapeo cobertura → riesgo
- LOW: Spruce/Fir (score 2), Cottonwood/Willow (1)
- MEDIUM: Ponderosa Pine (5), Aspen (4), Douglas-fir (6)
- HIGH: Lodgepole Pine (8), Krummholz (9)

Nota: la “puntuación de riesgo” (1–9) se usa para promedios y mapas de calor.

## 📊 Distribución de riesgo
- HIGH: ~52.3%
- MEDIUM: ~10.8%
- LOW: ~36.9%

Interpretación: predomina el riesgo alto por cobertura tipo Krummholz/Lodgepole.

## 🧭 Correlaciones (con fire_risk_score)
- Elevation: ≈ -0.231 (a mayor altitud, menor riesgo)
- Horizontal_Distance_To_Hydrology: ≈ +0.045 (más lejos del agua, ligeramente mayor riesgo)
- Slope: ≈ +0.014 (pendiente mayor, leve incremento)

Conclusión: el riesgo lo determina principalmente la cobertura; las variables geográficas modulan de forma moderada.

## 🗺️ Mapas de calor (resumen)
- Elevation × Slope → identifica combinaciones de elevación alta con pendientes pronunciadas como zonas a vigilar.
- Distancia a agua × Distancia a carreteras → zonas lejos del agua y con difícil acceso tienden a mayor riesgo.

## ⚠️ Zonas críticas (score ≥ 8)
- ~52.3% de las muestras
- Medias: Elevation ≈ 2,951 m; Slope ≈ 13.6°
- Coberturas predominantes: Krummholz, Lodgepole Pine.

## ✅ Recomendaciones operativas
- Priorizar vigilancia en áreas de elevación alta, pendiente pronunciada y lejos del agua.
- Foco en coberturas Krummholz/Lodgepole.
- Integrar señales satelitales (NDVI/NBR/hotspots) y meteorológicas para ajustar riesgo en tiempo real.

## 🔌 Uso en la API
- GET `/risk-metrics`: expone umbrales, correlaciones y mapeos (fuente: `src/utils/fire_risk_metrics.json`).
- POST `/predict`: devuelve clase de cobertura, confianza y riesgo derivado.

## 📓 Notebook
- Archivo: `notebooks/03_Fire_Risk_Analysis.ipynb`
- Contenido: carga de datos, mapeo de riesgo, distribución, correlaciones, mapas de calor y export de métricas para API.