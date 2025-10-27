# 🚀 Deployment Rápido - FireRiskAI

## 📋 Situación Actual

- ✅ Dashboard Streamlit (`streamlit_dashboard.py`) - Listo para deployar
- ❓ Backend FastAPI - Problemas en Render
- ✅ MongoDB Atlas - Configurado
- ✅ Variables de entorno - Configuradas

## 🎯 Opciones de Deployment

### **Opción 1: Streamlit Cloud (Solo Dashboard) ⚡**

**Ventajas:**
- Deployment automático
- Gratis
- Fácil de configurar
- Ideal para demos

**Limitaciones:**
- El backend debe estar desplegado en otro lado (Render, Railway, etc.)
- No puede correr el backend FastAPI

**Pasos:**
1. Ve a https://share.streamlit.io/
2. Conecta tu repositorio
3. Configura:
   - **Main file**: `streamlit_dashboard.py`
   - **Branch**: `development`
4. Agrega secrets (formato TOML):
```toml
[MongoDB]
MONGO_URI = "tu_mongo_uri"
DB_NAME = "ensemble_models"

[WeatherAPI]
WEATHER_API_KEY = "tu_api_key"

[Backend]
BASE_URL = "https://tu-backend-render.onrender.com"
```
5. Deploy! 🎉

### **Opción 2: Render (Backend + Dashboard) 🔄**

**Para el Backend (FastAPI):**
1. Crear nuevo Web Service en Render
2. Conectar tu repositorio
3. Configuración:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
4. Variables de entorno:
   - `MONGO_URI`
   - `WEATHER_API_KEY`
5. Deploy

**Para el Dashboard (Streamlit):**
1. Crear otro Web Service
2. **Runtime**: Streamlit
3. **Start Command**: `streamlit run streamlit_dashboard.py --server.port $PORT --server.address 0.0.0.0`
4. Mismas variables de entorno + `BASE_URL` del backend

### **Opción 3: Railway.app (Todo junto) 🚂**

**Ventajas:**
- Más simple que Render
- Deployment automático
- Gratis con limites generosos

**Pasos:**
1. Ve a https://railway.app/
2. Conecta tu GitHub
3. Crea 2 servicios:
   - **Backend**: FastAPI en `app.py`
   - **Dashboard**: Streamlit en `streamlit_dashboard.py`
4. Configura variables de entorno en ambos
5. Deploy!

## 🔧 Troubleshooting Render

### **Si el backend falla en Render:**

**Problemas comunes:**
1. **Timeout en startup** - El modelo pesa mucho
2. **Memory limit** - Muy poca RAM
3. **Port binding** - Puerto no configurado

**Soluciones:**

1. **Usar modelo más pequeño para testing**:
```bash
# Crear una versión ligera del modelo
# (Ya tienes esto en models/)
```

2. **Aumentar timeout en Render:**
```yaml
# En render.yaml
buildCommand: pip install -r requirements.txt
startCommand: uvicorn app:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 60
```

3. **Usar plan de pago** (si necesitas más recursos)

## 🎯 Recomendación Final

Para la presentación, usa:

**Backend**: Render.com o Railway.app
**Dashboard**: Streamlit Cloud

Esto te da:
- ✅ Máxima flexibilidad
- ✅ Deployment rápido
- ✅ Gratis (o muy barato)
- ✅ Funciona todo

## 📝 URLs Finales

Una vez desplegado:
- **Dashboard**: https://fireriskai.streamlit.app/
- **Backend**: https://fireriskai-backend.onrender.com/ (o railway)
- **API Docs**: https://fireriskai-backend.onrender.com/docs

## 🚨 Importante

- ⚠️ El backend en Streamlit Cloud NO funcionará (limite de Streamlit)
- ✅ Usa Render o Railway para el backend
- ✅ Usa Streamlit Cloud solo para el dashboard
- ✅ Conecta el dashboard al backend con `BASE_URL` en secrets

## 📞 Próximos Pasos

1. **Intenta deployar el backend en Railway** (más fácil que Render)
2. **Deploy el dashboard en Streamlit Cloud**
3. **Configura los secrets**
4. **Testa que todo funcione**

---

¿Necesitas ayuda con Railway o prefieres seguir intentando con Render?

