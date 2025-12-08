"""
Script de inicialización de datos de prueba
"""
import sys
import os

# Agregar root al path
sys.path.append(os.getcwd())

from src.infrastructure.database.connection import get_db_connection, inicializar_base_de_datos
from src.infrastructure.repositories.sqlite.curso_repository_sqlite import CursoRepositorySQLite
from src.infrastructure.repositories.sqlite.alumno_repository_sqlite import AlumnoRepositorySQLite
from src.infrastructure.repositories.sqlite.inscripcion_repository_sqlite import InscripcionRepositorySQLite
from src.domain.entities.curso import Curso
from src.domain.entities.alumno import Alumno
from src.domain.entities.inscripcion import Inscripcion
from datetime import date

def seed():
    print("🌱 Iniciando seed de la base de datos...")
    
    # Asegurar schema
    inicializar_base_de_datos()
    
    conn = get_db_connection()
    
    # Repos
    curso_repo = CursoRepositorySQLite(conn)
    alumno_repo = AlumnoRepositorySQLite(conn)
    inscripcion_repo = InscripcionRepositorySQLite(conn)
    
    # 1. Crear Cursos
    cursos_data = [
        ("Programación I", 2024, 1, "Prof. Valerio"),
        ("Matemática", 2024, 1, "Prof. Garcia"),
        ("Bases de Datos", 2024, 2, "Prof. Perez"),
        ("Programación II", 2023, 2, "Prof. Valerio")
    ]
    
    cursos_creados = []
    for nombre, anio, cuatri, docente in cursos_data:
        try:
            # Verificar si existe para no duplicar (simple check por nombre y anio)
            # Como no tenemos buscar por nombre, creamos y si falla unique, ignoramos
            curso = Curso(
                nombre_materia=nombre,
                anio=anio,
                cuatrimestre=cuatri,
                docente_responsable=docente
            )
            created = curso_repo.crear(curso)
            cursos_creados.append(created)
            print(f"✅ Curso creado: {nombre} ({anio})")
        except Exception as e:
            print(f"⚠️ Curso ya existe o error: {nombre} - {e}")
            # Intentar recuperarlo si existe (no implementado busqueda por nombre)
            pass

    # Recuperar todos los cursos para inscribir
    todos_cursos = curso_repo.obtener_todos()
    
    # 2. Crear Alumnos
    alumnos_data = [
        ("Juan", "Perez", "30123456", "juan.perez@email.com", 2024),
        ("Maria", "Gonzalez", "31123456", "maria.gonzalez@email.com", 2024),
        ("Carlos", "Lopez", "32123456", "carlos.lopez@email.com", 2023),
        ("Ana", "Martinez", "33123456", "ana.martinez@email.com", 2024)
    ]
    
    alumnos_creados = []
    for nombre, apellido, dni, email, cohorte in alumnos_data:
        try:
            alumno = Alumno(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                email=email,
                cohorte=cohorte
            )
            # Verificar existencia por DNI
            existente = alumno_repo.obtener_por_dni(dni)
            if not existente:
                 created = alumno_repo.crear(alumno)
                 alumnos_creados.append(created)
                 print(f"✅ Alumno creado: {nombre} {apellido}")
            else:
                 alumnos_creados.append(existente)
                 print(f"ℹ️ Alumno ya existe: {nombre} {apellido}")
        except Exception as e:
            print(f"❌ Error creando alumno {nombre}: {e}")

    # 3. Inscribir Alumnos a Cursos de su Cohorte
    print("📝 Procesando inscripciones...")
    count = 0
    for alumno in alumnos_creados:
        for curso in todos_cursos:
            if alumno.cohorte == curso.anio:
                # Inscribir
                try:
                    if not inscripcion_repo.existe(alumno.id, curso.id):
                        inscripcion = Inscripcion(
                            alumno_id=alumno.id,
                            curso_id=curso.id,
                            fecha_inscripcion=date.today()
                        )
                        inscripcion_repo.crear(inscripcion)
                        count += 1
                        print(f"   -> Inscripto {alumno.nombre_completo()} en {curso.nombre_materia}")
                except Exception as e:
                    print(f"   ❌ Error inscribiendo: {e}")
    
    print(f"✨ Seed completado. {count} inscripciones creadas.")

if __name__ == "__main__":
    seed()
