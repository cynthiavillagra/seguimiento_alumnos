"""
Implementación SQLite: CursoRepository
Sistema de Seguimiento de Alumnos
"""

import sqlite3
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.curso_repository_base import CursoRepositoryBase
from src.domain.entities.curso import Curso
from src.domain.exceptions.domain_exceptions import CursoNoEncontradoException


class CursoRepositorySQLite(CursoRepositoryBase):
    """
    Implementación SQLite del repositorio de Curso.
    """
    
    def __init__(self, conexion: sqlite3.Connection):
        self.conexion = conexion
        self.conexion.row_factory = sqlite3.Row
    
    def crear(self, curso: Curso) -> Curso:
        """Crea un nuevo curso en la base de datos"""
        cursor = self.conexion.cursor()
        
        cursor.execute("""
            INSERT INTO curso (nombre_materia, anio, cuatrimestre, docente_responsable, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
        """, (
            curso.nombre_materia,
            curso.anio,
            curso.cuatrimestre,
            curso.docente_responsable,
            datetime.now()
        ))
        
        self.conexion.commit()
        
        curso.id = cursor.lastrowid
        curso.fecha_creacion = datetime.now()
        
        return curso
    
    def obtener_por_id(self, id: int) -> Optional[Curso]:
        """Obtiene un curso por ID"""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM curso WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_curso(row)
        return None
    
    def obtener_todos(self, limite: Optional[int] = None, offset: int = 0) -> List[Curso]:
        """Obtiene todos los cursos con paginación opcional"""
        cursor = self.conexion.cursor()
        
        query = "SELECT * FROM curso ORDER BY anio DESC, cuatrimestre DESC, nombre_materia ASC"
        
        if limite is not None:
            query += f" LIMIT {limite} OFFSET {offset}"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        return [self._row_to_curso(row) for row in rows]
    
    def buscar_por_anio_y_cuatrimestre(self, anio: int, cuatrimestre: int) -> List[Curso]:
        """Obtiene cursos de un cuatrimestre específico"""
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT * FROM curso 
            WHERE anio = ? AND cuatrimestre = ?
            ORDER BY nombre_materia ASC
        """, (anio, cuatrimestre))
        
        rows = cursor.fetchall()
        return [self._row_to_curso(row) for row in rows]
    
    def actualizar(self, curso: Curso) -> Curso:
        """Actualiza un curso existente"""
        if curso.id is None:
            raise ValueError("El curso debe tener un ID para actualizarlo")
        
        # Verificar que existe
        existente = self.obtener_por_id(curso.id)
        if not existente:
            raise CursoNoEncontradoException(f"No existe curso con ID {curso.id}")
        
        cursor = self.conexion.cursor()
        cursor.execute("""
            UPDATE curso 
            SET nombre_materia = ?, anio = ?, cuatrimestre = ?, docente_responsable = ?
            WHERE id = ?
        """, (
            curso.nombre_materia,
            curso.anio,
            curso.cuatrimestre,
            curso.docente_responsable,
            curso.id
        ))
        
        self.conexion.commit()
        return curso
    
    def eliminar(self, id: int) -> bool:
        """Elimina un curso por ID"""
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM curso WHERE id = ?", (id,))
        self.conexion.commit()
        
        return cursor.rowcount > 0
    
    def _row_to_curso(self, row: sqlite3.Row) -> Curso:
        """Convierte una fila de SQLite a una entidad Curso"""
        return Curso(
            id=row['id'],
            nombre_materia=row['nombre_materia'],
            anio=row['anio'],
            cuatrimestre=row['cuatrimestre'],
            docente_responsable=row['docente_responsable'],
            fecha_creacion=datetime.fromisoformat(row['fecha_creacion']) if row['fecha_creacion'] else None
        )
