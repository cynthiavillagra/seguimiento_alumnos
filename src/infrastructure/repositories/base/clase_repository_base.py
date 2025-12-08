"""
Interfaz Base: ClaseRepository
Sistema de Seguimiento de Alumnos
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from src.domain.entities.clase import Clase

class ClaseRepositoryBase(ABC):
    
    @abstractmethod
    def crear(self, clase: Clase) -> Clase:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Clase]:
        pass
    
    @abstractmethod
    def obtener_por_curso(self, curso_id: int) -> List[Clase]:
        pass

    @abstractmethod
    def obtener_por_fecha(self, curso_id: int, fecha: date) -> Optional[Clase]:
        pass
    
    @abstractmethod
    def actualizar(self, clase: Clase) -> Clase:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
