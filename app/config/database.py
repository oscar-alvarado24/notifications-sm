import oracledb
import os
from contextlib import contextmanager

class DatabaseConfig:
    """Configuración de la base de datos Oracle"""
    
    def __init__(self):
        # Configuración desde variables de entorno o valores por defecto
        self.user = os.getenv('ORACLE_USER', 'tu_usuario')
        self.password = os.getenv('ORACLE_PASSWORD', 'tu_password')
        self.dsn = os.getenv('ORACLE_DSN', 'localhost:1521/free')
        self.pool_min = int(os.getenv('ORACLE_POOL_MIN', '2'))
        self.pool_max = int(os.getenv('ORACLE_POOL_MAX', '10'))
        self.pool_increment = int(os.getenv('ORACLE_POOL_INCREMENT', '1'))
        
        # Pool de conexiones
        from typing import Optional
        self._pool: Optional[oracledb.ConnectionPool] = None

    def create_pool(self):
        """Crea un pool de conexiones a Oracle"""
        try:
            self._pool = oracledb.create_pool(
                user=self.user,
                password=self.password,
                dsn=self.dsn,
                min=self.pool_min,
                max=self.pool_max,
                increment=self.pool_increment
            )
            print(f"Pool de conexiones creado exitosamente. Min: {self.pool_min}, Max: {self.pool_max}")
        except oracledb.Error as error:
            print(f"Error creando pool de conexiones: {error}")
            raise
    
    def get_connection(self):
        """Obtiene una conexión del pool"""
        try:
            if self._pool is None:
                self.create_pool()
            assert self._pool is not None, "El pool de conexiones no se pudo crear."
            return self._pool.acquire()
        except oracledb.Error as error:
            print(f"Error obteniendo conexión: {error}")
            raise
    
    @contextmanager
    def get_connection_context(self):
        """Context manager para manejo automático de conexiones"""
        connection = None
        try:
            connection = self.get_connection()
            yield connection
        except Exception as error:
            print(f"Error en la conexión: {error}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
    
    def close_pool(self):
        """Cierra el pool de conexiones"""
        if self._pool:
            self._pool.close()
            print("Pool de conexiones cerrado")

# Instancia global de configuración
db_config = DatabaseConfig()

def get_db_connection():
    """Función helper para obtener conexión"""
    return db_config.get_connection()

def init_database():
    """Inicializa el pool de conexiones"""
    db_config.create_pool()

def close_database():
    """Cierra el pool de conexiones"""
    db_config.close_pool()