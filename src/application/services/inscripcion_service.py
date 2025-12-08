"""
Servicio de Aplicación: InscripcionService
Sistema de Seguimiento de Alumnos
"""

from typing import List
from src.domain.entities.inscripcion import Inscripcion
from src.infrastructure.repositories.base.inscripcion_repository_base import InscripcionRepositoryBase
from src.infrastructure.repositories.base.alumno_repository_base import AlumnoRepositoryBase
from src.infrastructure.repositories.base.curso_repository_base import CursoRepositoryBase
from src.domain.exceptions.domain_exceptions import (
    AlumnoNoEncontradoException,
    CursoNoEncontradoException,
    AlumnoYaInscriptoException,
    InscripcionNoEncontradaException
)

class InscripcionService:
    
    def __init__(
        self, 
        inscripcion_repo: InscripcionRepositoryBase,
        alumno_repo: AlumnoRepositoryBase,
        curso_repo: CursoRepositoryBase
    ):
        self.inscripcion_repo = inscripcion_repo
        self.alumno_repo = alumno_repo
        self.curso_repo = curso_repo
    
    def matricular_alumno(self, alumno_id: int, curso_id: int) -> Inscripcion:
        # Validar existencia de alumno
        if not self.alumno_repo.obtener_por_id(alumno_id):
            raise AlumnoNoEncontradoException(f"No existe alumno con ID {alumno_id}")
        
        # Validar existencia de curso
        if not self.curso_repo.obtener_por_id(curso_id):
            raise CursoNoEncontradoException(f"No existe curso con ID {curso_id}")
            
        # Validar que no esté inscripto (aunque el repo lo valida, es bueno hacerlo aquí también o confiar en el repo)
        if self.inscripcion_repo.existe(alumno_id, curso_id):
            raise AlumnoYaInscriptoException(f"El alumno {alumno_id} ya está inscripto en el curso {curso_id}")
            
        inscripcion = Inscripcion(alumno_id=alumno_id, curso_id=curso_id)
        return self.inscripcion_repo.crear(inscripcion)
    
    def obtener_inscripcion(self, id: int) -> Inscripcion:
        inscripcion = self.inscripcion_repo.obtener_por_id(id)
        if not inscripcion:
            raise InscripcionNoEncontradaException(f"No existe inscripcion con ID {id}")
        return inscripcion
        
    def listar_inscripciones_alumno(self, alumno_id: int) -> List[Inscripcion]:
        if not self.alumno_repo.obtener_por_id(alumno_id):
            raise AlumnoNoEncontradoException(f"No existe alumno con ID {alumno_id}")
        return self.inscripcion_repo.obtener_por_alumno(alumno_id)
    
    def listar_inscripciones_curso(self, curso_id: int) -> List[Inscripcion]:
         if not self.curso_repo.obtener_por_id(curso_id):
            raise CursoNoEncontradoException(f"No existe curso con ID {curso_id}")
         return self.inscripcion_repo.obtener_por_curso(curso_id)

    def cancelar_inscripcion(self, id: int) -> bool:
        return self.inscripcion_repo.eliminar(id)
