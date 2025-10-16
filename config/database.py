"""
Configuración de base de datos MongoDB
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DatabaseConfig:
    """Configuración de la base de datos"""
    
    def __init__(self):
        self.mongodb_url = os.getenv('MONGODB_URL')
        self.database_name = os.getenv('MONGODB_DATABASE', 'ml_project')
        
        if not self.mongodb_url:
            raise ValueError("MONGODB_URL no está configurada en las variables de entorno")
    
    def get_connection_string(self):
        """Obtiene la cadena de conexión a MongoDB"""
        return self.mongodb_url
    
    def get_database_name(self):
        """Obtiene el nombre de la base de datos"""
        return self.database_name

# Instancia global de configuración
db_config = DatabaseConfig()
