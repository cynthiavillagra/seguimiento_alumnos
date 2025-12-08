"""
Implementación PostgreSQL: RegistroParticipacionRepository
Sistema de Seguimiento de Alumnos
"""

import psycopg2
from typing import List
from datetime import datetime

from src.infrastructure.repositories.base.participacion_repository_base import RegistroParticipacionRepositoryBase
from src.domain.entities.registro_participacion import RegistroParticipacion


class RegistroParticipacionRepositoryPostgres(RegistroParticipacionRepositoryBase):
    """
    Implementación PostgreSQL del repositorio de Participación.
    """
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, registro: RegistroParticipacion) -> RegistroParticipacion:
        """Crea un nuevo registro de participación"""
        query = """
            INSERT INTO registro_participacion (alumno_id, clase_id, nivel, comentario, fecha_registro)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, fecha_registro;
        """
        params = (
            registro.alumno_id,
            registro.clase_id,
            registro.nivel,
            registro.comentario,
            datetime.now()
        )
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                self.conexion.commit()
                
                registro.id = row['id']
                registro.fecha_registro = row['fecha_registro']
                return registro
        except Exception as e:
            self.conexion.rollback()
            raise e

    def obtener_por_clase(self, clase_id: int) -> List[RegistroParticipacion]:
        """Obtiene participaciones de una clase"""
        query = "SELECT * FROM registro_participacion WHERE clase_id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (clase_id,))
            rows = cursor.fetchall()
            return [self._row_to_participacion(row) for row in rows]

    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[RegistroParticipacion]:
        """Obtiene participaciones de un alumno en un curso"""
        query = """
            SELECT rp.* 
            FROM registro_participacion rp
            JOIN clase c ON rp.clase_id = c.id
            WHERE rp.alumno_id = %s AND c.curso_id = %s
            ORDER BY c.fecha ASC
        """
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (alumno_id, curso_id))
            rows = cursor.fetchall()
            return [self._row_to_participacion(row) for row in rows]

    def _row_to_participacion(self, row) -> RegistroParticipacion:
        return RegistroParticipacion(
            id=row['id'],
            alumno_id=row['alumno_id'],
            clase_id=row['clase_id'],
            nivel=row['nivel'],
            comentario=row['comentario'],
            fecha_registro=row['fecha_registro'] if row.get('fecha_registro') else None
        )
