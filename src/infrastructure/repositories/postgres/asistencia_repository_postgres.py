"""
Implementación PostgreSQL: RegistroAsistenciaRepository
Compatible con pg8000.
"""

from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.asistencia_repository_base import RegistroAsistenciaRepositoryBase
from src.domain.entities.registro_asistencia import RegistroAsistencia


class RegistroAsistenciaRepositoryPostgres(RegistroAsistenciaRepositoryBase):
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        # pg8000 no soporta ON CONFLICT, usamos delete+insert
        delete_query = "DELETE FROM registro_asistencia WHERE alumno_id = %s AND clase_id = %s"
        insert_query = """
            INSERT INTO registro_asistencia (alumno_id, clase_id, estado, fecha_registro)
            VALUES (%s, %s, %s, %s)
            RETURNING id, fecha_registro
        """
        params = (
            registro.alumno_id,
            registro.clase_id,
            registro.estado,
            datetime.now()
        )
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(delete_query, (registro.alumno_id, registro.clase_id))
            cursor.execute(insert_query, params)
            row = cursor.fetchone()
            self.conexion.commit()
            
            registro.id = row[0]
            registro.fecha_registro = row[1]
            return registro
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def obtener_por_clase(self, clase_id: int) -> List[RegistroAsistencia]:
        query = "SELECT id, alumno_id, clase_id, estado, fecha_registro FROM registro_asistencia WHERE clase_id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (clase_id,))
            rows = cursor.fetchall()
            return [self._row_to_asistencia(row) for row in rows]
        finally:
            cursor.close()

    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[RegistroAsistencia]:
        query = """
            SELECT ra.id, ra.alumno_id, ra.clase_id, ra.estado, ra.fecha_registro
            FROM registro_asistencia ra
            JOIN clase c ON ra.clase_id = c.id
            WHERE ra.alumno_id = %s AND c.curso_id = %s
        """
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (alumno_id, curso_id))
            rows = cursor.fetchall()
            return [self._row_to_asistencia(row) for row in rows]
        finally:
            cursor.close()

    def obtener_por_alumno_y_clase(self, alumno_id: int, clase_id: int) -> Optional[RegistroAsistencia]:
        query = "SELECT id, alumno_id, clase_id, estado, fecha_registro FROM registro_asistencia WHERE alumno_id = %s AND clase_id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (alumno_id, clase_id))
            row = cursor.fetchone()
            return self._row_to_asistencia(row) if row else None
        finally:
            cursor.close()

    def actualizar(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        return self.crear(registro)

    def _row_to_asistencia(self, row) -> RegistroAsistencia:
        return RegistroAsistencia(
            id=row[0],
            alumno_id=row[1],
            clase_id=row[2],
            estado=row[3],
            fecha_registro=row[4] if len(row) > 4 else None
        )
