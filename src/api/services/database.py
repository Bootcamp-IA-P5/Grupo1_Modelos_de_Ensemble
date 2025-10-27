"""
Servicio de conexión a MongoDB
EcoPrint - Sistema de Predicción de Riesgo de Incendios Forestales
"""

import os
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
        """
        self.client = None
        self.database = None
        
        # Obtener configuración desde variables de entorno
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME", "ensemble_models")
        
        logger.info(f"🔧 DatabaseService inicializado para: {self.db_name}")
    
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
            
            # Crear cliente asíncrono
            self.client = AsyncIOMotorClient(self.mongo_uri)
            
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
