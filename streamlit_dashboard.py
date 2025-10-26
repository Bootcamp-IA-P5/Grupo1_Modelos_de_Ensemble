"""
FireRiskAI - Dashboard Streamlit Completo
Visualiza todas las funcionalidades del backend
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# Configuración de la página
st.set_page_config(
    page_title="FireRiskAI Dashboard",
    page_icon="🔥",
    layout="wide"
)

# URL base del backend
BASE_URL = "http://localhost:8000"

# Título principal
st.title("🔥 FireRiskAI - Dashboard de Monitoreo")

# Sidebar para navegación
st.sidebar.title("📋 Menú")
page = st.sidebar.selectbox(
    "Selecciona una sección:",
    ["🏠 Inicio", "📊 Métricas", "🧪 A/B Testing", "🔍 Data Drift", "🤖 Modelos", "🌤️ Clima"]
)

# Función para hacer peticiones al backend
@st.cache_data(ttl=10)
def fetch_data(endpoint):
    """Hacer petición al backend con caché de 10 segundos"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error conectando al backend: {e}")
        return None

# Página: Inicio
if page == "🏠 Inicio":
    st.header("Bienvenido al Dashboard de FireRiskAI")
    st.write("""
    Este dashboard permite monitorear todas las funcionalidades del backend:
    
    - ✅ **Predicciones**: Ver métricas de producción
    - 🧪 **A/B Testing**: Comparar modelos en tiempo real
    - 🔍 **Data Drift**: Detectar cambios en los datos
    - 🤖 **Modelos**: Gestionar y reemplazar modelos
    - 🌤️ **Clima**: Integración con API del clima
    """)
    
    # Verificar estado del backend
    st.subheader("Estado del Backend")
    health = fetch_data("/health")
    if health:
        st.success("✅ Backend conectado y funcionando")
        st.json(health)
    else:
        st.error("❌ Backend no disponible")
        st.warning("Asegúrate de que el servidor FastAPI esté corriendo en el puerto 8000")

