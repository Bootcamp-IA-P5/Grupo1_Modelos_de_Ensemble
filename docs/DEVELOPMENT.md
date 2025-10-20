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
streamlit run main.py
```

### 4. Acceder a la aplicación
- **Streamlit**: http://localhost:8501

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

# Ejecutar Streamlit localmente
streamlit run main.py
```

## Estructura del Proyecto

```
├── main.py                 # Aplicación principal (Streamlit)
├── requirements.txt        # Dependencias Python
├── Dockerfile             # Configuración Docker
├── docker-compose.yml     # Docker Compose
├── README.md              # Documentación principal
├── .gitignore             # Archivos ignorados por Git
│
├── src/                   # TODO EL CÓDIGO PYTHON
│   ├── data/              # Código para manejar datos
│   ├── models/            # Código de modelos ML
│   ├── utils/             # Utilidades
│   └── visualization/     # Código para gráficos
│
├── data/                  # Datos (raw/processed)
├── models/                # Modelos entrenados guardados (.pkl, .joblib)
├── notebooks/             # Jupyter notebooks
├── tests/                 # Tests unitarios
└── config/                # Configuraciones
```

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
