"""
Servicio de Aplicación: AsistenciaService
Sistema de Seguimiento de Alumnos
"""

from typing import List
from src.domain.entities.registro_asistencia import RegistroAsistencia
from src.domain.value_objects.enums import EstadoAsistencia
from src.infrastructure.repositories.base.asistencia_repository_base import RegistroAsistenciaRepositoryBase
from src.infrastructure.repositories.base.clase_repository_base import ClaseRepositoryBase
from src.infrastructure.repositories.base.inscripcion_repository_base import InscripcionRepositoryBase
from src.domain.exceptions.domain_exceptions import (
    ClaseNoEncontradaException,
    AlumnoNoInscriptoException,
    AsistenciaYaRegistradaException
)

class AsistenciaService:
    
    def __init__(
        self, 
        asistencia_repo: RegistroAsistenciaRepositoryBase,
        clase_repo: ClaseRepositoryBase,
        inscripcion_repo: InscripcionRepositoryBase
    ):
        self.asistencia_repo = asistencia_repo
        self.clase_repo = clase_repo
        self.inscripcion_repo = inscripcion_repo
    
    def registrar_asistencia(self, alumno_id: int, clase_id: int, estado: str) -> RegistroAsistencia:
        # Obtener clase para saber el curso
        clase = self.clase_repo.obtener_por_id(clase_id)
        if not clase:
            raise ClaseNoEncontradaException(f"Clase {clase_id} no encontrada")
            
        # Validar inscripción
        if not self.inscripcion_repo.existe(alumno_id, clase.curso_id):
            raise AlumnoNoInscriptoException(f"El alumno {alumno_id} no está inscripto en el curso de esta clase")
            
        # Validar duplicados (aunque el repo también lo hace)
        if self.asistencia_repo.existe(alumno_id, clase_id):
             raise AsistenciaYaRegistradaException(f"Ya existe asistencia para alumno {alumno_id} en clase {clase_id}")

        registro = RegistroAsistencia(
            alumno_id=alumno_id,
            clase_id=clase_id,
            estado=EstadoAsistencia(estado)
        )
        return self.asistencia_repo.crear(registro)
    
    def listar_asistencias_clase(self, clase_id: int) -> List[RegistroAsistencia]:
        if not self.clase_repo.obtener_por_id(clase_id):
            raise ClaseNoEncontradaException(f"Clase {clase_id} no encontrada")
        return self.asistencia_repo.obtener_por_clase(clase_id)
    
    def listar_asistencias_alumno_curso(self, alumno_id: int, curso_id: int) -> List[RegistroAsistencia]:
        # Aquí también deberíamos validar que el curso y alumno existan, idealmente
        return self.asistencia_repo.obtener_por_alumno_y_curso(alumno_id, curso_id)

    def actualizar_asistencia(self, asistencia_id: int, nuevo_estado: str) -> RegistroAsistencia:
        registro = self.asistencia_repo.obtener_por_id(asistencia_id)
        if not registro:
            # TODO: Add specific exception
             raise ValueError(f"Asistencia {asistencia_id} no encontrada")
             
        registro.estado = EstadoAsistencia(nuevo_estado)
        return self.asistencia_repo.actualizar(registro)

    def eliminar_asistencia(self, asistencia_id: int) -> bool:
        return self.asistencia_repo.eliminar(asistencia_id)
