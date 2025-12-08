"""
Implementación PostgreSQL: RegistroParticipacionRepository
Compatible con pg8000.
"""

from typing import List
from datetime import datetime

from src.infrastructure.repositories.base.participacion_repository_base import RegistroParticipacionRepositoryBase
from src.domain.entities.registro_participacion import RegistroParticipacion


class RegistroParticipacionRepositoryPostgres(RegistroParticipacionRepositoryBase):
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, registro: RegistroParticipacion) -> RegistroParticipacion:
        query = """
            INSERT INTO registro_participacion (alumno_id, clase_id, nivel, comentario, fecha_registro)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, fecha_registro
        """
        params = (
            registro.alumno_id,
            registro.clase_id,
            registro.nivel,
            registro.comentario,
            datetime.now()
        )
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, params)
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

    def obtener_por_clase(self, clase_id: int) -> List[RegistroParticipacion]:
        query = "SELECT id, alumno_id, clase_id, nivel, comentario, fecha_registro FROM registro_participacion WHERE clase_id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (clase_id,))
            rows = cursor.fetchall()
            return [self._row_to_participacion(row) for row in rows]
        finally:
            cursor.close()

    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[RegistroParticipacion]:
        query = """
            SELECT rp.id, rp.alumno_id, rp.clase_id, rp.nivel, rp.comentario, rp.fecha_registro
            FROM registro_participacion rp
            JOIN clase c ON rp.clase_id = c.id
            WHERE rp.alumno_id = %s AND c.curso_id = %s
        """
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (alumno_id, curso_id))
            rows = cursor.fetchall()
            return [self._row_to_participacion(row) for row in rows]
        finally:
            cursor.close()

    def _row_to_participacion(self, row) -> RegistroParticipacion:
        return RegistroParticipacion(
            id=row[0],
            alumno_id=row[1],
            clase_id=row[2],
            nivel=row[3],
            comentario=row[4],
            fecha_registro=row[5] if len(row) > 5 else None
        )
