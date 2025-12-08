"""
Implementación SQLite: RegistroAsistenciaRepository
Sistema de Seguimiento de Alumnos
"""

import sqlite3
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.asistencia_repository_base import RegistroAsistenciaRepositoryBase
from src.domain.entities.registro_asistencia import RegistroAsistencia
from src.domain.value_objects.enums import EstadoAsistencia
from src.domain.exceptions.domain_exceptions import AsistenciaYaRegistradaException

class RegistroAsistenciaRepositorySQLite(RegistroAsistenciaRepositoryBase):
    
    def __init__(self, conexion: sqlite3.Connection):
        self.conexion = conexion
        self.conexion.row_factory = sqlite3.Row
    
    def crear(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                INSERT INTO registro_asistencia (alumno_id, clase_id, estado, fecha_registro)
                VALUES (?, ?, ?, ?)
            """, (
                registro.alumno_id,
                registro.clase_id,
                registro.estado.value,
                datetime.now()
            ))
            self.conexion.commit()
            
            registro.id = cursor.lastrowid
            registro.fecha_registro = datetime.now()
            return registro
        except sqlite3.IntegrityError as e:
            if 'UNIQUE' in str(e) or 'unique' in str(e).lower():
                 raise AsistenciaYaRegistradaException(f"Ya existe registro de asistencia para alumno {registro.alumno_id} en clase {registro.clase_id}")
            raise

    def obtener_por_id(self, id: int) -> Optional[RegistroAsistencia]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM registro_asistencia WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._row_to_registro(row) if row else None
    
    def obtener_por_clase(self, clase_id: int) -> List[RegistroAsistencia]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM registro_asistencia WHERE clase_id = ?", (clase_id,))
        rows = cursor.fetchall()
        return [self._row_to_registro(row) for row in rows]
    
    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[RegistroAsistencia]:
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT ra.* 
            FROM registro_asistencia ra
            JOIN clase c ON ra.clase_id = c.id
            WHERE ra.alumno_id = ? AND c.curso_id = ?
            ORDER BY c.fecha ASC
        """, (alumno_id, curso_id))
        rows = cursor.fetchall()
        return [self._row_to_registro(row) for row in rows]

    def existe(self, alumno_id: int, clase_id: int) -> bool:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT 1 FROM registro_asistencia WHERE alumno_id = ? AND clase_id = ?", (alumno_id, clase_id))
        return cursor.fetchone() is not None
    
    def actualizar(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        if registro.id is None:
             raise ValueError("ID requerido para actualizar")
             
        cursor = self.conexion.cursor()
        cursor.execute("""
            UPDATE registro_asistencia
            SET estado = ?
            WHERE id = ?
        """, (
            registro.estado.value,
            registro.id
        ))
        self.conexion.commit()
        return registro
    
    def eliminar(self, id: int) -> bool:
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM registro_asistencia WHERE id = ?", (id,))
        self.conexion.commit()
        return cursor.rowcount > 0

    def _row_to_registro(self, row: sqlite3.Row) -> RegistroAsistencia:
        return RegistroAsistencia(
            id=row['id'],
            alumno_id=row['alumno_id'],
            clase_id=row['clase_id'],
            estado=EstadoAsistencia(row['estado']),
            fecha_registro=datetime.fromisoformat(row['fecha_registro']) if row['fecha_registro'] else None
        )
