"""
Implementación PostgreSQL: EntregaTPRepository
Compatible con pg8000.
"""

from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.entrega_repository_base import EntregaTPRepositoryBase
from src.domain.entities.entrega_tp import EntregaTP


class EntregaTPRepositoryPostgres(EntregaTPRepositoryBase):
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, entrega: EntregaTP) -> EntregaTP:
        # Usar delete+insert en lugar de ON CONFLICT
        delete_query = "DELETE FROM entrega_tp WHERE trabajo_practico_id = %s AND alumno_id = %s"
        insert_query = """
            INSERT INTO entrega_tp (trabajo_practico_id, alumno_id, fecha_entrega_real, entregado, es_tardia, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, fecha_registro
        """
        params = (
            entrega.trabajo_practico_id,
            entrega.alumno_id,
            entrega.fecha_entrega_real,
            entrega.entregado,
            entrega.es_tardia,
            datetime.now()
        )
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(delete_query, (entrega.trabajo_practico_id, entrega.alumno_id))
            cursor.execute(insert_query, params)
            row = cursor.fetchone()
            self.conexion.commit()
            
            entrega.id = row[0]
            entrega.fecha_registro = row[1]
            return entrega
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def obtener_por_tp(self, tp_id: int) -> List[EntregaTP]:
        query = "SELECT id, trabajo_practico_id, alumno_id, fecha_entrega_real, entregado, es_tardia, fecha_registro FROM entrega_tp WHERE trabajo_practico_id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (tp_id,))
            rows = cursor.fetchall()
            return [self._row_to_entrega(row) for row in rows]
        finally:
            cursor.close()

    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[EntregaTP]:
        query = """
            SELECT e.id, e.trabajo_practico_id, e.alumno_id, e.fecha_entrega_real, e.entregado, e.es_tardia, e.fecha_registro
            FROM entrega_tp e
            JOIN trabajo_practico tp ON e.trabajo_practico_id = tp.id
            WHERE e.alumno_id = %s AND tp.curso_id = %s
        """
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (alumno_id, curso_id))
            rows = cursor.fetchall()
            return [self._row_to_entrega(row) for row in rows]
        finally:
            cursor.close()

    def obtener_por_alumno_y_tp(self, alumno_id: int, tp_id: int) -> Optional[EntregaTP]:
        query = "SELECT id, trabajo_practico_id, alumno_id, fecha_entrega_real, entregado, es_tardia, fecha_registro FROM entrega_tp WHERE alumno_id = %s AND trabajo_practico_id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (alumno_id, tp_id))
            row = cursor.fetchone()
            return self._row_to_entrega(row) if row else None
        finally:
            cursor.close()

    def actualizar(self, entrega: EntregaTP) -> EntregaTP:
        return self.crear(entrega)

    def _row_to_entrega(self, row) -> EntregaTP:
        return EntregaTP(
            id=row[0],
            trabajo_practico_id=row[1],
            alumno_id=row[2],
            fecha_entrega_real=row[3],
            entregado=bool(row[4]),
            es_tardia=bool(row[5]),
            fecha_registro=row[6] if len(row) > 6 else None
        )
