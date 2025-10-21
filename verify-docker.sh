#!/bin/bash

# Script de verificación para Docker
# EcoPrint AI - Sistema de Predicción de Riesgo de Incendios Forestales

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_message() {
    echo -e "${GREEN}[EcoPrint AI]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_message "Verificando configuración de Docker para EcoPrint AI..."

# ===========================================
# Verificar Docker
# ===========================================
print_info "Verificando Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_message "✅ Docker encontrado: $DOCKER_VERSION"
else
    print_error "❌ Docker no está instalado"
    print_info "Instala Docker desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# ===========================================
# Verificar Docker Compose
# ===========================================
print_info "Verificando Docker Compose..."
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    print_message "✅ Docker Compose encontrado: $COMPOSE_VERSION"
else
    print_error "❌ Docker Compose no está instalado"
    exit 1
fi

# ===========================================
# Verificar Docker daemon
# ===========================================
print_info "Verificando Docker daemon..."
if docker info &> /dev/null; then
    print_message "✅ Docker daemon está corriendo"
else
    print_warning "⚠️ Docker daemon no está corriendo"
    print_info "Inicia Docker Desktop o ejecuta: sudo systemctl start docker"
    print_info "Luego ejecuta este script nuevamente"
    exit 1
fi

# ===========================================
# Verificar archivos necesarios
# ===========================================
print_info "Verificando archivos de configuración..."

REQUIRED_FILES=(
    "Dockerfile"
    "docker-compose.yml"
    ".dockerignore"
    "requirements.txt"
    "app.py"
    ".env"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_message "✅ $file encontrado"
    else
        print_error "❌ $file no encontrado"
        exit 1
    fi
done

# ===========================================
# Verificar estructura del proyecto
# ===========================================
print_info "Verificando estructura del proyecto..."

REQUIRED_DIRS=(
    "src"
    "models"
    "docs"
    "tests"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_message "✅ Directorio $dir encontrado"
    else
        print_error "❌ Directorio $dir no encontrado"
        exit 1
    fi
done

# ===========================================
# Verificar variables de entorno
# ===========================================
print_info "Verificando variables de entorno..."

if grep -q "MONGO_URI" .env; then
    print_message "✅ MONGO_URI configurada"
else
    print_warning "⚠️ MONGO_URI no encontrada en .env"
fi

if grep -q "DB_NAME" .env; then
    print_message "✅ DB_NAME configurada"
else
    print_warning "⚠️ DB_NAME no encontrada en .env"
fi

# ===========================================
# Verificar sintaxis de Docker Compose
# ===========================================
print_info "Verificando sintaxis de docker-compose.yml..."
if docker-compose config &> /dev/null; then
    print_message "✅ docker-compose.yml tiene sintaxis válida"
else
    print_error "❌ Error en sintaxis de docker-compose.yml"
    docker-compose config
    exit 1
fi

# ===========================================
# Verificar Dockerfile
# ===========================================
print_info "Verificando Dockerfile..."
if [ -s "Dockerfile" ]; then
    print_message "✅ Dockerfile no está vacío"
else
    print_error "❌ Dockerfile está vacío o no existe"
    exit 1
fi

# ===========================================
# Resumen final
# ===========================================
print_message "🎉 Verificación completada exitosamente!"
echo
print_info "📋 Resumen:"
print_info "  • Docker: ✅ Instalado y funcionando"
print_info "  • Docker Compose: ✅ Instalado"
print_info "  • Archivos de configuración: ✅ Presentes"
print_info "  • Estructura del proyecto: ✅ Correcta"
print_info "  • Sintaxis: ✅ Válida"
echo
print_info "🚀 Listo para desplegar con:"
print_info "  ./deploy.sh"
echo
print_message "¡EcoPrint AI está listo para Docker! 🐳"
