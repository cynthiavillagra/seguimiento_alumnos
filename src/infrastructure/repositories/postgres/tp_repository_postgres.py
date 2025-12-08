"""
Implementación PostgreSQL: TrabajoPracticoRepository
Sistema de Seguimiento de Alumnos
"""

import psycopg2
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.tp_repository_base import TrabajoPracticoRepositoryBase
from src.domain.entities.trabajo_practico import TrabajoPractico
from src.domain.exceptions.domain_exceptions import TPNoEncontradoException


class TrabajoPracticoRepositoryPostgres(TrabajoPracticoRepositoryBase):
    """
    Implementación PostgreSQL del repositorio de TP.
    """
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, tp: TrabajoPractico) -> TrabajoPractico:
        """Crea un nuevo TP"""
        query = """
            INSERT INTO trabajo_practico (curso_id, titulo, descripcion, fecha_entrega, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, fecha_creacion;
        """
        params = (
            tp.curso_id,
            tp.titulo,
            tp.descripcion,
            tp.fecha_entrega,
            datetime.now()
        )
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                self.conexion.commit()
                
                tp.id = row['id']
                tp.fecha_creacion = row['fecha_creacion']
                return tp
        except Exception as e:
            self.conexion.rollback()
            raise e

    def obtener_por_id(self, id: int) -> Optional[TrabajoPractico]:
        """Obtiene un TP por ID"""
        query = "SELECT * FROM trabajo_practico WHERE id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_tp(row) if row else None

    def obtener_por_curso(self, curso_id: int) -> List[TrabajoPractico]:
        """Obtiene TPs de un curso"""
        query = "SELECT * FROM trabajo_practico WHERE curso_id = %s ORDER BY fecha_entrega ASC"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (curso_id,))
            rows = cursor.fetchall()
            return [self._row_to_tp(row) for row in rows]

    def actualizar(self, tp: TrabajoPractico) -> TrabajoPractico:
        """Actualiza un TP existente"""
        if tp.id is None:
            raise ValueError("El TP debe tener un ID para actualizarlo")
            
        check_query = "SELECT id FROM trabajo_practico WHERE id = %s"
        update_query = """
            UPDATE trabajo_practico 
            SET titulo = %s, descripcion = %s, fecha_entrega = %s
            WHERE id = %s
        """
        params = (tp.titulo, tp.descripcion, tp.fecha_entrega, tp.id)
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(check_query, (tp.id,))
                if not cursor.fetchone():
                    raise TPNoEncontradoException(f"No existe TP con ID {tp.id}")
                
                cursor.execute(update_query, params)
                self.conexion.commit()
                return tp
        except Exception as e:
            self.conexion.rollback()
            raise e

    def eliminar(self, id: int) -> bool:
        """Elimina un TP por ID"""
        query = "DELETE FROM trabajo_practico WHERE id = %s"
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, (id,))
                deleted = cursor.rowcount > 0
                self.conexion.commit()
                return deleted
        except Exception as e:
            self.conexion.rollback()
            raise e

    def _row_to_tp(self, row) -> TrabajoPractico:
        return TrabajoPractico(
            id=row['id'],
            curso_id=row['curso_id'],
            titulo=row['titulo'],
            descripcion=row['descripcion'],
            fecha_entrega=row['fecha_entrega'],
            fecha_creacion=row['fecha_creacion'] if row.get('fecha_creacion') else None
        )
