"""
Servicio de Aplicación: CursoService
Sistema de Seguimiento de Alumnos
"""

from typing import List, Optional
from src.domain.entities.curso import Curso
from src.infrastructure.repositories.base.curso_repository_base import CursoRepositoryBase
from src.domain.exceptions.domain_exceptions import (
    CursoNoEncontradoException,
    CuatrimestreInvalidoException,
    BusinessRuleException
)


class CursoService:
    """
    Servicio de Aplicación para gestión de Cursos.
    """
    
    def __init__(self, curso_repository: CursoRepositoryBase):
        self.curso_repo = curso_repository
    
    def crear_curso(
        self,
        nombre_materia: str,
        anio: int,
        cuatrimestre: int,
        docente_responsable: str
    ) -> Curso:
        """
        Crea un nuevo curso.
        """
        try:
            curso = Curso(
                nombre_materia=nombre_materia,
                anio=anio,
                cuatrimestre=cuatrimestre,
                docente_responsable=docente_responsable
            )
        except ValueError as e:
            if 'Cuatrimestre' in str(e):
                raise CuatrimestreInvalidoException(str(e))
            raise
        
        # Validación de negocio adicional si hiciera falta (e.g. no repetir curso en mismo periodo con mismo nombre)
        # Por ahora asumimos que se puede.
        
        return self.curso_repo.crear(curso)
    
    def obtener_curso(self, curso_id: int) -> Curso:
        """Obtiene un curso por ID"""
        curso = self.curso_repo.obtener_por_id(curso_id)
        if not curso:
            raise CursoNoEncontradoException(f"No existe curso con ID {curso_id}")
        return curso
    
    def listar_cursos(
        self,
        limite: Optional[int] = None,
        offset: int = 0,
        anio: Optional[int] = None,
        cuatrimestre: Optional[int] = None
    ) -> List[Curso]:
        """Lista cursos con filtros opcionales."""
        if anio is not None and cuatrimestre is not None:
            return self.curso_repo.buscar_por_anio_y_cuatrimestre(anio, cuatrimestre)
        
        # Si hubiera más filtros, se aplicarían aquí.
        # Por simplificación, repo.obtener_todos ordenará por fecha/periodo.
        return self.curso_repo.obtener_todos(limite=limite, offset=offset)
    
    def actualizar_curso(
        self,
        curso_id: int,
        nombre_materia: Optional[str] = None,
        anio: Optional[int] = None,
        cuatrimestre: Optional[int] = None,
        docente_responsable: Optional[str] = None
    ) -> Curso:
        """Actualiza un curso existente."""
        curso = self.obtener_curso(curso_id)
        
        if nombre_materia is not None:
            curso.nombre_materia = nombre_materia
        if anio is not None:
            curso.anio = anio
        if cuatrimestre is not None:
            curso.cuatrimestre = cuatrimestre
        if docente_responsable is not None:
            curso.docente_responsable = docente_responsable
            
        try:
            curso._validar_datos()
        except ValueError as e:
             if 'Cuatrimestre' in str(e):
                raise CuatrimestreInvalidoException(str(e))
             raise
             
        return self.curso_repo.actualizar(curso)
    
    def eliminar_curso(self, curso_id: int) -> bool:
        """Elimina un curso."""
        return self.curso_repo.eliminar(curso_id)
