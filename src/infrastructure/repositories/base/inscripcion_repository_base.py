"""
Interfaz Base: InscripcionRepository
Sistema de Seguimiento de Alumnos
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.inscripcion import Inscripcion

class InscripcionRepositoryBase(ABC):
    
    @abstractmethod
    def crear(self, inscripcion: Inscripcion) -> Inscripcion:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Inscripcion]:
        pass
    
    @abstractmethod
    def obtener_por_alumno(self, alumno_id: int) -> List[Inscripcion]:
        pass
    
    @abstractmethod
    def obtener_por_curso(self, curso_id: int) -> List[Inscripcion]:
        pass
    
    @abstractmethod
    def existe(self, alumno_id: int, curso_id: int) -> bool:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
