"""
Aplicación principal de Streamlit para el proyecto de clasificación multiclase
"""

import streamlit as st

def main():
    st.title("🎯 Proyecto de Clasificación Multiclase")
    st.subheader("Grupo 1 - Modelos de Ensemble")
    
    st.write("""
    Esta es la aplicación principal del proyecto de clasificación multiclase.
    
    **Funcionalidades:**
    - Carga y análisis de datos
    - Entrenamiento de modelos de ensemble
    - Predicciones multiclase
    - Evaluación de métricas
    """)
    
    st.info("🚧 En desarrollo - Próximamente más funcionalidades")

if __name__ == "__main__":
    main()
