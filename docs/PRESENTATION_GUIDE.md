# 📋 Guía de Presentación - FireRiskAI Dashboard

## 🎯 Objetivo

Esta guía explica cómo presentar las funcionalidades avanzadas del proyecto (A/B Testing, Data Drift y Auto Model Replacement) durante la demostración.

## 🚀 Cómo Iniciar el Dashboard

### **1. Iniciar el Backend**

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### **2. Iniciar Streamlit Dashboard**

```bash
streamlit run streamlit_dashboard.py
```

El dashboard estará disponible en: `http://localhost:8501`

## 📊 Páginas del Dashboard

### **Página Principal: Inicio**
- Título del proyecto y descripción
- Problemática y solución
- Información del dataset
- Métricas clave del modelo
- Estado del sistema

### **Predicción**
- Formulario para introducir features
- Botón de predicción
- Resultado con confianza y nivel de riesgo
- Sistema de feedback (thumbs up/down)

### **EDA (Análisis Exploratorio)**
- Distribución de clases
- Histogramas de features importantes
- Matriz de correlación
- Box plots comparativos
- Análisis de outliers
- Estadísticas descriptivas

### **Modelo**
- Información detallada del modelo
- Métricas por clase
- Feature Importance
- Matriz de Confusión interactiva
- Configuración e hiperparámetros
- Comparación Train vs Validation

### **Reentrenamiento**
- Contador de datos nuevos recolectados
- Análisis de calidad de datos
- Comparación modelo actual vs esperado
- Botón para lanzar reentrenamiento

### **🧪 A/B Testing** ⭐
- Distribución de tráfico entre modelos
- Estadísticas de rendimiento por modelo
- Visualización de predicciones acumuladas
- Opción para cambiar pesos de distribución

### **🔍 Data Drift** ⭐
- Estado del baseline
- Historial de detecciones
- Alertas activas
- Botón para establecer baseline

### **🤖 Gestión de Modelos** ⭐
- Comparación automática de modelos
- Recomendación de reemplazo
- Botón para activar modelo mejor
- Reemplazo manual si es necesario

### **Documentación Técnica**
- Pipeline de preprocesamiento
- Arquitectura del modelo
- Guías de uso de la API

### **Acerca del Proyecto**
- Equipo de desarrollo
- Objetivos del proyecto
- Enlaces (GitHub, Trello)
- Contacto

## 🎬 Guión de Presentación (10-15 minutos)

### **1. Introducción (2 min)**
- Ir a **Inicio**
- Mostrar título y descripción del proyecto
- Explicar el problema: clasificar 7 tipos de vegetación forestal
- Mostrar métricas principales: 97% accuracy

### **2. Predicción (2 min)**
- Ir a **Predicción**
- Mostrar formulario con features topográficas
- Hacer una predicción en tiempo real
- Explicar resultado: clase, confianza, nivel de riesgo

### **3. EDA y Análisis (2 min)**
- Ir a **EDA**
- Mostrar distribución de clases
- Explicar dataset balanceado/desbalanceado
- Mostrar importancia de features

### **4. A/B Testing (3 min)** ⭐ **DESTACAR**
- Ir a **A/B Testing**
- Explicar: "Estamos comparando 3 modelos en producción"
- Mostrar distribución de tráfico: 33% para cada uno
- Mostrar estadísticas acumuladas
- **Acción**: Cambiar pesos a XGBoost 70%, RF 15%, ET 15%
- Explicar: "Esto permite comparar rendimiento en producción real"

### **5. Data Drift Monitoring (2 min)** ⭐ **DESTACAR**
- Ir a **Data Drift**
- Explicar: "Detecta cuando los datos cambian significativamente"
- Establecer baseline si no está establecido
- Mostrar alertas si hay drift detectado
- Explicar: "Si hay drift, el modelo puede no funcionar bien"

### **6. Auto Model Replacement (2 min)** ⭐ **DESTACAR**
- Ir a **Gestión de Modelos**
- Mostrar comparación de modelos
- Explicar: "Sistema compara automáticamente y recomienda"
- Mostrar métricas: Accuracy, F1-Score, Overfitting
- Si hay mejor modelo, mostrar recomendación
- **Acción**: Hacer clic en "Reemplazar" (si aplica)
- Explicar: "Esto asegura que siempre usamos el mejor modelo"

### **7. Resumen (1 min)**
- Ir a **Acerca del Proyecto**
- Mostrar stack tecnológico
- Mostrar estado del proyecto
- Enlaces al repositorio

## 🎯 Puntos Clave para Destacar

### **1. A/B Testing**
- ✅ Permite comparar modelos en producción real
- ✅ Distribución configurable de tráfico
- ✅ Estadísticas en tiempo real
- ✅ Útil para decidir qué modelo usar

### **2. Data Drift Monitoring**
- ✅ Detecta cambios en la distribución de datos
- ✅ Alertas automáticas
- ✅ Historial de detecciones
- ✅ Permite reentrenar cuando sea necesario

### **3. Auto Model Replacement**
- ✅ Comparación automática de modelos
- ✅ Recomendación inteligente
- ✅ Reemplazo con un clic
- ✅ Garantiza mejor rendimiento

## 💡 Tips para la Presentación

1. **Demonstración en vivo**: Hacer predicciones reales durante la presentación
2. **Navegar fluidamente**: Mostrar transiciones entre páginas
3. **Destacar MLOps**: A/B Testing, Data Drift y Auto Replacement son claves
4. **Interactividad**: Usar botones y gráficos interactivos
5. **Backend activo**: Asegurar que el backend esté corriendo

## 🔧 Problemas Comunes

### **Backend no responde**
```bash
# Verificar que está corriendo
curl http://localhost:8000/health
```

### **Dashboard no carga**
```bash
# Reiniciar Streamlit
streamlit run streamlit_dashboard.py --server.port 8501
```

### **Modelos no encontrados**
- Verificar que existen archivos en `models/`:
  - `best_model.pkl`
  - `scaler.pkl`
  - `metadata.json`

## 📝 Notas Finales

- Todas las funcionalidades están implementadas y funcionando
- El dashboard es interactivo y permite demostración en tiempo real
- Se puede conectar a MongoDB en producción para datos reales
- Los modelos están entrenados y optimizados
- Backend desplegado en Render.com
- Código disponible en GitHub

---

**© 2025 Grupo 1 - FireRiskAI**

