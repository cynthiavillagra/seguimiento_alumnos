"""
Interfaz Base: TrabajoPracticoRepository
Sistema de Seguimiento de Alumnos
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.trabajo_practico import TrabajoPractico

class TrabajoPracticoRepositoryBase(ABC):
    
    @abstractmethod
    def crear(self, tp: TrabajoPractico) -> TrabajoPractico:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[TrabajoPractico]:
        pass
    
    @abstractmethod
    def obtener_por_curso(self, curso_id: int) -> List[TrabajoPractico]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[TrabajoPractico]:
        pass
    
    @abstractmethod
    def actualizar(self, tp: TrabajoPractico) -> TrabajoPractico:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
