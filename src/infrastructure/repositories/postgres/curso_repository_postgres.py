"""
Implementación PostgreSQL: CursoRepository
Sistema de Seguimiento de Alumnos
"""

import psycopg2
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.curso_repository_base import CursoRepositoryBase
from src.domain.entities.curso import Curso
from src.domain.exceptions.domain_exceptions import CursoNoEncontradoException


class CursoRepositoryPostgres(CursoRepositoryBase):
    """
    Implementación PostgreSQL del repositorio de Curso.
    """
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, curso: Curso) -> Curso:
        """Crea un nuevo curso en la base de datos"""
        query = """
            INSERT INTO curso (nombre_materia, anio, cuatrimestre, docente_responsable, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, fecha_creacion;
        """
        params = (
            curso.nombre_materia,
            curso.anio,
            curso.cuatrimestre,
            curso.docente_responsable,
            datetime.now()
        )
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                self.conexion.commit()
                
                curso.id = row['id']
                curso.fecha_creacion = row['fecha_creacion']
                return curso
        except Exception as e:
            self.conexion.rollback()
            raise e

    def obtener_por_id(self, id: int) -> Optional[Curso]:
        """Obtiene un curso por ID"""
        query = "SELECT * FROM curso WHERE id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_curso(row) if row else None

    def obtener_todos(self, limite: Optional[int] = None, offset: int = 0) -> List[Curso]:
        """Obtiene todos los cursos con paginación opcional"""
        query = "SELECT * FROM curso ORDER BY anio DESC, cuatrimestre DESC, nombre_materia ASC"
        
        if limite is not None:
            query += f" LIMIT {limite} OFFSET {offset}"
            
        with self.conexion.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._row_to_curso(row) for row in rows]

    def buscar_por_anio_y_cuatrimestre(self, anio: int, cuatrimestre: int) -> List[Curso]:
        """Obtiene cursos de un cuatrimestre específico"""
        query = """
            SELECT * FROM curso 
            WHERE anio = %s AND cuatrimestre = %s
            ORDER BY nombre_materia ASC
        """
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (anio, cuatrimestre))
            rows = cursor.fetchall()
            return [self._row_to_curso(row) for row in rows]

    def actualizar(self, curso: Curso) -> Curso:
        """Actualiza un curso existente"""
        if curso.id is None:
            raise ValueError("El curso debe tener un ID para actualizarlo")
            
        check_query = "SELECT id FROM curso WHERE id = %s"
        update_query = """
            UPDATE curso 
            SET nombre_materia = %s, anio = %s, cuatrimestre = %s, docente_responsable = %s
            WHERE id = %s
        """
        params = (
            curso.nombre_materia,
            curso.anio,
            curso.cuatrimestre,
            curso.docente_responsable,
            curso.id
        )
        
        try:
            with self.conexion.cursor() as cursor:
                # Verificar existencia
                cursor.execute(check_query, (curso.id,))
                if not cursor.fetchone():
                    raise CursoNoEncontradoException(f"No existe curso con ID {curso.id}")
                
                # Actualizar
                cursor.execute(update_query, params)
                self.conexion.commit()
                return curso
        except Exception as e:
            self.conexion.rollback()
            raise e

    def eliminar(self, id: int) -> bool:
        """Elimina un curso por ID"""
        query = "DELETE FROM curso WHERE id = %s"
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, (id,))
                deleted = cursor.rowcount > 0
                self.conexion.commit()
                return deleted
        except Exception as e:
            self.conexion.rollback()
            raise e

    def _row_to_curso(self, row) -> Curso:
        """Convierte una fila de BD a una entidad Curso"""
        return Curso(
            id=row['id'],
            nombre_materia=row['nombre_materia'],
            anio=row['anio'],
            cuatrimestre=row['cuatrimestre'],
            docente_responsable=row['docente_responsable'],
            fecha_creacion=row['fecha_creacion'] if row.get('fecha_creacion') else None
        )
