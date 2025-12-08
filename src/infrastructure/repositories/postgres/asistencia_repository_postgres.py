"""
Implementación PostgreSQL: RegistroAsistenciaRepository
Sistema de Seguimiento de Alumnos
"""

import psycopg2
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.asistencia_repository_base import RegistroAsistenciaRepositoryBase
from src.domain.entities.registro_asistencia import RegistroAsistencia


class RegistroAsistenciaRepositoryPostgres(RegistroAsistenciaRepositoryBase):
    """
    Implementación PostgreSQL del repositorio de Asistencia.
    """
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        """Crea un nuevo registro de asistencia"""
        # Usamos UPSERT (INSERT ... ON CONFLICT DO UPDATE)
        query = """
            INSERT INTO registro_asistencia (alumno_id, clase_id, estado, fecha_registro)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (alumno_id, clase_id) 
            DO UPDATE SET estado = EXCLUDED.estado, fecha_registro = EXCLUDED.fecha_registro
            RETURNING id, fecha_registro;
        """
        params = (
            registro.alumno_id,
            registro.clase_id,
            registro.estado,
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

    def obtener_por_clase(self, clase_id: int) -> List[RegistroAsistencia]:
        """Obtiene registros de una clase"""
        query = "SELECT * FROM registro_asistencia WHERE clase_id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (clase_id,))
            rows = cursor.fetchall()
            return [self._row_to_asistencia(row) for row in rows]

    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[RegistroAsistencia]:
        """Obtiene registros de un alumno en un curso"""
        query = """
            SELECT ra.* 
            FROM registro_asistencia ra
            JOIN clase c ON ra.clase_id = c.id
            WHERE ra.alumno_id = %s AND c.curso_id = %s
            ORDER BY c.fecha ASC
        """
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (alumno_id, curso_id))
            rows = cursor.fetchall()
            return [self._row_to_asistencia(row) for row in rows]

    def obtener_por_alumno_y_clase(self, alumno_id: int, clase_id: int) -> Optional[RegistroAsistencia]:
        """Obtiene un registro específico"""
        query = "SELECT * FROM registro_asistencia WHERE alumno_id = %s AND clase_id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (alumno_id, clase_id))
            row = cursor.fetchone()
            return self._row_to_asistencia(row) if row else None

    def actualizar(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        """Actualiza un registro existente"""
        # Reutilizamos crear por la lógica de UPSERT, pero si quisieramos estricto:
        query = """
            UPDATE registro_asistencia 
            SET estado = %s
            WHERE alumno_id = %s AND clase_id = %s
            RETURNING id, fecha_registro
        """
        params = (registro.estado, registro.alumno_id, registro.clase_id)
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                if not row:
                    # Si no existe, lo creamos
                    return self.crear(registro)
                
                self.conexion.commit()
                registro.id = row['id']
                registro.fecha_registro = row['fecha_registro']
                return registro
        except Exception as e:
            self.conexion.rollback()
            raise e

    def _row_to_asistencia(self, row) -> RegistroAsistencia:
        return RegistroAsistencia(
            id=row['id'],
            alumno_id=row['alumno_id'],
            clase_id=row['clase_id'],
            estado=row['estado'],
            fecha_registro=row['fecha_registro'] if row.get('fecha_registro') else None
        )
