"""
Gestión de Conexión a Base de Datos PostgreSQL
Sistema de Seguimiento de Alumnos

Usa pg8000 (driver puro Python) para compatibilidad con Vercel.
"""

import os
from urllib.parse import urlparse

# Singleton de conexión
_connection = None

def get_db_connection():
    """
    Obtiene una conexión a la base de datos PostgreSQL.
    Usa pg8000 como driver (pure Python, compatible con Vercel).
    """
    global _connection
    
    # Verificar si la conexión está cerrada
    if _connection is not None:
        try:
            # Test simple
            cursor = _connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
        except Exception:
            _connection = None
    
    if _connection is None:
        import pg8000
        
        # Obtener URL de conexión
        db_url = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
        
        if not db_url:
            raise Exception("CRITICAL: No se encontró DATABASE_URL ni POSTGRES_URL")
        
        # Parsear la URL
        # Formato: postgres://user:pass@host:port/database?sslmode=require
        parsed = urlparse(db_url)
        
        # pg8000 usa parámetros separados, no URL
        connect_params = {
            'user': parsed.username,
            'password': parsed.password,
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path.lstrip('/'),
            'ssl_context': True  # Habilitar SSL
        }
        
        print(f"Conectando a PostgreSQL: {parsed.hostname}:{parsed.port or 5432}/{parsed.path.lstrip('/')}")
        
        try:
            _connection = pg8000.connect(**connect_params)
            print("✅ Conexión a PostgreSQL exitosa (pg8000)")
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL: {e}")
            raise e
    
    return _connection


def inicializar_base_de_datos():
    """
    Inicializa el schema de la base de datos.
    """
    from src.infrastructure.database.postgres_schema import POSTGRES_SCHEMA
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # pg8000 no soporta ejecutar múltiples statements de una vez
        # Dividir el schema en statements individuales
        statements = POSTGRES_SCHEMA.split(';')
        
        for stmt in statements:
            stmt = stmt.strip()
            if stmt and not stmt.startswith('--'):
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    # Ignorar errores de "ya existe" para ser idempotente
                    if 'already exists' not in str(e).lower():
                        print(f"⚠️ Error en statement: {e}")
        
        conn.commit()
        print("✅ Schema PostgreSQL inicializado correctamente")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error inicializando schema: {e}")
        raise e
    finally:
        cursor.close()
