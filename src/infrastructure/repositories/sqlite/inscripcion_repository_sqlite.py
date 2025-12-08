"""
Implementación SQLite: InscripcionRepository
Sistema de Seguimiento de Alumnos
"""

import sqlite3
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.inscripcion_repository_base import InscripcionRepositoryBase
from src.domain.entities.inscripcion import Inscripcion
from src.domain.exceptions.domain_exceptions import AlumnoYaInscriptoException

class InscripcionRepositorySQLite(InscripcionRepositoryBase):
    
    def __init__(self, conexion: sqlite3.Connection):
        self.conexion = conexion
        self.conexion.row_factory = sqlite3.Row
    
    def crear(self, inscripcion: Inscripcion) -> Inscripcion:
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                INSERT INTO inscripcion (alumno_id, curso_id, fecha_inscripcion)
                VALUES (?, ?, ?)
            """, (
                inscripcion.alumno_id,
                inscripcion.curso_id,
                datetime.now()
            ))
            self.conexion.commit()
            
            inscripcion.id = cursor.lastrowid
            inscripcion.fecha_inscripcion = datetime.now()
            return inscripcion
            
        except sqlite3.IntegrityError as e:
            if 'UNIQUE' in str(e) or 'unique' in str(e).lower():
                raise AlumnoYaInscriptoException(f"El alumno {inscripcion.alumno_id} ya está inscripto en el curso {inscripcion.curso_id}")
            raise

    def obtener_por_id(self, id: int) -> Optional[Inscripcion]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM inscripcion WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._row_to_inscripcion(row) if row else None
    
    def obtener_por_alumno(self, alumno_id: int) -> List[Inscripcion]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM inscripcion WHERE alumno_id = ?", (alumno_id,))
        rows = cursor.fetchall()
        return [self._row_to_inscripcion(row) for row in rows]
    
    def obtener_por_curso(self, curso_id: int) -> List[Inscripcion]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM inscripcion WHERE curso_id = ?", (curso_id,))
        rows = cursor.fetchall()
        return [self._row_to_inscripcion(row) for row in rows]
    
    def existe(self, alumno_id: int, curso_id: int) -> bool:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT 1 FROM inscripcion WHERE alumno_id = ? AND curso_id = ?", (alumno_id, curso_id))
        return cursor.fetchone() is not None
    
    def eliminar(self, id: int) -> bool:
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM inscripcion WHERE id = ?", (id,))
        self.conexion.commit()
        return cursor.rowcount > 0

    def _row_to_inscripcion(self, row: sqlite3.Row) -> Inscripcion:
        return Inscripcion(
            id=row['id'],
            alumno_id=row['alumno_id'],
            curso_id=row['curso_id'],
            fecha_inscripcion=datetime.fromisoformat(row['fecha_inscripcion']) if row['fecha_inscripcion'] else None
        )
