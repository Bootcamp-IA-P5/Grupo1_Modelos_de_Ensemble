# 🐳 **Guía de Despliegue con Docker - EcoPrint AI**

Esta guía explica cómo desplegar **EcoPrint AI** usando Docker y Docker Compose.



### **1. Instalar Docker**
```bash
# macOS (con Homebrew)
brew install --cask docker

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Windows
# Descargar Docker Desktop desde https://www.docker.com/products/docker-desktop
```

### **2. Verificar instalación**
```bash
docker --version
docker-compose --version
```

### **3. Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar variables necesarias
nano .env
```

**Variables importantes:**
```env
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
DB_NAME=ensemble_models
```

## 🚀 **DESPLIEGUE RÁPIDO**

### **Opción 1: Script automático (Recomendado)**
```bash
# Ejecutar script de despliegue
./deploy.sh
```

### **Opción 2: Comandos manuales**
```bash
# 1. Construir imagen
docker build -t ecoprint-ai:latest .

# 2. Iniciar solo la API (con MongoDB Atlas)
docker-compose up -d ecoprint-api

# 3. O iniciar con MongoDB local
docker-compose --profile local-db up -d
```

## 🏗️ **ARQUITECTURA DE CONTENEDORES**

### **Servicios incluidos:**

#### **1. ecoprint-api** (Puerto 8000)
- **Función**: API Backend de FastAPI
- **Imagen**: Construida desde Dockerfile
- **Puerto**: 8000
- **Variables**: MONGO_URI, DB_NAME

#### **2. mongo** (Puerto 27017) - Opcional
- **Función**: Base de datos MongoDB local
- **Imagen**: mongo:7.0
- **Puerto**: 27017
- **Volumen**: mongo_data

#### **3. mongo-express** (Puerto 8081) - Opcional
- **Función**: Interfaz web para administrar MongoDB
- **Imagen**: mongo-express:1.0.0
- **Puerto**: 8081
- **Credenciales**: admin/admin123

## 🔧 **CONFIGURACIÓN AVANZADA**

### **1. Variables de entorno**

**Archivo `.env`:**
```env
# MongoDB
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
DB_NAME=ensemble_models

# API
API_HOST=0.0.0.0
API_PORT=8000
PYTHONPATH=/app
```

### **2. Volúmenes persistentes**

**Datos que persisten:**
- `./models` → Modelos de ML (solo lectura)
- `./logs` → Logs de la aplicación
- `mongo_data` → Datos de MongoDB (si usas MongoDB local)

### **3. Redes**

**Red personalizada:**
- `ecoprint-network`: Red bridge para comunicación entre contenedores

## 📊 **MONITOREO Y LOGS**

### **Ver logs en tiempo real:**
```bash
# Todos los servicios
docker-compose logs -f

# Solo la API
docker-compose logs -f ecoprint-api

# Solo MongoDB
docker-compose logs -f mongo
```

### **Verificar estado:**
```bash
# Estado de contenedores
docker-compose ps

# Uso de recursos
docker stats

# Health check
curl http://localhost:8000/health
```

## 🛠️ **COMANDOS ÚTILES**

### **Gestión de contenedores:**
```bash
# Iniciar servicios
docker-compose up -d

# Parar servicios
docker-compose down

# Reiniciar un servicio
docker-compose restart ecoprint-api

# Reconstruir imagen
docker-compose build --no-cache ecoprint-api
```

### **Acceso a contenedores:**
```bash
# Entrar al contenedor de la API
docker-compose exec ecoprint-api bash

# Entrar al contenedor de MongoDB
docker-compose exec mongo mongosh
```

### **Limpieza:**
```bash
# Parar y eliminar contenedores
docker-compose down

# Eliminar volúmenes
docker-compose down -v

# Eliminar imágenes
docker rmi ecoprint-ai:latest
```

## 🔍 **SOLUCIÓN DE PROBLEMAS**

### **Problema: La API no inicia**
```bash
# Ver logs detallados
docker-compose logs ecoprint-api

# Verificar variables de entorno
docker-compose exec ecoprint-api env | grep MONGO
```

### **Problema: Error de conexión a MongoDB**
```bash
# Verificar que MongoDB esté corriendo
docker-compose ps mongo

# Verificar conectividad
docker-compose exec ecoprint-api ping mongo
```

### **Problema: Puerto ocupado**
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar puerto 8001 en lugar de 8000
```

## 🌐 **ACCESO A LA APLICACIÓN**

### **Endpoints disponibles:**
- **API Principal**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Mongo Express**: http://localhost:8081 (si usas MongoDB local)

### **Ejemplo de uso:**
```bash
# Health check
curl http://localhost:8000/health

# Información del modelo
curl http://localhost:8000/model/info

# Hacer predicción
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [2000, 180, 15, 300, 50, 1000, 200, 220, 180, 2000] + [0] * 44,
    "user_id": "test_user"
  }'
```

## 🚀 **DESPLIEGUE EN PRODUCCIÓN**

### **1. Configuración de producción:**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  ecoprint-api:
    image: ecoprint-ai:latest
    restart: always
    environment:
      - MONGO_URI=${MONGO_URI}
      - DB_NAME=${DB_NAME}
    ports:
      - "80:8000"
```

### **2. Usar con orquestadores:**
- **Kubernetes**: Para escalado automático
- **Docker Swarm**: Para clusters simples
- **AWS ECS**: Para despliegue en la nube

## 📈 **OPTIMIZACIONES**

### **1. Imagen multi-stage:**
- Reduce tamaño de imagen final
- Separa dependencias de build y runtime

### **2. Usuario no-root:**
- Mejora seguridad del contenedor
- Evita ejecutar como root

### **3. Health checks:**
- Monitoreo automático del estado
- Reinicio automático si falla

## ✅ **VERIFICACIÓN DEL DESPLIEGUE**

### **Checklist de verificación:**
- [ ] Contenedores están corriendo (`docker-compose ps`)
- [ ] API responde en http://localhost:8000/health
- [ ] Documentación accesible en http://localhost:8000/docs
- [ ] MongoDB conectado (verificar logs)
- [ ] Tests pasan (`docker-compose exec ecoprint-api python -m pytest`)

---

**EcoPrint AI** - Sistema de Predicción de Riesgo de Incendios Forestales 🌲🔥

*"Containerizado para máxima portabilidad y escalabilidad"*
