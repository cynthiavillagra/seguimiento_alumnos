import os
import psycopg2
from psycopg2.extras import RealDictCursor

from src.infrastructure.database.postgres_schema import POSTGRES_SCHEMA

# Singleton de conexión
class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """
        Obtiene una conexión a la base de datos (PostgreSQL).
        """
        # Verificar si la conexión está cerrada y reconectar
        if self._connection and (self._connection.closed != 0):
             self._connection = None
             
        if self._connection is None:
            # 1. Intentar conectar a PostgreSQL (Producción/Vercel)
            # DATABASE_URL es estándar en Vercel, POSTGRES_URL también suele estar
            db_url = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
            
            if db_url:
                try:
                    # NOTA CRÍTICA PARA VERCEL/NEON:
                    # En entornos serverless con pooling, a veces necesitamos 'sslmode' explícito si la URL no lo tiene.
                    # Psycopg2-binary suele necesitar libpq, que Vercel provee.
                    
                    print(f"Intentando conectar a Postgres... (URL length: {len(db_url)})")
                    
                    # Forzar SSL si no está en la URL (común en Neon/Vercel)
                    connect_args = {'cursor_factory': RealDictCursor}
                    if 'sslmode' not in db_url:
                        connect_args['sslmode'] = 'require'
                        
                    self._connection = psycopg2.connect(db_url, **connect_args)
                    print("✅ Conexión a PostgreSQL exitosa")
                except Exception as e:
                    print(f"❌ Error conectando a PostgreSQL: {e}")
                    raise e
            else:
                # Si no hay URL, estamos en local sin configurar -> Error
                raise Exception("CRITICAL: No se encontró DATABASE_URL ni POSTGRES_URL. Configura las variables de entorno.")
                
        return self._connection

def get_db_connection():
    """Helper para obtener la conexión"""
    return DatabaseConnection().get_connection()

def inicializar_base_de_datos():
    """
    Inicializa el schema de la base de datos utilizando el string embebido
    para evitar problemas de lectura de archivos en Vercel (Serverless).
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Ejecutar script embebido
            cursor.execute(POSTGRES_SCHEMA)
            conn.commit()
            print("✅ Schema PostgreSQL inicializado correctamente")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error inicializando schema: {e}")
        raise e
