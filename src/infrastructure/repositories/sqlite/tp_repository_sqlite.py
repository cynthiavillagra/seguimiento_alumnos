"""
Implementación SQLite: TrabajoPracticoRepository
Sistema de Seguimiento de Alumnos
"""

import sqlite3
from typing import List, Optional
from datetime import datetime, date

from src.infrastructure.repositories.base.tp_repository_base import TrabajoPracticoRepositoryBase
from src.domain.entities.trabajo_practico import TrabajoPractico

class TrabajoPracticoRepositorySQLite(TrabajoPracticoRepositoryBase):
    
    def __init__(self, conexion: sqlite3.Connection):
        self.conexion = conexion
        self.conexion.row_factory = sqlite3.Row
    
    def crear(self, tp: TrabajoPractico) -> TrabajoPractico:
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT INTO trabajo_practico (curso_id, titulo, descripcion, fecha_entrega, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tp.curso_id,
            tp.titulo,
            tp.descripcion,
            tp.fecha_entrega.isoformat(),
            datetime.now()
        ))
        self.conexion.commit()
        
        tp.id = cursor.lastrowid
        tp.fecha_creacion = datetime.now()
        return tp

    def obtener_por_id(self, id: int) -> Optional[TrabajoPractico]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM trabajo_practico WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._row_to_tp(row) if row else None
    
    def obtener_por_curso(self, curso_id: int) -> List[TrabajoPractico]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM trabajo_practico WHERE curso_id = ? ORDER BY fecha_entrega ASC", (curso_id,))
        rows = cursor.fetchall()
        return [self._row_to_tp(row) for row in rows]
    
    def actualizar(self, tp: TrabajoPractico) -> TrabajoPractico:
        if tp.id is None:
             raise ValueError("ID requerido para actualizar")
             
        cursor = self.conexion.cursor()
        cursor.execute("""
            UPDATE trabajo_practico
            SET titulo = ?, descripcion = ?, fecha_entrega = ?
            WHERE id = ?
        """, (
            tp.titulo,
            tp.descripcion,
            tp.fecha_entrega.isoformat(),
            tp.id
        ))
        self.conexion.commit()
        return tp
    
    def eliminar(self, id: int) -> bool:
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM trabajo_practico WHERE id = ?", (id,))
        self.conexion.commit()
        return cursor.rowcount > 0

    def _row_to_tp(self, row: sqlite3.Row) -> TrabajoPractico:
        return TrabajoPractico(
            id=row['id'],
            curso_id=row['curso_id'],
            titulo=row['titulo'],
            descripcion=row['descripcion'],
            fecha_entrega=date.fromisoformat(row['fecha_entrega']),
            fecha_creacion=datetime.fromisoformat(row['fecha_creacion']) if row['fecha_creacion'] else None
        )
