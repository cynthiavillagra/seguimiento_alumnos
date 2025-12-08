"""
Interfaz Base: RegistroParticipacionRepository
Sistema de Seguimiento de Alumnos
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.registro_participacion import RegistroParticipacion

class RegistroParticipacionRepositoryBase(ABC):
    
    @abstractmethod
    def crear(self, registro: RegistroParticipacion) -> RegistroParticipacion:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[RegistroParticipacion]:
        pass
    
    @abstractmethod
    def obtener_por_clase(self, clase_id: int) -> List[RegistroParticipacion]:
        pass

    @abstractmethod
    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[RegistroParticipacion]:
        pass
    
    @abstractmethod
    def actualizar(self, registro: RegistroParticipacion) -> RegistroParticipacion:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
