"""
Gestión de Conexión a Base de Datos SQLite
Sistema de Seguimiento de Alumnos

Decisión de diseño: Singleton para la conexión
- En el MVP, usamos una única conexión SQLite
- En producción con PostgreSQL, usaríamos un pool de conexiones
- Esta clase centraliza la creación y configuración de la conexión
"""

import sqlite3
import os
from pathlib import Path
from typing import Optional


class DatabaseConnection:
    """
    Gestiona la conexión a la base de datos SQLite.
    
    Responsabilidades:
    - Crear la conexión a SQLite
    - Inicializar el schema si no existe
    - Configurar opciones de conexión (foreign keys, etc.)
    - Proveer métodos para obtener la conexión
    
    Decisión de diseño: Patrón Singleton
    - Solo una instancia de conexión en toda la aplicación
    - Evita múltiples conexiones innecesarias
    - Facilita el manejo de transacciones
    """
    
    _instance: Optional['DatabaseConnection'] = None
    _conexion: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        """
        Implementación del patrón Singleton.
        
        Garantiza que solo exista una instancia de DatabaseConnection.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa la conexión (solo la primera vez)"""
        if self._conexion is None:
            self._conectar()
    
    def _conectar(self, db_path: Optional[str] = None):
        """
        Crea la conexión a SQLite.
        
        Args:
            db_path: Ruta al archivo de BD. Si es None, usa la ruta por defecto.
        """
        if db_path is None:
            # Decisión de diseño: Leer desde variable de entorno primero
            # Esto permite configurar la ruta en Vercel (/tmp/database.db)
            db_path = os.environ.get("DATABASE_PATH")
            
            if db_path is None:
                # Si no hay variable de entorno, usar ruta por defecto
                project_root = Path(__file__).parent.parent.parent.parent
                db_path = project_root / "database.db"
        
        # Crear directorio si no existe
        db_dir = os.path.dirname(db_path)
        if db_dir:  # Solo si hay directorio (no es solo nombre de archivo)
            os.makedirs(db_dir, exist_ok=True)
        
        # Conectar a SQLite
        self._conexion = sqlite3.connect(
            db_path,
            check_same_thread=False  # Permite usar la conexión desde múltiples threads (necesario para FastAPI)
        )
        
        # Configurar opciones de conexión
        self._configurar_conexion()
        
        print(f"✅ Conectado a base de datos: {db_path}")
    
    def _configurar_conexion(self):
        """
        Configura opciones de la conexión SQLite.
        
        Decisión de diseño: Habilitar foreign keys
        - SQLite NO habilita foreign keys por defecto
        - Debemos habilitarlas explícitamente
        - Esto garantiza integridad referencial
        """
        if self._conexion:
            # Habilitar foreign keys
            self._conexion.execute("PRAGMA foreign_keys = ON")
            
            # Configurar row_factory para acceder a columnas por nombre
            self._conexion.row_factory = sqlite3.Row
    
    def get_conexion(self) -> sqlite3.Connection:
        """
        Obtiene la conexión activa.
        
        Returns:
            sqlite3.Connection: Conexión a la base de datos
        """
        if self._conexion is None:
            self._conectar()
        return self._conexion
    
    def inicializar_schema(self, schema_path: Optional[str] = None):
        """
        Inicializa el schema de la base de datos ejecutando el archivo SQL.
        
        Args:
            schema_path: Ruta al archivo schema.sql. Si es None, usa la ruta por defecto.
        """
        if schema_path is None:
            schema_path = Path(__file__).parent / "schema.sql"
        
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"No se encontró el archivo de schema: {schema_path}")
        
        # Leer el archivo SQL
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Ejecutar el schema
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        
        try:
            cursor.executescript(schema_sql)
            conexion.commit()
            print("✅ Schema de base de datos inicializado correctamente")
        except sqlite3.Error as e:
            print(f"❌ Error al inicializar schema: {e}")
            raise
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if self._conexion:
            self._conexion.close()
            self._conexion = None
            print("✅ Conexión a base de datos cerrada")
    
    def crear_conexion_test(self) -> sqlite3.Connection:
        """
        Crea una conexión en memoria para tests.
        
        Decisión de diseño: BD en memoria para tests
        - Los tests no deben afectar la BD real
        - BD en memoria es mucho más rápida
        - Se destruye automáticamente al cerrar la conexión
        
        Returns:
            sqlite3.Connection: Conexión a BD en memoria
        """
        conexion = sqlite3.connect(":memory:", check_same_thread=False)
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.row_factory = sqlite3.Row
        
        # Inicializar schema en la BD de test
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        conexion.executescript(schema_sql)
        conexion.commit()
        
        return conexion


# ============================================================================
# Funciones de conveniencia
# ============================================================================

def get_db_connection() -> sqlite3.Connection:
    """
    Función de conveniencia para obtener la conexión a la BD.
    
    Útil para inyección de dependencias en FastAPI.
    
    Returns:
        sqlite3.Connection: Conexión activa
    """
    db = DatabaseConnection()
    return db.get_conexion()


def inicializar_base_de_datos():
    """
    Inicializa la base de datos (crea tablas si no existen).
    
    Esta función debe llamarse al iniciar la aplicación.
    """
    db = DatabaseConnection()
    db.inicializar_schema()
