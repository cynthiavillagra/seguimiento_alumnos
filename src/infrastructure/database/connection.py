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
    
    # Verificar si la conexión está cerrada o en mal estado
    if _connection is not None:
        try:
            # Limpiar cualquier transacción pendiente
            try:
                _connection.rollback()
            except:
                pass
            
            # Test simple
            cursor = _connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            _connection.commit()
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
            # pg8000 starts in autocommit=False, which is fine
            print("✅ Conexión a PostgreSQL exitosa (pg8000)")
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL: {e}")
            raise e
    
    return _connection


def inicializar_base_de_datos():
    """
    Inicializa el schema de la base de datos.
    Ejecuta cada statement por separado para manejar errores de 'ya existe'.
    Mejorado para manejar bloques $$ (fusiones/triggers).
    """
    from src.infrastructure.database.postgres_schema import POSTGRES_SCHEMA
    
    conn = get_db_connection()
    
    # Lógica de splitting manual para respetar $$ ... $$
    statements = []
    current_stmt = []
    in_dollar_quote = False
    
    # Procesar carácter por carácter (ineficiente pero seguro para scripts cortos)
    # O más simple: iterar por líneas
    
    raw_statements = POSTGRES_SCHEMA.splitlines()
    buffer = []
    
    for line in raw_statements:
        stripped = line.strip()
        if not stripped or stripped.startswith('--'):
            continue
            
        buffer.append(line)
        
        # Detección simplificada de $$
        if '$$' in line:
            in_dollar_quote = not in_dollar_quote
            
        # Si terminamos con ; y NO estamos dentro de $$, es un statement
        if line.strip().endswith(';') and not in_dollar_quote:
            statements.append('\n'.join(buffer))
            buffer = []
            
    # Agregar último si quedó
    if buffer:
        statements.append('\n'.join(buffer))
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for stmt in statements:
        stmt = stmt.strip()
        if not stmt: continue
            
        cursor = conn.cursor()
        try:
            cursor.execute(stmt)
            conn.commit()
            success_count += 1
        except Exception as e:
            conn.rollback()
            error_str = str(e).lower()
            if 'already exists' in error_str or 'duplicate' in error_str:
                skip_count += 1
            else:
                error_count += 1
                print(f"⚠️ Error en statement: {e}")
                # print(f"SQL Parcial: {stmt[:50]}...") 
        finally:
            cursor.close()
    
    print(f"✅ Schema inicializado: {success_count} OK, {skip_count} ya existían, {error_count} errores")
    return {"success": success_count, "skipped": skip_count, "errors": error_count}

