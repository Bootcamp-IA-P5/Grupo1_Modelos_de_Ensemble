FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/raw data/processed models logs

# Puerto para Streamlit
EXPOSE 8501

# Comando por defecto
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
