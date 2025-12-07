"""
Módulo de Conexión a PostgreSQL
Maneja la conexión a Vercel Postgres
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """
    Obtiene una conexión a PostgreSQL
    
    Returns:
        psycopg2.connection: Conexión a la base de datos
    """
    postgres_url = os.getenv('POSTGRES_URL')
    
    if not postgres_url:
        raise Exception("POSTGRES_URL no encontrada en variables de entorno")
    
    return psycopg2.connect(postgres_url)

def execute_query(query, params=None, fetch_one=False):
    """
    Ejecuta una query y devuelve los resultados
    
    Args:
        query (str): Query SQL a ejecutar
        params (tuple): Parámetros para la query
        fetch_one (bool): Si True, devuelve solo un resultado
        
    Returns:
        list|dict: Resultados de la query
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
            return dict(result) if result else None
        else:
            results = cursor.fetchall()
            return [dict(row) for row in results]
    finally:
        cursor.close()
        conn.close()

def execute_insert(query, params=None):
    """
    Ejecuta un INSERT y devuelve el ID insertado
    
    Args:
        query (str): Query INSERT
        params (tuple): Parámetros
        
    Returns:
        int: ID del registro insertado
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, params or ())
        conn.commit()
        
        # Obtener el ID insertado
        cursor.execute("SELECT LASTVAL()")
        inserted_id = cursor.fetchone()[0]
        
        return inserted_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def execute_update(query, params=None):
    """
    Ejecuta un UPDATE o DELETE
    
    Args:
        query (str): Query UPDATE/DELETE
        params (tuple): Parámetros
        
    Returns:
        int: Número de filas afectadas
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, params or ())
        conn.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
