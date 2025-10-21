# Dockerfile para EcoPrint AI - Sistema de Predicción de Riesgo de Incendios Forestales
# Multi-stage build para optimizar el tamaño de la imagen

# ===========================================
# STAGE 1: Build stage
# ===========================================
FROM python:3.11-slim as builder

# Instalar dependencias del sistema necesarias para compilar
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ===========================================
# STAGE 2: Runtime stage
# ===========================================
FROM python:3.11-slim

# Instalar dependencias del sistema para runtime
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd -r ecoprint && useradd -r -g ecoprint ecoprint

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde el stage anterior
COPY --from=builder /root/.local /home/ecoprint/.local

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/processed data/raw data/external models logs

# Cambiar ownership de archivos al usuario ecoprint
RUN chown -R ecoprint:ecoprint /app

# Cambiar al usuario no-root
USER ecoprint

# Agregar el directorio de dependencias al PATH
ENV PATH=/home/ecoprint/.local/bin:$PATH

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
