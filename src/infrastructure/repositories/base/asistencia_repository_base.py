"""
Interfaz Base: RegistroAsistenciaRepository
Sistema de Seguimiento de Alumnos
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.registro_asistencia import RegistroAsistencia

class RegistroAsistenciaRepositoryBase(ABC):
    
    @abstractmethod
    def crear(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[RegistroAsistencia]:
        pass
    
    @abstractmethod
    def obtener_por_clase(self, clase_id: int) -> List[RegistroAsistencia]:
        pass

    @abstractmethod
    def obtener_por_alumno_y_curso(self, alumno_id: int, curso_id: int) -> List[RegistroAsistencia]:
        # Esto va a requerir JOINs en la implementación
        pass
    
    @abstractmethod
    def existe(self, alumno_id: int, clase_id: int) -> bool:
        pass
    
    @abstractmethod
    def actualizar(self, registro: RegistroAsistencia) -> RegistroAsistencia:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
