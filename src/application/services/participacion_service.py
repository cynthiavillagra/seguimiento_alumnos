"""
Servicio de Aplicación: ParticipacionService
Sistema de Seguimiento de Alumnos
"""

from typing import List, Optional
from src.domain.entities.registro_participacion import RegistroParticipacion
from src.domain.value_objects.enums import NivelParticipacion
from src.infrastructure.repositories.base.participacion_repository_base import RegistroParticipacionRepositoryBase
from src.infrastructure.repositories.base.clase_repository_base import ClaseRepositoryBase
from src.infrastructure.repositories.base.inscripcion_repository_base import InscripcionRepositoryBase
from src.domain.exceptions.domain_exceptions import (
    ClaseNoEncontradaException,
    AlumnoNoInscriptoException
)

class ParticipacionService:
    
    def __init__(
        self, 
        participacion_repo: RegistroParticipacionRepositoryBase,
        clase_repo: ClaseRepositoryBase,
        inscripcion_repo: InscripcionRepositoryBase
    ):
        self.participacion_repo = participacion_repo
        self.clase_repo = clase_repo
        self.inscripcion_repo = inscripcion_repo
    
    def registrar_participacion(self, alumno_id: int, clase_id: int, nivel: str, comentario: Optional[str] = None) -> RegistroParticipacion:
        # Obtener clase
        clase = self.clase_repo.obtener_por_id(clase_id)
        if not clase:
            raise ClaseNoEncontradaException(f"Clase {clase_id} no encontrada")
            
        # Validar inscripción
        if not self.inscripcion_repo.existe(alumno_id, clase.curso_id):
            raise AlumnoNoInscriptoException(f"El alumno {alumno_id} no está inscripto en el curso de esta clase")
            
        # Nota: A diferencia de asistencia, PUEDE haber múltiples registros de participación por clase?
        # El schema.sql NO tiene UNIQUE(alumno_id, clase_id) para participacion.
        # Asumimos que sí puede haber varios aportes en una clase.
        
        registro = RegistroParticipacion(
            alumno_id=alumno_id,
            clase_id=clase_id,
            nivel=NivelParticipacion(nivel),
            comentario=comentario
        )
        return self.participacion_repo.crear(registro)
    
    def listar_participaciones_clase(self, clase_id: int) -> List[RegistroParticipacion]:
        if not self.clase_repo.obtener_por_id(clase_id):
            raise ClaseNoEncontradaException(f"Clase {clase_id} no encontrada")
        return self.participacion_repo.obtener_por_clase(clase_id)
    
    def listar_participaciones_alumno_curso(self, alumno_id: int, curso_id: int) -> List[RegistroParticipacion]:
        return self.participacion_repo.obtener_por_alumno_y_curso(alumno_id, curso_id)

    def actualizar_participacion(self, participacion_id: int, nivel: Optional[str] = None, comentario: Optional[str] = None) -> RegistroParticipacion:
        registro = self.participacion_repo.obtener_por_id(participacion_id)
        if not registro:
             raise ValueError(f"Participación {participacion_id} no encontrada")
             
        if nivel is not None:
             registro.nivel = NivelParticipacion(nivel)
        
        if comentario is not None:
            registro.comentario = comentario
            
        return self.participacion_repo.actualizar(registro)

    def eliminar_participacion(self, participacion_id: int) -> bool:
        return self.participacion_repo.eliminar(participacion_id)
