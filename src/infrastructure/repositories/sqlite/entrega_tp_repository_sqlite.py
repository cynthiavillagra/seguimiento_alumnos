"""
Implementación SQLite: EntregaTPRepository
Sistema de Seguimiento de Alumnos
"""

import sqlite3
from typing import List, Optional
from datetime import datetime, date

from src.infrastructure.repositories.base.entrega_tp_repository_base import EntregaTPRepositoryBase
from src.domain.entities.entrega_tp import EntregaTP

class EntregaTPRepositorySQLite(EntregaTPRepositoryBase):
    
    def __init__(self, conexion: sqlite3.Connection):
        self.conexion = conexion
        self.conexion.row_factory = sqlite3.Row
    
    def crear_o_actualizar(self, entrega: EntregaTP) -> EntregaTP:
        # Decisión de Diseño: Implementar UPSERT
        # Si ya existe entrega para ese alumno y TP, actualizamos. Si no, creamos.
        # SQLite tiene ON CONFLICT DO UPDATE
        
        cursor = self.conexion.cursor()
        
        cursor.execute("""
            INSERT INTO entrega_tp (trabajo_practico_id, alumno_id, fecha_entrega_real, entregado, es_tardia, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(trabajo_practico_id, alumno_id) DO UPDATE SET
            fecha_entrega_real=excluded.fecha_entrega_real,
            entregado=excluded.entregado,
            es_tardia=excluded.es_tardia,
            fecha_registro=excluded.fecha_registro
        """, (
            entrega.trabajo_practico_id,
            entrega.alumno_id,
            entrega.fecha_entrega_real.isoformat() if entrega.fecha_entrega_real else None,
            entrega.entregado,
            entrega.es_tardia,
            datetime.now()
        ))
        self.conexion.commit()
        
        # Recuperar el ID (si fue update lastrowid puede no ser confiable en versiones viejas de sqlite, pero en upsert suele funcionar)
        # Para estar seguros, buscamos por unique key
        entrega_bd = self.obtener_por_alumno_y_tp(entrega.alumno_id, entrega.trabajo_practico_id)
        return entrega_bd

    def obtener_por_id(self, id: int) -> Optional[EntregaTP]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM entrega_tp WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._row_to_entrega(row) if row else None
    
    def obtener_por_tp(self, tp_id: int) -> List[EntregaTP]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM entrega_tp WHERE trabajo_practico_id = ?", (tp_id,))
        rows = cursor.fetchall()
        return [self._row_to_entrega(row) for row in rows]
    
    def obtener_por_alumno_y_tp(self, alumno_id: int, tp_id: int) -> Optional[EntregaTP]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM entrega_tp WHERE alumno_id = ? AND trabajo_practico_id = ?", (alumno_id, tp_id))
        row = cursor.fetchone()
        return self._row_to_entrega(row) if row else None
        
    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[EntregaTP]:
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT et.* 
            FROM entrega_tp et
            JOIN trabajo_practico tp ON et.trabajo_practico_id = tp.id
            WHERE et.alumno_id = ? AND tp.curso_id = ?
            ORDER BY tp.fecha_entrega ASC
        """, (alumno_id, curso_id))
        rows = cursor.fetchall()
        return [self._row_to_entrega(row) for row in rows]
    
    def eliminar(self, id: int) -> bool:
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM entrega_tp WHERE id = ?", (id,))
        self.conexion.commit()
        return cursor.rowcount > 0

    def _row_to_entrega(self, row: sqlite3.Row) -> EntregaTP:
        return EntregaTP(
            id=row['id'],
            trabajo_practico_id=row['trabajo_practico_id'],
            alumno_id=row['alumno_id'],
            fecha_entrega_real=date.fromisoformat(row['fecha_entrega_real']) if row['fecha_entrega_real'] else None,
            entregado=bool(row['entregado']),
            es_tardia=bool(row['es_tardia']),
            fecha_registro=datetime.fromisoformat(row['fecha_registro']) if row['fecha_registro'] else None
        )
