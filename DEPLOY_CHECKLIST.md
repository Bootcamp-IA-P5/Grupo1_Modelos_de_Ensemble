# ✅ Checklist de Deployment - FireRiskAI

## 🎯 Objetivo
Desplegar el dashboard en Streamlit Cloud y el backend en Render

---

## ✅ PASO 1: Subir Código a GitHub

- [x] Código en GitHub
- [x] Branch: `development`
- [x] `.gitignore` configurado
- [x] No hay secrets en el repo

---

## ✅ PASO 2: Configurar Backend en Render

### **Ir a Render:**
https://dashboard.render.com/

### **Crear nuevo servicio:**
1. Click "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio de GitHub

### **Configuración:**
- **Name**: `fireriskai-backend`
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### **Variables de entorno:**
```
MONGO_URI=tu_mongo_uri_aqui
WEATHER_API_KEY=tu_api_key_aqui
DB_NAME=ensemble_models
APP_PORT=8000
LOG_LEVEL=INFO
```

### **Deploy y esperar:**
- [ ] Backend deployado
- [ ] URL obtenida: `https://fireriskai-backend.onrender.com`

---

## ✅ PASO 3: Configurar Dashboard en Streamlit Cloud

### **Ir a Streamlit Cloud:**
https://share.streamlit.io/

### **Crear nueva app:**
1. Click "New app"
2. Conecta tu repositorio de GitHub

### **Configuración:**
- **Repository**: `tu-usuario/Grupo1_Modelos_de_Ensemble`
- **Branch**: `development`
- **Main file path**: `streamlit_dashboard.py`

### **Configurar Secrets:**
Click en "Advanced settings" → "Secrets" → Pegar esto:

```toml
[MongoDB]
MONGO_URI = "tu_mongo_uri_aqui"
DB_NAME = "ensemble_models"

[WeatherAPI]
WEATHER_API_KEY = "tu_weather_api_key_aqui"

[Backend]
BASE_URL = "https://fireriskai-backend.onrender.com"
```

### **Reemplazar valores:**
- `tu_mongo_uri_aqui` → Tu URI de MongoDB
- `tu_weather_api_key_aqui` → Tu API key de weatherapi.com
- `https://fireriskai-backend.onrender.com` → URL de tu backend en Render

### **Deploy:**
- [ ] Dashboard deployado
- [ ] URL obtenida: `https://fireriskai.streamlit.app/`

---

## ✅ PASO 4: Verificar que Todo Funciona

- [ ] Dashboard carga correctamente
- [ ] Backend responde en `/health`
- [ ] Predicción funciona desde el dashboard
- [ ] MongoDB conectado
- [ ] Weather API funciona

---

## 📝 URLs Finales

Una vez desplegado:

- **Dashboard**: https://fireriskai.streamlit.app/
- **Backend**: https://fireriskai-backend.onrender.com/
- **API Docs**: https://fireriskai-backend.onrender.com/docs

---

## 🎉 ¡Listo para Presentar!

El dashboard estará disponible públicamente en la URL de Streamlit Cloud.

---

## 🐛 Troubleshooting

### **Dashboard no carga:**
- Verificar que los secrets estén configurados
- Ver logs en Streamlit Cloud

### **No se conecta al backend:**
- Verificar que `BASE_URL` en secrets sea correcta
- Verificar que el backend esté corriendo en Render

### **Error de MongoDB:**
- Verificar que `MONGO_URI` sea correcta
- Verificar que el cluster en MongoDB Atlas esté activo

---

**© 2025 Grupo 1 - FireRiskAI**

