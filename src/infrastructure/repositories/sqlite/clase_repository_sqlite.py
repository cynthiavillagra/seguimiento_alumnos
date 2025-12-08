"""
Implementación SQLite: ClaseRepository
Sistema de Seguimiento de Alumnos
"""

import sqlite3
from typing import List, Optional
from datetime import date, datetime

from src.infrastructure.repositories.base.clase_repository_base import ClaseRepositoryBase
from src.domain.entities.clase import Clase
from src.domain.exceptions.domain_exceptions import ClaseNoEncontradaException, BusinessRuleException

class ClaseRepositorySQLite(ClaseRepositoryBase):
    
    def __init__(self, conexion: sqlite3.Connection):
        self.conexion = conexion
        self.conexion.row_factory = sqlite3.Row
    
    def crear(self, clase: Clase) -> Clase:
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                INSERT INTO clase (curso_id, fecha, numero_clase, tema, fecha_creacion)
                VALUES (?, ?, ?, ?, ?)
            """, (
                clase.curso_id,
                clase.fecha.isoformat(),
                clase.numero_clase,
                clase.tema,
                datetime.now()
            ))
            self.conexion.commit()
            
            clase.id = cursor.lastrowid
            clase.fecha_creacion = datetime.now()
            return clase
        except sqlite3.IntegrityError as e:
            if 'UNIQUE' in str(e) or 'unique' in str(e).lower():
                 # Puede ser curso_id + numero_clase duplicado
                 raise BusinessRuleException(f"Ya existe una clase con número {clase.numero_clase} para este curso.")
            raise

    def obtener_por_id(self, id: int) -> Optional[Clase]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM clase WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._row_to_clase(row) if row else None
    
    def obtener_por_curso(self, curso_id: int) -> List[Clase]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM clase WHERE curso_id = ? ORDER BY numero_clase ASC", (curso_id,))
        rows = cursor.fetchall()
        return [self._row_to_clase(row) for row in rows]

    def obtener_por_fecha(self, curso_id: int, fecha: date) -> Optional[Clase]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM clase WHERE curso_id = ? AND fecha = ?", (curso_id, fecha.isoformat()))
        row = cursor.fetchone()
        return self._row_to_clase(row) if row else None
    
    def actualizar(self, clase: Clase) -> Clase:
        if clase.id is None:
            raise ValueError("ID requerido para actualizar")
            
        cursor = self.conexion.cursor()
        
        # Verificar existencia
        existente = self.obtener_por_id(clase.id)
        if not existente:
            raise ClaseNoEncontradaException(f"No existe clase con ID {clase.id}")

        try:
            cursor.execute("""
                UPDATE clase
                SET numero_clase = ?, fecha = ?, tema = ?
                WHERE id = ?
            """, (
                clase.numero_clase,
                clase.fecha.isoformat(),
                clase.tema,
                clase.id
            ))
            self.conexion.commit()
            return clase
        except sqlite3.IntegrityError as e:
            if 'UNIQUE' in str(e) or 'unique' in str(e).lower():
                 raise BusinessRuleException(f"Ya existe una clase con número {clase.numero_clase} para este curso.")
            raise
    
    def eliminar(self, id: int) -> bool:
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM clase WHERE id = ?", (id,))
        self.conexion.commit()
        return cursor.rowcount > 0

    def _row_to_clase(self, row: sqlite3.Row) -> Clase:
        return Clase(
            id=row['id'],
            curso_id=row['curso_id'],
            fecha=date.fromisoformat(row['fecha']),
            numero_clase=row['numero_clase'],
            tema=row['tema'],
            fecha_creacion=datetime.fromisoformat(row['fecha_creacion']) if row['fecha_creacion'] else None
        )
