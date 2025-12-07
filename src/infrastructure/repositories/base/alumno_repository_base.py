"""
Interfaz Base: AlumnoRepository
Sistema de Seguimiento de Alumnos

Decisión de diseño: Patrón Repository + Dependency Inversion Principle
- Esta interfaz define el CONTRATO de lo que puede hacer un repositorio de alumnos
- NO especifica CÓMO lo hace (eso es responsabilidad de las implementaciones)
- Permite cambiar de SQLite a PostgreSQL sin tocar la lógica de negocio
- Facilita testing con repositorios mock
- Mantiene el dominio independiente de la infraestructura

Principio SOLID aplicado: Dependency Inversion
- Los módulos de alto nivel (servicios) dependen de abstracciones (esta interfaz)
- Los módulos de bajo nivel (implementaciones SQLite) también dependen de abstracciones
- Las abstracciones no dependen de detalles, los detalles dependen de abstracciones
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.alumno import Alumno


class AlumnoRepositoryBase(ABC):
    """
    Interfaz base para repositorios de Alumno.
    
    Define las operaciones CRUD básicas que cualquier implementación
    de repositorio de alumnos debe proveer.
    
    Decisión de diseño: ABC (Abstract Base Class)
    - Usamos ABC de Python para definir interfaces
    - Los métodos abstractos DEBEN ser implementados por las subclases
    - Si una subclase no implementa todos los métodos, no se puede instanciar
    """
    
    @abstractmethod
    def crear(self, alumno: Alumno) -> Alumno:
        """
        Crea un nuevo alumno en el sistema.
        
        Args:
            alumno: Instancia de Alumno a crear (sin ID)
        
        Returns:
            Alumno: El alumno creado con ID asignado
        
        Raises:
            DNIDuplicadoException: Si ya existe un alumno con ese DNI
            ValidationException: Si los datos del alumno son inválidos
        """
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        """
        Obtiene un alumno por su ID.
        
        Args:
            id: ID del alumno a buscar
        
        Returns:
            Alumno si existe, None si no existe
        """
        pass
    
    @abstractmethod
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """
        Obtiene un alumno por su DNI.
        
        Útil para validar unicidad de DNI.
        
        Args:
            dni: DNI del alumno a buscar
        
        Returns:
            Alumno si existe, None si no existe
        """
        pass
    
    @abstractmethod
    def obtener_todos(self, limite: Optional[int] = None, offset: int = 0) -> List[Alumno]:
        """
        Obtiene todos los alumnos del sistema.
        
        Args:
            limite: Número máximo de resultados (para paginación)
            offset: Número de resultados a saltar (para paginación)
        
        Returns:
            Lista de alumnos (puede estar vacía)
        """
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Alumno]:
        """
        Busca alumnos por nombre o apellido (búsqueda parcial).
        
        Args:
            nombre: Texto a buscar en nombre o apellido
        
        Returns:
            Lista de alumnos que coinciden (puede estar vacía)
        """
        pass
    
    @abstractmethod
    def obtener_por_cohorte(self, cohorte: int) -> List[Alumno]:
        """
        Obtiene todos los alumnos de una cohorte específica.
        
        Args:
            cohorte: Año de cohorte
        
        Returns:
            Lista de alumnos de esa cohorte
        """
        pass
    
    @abstractmethod
    def actualizar(self, alumno: Alumno) -> Alumno:
        """
        Actualiza los datos de un alumno existente.
        
        Args:
            alumno: Alumno con datos actualizados (debe tener ID)
        
        Returns:
            Alumno actualizado
        
        Raises:
            AlumnoNoEncontradoException: Si el alumno no existe
            DNIDuplicadoException: Si el nuevo DNI ya existe en otro alumno
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina un alumno del sistema.
        
        Decisión de diseño: Soft delete vs Hard delete
        - En producción, se recomienda soft delete (marcar como inactivo)
        - En el MVP, hacemos hard delete por simplicidad
        - La implementación puede decidir cuál usar
        
        Args:
            id: ID del alumno a eliminar
        
        Returns:
            True si se eliminó, False si no existía
        """
        pass
    
    @abstractmethod
    def contar_total(self) -> int:
        """
        Cuenta el total de alumnos en el sistema.
        
        Útil para paginación y estadísticas.
        
        Returns:
            Número total de alumnos
        """
        pass
