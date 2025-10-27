# 🚀 Guía de Deployment en Streamlit Cloud

## 📋 Prerrequisitos

1. **Cuenta de Streamlit Cloud** - https://share.streamlit.io/
2. **Repositorio en GitHub** - Con el código del proyecto
3. **Backend desplegado** - En Render.com o similar

## 🛠️ Configuración

### **1. Preparar Secrets**

Streamlit Cloud usa un archivo `.streamlit/secrets.toml` para configurar variables de entorno.

**No comites el archivo de secrets** - Se configura en Streamlit Cloud directamente.

#### **Variables Necesarias:**

```toml
[MongoDB]
MONGO_URI = "mongodb+srv://..."
DB_NAME = "ensemble_models"

[WeatherAPI]
WEATHER_API_KEY = "tu_api_key"

[Backend]
BASE_URL = "https://tu-app-render.onrender.com"
```

### **2. Configurar Secrets en Streamlit Cloud**

1. Ve a https://share.streamlit.io/
2. Conecta tu repositorio de GitHub
3. En la configuración de la app, busca "Secrets"
4. Pega el contenido de `.streamlit/secrets.toml.example` (sin el `.example`)
5. Reemplaza los valores con tus valores reales

### **3. Cómo Obtener los Secrets**

#### **MongoDB URI:**
```
De tu cuenta de MongoDB Atlas:
- Database → Connect → Connect your application
- Copia la URI de conexión
```

#### **Weather API Key:**
```
De https://www.weatherapi.com/:
- Regístrate y obtén tu API key
```

#### **Backend URL:**
```
De tu deployment en Render.com:
- Copia la URL de tu app (e.g., https://fireriskai.onrender.com)
```

## 📝 Configuración en Streamlit Cloud

### **Settings de la App:**

- **Repository**: `tu-usuario/Grupo1_Modelos_de_Ensemble`
- **Branch**: `development` o `main`
- **Main file path**: `streamlit_dashboard.py`
- **Python version**: 3.11

### **Secrets (Toml format):**

```toml
[MongoDB]
MONGO_URI = "mongodb+srv://..."
DB_NAME = "ensemble_models"

[WeatherAPI]
WEATHER_API_KEY = "abc123..."

[Backend]
BASE_URL = "https://fireriskai-backend.onrender.com"
```

## 🔧 Configuración del Código

El código ya está preparado para leer secrets de Streamlit:

```python
# En streamlit_dashboard.py (línea 22-28)
try:
    BASE_URL = st.secrets["Backend"]["BASE_URL"]
except (KeyError, FileNotFoundError):
    BASE_URL = "http://localhost:8000"  # Fallback local
```

## ✅ Checklist de Deployment

### **Antes de Deployar:**

- [ ] Backend desplegado en Render.com
- [ ] MongoDB Atlas configurado
- [ ] API keys obtenidas (Weather API)
- [ ] Repositorio en GitHub
- [ ] Code en branch `development` o `main`

### **En Streamlit Cloud:**

- [ ] Conectar repositorio de GitHub
- [ ] Configurar secrets en formato TOML
- [ ] Configurar branch correcto
- [ ] Configurar main file path (`streamlit_dashboard.py`)
- [ ] Desplegar y probar

### **Después del Deployment:**

- [ ] Verificar que la app carga
- [ ] Probar predicción desde el dashboard
- [ ] Verificar conexión con backend
- [ ] Probar todas las páginas del dashboard

## 🐛 Troubleshooting

### **Error: "Cannot connect to backend"**

**Causa**: El backend no está desplegado o la URL es incorrecta.

**Solución**:
- Verificar que el backend esté corriendo en Render.com
- Verificar que la URL en secrets sea correcta
- Verificar que el backend tenga CORS habilitado

### **Error: "MongoDB connection failed"**

**Causa**: URI de MongoDB incorrecta o firewall bloqueando conexión.

**Solución**:
- Verificar que la URI tenga la contraseña correcta
- Verificar que el IP esté permitido en MongoDB Atlas

### **Error: "API key invalid"**

**Causa**: Weather API key incorrecta o no configurada.

**Solución**:
- Verificar que la key sea correcta en secrets
- Verificar que la key tenga créditos disponibles

## 📊 URLs del Sistema

### **Producción:**

- **Streamlit Dashboard**: https://fireriskai.streamlit.app/
- **Backend API**: https://fireriskai-backend.onrender.com/
- **Documentación API**: https://fireriskai-backend.onrender.com/docs

### **Local (Desarrollo):**

- **Streamlit Dashboard**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 🔐 Seguridad

### **⚠️ IMPORTANTE:**

1. **NUNCA comitas el archivo de secrets** con valores reales
2. **Solo usa `.streamlit/secrets.toml.example`** en el repositorio
3. **Los valores reales se configuran solo en Streamlit Cloud**
4. **No compartas tus API keys públicamente**

## 📝 Archivos a NO Comitear

```bash
# Nunca comites estos archivos con valores reales:
.streamlit/secrets.toml  # ❌ NO comitear
.env                     # ❌ NO comitear
*.pkl                    # ❌ Modelos grandes
venv/                    # ❌ Entorno virtual
```

## ✅ Archivos Seguros para Comitear

```bash
# ✅ Estos archivos son seguros:
.streamlit/secrets.toml.example  # Solo plantilla
env.example                     # Solo ejemplo
streamlit_dashboard.py          # Código
requirements.txt                # Dependencias
README.md                       # Documentación
```

## 🎉 Deployment Exitoso

Una vez desplegado, tu dashboard estará disponible en:

**https://tu-usuario-streamlit.streamlit.app/**

## 📚 Referencias

- **Streamlit Cloud**: https://share.streamlit.io/
- **Streamlit Secrets**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- **Render.com**: https://render.com/
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas

---

**© 2025 Grupo 1 - FireRiskAI**

