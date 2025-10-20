#!/usr/bin/env python
# coding: utf-8

# # 🔥 FireRiskAI - Análisis de Riesgo de Incendios Forestales
# 
# ## 📊 EDA Específico para Prevención de Incendios
# 
# Este notebook analiza el dataset Forest Cover Type desde la perspectiva de **prevención de incendios forestales**, mapeando tipos de cobertura vegetal a niveles de riesgo de incendio basados en características geográficas y climáticas.
# 
# ### 🎯 Objetivos:
# 1. **Mapear inflamabilidad** por tipo de bosque
# 2. **Analizar correlación** geográfica con riesgo
# 3. **Identificar zonas críticas** de alto riesgo
# 4. **Crear visualizaciones** para toma de decisiones

# In[ ]:


# ============================================
# 📚 IMPORTS Y CONFIGURACIÓN
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ucimlrepo import fetch_ucirepo
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

print("- Análisis de Riesgo de Incendios Forestales")
print("=" * 60)


# In[ ]:


# ============================================
# 📊 CARGA DE DATOS
# ============================================

print("📥 Cargando Forest Cover Type Dataset...")
covertype = fetch_ucirepo(id=31)
X = covertype.data.features
y = covertype.data.targets.iloc[:, 0]

# Crear DataFrame combinado
df = pd.concat([X, y], axis=1)
df.columns = list(X.columns) + ['Cover_Type']

print(f"✅ Dataset cargado: {df.shape[0]:,} muestras, {df.shape[1]} features")
print(f"📋 Tipos de bosque: {sorted(df['Cover_Type'].unique())}")
print(f"\n📊 Primeras 5 filas:")
df.head()


# In[ ]:


# ============================================
# 🔥 MAPEO DE INFLAMABILIDAD POR TIPO DE BOSQUE
# ============================================

print("🔥 MAPEO DE INFLAMABILIDAD POR TIPO DE BOSQUE")
print("=" * 50)

# Definir niveles de riesgo basados en características de inflamabilidad
fire_risk_mapping = {
    1: {
        "name": "Spruce/Fir (Abeto/Pícea)",
        "risk": "BAJO",
        "score": 2,
        "reason": "Coníferas densas pero húmedas, resistentes al fuego",
        "color": "green"
    },
    2: {
        "name": "Lodgepole Pine (Pino Lodgepole)",
        "risk": "ALTO",
        "score": 8,
        "reason": "Pinos densos, muy inflamables, propagación rápida",
        "color": "red"
    },
    3: {
        "name": "Ponderosa Pine (Pino Ponderosa)",
        "risk": "MEDIO",
        "score": 5,
        "reason": "Pinos dispersos, corteza gruesa, moderadamente resistente",
        "color": "orange"
    },
    4: {
        "name": "Cottonwood/Willow (Álamo/Sauce)",
        "risk": "BAJO",
        "score": 1,
        "reason": "Árboles de hoja ancha, cerca del agua, muy resistentes",
        "color": "green"
    },
    5: {
        "name": "Aspen (Álamo temblón)",
        "risk": "MEDIO",
        "score": 4,
        "reason": "Hojas caducas, pero troncos secos pueden arder",
        "color": "orange"
    },
    6: {
        "name": "Douglas-fir (Abeto de Douglas)",
        "risk": "MEDIO",
        "score": 6,
        "reason": "Coníferas grandes, corteza inflamable en condiciones secas",
        "color": "orange"
    },
    7: {
        "name": "Krummholz (Vegetación alpina)",
        "risk": "ALTO",
        "score": 9,
        "reason": "Vegetación alpina seca, vientos fuertes, propagación extrema",
        "color": "red"
    }
}

# Crear variables de riesgo
df['fire_risk_score'] = df['Cover_Type'].map({k: v['score'] for k, v in fire_risk_mapping.items()})
df['fire_risk_level'] = df['Cover_Type'].map({k: v['risk'] for k, v in fire_risk_mapping.items()})
df['forest_type_name'] = df['Cover_Type'].map({k: v['name'] for k, v in fire_risk_mapping.items()})

print("✅ Mapeo de inflamabilidad completado")
print("\n📋 Tabla de mapeo:")
for cover_type, info in fire_risk_mapping.items():
    print(f"{cover_type}. {info['name']} - {info['risk']} (Score: {info['score']})")
    print(f"   Razón: {info['reason']}")
    print()

