"""
Interfaz Base: EntregaTPRepository
Sistema de Seguimiento de Alumnos
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.entrega_tp import EntregaTP

class EntregaTPRepositoryBase(ABC):
    
    @abstractmethod
    def crear_o_actualizar(self, entrega: EntregaTP) -> EntregaTP:
        # UPSERT functionality might be useful here
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[EntregaTP]:
        pass
    
    @abstractmethod
    def obtener_por_tp(self, tp_id: int) -> List[EntregaTP]:
        pass
    
    @abstractmethod
    def obtener_por_alumno_y_tp(self, alumno_id: int, tp_id: int) -> Optional[EntregaTP]:
        pass
        
    @abstractmethod
    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[EntregaTP]:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
