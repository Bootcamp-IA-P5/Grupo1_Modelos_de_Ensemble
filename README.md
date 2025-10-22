# 🌟 Clasificador Multiclase de Alto Rendimiento

Proyecto integral de **Clasificación Multiclase** en Machine Learning, centrado en resolver un problema real. El desarrollo abarca desde el análisis de datos hasta la puesta en producción con prácticas MLOps.

---

## 🧭 Índice

* 📌 Resumen del Proyecto
* 📂 Enunciado y Desafío
* 🎯 Concepto Clave: Clasificación Multiclase
* 📦 Condiciones y Entregables
* 🛠️ Tecnologías Clave
* 🏆 Niveles de Entrega (Hoja de Ruta)
* 👩‍💻 Contribuidores
---

## 📌 Resumen del Proyecto

Este proyecto tiene como finalidad desarrollar un **modelo de machine learning** capaz de resolver un problema real utilizando algoritmos de **clasificación multiclase**.

A través de este reto, se busca aplicar y consolidar el conocimiento adquirido sobre:
1.  Análisis exploratorio de datos (EDA) y visualización.
2.  Preprocesamiento y *Feature Engineering*.
3.  Construcción de modelos supervisados (desde algoritmos básicos hasta *ensembles* y Redes Neuronales).
4.  Evaluación rigurosa de resultados (métricas multiclase).
5.  Productivización y prácticas MLOps.

## 📂 Enunciado y Desafío

El reto principal es crear una solución *end-to-end* (de principio a fin) que demuestre la capacidad de abordar un problema complejo de clasificación.

### ✨ Puntos Focales

| ✅ Fortalezas Clave | ⚠️ Restricción Crítica |
| :--- | :--- |
| Enfoque en métricas específicas multiclase (Precision, Recall, F1 por clase). | **Overfitting** debe ser **inferior al 5%** (diferencia entre *training* y *validation*). |
| Aplicación de técnicas avanzadas (Validación Cruzada Estratificada, Optimización de Hiperparámetros). | Requiere la entrega de una **aplicación funcional** (Streamlit/Gradio/Dash). |
| Implementación de *pipelines* de MLOps y Dockerización. | El proyecto es **Grupal** y requiere organización con Trello/similar. |

## 🎯 Concepto Clave: Clasificación Multiclase

La **clasificación multiclase** es una tarea de aprendizaje supervisado donde una instancia de entrada se asigna a **una única clase** entre **tres o más posibles** categorías mutuamente excluyentes.

> **Dataset Sugerido (Opcional):** [Forest Cover Type Dataset](https://archive.ics.uci.edu/ml/datasets/Covertype). Se fomenta la autenticidad y la búsqueda de un dataset original que resuelva un problema de interés.

---

## 📦 Condiciones y Entregables

* **Modalidad:** Proyecto **Grupal**.
* **Requerimiento de Overfitting:** Diferencia de métrica $< 5\%$ entre *training* y *validation*.

### 📝 Entregables Requeridos

1.  **Aplicación Web** que reciba datos y devuelva una predicción multiclase (Streamlit/Dash/Gradio).
2.  **Repositorio en GitHub** con buena gestión de ramas (*GitFlow* o similar) y *commits* limpios.
3.  **Informe Técnico** detallado con métricas, EDA, preprocesamiento y análisis de errores.
4.  **Presentaciones:** Una para **negocio** (visión general) y otra **técnica** (código y arquitectura).
5.  **Enlace a Herramienta de Organización** (Trello, Jira, Notion, etc.).

---

## 🛠️ Herramientas y Tecnologías

### ⚙️ Backend y Modelo

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/stable/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-005EB8?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/en/latest/)

### 🌐 Frontend y Productivización

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)

---

## 🏆 Niveles de Entrega (Hoja de Ruta)

### 🟢 Nivel Esencial

El mínimo funcional y bien documentado.

* ✅ Modelo de Clasificación Multiclase funcional (mínimo 3 clases).
* ✅ **EDA completo** con visualizaciones orientadas a clasificación.
* ✅ Overfitting **< 5%**.
* ✅ **Aplicación básica** (Streamlit/Gradio/Dash).
* ✅ Informe con **todas las métricas multiclase requeridas**: Accuracy global, Precision, Recall y F1 *por clase*, Matriz de confusión, *Feature Importance*.

### 🟡 Nivel Medio

Enfoque en la robustez y optimización del modelo.

* ✅ Aplicación de **modelos de *ensemble***.
* ✅ Implementación de **Validación Cruzada Estratificada** (`StratifiedKFold`).
* ✅ **Optimización de hiperparámetros** (GridSearch, RandomizedSearch, Optuna).
* ✅ Sistema de **recogida de feedback** y **pipeline de recolección de datos nuevos**.

### 🟠 Nivel Avanzado

Enfoque en la productivización y calidad de ingeniería.

* ✅ **Dockerización completa** del proyecto.
* ✅ Integración con **bases de datos** para almacenar datos recolectados.
* ✅ **Despliegue en la nube** (Render, Vercel, AWS, etc.).
* ✅ Implementación de **tests unitarios** (datos, modelo y métricas).

### 🔴 Nivel Experto

Adopción de prácticas MLOps avanzadas.

* ✅ Entrenamiento de **Redes Neuronales**.
* ✅ Implementación de prácticas **MLOps**:
    * **A/B Testing** para comparación de modelos.
    * **Monitoreo de Data Drift** con alertas.
    * **Sustitución automática del modelo** en producción.

---

## 👩‍💻 Contribuidores

| Nombre | GitHub | LinkedIn |
| :--- | :--- | :--- |
| *[Nombre del Contribuidor 1]* | *[Enlace GitHub]* | *[Enlace LinkedIn]* |
| *[Nombre del Contribuidor 2]* | *[Enlace GitHub]* | *[Enlace LinkedIn]* |
| *[Nombre del Contribuidor 3]* | *[Enlace GitHub]* | *[Enlace LinkedIn]* |
| *[Nombre del Contribuidor 4]* | *[Enlace GitHub]* | *[Enlace LinkedIn]* |
