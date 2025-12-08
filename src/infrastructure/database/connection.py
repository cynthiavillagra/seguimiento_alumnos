"""
Gestión de Conexión a Base de Datos PostgreSQL
Sistema de Seguimiento de Alumnos

Decisión de diseño: Cambio a PostgreSQL
- Se utiliza psycopg2 como driver
- Se soporta conexión vía URL (POSTGRES_URL)
- Se utiliza RealDictCursor para compatibilidad con el código que espera diccionarios
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from pathlib import Path

class DatabaseConnection:
    """
    Gestiona la conexión a la base de datos PostgreSQL.
    Patrón Singleton para mantener una referencia a la conexión.
    """
    
    _instance: Optional['DatabaseConnection'] = None
    _conexion = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._conexion is None:
            self._conectar()
    
    def _conectar(self):
        """Establece conexión con PostgreSQL"""
        # 1. Obtener URL de conexión
        # Vercel provee: POSTGRES_URL, POSTGRES_PRISMA_URL, etc.
        # Preferimos POSTGRES_URL o DATABASE_URL
        db_url = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
        
        if not db_url:
            # Fallback local para desarrollo si no hay variables
            # Asumimos una instalación local default o error
            print("⚠️ No se encontró POSTGRES_URL ni DATABASE_URL.")
            print("   Asegúrate de tener un .env con la conexión a Postgres.")
            # Intentar conexión local default (opcional)
            # db_url = "postgresql://postgres:postgres@localhost:5432/seguimiento_alumnos"
            raise ValueError("Variable de entorno POSTGRES_URL o DATABASE_URL requerida")

        try:
            # 2. Conectar
            self._conexion = psycopg2.connect(
                db_url,
                cursor_factory=RealDictCursor
            )
            # Autocommit para simplificar manejo de transacciones en operaciones simples
            self._conexion.autocommit = False 
            print("✅ Conectado a PostgreSQL")
            
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL: {e}")
            raise e

    def get_conexion(self):
        """Retorna la conexión activa. Reconecta si está cerrada."""
        if self._conexion is None or self._conexion.closed:
            self._conectar()
        return self._conexion
    
    def inicializar_schema(self, schema_path: Optional[str] = None):
        """Ejecuta el script de esquema para inicializar tablas"""
        if schema_path is None:
            schema_path = Path(__file__).parent / "schema_postgres.sql"
        
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema no encontrado: {schema_path}")
            
        with open(schema_path, "r", encoding="utf-8") as f:
            sql = f.read()
            
        conn = self.get_conexion()
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
            print("✅ Schema PostgreSQL inicializado")
        except Exception as e:
            conn.rollback()
            print(f"❌ Error inicializando schema: {e}")
            raise

    def cerrar(self):
        if self._conexion and not self._conexion.closed:
            self._conexion.close()
            print("✅ Conexión PostgreSQL cerrada")

def get_db_connection():
    db = DatabaseConnection()
    return db.get_conexion()

def inicializar_base_de_datos():
    db = DatabaseConnection()
    # Solo inicializar si es solicitado explícitamente o en entorno controlado
    # En producción (Vercel), cuidado con reiniciar el schema
    # Pero para el primer deploy es útil.
    try:
        db.inicializar_schema()
    except Exception as e:
        print(f"⚠️ Error al intentar inicializar DB (puede que ya exista): {e}")

