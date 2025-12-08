"""
Interfaz Base: CursoRepository
Sistema de Seguimiento de Alumnos
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.curso import Curso


class CursoRepositoryBase(ABC):
    """
    Interfaz base para repositorios de Curso.
    """
    
    @abstractmethod
    def crear(self, curso: Curso) -> Curso:
        """Crea un nuevo curso en el sistema."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Curso]:
        """Obtiene un curso por su ID."""
        pass
    
    @abstractmethod
    def obtener_todos(self, limite: Optional[int] = None, offset: int = 0) -> List[Curso]:
        """Obtiene todos los cursos del sistema."""
        pass
    
    @abstractmethod
    def buscar_por_anio_y_cuatrimestre(self, anio: int, cuatrimestre: int) -> List[Curso]:
        """Obtiene cursos de un cuatrimestre específico."""
        pass
    
    @abstractmethod
    def actualizar(self, curso: Curso) -> Curso:
        """Actualiza los datos de un curso existente."""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un curso del sistema."""
        pass
