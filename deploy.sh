#!/bin/bash

# Script de despliegue para EcoPrint AI
# Sistema de Predicción de Riesgo de Incendios Forestales

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
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

# ===========================================
# Verificaciones previas
# ===========================================
print_message "Iniciando despliegue de EcoPrint AI..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Verificar que Docker Compose esté instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Verificar que existe el archivo .env
if [ ! -f .env ]; then
    print_warning "Archivo .env no encontrado. Creando desde env.example..."
    if [ -f env.example ]; then
        cp env.example .env
        print_warning "Por favor configura las variables de entorno en .env antes de continuar."
        exit 1
    else
        print_error "No se encontró env.example. Por favor crea un archivo .env con las variables necesarias."
        exit 1
    fi
fi

# ===========================================
# Construir imagen Docker
# ===========================================
print_message "Construyendo imagen Docker..."
docker build -t ecoprint-ai:latest .

if [ $? -eq 0 ]; then
    print_message "✅ Imagen construida exitosamente"
else
    print_error "❌ Error construyendo la imagen"
    exit 1
fi

# ===========================================
# Parar contenedores existentes
# ===========================================
print_message "Deteniendo contenedores existentes..."
docker-compose down

# ===========================================
# Iniciar servicios
# ===========================================
print_message "Iniciando servicios..."

# Preguntar si quiere usar MongoDB local
read -p "¿Quieres usar MongoDB local? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Iniciando con MongoDB local..."
    docker-compose --profile local-db up -d
else
    print_info "Iniciando solo la API (usando MongoDB Atlas)..."
    docker-compose up -d ecoprint-api
fi

# ===========================================
# Verificar estado de los servicios
# ===========================================
print_message "Verificando estado de los servicios..."

# Esperar a que la API esté lista
print_info "Esperando a que la API esté lista..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health &> /dev/null; then
        print_message "✅ API está funcionando correctamente"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "❌ La API no respondió después de 30 intentos"
        print_info "Revisa los logs con: docker-compose logs ecoprint-api"
        exit 1
    fi
    sleep 2
done

# ===========================================
# Mostrar información de acceso
# ===========================================
print_message "🎉 Despliegue completado exitosamente!"
echo
print_info "📊 Servicios disponibles:"
print_info "  • API: http://localhost:8000"
print_info "  • Docs: http://localhost:8000/docs"
print_info "  • Health: http://localhost:8000/health"

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "  • MongoDB: localhost:27017"
    print_info "  • Mongo Express: http://localhost:8081 (admin/admin123)"
fi

echo
print_info "🔧 Comandos útiles:"
print_info "  • Ver logs: docker-compose logs -f"
print_info "  • Parar servicios: docker-compose down"
print_info "  • Reiniciar: docker-compose restart"
print_info "  • Estado: docker-compose ps"

echo
print_message "¡EcoPrint AI está listo para usar! 🌲🔥"
