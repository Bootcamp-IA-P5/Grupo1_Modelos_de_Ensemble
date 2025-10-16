# 🚀 Guía de Desarrollo

## Configuración Inicial

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Grupo1_Modelos_de_Ensemble
```

### 2. Configurar entorno virtual
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate     # En Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
# Con entorno virtual activado
python main.py
```

### 4. Acceder a la aplicación
- **API FastAPI**: http://localhost:8000
  - Endpoints para datos y modelos
  - Recibir/enviar datos programáticamente
- **Documentación API**: http://localhost:8000/docs
  - Interfaz interactiva para probar endpoints

## Comandos Útiles

### Docker
```bash
# Levantar servicios
docker-compose up -d

# Parar servicios
docker-compose down

# Reconstruir imagen
docker-compose build --no-cache

# Entrar al contenedor
docker-compose exec app bash
```

### Desarrollo
```bash
# Instalar dependencias localmente (opcional)
pip install -r requirements.txt

# Ejecutar aplicación localmente
python main.py
```

## Estructura del Proyecto

```
├── main.py                 # Aplicación principal (punto de entrada)
├── requirements.txt        # Dependencias Python
├── .env                   # Variables de entorno (NO subir a Git)
├── README.md              # Documentación principal
├── .gitignore             # Archivos ignorados por Git
│
├── src/                   # TODO EL CÓDIGO PYTHON
│   ├── data/              # Código para manejar datos
│   ├── models/            # Código de modelos ML
│   ├── utils/             # Utilidades
│   ├── visualization/     # Código para gráficos
│   └── api/               # API FastAPI (backend)
│
├── data/                  # Datos (raw/processed)
├── models/                # Modelos entrenados guardados (.pkl, .joblib)
├── notebooks/             # Jupyter notebooks
├── tests/                 # Tests unitarios
└── config/                # Configuraciones
```

## ¿Qué hace cada archivo?

### **Archivos principales:**
- **`main.py`**: Punto de entrada principal (ejecuta la API)
- **`src/api/api.py`**: API con FastAPI (backend)
- **`.env`**: Configuración de MongoDB (cada uno tiene su propio archivo)

### **Carpetas de código (`src/`):**
- **`data/`**: Código para cargar, limpiar y procesar datos
- **`models/`**: Código para entrenar y usar modelos de ML
- **`utils/`**: Funciones auxiliares y utilidades
- **`visualization/`**: Código para crear gráficos y visualizaciones
- **`api/`**: Endpoints de la API para comunicación entre aplicaciones

### **Carpetas de archivos:**
- **`data/`**: Archivos de datos (.csv, .json, etc.)
- **`models/`**: Modelos guardados (.pkl, .joblib)
- **`notebooks/`**: Jupyter notebooks para análisis
- **`tests/`**: Tests unitarios del código

## Flujo de Trabajo

1. **Crear rama**: `git checkout -b feature/nombre-feature`
2. **Desarrollar**: Hacer cambios en el código
3. **Probar**: `docker-compose up` para verificar
4. **Commit**: `git add . && git commit -m "mensaje"`
5. **Push**: `git push origin feature/nombre-feature`
6. **Pull Request**: Crear PR en GitHub

## Variables de Entorno

Copia `env.example` a `.env` y configura:
```bash
cp env.example .env
```

## Troubleshooting

### Puerto ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8502:8501"  # Usar puerto 8502
```

### Problemas de permisos
```bash
# En macOS/Linux
sudo chown -R $USER:$USER .
```
