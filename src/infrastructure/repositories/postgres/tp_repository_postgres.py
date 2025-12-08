"""
Implementación PostgreSQL: TrabajoPracticoRepository
Compatible con pg8000.
"""

from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.tp_repository_base import TrabajoPracticoRepositoryBase
from src.domain.entities.trabajo_practico import TrabajoPractico
from src.domain.exceptions.domain_exceptions import TPNoEncontradoException


class TrabajoPracticoRepositoryPostgres(TrabajoPracticoRepositoryBase):
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, tp: TrabajoPractico) -> TrabajoPractico:
        query = """
            INSERT INTO trabajo_practico (curso_id, titulo, descripcion, fecha_entrega, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, fecha_creacion
        """
        params = (
            tp.curso_id,
            tp.titulo,
            tp.descripcion,
            tp.fecha_entrega,
            datetime.now()
        )
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            self.conexion.commit()
            
            tp.id = row[0]
            tp.fecha_creacion = row[1]
            return tp
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def obtener_por_id(self, id: int) -> Optional[TrabajoPractico]:
        query = "SELECT id, curso_id, titulo, descripcion, fecha_entrega, fecha_creacion FROM trabajo_practico WHERE id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_tp(row) if row else None
        finally:
            cursor.close()

    def obtener_por_curso(self, curso_id: int) -> List[TrabajoPractico]:
        query = "SELECT id, curso_id, titulo, descripcion, fecha_entrega, fecha_creacion FROM trabajo_practico WHERE curso_id = %s ORDER BY fecha_entrega"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (curso_id,))
            rows = cursor.fetchall()
            return [self._row_to_tp(row) for row in rows]
        finally:
            cursor.close()

    def actualizar(self, tp: TrabajoPractico) -> TrabajoPractico:
        if tp.id is None:
            raise ValueError("El TP debe tener un ID")
        
        query = """
            UPDATE trabajo_practico 
            SET titulo = %s, descripcion = %s, fecha_entrega = %s
            WHERE id = %s
        """
        params = (tp.titulo, tp.descripcion, tp.fecha_entrega, tp.id)
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, params)
            self.conexion.commit()
            return tp
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def eliminar(self, id: int) -> bool:
        query = "DELETE FROM trabajo_practico WHERE id = %s"
        
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

    def _row_to_tp(self, row) -> TrabajoPractico:
        return TrabajoPractico(
            id=row[0],
            curso_id=row[1],
            titulo=row[2],
            descripcion=row[3],
            fecha_entrega=row[4],
            fecha_creacion=row[5] if len(row) > 5 else None
        )
