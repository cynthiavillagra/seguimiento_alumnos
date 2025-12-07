"""
Script para Cargar Datos de Ejemplo
Sistema de Seguimiento de Alumnos

Este script carga datos de ejemplo en la base de datos para testing y demostración.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.database.connection import get_db_connection
from src.infrastructure.repositories.sqlite.alumno_repository_sqlite import AlumnoRepositorySQLite
from src.application.services.alumno_service import AlumnoService


def cargar_alumnos_ejemplo():
    """Carga alumnos de ejemplo"""
    print("\n📝 Cargando alumnos de ejemplo...")
    
    conexion = get_db_connection()
    alumno_repo = AlumnoRepositorySQLite(conexion)
    alumno_service = AlumnoService(alumno_repo)
    
    alumnos_ejemplo = [
        {
            "nombre": "Juan",
            "apellido": "Pérez",
            "dni": "12345678",
            "email": "juan.perez@example.com",
            "cohorte": 2024
        },
        {
            "nombre": "Ana",
            "apellido": "García",
            "dni": "23456789",
            "email": "ana.garcia@example.com",
            "cohorte": 2024
        },
        {
            "nombre": "Pedro",
            "apellido": "Gómez",
            "dni": "34567890",
            "email": "pedro.gomez@example.com",
            "cohorte": 2023
        },
        {
            "nombre": "María",
            "apellido": "López",
            "dni": "45678901",
            "email": "maria.lopez@example.com",
            "cohorte": 2024
        },
        {
            "nombre": "Carlos",
            "apellido": "Rodríguez",
            "dni": "56789012",
            "email": "carlos.rodriguez@example.com",
            "cohorte": 2024
        }
    ]
    
    creados = 0
    for alumno_data in alumnos_ejemplo:
        try:
            alumno = alumno_service.crear_alumno(**alumno_data)
            print(f"   ✅ Creado: {alumno.nombre_completo()} (ID: {alumno.id})")
            creados += 1
        except Exception as e:
            print(f"   ⚠️  Error al crear {alumno_data['nombre']} {alumno_data['apellido']}: {e}")
    
    print(f"\n✅ {creados} alumnos creados")
    return creados


def main():
    """Función principal"""
    print("=" * 70)
    print("🌱 Cargando Datos de Ejemplo")
    print("=" * 70)
    
    try:
        total_creados = 0
        
        # Cargar alumnos
        total_creados += cargar_alumnos_ejemplo()
        
        # Aquí se pueden agregar más funciones para cargar cursos, clases, etc.
        # total_creados += cargar_cursos_ejemplo()
        # total_creados += cargar_clases_ejemplo()
        
        print("\n" + "=" * 70)
        print(f"✅ Datos de ejemplo cargados correctamente")
        print(f"   Total de registros creados: {total_creados}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error al cargar datos de ejemplo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
