"""
Implementación SQLite: RegistroParticipacionRepository
Sistema de Seguimiento de Alumnos
"""

import sqlite3
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.participacion_repository_base import RegistroParticipacionRepositoryBase
from src.domain.entities.registro_participacion import RegistroParticipacion
from src.domain.value_objects.enums import NivelParticipacion

class RegistroParticipacionRepositorySQLite(RegistroParticipacionRepositoryBase):
    
    def __init__(self, conexion: sqlite3.Connection):
        self.conexion = conexion
        self.conexion.row_factory = sqlite3.Row
    
    def crear(self, registro: RegistroParticipacion) -> RegistroParticipacion:
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT INTO registro_participacion (alumno_id, clase_id, nivel, comentario, fecha_registro)
            VALUES (?, ?, ?, ?, ?)
        """, (
            registro.alumno_id,
            registro.clase_id,
            registro.nivel.value,
            registro.comentario,
            datetime.now()
        ))
        self.conexion.commit()
        
        registro.id = cursor.lastrowid
        registro.fecha_registro = datetime.now()
        return registro

    def obtener_por_id(self, id: int) -> Optional[RegistroParticipacion]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM registro_participacion WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._row_to_registro(row) if row else None
    
    def obtener_por_clase(self, clase_id: int) -> List[RegistroParticipacion]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM registro_participacion WHERE clase_id = ?", (clase_id,))
        rows = cursor.fetchall()
        return [self._row_to_registro(row) for row in rows]
    
    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[RegistroParticipacion]:
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT rp.* 
            FROM registro_participacion rp
            JOIN clase c ON rp.clase_id = c.id
            WHERE rp.alumno_id = ? AND c.curso_id = ?
            ORDER BY c.fecha ASC
        """, (alumno_id, curso_id))
        rows = cursor.fetchall()
        return [self._row_to_registro(row) for row in rows]
    
    def actualizar(self, registro: RegistroParticipacion) -> RegistroParticipacion:
        if registro.id is None:
             raise ValueError("ID requerido para actualizar")
             
        cursor = self.conexion.cursor()
        cursor.execute("""
            UPDATE registro_participacion
            SET nivel = ?, comentario = ?
            WHERE id = ?
        """, (
            registro.nivel.value,
            registro.comentario,
            registro.id
        ))
        self.conexion.commit()
        return registro
    
    def eliminar(self, id: int) -> bool:
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM registro_participacion WHERE id = ?", (id,))
        self.conexion.commit()
        return cursor.rowcount > 0

    def _row_to_registro(self, row: sqlite3.Row) -> RegistroParticipacion:
        return RegistroParticipacion(
            id=row['id'],
            alumno_id=row['alumno_id'],
            clase_id=row['clase_id'],
            nivel=NivelParticipacion(row['nivel']),
            comentario=row['comentario'],
            fecha_registro=datetime.fromisoformat(row['fecha_registro']) if row['fecha_registro'] else None
        )
