"""
Servicio de conexión a MongoDB
EcoPrint - Sistema de Predicción de Riesgo de Incendios Forestales
"""

import os
import platform
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseService:
    """
    Servicio para manejar la conexión a MongoDB Atlas
    
    ¿Por qué una clase?
    - Encapsula toda la lógica de conexión
    - Permite reutilizar la conexión en toda la app
    - Maneja errores de forma centralizada
    """
    
    def __init__(self):
        """
        Inicializar el servicio de base de datos
        
        ¿Por qué en __init__?
        - Configuramos las variables una sola vez
        - No conectamos hasta que se necesite (lazy loading)
        - Detectamos el SO automáticamente
        """
        self.client = None
        self.database = None
        self.os_name = platform.system().lower()
        
        # Obtener configuración desde variables de entorno
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME", "ensemble_models")
        
        logger.info(f"🔧 DatabaseService inicializado para: {self.db_name} en {self.os_name}")
    
    def _get_ssl_config(self):
        """
        Obtener configuración SSL según el sistema operativo
        
        ¿Por qué diferentes configuraciones?
        - Windows: Problemas con certificados SSL
        - Mac/Linux: Configuración estándar funciona bien
        """
        
        if self.os_name == "windows":
            # Configuración para Windows (más permisiva)
            return {
                'serverSelectionTimeoutMS': 60000,  # 60 segundos
                'connectTimeoutMS': 60000,         # 60 segundos
                'socketTimeoutMS': 60000,          # 60 segundos
                'maxPoolSize': 5,                  # Menos conexiones
                'retryWrites': True,
                'retryReads': True,
                'ssl': True,
                'ssl_cert_reqs': 0,                # No verificar certificados
                'tls': True,
                'tlsAllowInvalidCertificates': True,
                'tlsAllowInvalidHostnames': True,
                'tlsInsecure': True,               # Permitir conexiones inseguras
                'directConnection': False,         # Usar replica set
                'readPreference': 'primaryPreferred',
            }
        else:
            # Configuración para Mac/Linux (estándar)
            return {
                'serverSelectionTimeoutMS': 30000,  # 30 segundos
                'connectTimeoutMS': 30000,         # 30 segundos
                'socketTimeoutMS': 30000,          # 30 segundos
                'maxPoolSize': 10,                 # Más conexiones
                'retryWrites': True,
                'retryReads': True,
                'ssl': True,
                'tls': True,
                'readPreference': 'primaryPreferred',
            }
    
    async def connect(self):
        """
        Conectar a MongoDB Atlas
        
        ¿Por qué async?
        - MongoDB es una operación de red (I/O)
        - No bloquea el servidor mientras conecta
        - Mejor rendimiento para APIs
        """
        try:
            # Verificar que tenemos la URI
            if not self.mongo_uri:
                logger.error("❌ MONGO_URI no configurada en variables de entorno")
                return False
            
            # Verificar que no tenga placeholder
            if "<db_password>" in self.mongo_uri:
                logger.error("❌ Reemplaza <db_password> con tu contraseña real")
                return False
            
            logger.info("🔌 Conectando a MongoDB Atlas...")
            
            # Crear cliente asíncrono con configuración según el SO
            ssl_config = self._get_ssl_config()
            self.client = AsyncIOMotorClient(self.mongo_uri, **ssl_config)
            
            # Seleccionar base de datos
            self.database = self.client[self.db_name]
            
            # Verificar conexión con ping
            await self.client.admin.command('ping')
            
            logger.info(f"✅ Conectado a MongoDB: {self.db_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error conectando a MongoDB: {e}")
            return False
    
    async def disconnect(self):
        """
        Desconectar de MongoDB
        
        ¿Por qué es importante?
        - Libera recursos del servidor
        - Cierra conexiones correctamente
        - Evita memory leaks
        """
        if self.client:
            self.client.close()
            logger.info("🔌 Desconectado de MongoDB")
    
    def get_collection(self, collection_name: str):
        """
        Obtener una colección específica
        
        ¿Por qué este método?
        - Centraliza el acceso a colecciones
        - Verifica que estemos conectados
        - Consistencia en toda la app
        """
        if self.database is None:
            raise RuntimeError("❌ Base de datos no conectada. Llama a connect() primero.")
        
        return self.database[collection_name]

# Instancia global del servicio
# ¿Por qué global?
# - Una sola conexión para toda la app
# - Fácil acceso desde cualquier parte
# - Patrón singleton
db_service = DatabaseService()
