"""
Implementación PostgreSQL: InscripcionRepository
Compatible con pg8000.
"""

from typing import List, Optional
from datetime import datetime, date

from src.infrastructure.repositories.base.inscripcion_repository_base import InscripcionRepositoryBase
from src.domain.entities.inscripcion import Inscripcion
from src.domain.exceptions.domain_exceptions import InscripcionDuplicadaException


class InscripcionRepositoryPostgres(InscripcionRepositoryBase):
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, inscripcion: Inscripcion) -> Inscripcion:
        query = """
            INSERT INTO inscripcion (alumno_id, curso_id, fecha_inscripcion)
            VALUES (%s, %s, %s)
            RETURNING id, fecha_inscripcion
        """
        params = (
            inscripcion.alumno_id,
            inscripcion.curso_id,
            inscripcion.fecha_inscripcion or date.today()
        )
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            self.conexion.commit()
            
            inscripcion.id = row[0]
            inscripcion.fecha_inscripcion = row[1]
            return inscripcion
            
        except Exception as e:
            self.conexion.rollback()
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                raise InscripcionDuplicadaException(f"El alumno ya está inscripto en este curso")
            raise e
        finally:
            cursor.close()

    def obtener_por_id(self, id: int) -> Optional[Inscripcion]:
        query = "SELECT id, alumno_id, curso_id, fecha_inscripcion FROM inscripcion WHERE id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            self.conexion.commit()
            return self._row_to_inscripcion(row) if row else None
        finally:
            cursor.close()

    def obtener_por_alumno(self, alumno_id: int) -> List[Inscripcion]:
        query = "SELECT id, alumno_id, curso_id, fecha_inscripcion FROM inscripcion WHERE alumno_id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (alumno_id,))
            rows = cursor.fetchall()
            self.conexion.commit()
            return [self._row_to_inscripcion(row) for row in rows]
        finally:
            cursor.close()

    def obtener_por_curso(self, curso_id: int) -> List[Inscripcion]:
        query = "SELECT id, alumno_id, curso_id, fecha_inscripcion FROM inscripcion WHERE curso_id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (curso_id,))
            rows = cursor.fetchall()
            self.conexion.commit()
            return [self._row_to_inscripcion(row) for row in rows]
        finally:
            cursor.close()

    def existe(self, alumno_id: int, curso_id: int) -> bool:
        query = "SELECT 1 FROM inscripcion WHERE alumno_id = %s AND curso_id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (alumno_id, curso_id))
            result = cursor.fetchone() is not None
            self.conexion.commit()
            return result
        finally:
            cursor.close()

    def eliminar(self, id: int) -> bool:
        query = "DELETE FROM inscripcion WHERE id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (id,))
            deleted = cursor.rowcount > 0
            self.conexion.commit()
            return deleted
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def _row_to_inscripcion(self, row) -> Inscripcion:
        return Inscripcion(
            id=row[0],
            alumno_id=row[1],
            curso_id=row[2],
            fecha_inscripcion=row[3]
        )