# Página: Métricas
elif page == "📊 Métricas":
    st.header("📊 Dashboard de Métricas")
    
    # Obtener métricas del backend
    metrics = fetch_data("/metrics")
    
    if metrics:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Accuracy", f"{metrics.get('model_performance', {}).get('accuracy', 0)*100:.2f}%")
        with col2:
            st.metric("Precision", f"{metrics.get('model_performance', {}).get('precision', 0)*100:.2f}%")
        with col3:
            st.metric("Recall", f"{metrics.get('model_performance', {}).get('recall', 0)*100:.2f}%")
        with col4:
            st.metric("F1 Score", f"{metrics.get('model_performance', {}).get('f1_score', 0)*100:.2f}%")
        
        # Métricas de producción
        st.subheader("Métricas de Producción")
        prod_metrics = metrics.get("production_metrics", {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Predicciones", prod_metrics.get("total_predictions", 0))
        with col2:
            st.metric("Confianza Promedio", f"{prod_metrics.get('avg_confidence', 0)*100:.2f}%")
        with col3:
            st.metric("Tiempo Promedio", f"{prod_metrics.get('avg_processing_time', 0):.2f}ms")
        
        # Análisis de confianza
        st.subheader("Análisis de Confianza")
        conf_analysis = metrics.get("confidence_analysis", {})
        
        high_conf = conf_analysis.get("high_confidence_count", 0)
        low_conf = conf_analysis.get("low_confidence_count", 0)
        
        df_conf = pd.DataFrame({
            "Confianza": ["Alta (>0.8)", "Baja (<0.8)"],
            "Cantidad": [high_conf, low_conf]
        })
        
        fig = px.pie(df_conf, values="Cantidad", names="Confianza", title="Distribución de Confianza")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No se pudieron obtener las métricas")

# Página: A/B Testing
elif page == "🧪 A/B Testing":
    st.header("🧪 A/B Testing - Comparación de Modelos")
    
    # Estadísticas de A/B Testing
    stats = fetch_data("/ab-testing/stats")
    
    if stats:
        ab_stats = stats.get("ab_testing_stats", {})
        
        # Modelos y pesos
        st.subheader("Distribución de Tráfico")
        weights = ab_stats.get("model_weights", {})
        
        if weights:
            df_weights = pd.DataFrame({
                "Modelo": list(weights.keys()),
                "Peso": [w * 100 for w in weights.values()]
            })
            
            fig = px.bar(df_weights, x="Modelo", y="Peso", title="Distribución de Tráfico (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Rendimiento de modelos
        st.subheader("Rendimiento de Modelos")
        perf = ab_stats.get("model_performance", {})
        
        if perf:
            df_perf = pd.DataFrame([
                {
                    "Modelo": model,
                    "Predicciones": data.get("total_predictions", 0),
                    "Confianza Promedio": data.get("avg_confidence", 0) * 100,
                    "Tiempo Promedio": data.get("avg_processing_time", 0)
                }
                for model, data in perf.items()
            ])
            
            if not df_perf.empty:
                st.dataframe(df_perf)
                fig = px.bar(
                    df_perf, 
                    x="Modelo", 
                    y="Confianza Promedio", 
                    title="Confianza Promedio por Modelo"
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No se pudieron obtener estadísticas de A/B Testing")

# Página: Data Drift
elif page == "🔍 Data Drift":
    st.header("🔍 Data Drift Monitoring")
    
    # Estado actual
    drift_status = fetch_data("/drift/status")
    
    if drift_status:
        st.subheader("Estado Actual")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            has_baseline = drift_status.get("has_baseline", False)
            st.metric("Baseline Establecido", "✅ Sí" if has_baseline else "❌ No")
        with col2:
            st.metric("Total Detecciones", drift_status.get("total_detections", 0))
        with col3:
            st.metric("Threshold", drift_status.get("threshold", 0.1))
        
        # Alertas de drift
        drift_alerts = fetch_data("/drift/alerts")
        
        if drift_alerts and drift_alerts.get("has_active_alerts"):
            st.error("⚠️ ALERTAS ACTIVAS DE DRIFT")
            
            for alert in drift_alerts.get("alerts", []):
                st.warning(f"""
                **{alert.get('type', 'Unknown')}**
                - Severidad: {alert.get('severity', 'Unknown')}
                - Mensaje: {alert.get('message', '')}
                - Timestamp: {alert.get('timestamp', '')}
                """)
        else:
            st.success("✅ No hay alertas de drift activas")
        
        # Historial de drift
        drift_history = fetch_data("/drift/history")
        
        if drift_history and drift_history.get("history"):
            st.subheader("Historial de Drift")
            df_history = pd.DataFrame(drift_history.get("history", []))
            
            if not df_history.empty:
                st.dataframe(df_history)
    else:
        st.error("No se pudo obtener el estado de Data Drift")

# Página: Modelos
elif page == "🤖 Modelos":
    st.header("🤖 Gestión de Modelos")
    
    # Comparar modelos
    model_compare = fetch_data("/models/compare")
    
    if model_compare:
        st.subheader("Comparación de Modelos")
        
        best_model = model_compare.get("best_model", "N/A")
        current_model = model_compare.get("current_model", "N/A")
        should_replace = model_compare.get("should_replace", False)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Modelo Actual", str(current_model).upper() if current_model else "N/A")
        with col2:
            st.metric("Mejor Modelo", str(best_model).upper() if best_model else "N/A")
        with col3:
            st.metric("¿Debería Reemplazarse?", "✅ Sí" if should_replace else "❌ No")
        
        # Estadísticas de modelos
        model_stats = model_compare.get("model_stats", {})
        
        if model_stats:
            df_stats = pd.DataFrame([
                {"Modelo": model, "Accuracy": data.get("accuracy", 0) * 100}
                for model, data in model_stats.items()
            ])
            
            fig = px.bar(df_stats, x="Modelo", y="Accuracy", title="Accuracy por Modelo")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df_stats)
        
        # Botón para reemplazar modelo
        if should_replace:
            st.warning(f"⚠️ El modelo {best_model} es mejor que el actual")
            if st.button(f"🔄 Reemplazar modelo a {best_model}"):
                response = requests.post(f"{BASE_URL}/models/replace/{best_model}")
                if response.status_code == 200:
                    st.success(f"✅ Modelo reemplazado a {best_model}")
                    st.rerun()
    else:
        st.error("No se pudieron comparar los modelos")

# Página: Clima
elif page == "🌤️ Clima":
    st.header("🌤️ Weather API Integration")
    
    st.write("Ingresa coordenadas para obtener el clima:")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitud", value=40.7128)
    with col2:
        lon = st.number_input("Longitud", value=-74.0060)
    
    if st.button("Obtener Clima"):
        response = requests.get(f"{BASE_URL}/weather", params={"lat": lat, "lon": lon})
        if response.status_code == 200:
            weather = response.json()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Temperatura", f"{weather.get('temperature', 0)}°C")
            with col2:
                st.metric("Humedad", f"{weather.get('humidity', 0)}%")
            with col3:
                st.metric("Condición", weather.get("description", "N/A"))
        else:
            st.error("Error obteniendo datos del clima")

# Botón de refresh manual
if st.sidebar.button("🔄 Actualizar Datos"):
    st.rerun()

