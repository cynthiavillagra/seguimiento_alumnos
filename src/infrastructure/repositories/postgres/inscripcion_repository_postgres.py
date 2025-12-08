"""
Implementación PostgreSQL: InscripcionRepository
Sistema de Seguimiento de Alumnos
"""

import psycopg2
from typing import List, Optional
from datetime import datetime, date

from src.infrastructure.repositories.base.inscripcion_repository_base import InscripcionRepositoryBase
from src.domain.entities.inscripcion import Inscripcion
from src.domain.exceptions.domain_exceptions import (
    InscripcionDuplicadaException,
    InscripcionNoEncontradaException
)


class InscripcionRepositoryPostgres(InscripcionRepositoryBase):
    """
    Implementación PostgreSQL del repositorio de Inscripción.
    """
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, inscripcion: Inscripcion) -> Inscripcion:
        """Crea una nueva inscripción"""
        query = """
            INSERT INTO inscripcion (alumno_id, curso_id, fecha_inscripcion)
            VALUES (%s, %s, %s)
            RETURNING id, fecha_inscripcion;
        """
        params = (
            inscripcion.alumno_id,
            inscripcion.curso_id,
            inscripcion.fecha_inscripcion or date.today()
        )
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                self.conexion.commit()
                
                inscripcion.id = row['id']
                inscripcion.fecha_inscripcion = row['fecha_inscripcion']
                return inscripcion
                
        except psycopg2.errors.UniqueViolation:
            self.conexion.rollback()
            raise InscripcionDuplicadaException(
                f"El alumno {inscripcion.alumno_id} ya está inscripto en el curso {inscripcion.curso_id}"
            )
        except Exception as e:
            self.conexion.rollback()
            raise e

    def obtener_por_id(self, id: int) -> Optional[Inscripcion]:
        """Obtiene una inscripción por ID"""
        query = "SELECT * FROM inscripcion WHERE id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_inscripcion(row) if row else None

    def obtener_por_alumno(self, alumno_id: int) -> List[Inscripcion]:
        """Obtiene todas las inscripciones de un alumno"""
        query = "SELECT * FROM inscripcion WHERE alumno_id = %s ORDER BY fecha_inscripcion DESC"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (alumno_id,))
            rows = cursor.fetchall()
            return [self._row_to_inscripcion(row) for row in rows]

    def obtener_por_curso(self, curso_id: int) -> List[Inscripcion]:
        """Obtiene todas las inscripciones de un curso"""
        query = "SELECT * FROM inscripcion WHERE curso_id = %s ORDER BY fecha_inscripcion DESC"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (curso_id,))
            rows = cursor.fetchall()
            return [self._row_to_inscripcion(row) for row in rows]

    def existe(self, alumno_id: int, curso_id: int) -> bool:
        """Verifica si existe una inscripción"""
        query = "SELECT 1 FROM inscripcion WHERE alumno_id = %s AND curso_id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (alumno_id, curso_id))
            return cursor.fetchone() is not None

    def eliminar(self, id: int) -> bool:
        """Elimina una inscripción por ID"""
        query = "DELETE FROM inscripcion WHERE id = %s"
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, (id,))
                deleted = cursor.rowcount > 0
                self.conexion.commit()
                return deleted
        except Exception as e:
            self.conexion.rollback()
            raise e

    def _row_to_inscripcion(self, row) -> Inscripcion:
        """Convierte una fila de BD a una entidad Inscripcion"""
        # Postgres returns date/datetime objects directly
        return Inscripcion(
            id=row['id'],
            alumno_id=row['alumno_id'],
            curso_id=row['curso_id'],
            fecha_inscripcion=row['fecha_inscripcion']
        )
