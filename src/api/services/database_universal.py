"""
Servicio de MongoDB Universal
Funciona en Windows, Mac y Linux
Detecta automáticamente el SO y usa la configuración apropiada
"""

import os
import platform
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class DatabaseServiceUniversal:
    """
    Servicio de MongoDB que funciona en todos los sistemas operativos
    """
    
    def __init__(self):
        self.client = None
        self.database = None
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME", "ensemble_models")
        self.os_name = platform.system().lower()
        
        logger.info(f" DatabaseServiceUniversal inicializado para: {self.db_name} en {self.os_name}")
    
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
        Conectar a MongoDB con configuración automática según el SO
        """
        try:
            if not self.mongo_uri:
                logger.error("❌ MONGO_URI no configurada")
                return False
            
            if "<db_password>" in self.mongo_uri:
                logger.error("❌ Reemplaza <db_password> con tu contraseña real")
                return False
            
            logger.info(f"🔌 Conectando a MongoDB Atlas ({self.os_name})...")
            
            # Obtener configuración SSL según el SO
            ssl_config = self._get_ssl_config()
            
            # Crear cliente con configuración específica del SO
            self.client = AsyncIOMotorClient(self.mongo_uri, **ssl_config)
            self.database = self.client[self.db_name]
            
            # Probar conexión
            await self.client.admin.command('ping')
            logger.info(f"✅ Conectado a MongoDB ({self.os_name}): {self.db_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error conectando a MongoDB ({self.os_name}): {e}")
            return False
    
    async def disconnect(self):
        """Desconectar de MongoDB"""
        if self.client:
            self.client.close()
            logger.info("🔌 Desconectado de MongoDB")
    
    def get_collection(self, collection_name: str):
        """Obtener colección"""
        if self.database is None:
            raise RuntimeError("❌ Base de datos no conectada")
        return self.database[collection_name]
    
    def get_system_info(self):
        """Obtener información del sistema"""
        return {
            "os": self.os_name,
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "database": self.db_name,
            "connected": self.client is not None and self.client.is_connected
        }

# Instancia global universal
db_service_universal = DatabaseServiceUniversal()
