"""
Script de Inicialización de Base de Datos
Sistema de Seguimiento de Alumnos

Este script inicializa la base de datos SQLite con el schema definido.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path para poder importar src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.database.connection import DatabaseConnection


def main():
    """
    Inicializa la base de datos.
    
    Pasos:
    1. Crea la conexión a SQLite
    2. Ejecuta el schema.sql
    3. Verifica que las tablas se crearon correctamente
    """
    print("=" * 70)
    print("🔧 Inicializando Base de Datos")
    print("=" * 70)
    
    try:
        # Crear conexión e inicializar schema
        db = DatabaseConnection()
        db.inicializar_schema()
        
        # Verificar que las tablas se crearon
        conexion = db.get_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """)
        
        tablas = cursor.fetchall()
        
        print("\n✅ Tablas creadas:")
        for tabla in tablas:
            print(f"   - {tabla[0]}")
        
        print(f"\n✅ Total de tablas: {len(tablas)}")
        print("\n" + "=" * 70)
        print("✅ Base de datos inicializada correctamente")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error al inicializar base de datos: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
