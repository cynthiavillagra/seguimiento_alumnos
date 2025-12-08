"""
Implementación PostgreSQL: CursoRepository
Sistema de Seguimiento de Alumnos

Compatible con pg8000 (pure Python driver).
"""

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
        """Crea un nuevo curso"""
        query = """
            INSERT INTO curso (nombre_materia, anio, cuatrimestre, docente_responsable, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, fecha_creacion
        """
        params = (
            curso.nombre_materia,
            curso.anio,
            curso.cuatrimestre,
            curso.docente_responsable,
            datetime.now()
        )
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            self.conexion.commit()
            
            curso.id = row[0]
            curso.fecha_creacion = row[1]
            return curso
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def obtener_por_id(self, id: int) -> Optional[Curso]:
        """Obtiene un curso por ID"""
        query = "SELECT id, nombre_materia, anio, cuatrimestre, docente_responsable, fecha_creacion FROM curso WHERE id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            self.conexion.commit()
            return self._row_to_curso(row) if row else None
        finally:
            cursor.close()

    def obtener_todos(self, limite: Optional[int] = None, offset: int = 0) -> List[Curso]:
        """Obtiene todos los cursos"""
        query = "SELECT id, nombre_materia, anio, cuatrimestre, docente_responsable, fecha_creacion FROM curso ORDER BY anio DESC, cuatrimestre DESC"
        
        if limite is not None:
            query += f" LIMIT {limite} OFFSET {offset}"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            self.conexion.commit()  # Close transaction
            return [self._row_to_curso(row) for row in rows]
        finally:
            cursor.close()

    def obtener_por_anio(self, anio: int) -> List[Curso]:
        """Obtiene cursos de un año específico"""
        query = "SELECT id, nombre_materia, anio, cuatrimestre, docente_responsable, fecha_creacion FROM curso WHERE anio = %s ORDER BY cuatrimestre"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (anio,))
            rows = cursor.fetchall()
            self.conexion.commit()
            return [self._row_to_curso(row) for row in rows]
        finally:
            cursor.close()

    def buscar_por_anio_y_cuatrimestre(self, anio: int, cuatrimestre: int) -> List[Curso]:
        """Obtiene cursos de un cuatrimestre específico"""
        query = "SELECT id, nombre_materia, anio, cuatrimestre, docente_responsable, fecha_creacion FROM curso WHERE anio = %s AND cuatrimestre = %s ORDER BY nombre_materia"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (anio, cuatrimestre))
            rows = cursor.fetchall()
            self.conexion.commit()
            return [self._row_to_curso(row) for row in rows]
        finally:
            cursor.close()

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
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(check_query, (curso.id,))
            if not cursor.fetchone():
                raise CursoNoEncontradoException(f"No existe curso con ID {curso.id}")
            
            cursor.execute(update_query, params)
            self.conexion.commit()
            return curso
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def eliminar(self, id: int) -> bool:
        """Elimina un curso por ID"""
        query = "DELETE FROM curso WHERE id = %s"
        
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

    def _row_to_curso(self, row) -> Curso:
        """Convierte una tupla a Curso"""
        return Curso(
            id=row[0],
            nombre_materia=row[1],
            anio=row[2],
            cuatrimestre=row[3],
            docente_responsable=row[4],
            fecha_creacion=row[5] if len(row) > 5 else None
        )
