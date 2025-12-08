"""
Implementación PostgreSQL: EntregaTPRepository
Sistema de Seguimiento de Alumnos
"""

import psycopg2
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.entrega_repository_base import EntregaTPRepositoryBase
from src.domain.entities.entrega_tp import EntregaTP


class EntregaTPRepositoryPostgres(EntregaTPRepositoryBase):
    """
    Implementación PostgreSQL del repositorio de EntregaTP.
    """
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, entrega: EntregaTP) -> EntregaTP:
        """Crea o actualiza una entrega de TP (UPSERT)"""
        # Nota: En Postgres podemos usar ON CONFLICT para hacer upsert
        query = """
            INSERT INTO entrega_tp (trabajo_practico_id, alumno_id, fecha_entrega_real, entregado, es_tardia, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (trabajo_practico_id, alumno_id) 
            DO UPDATE SET 
                fecha_entrega_real = EXCLUDED.fecha_entrega_real,
                entregado = EXCLUDED.entregado,
                es_tardia = EXCLUDED.es_tardia,
                fecha_registro = EXCLUDED.fecha_registro
            RETURNING id, fecha_registro;
        """
        params = (
            entrega.trabajo_practico_id,
            entrega.alumno_id,
            entrega.fecha_entrega_real,
            entrega.entregado,
            entrega.es_tardia,
            datetime.now()
        )
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                self.conexion.commit()
                
                entrega.id = row['id']
                entrega.fecha_registro = row['fecha_registro']
                return entrega
        except Exception as e:
            self.conexion.rollback()
            raise e

    def obtener_por_tp(self, tp_id: int) -> List[EntregaTP]:
        """Obtiene entregas de un TP"""
        query = "SELECT * FROM entrega_tp WHERE trabajo_practico_id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (tp_id,))
            rows = cursor.fetchall()
            return [self._row_to_entrega(row) for row in rows]

    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[EntregaTP]:
        """Obtiene entregas de un alumno en un curso"""
        # Join con TP para filtrar por curso
        query = """
            SELECT e.* 
            FROM entrega_tp e
            JOIN trabajo_practico tp ON e.trabajo_practico_id = tp.id
            WHERE e.alumno_id = %s AND tp.curso_id = %s
            ORDER BY tp.fecha_entrega ASC
        """
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (alumno_id, curso_id))
            rows = cursor.fetchall()
            return [self._row_to_entrega(row) for row in rows]

    def obtener_por_alumno_y_tp(self, alumno_id: int, tp_id: int) -> Optional[EntregaTP]:
        """Obtiene una entrega específica"""
        query = "SELECT * FROM entrega_tp WHERE alumno_id = %s AND trabajo_practico_id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (alumno_id, tp_id))
            row = cursor.fetchone()
            return self._row_to_entrega(row) if row else None

    def actualizar(self, entrega: EntregaTP) -> EntregaTP:
        """Actualiza una entrega existente"""
        # Reutilizamos crear por el upsert
        return self.crear(entrega)

    def _row_to_entrega(self, row) -> EntregaTP:
        return EntregaTP(
            id=row['id'],
            trabajo_practico_id=row['trabajo_practico_id'],
            alumno_id=row['alumno_id'],
            fecha_entrega_real=row['fecha_entrega_real'],
            # Convertir integer/boolean de Postgres
            entregado=bool(row['entregado']),
            es_tardia=bool(row['es_tardia']),
            fecha_registro=row['fecha_registro'] if row.get('fecha_registro') else None
        )
