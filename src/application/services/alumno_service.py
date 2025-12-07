"""
Servicio de Aplicación: AlumnoService
Sistema de Seguimiento de Alumnos

Decisión de diseño: Capa de Servicios
- Los servicios orquestan casos de uso
- Coordinan entidades de dominio y repositorios
- NO contienen lógica de negocio pura (eso va en entidades)
- NO conocen detalles de HTTP, JSON, SQL (eso va en otras capas)
- Implementan los casos de uso definidos en la documentación
"""

from typing import List, Optional
from src.domain.entities.alumno import Alumno
from src.infrastructure.repositories.base.alumno_repository_base import AlumnoRepositoryBase
from src.domain.exceptions.domain_exceptions import (
    AlumnoNoEncontradoException,
    DNIDuplicadoException,
    EmailInvalidoException
)


class AlumnoService:
    """
    Servicio de Aplicación para gestión de Alumnos.
    
    Responsabilidades:
    - Implementar casos de uso relacionados con alumnos
    - Validar reglas de negocio que requieren acceso a repositorio
    - Coordinar operaciones entre múltiples entidades/repositorios
    - Manejar transacciones (en casos complejos)
    
    Casos de Uso implementados:
    - CU-10: Crear Alumno
    - CU-04: Consultar Ficha de Alumno (parcial, solo datos básicos)
    
    Decisión de diseño: Inyección de Dependencias
    - El servicio recibe el repositorio por constructor
    - Depende de la INTERFAZ (AlumnoRepositoryBase), no de la implementación
    - Esto permite:
      * Cambiar de SQLite a PostgreSQL sin tocar este código
      * Testear con repositorios mock
      * Mantener bajo acoplamiento
    """
    
    def __init__(self, alumno_repository: AlumnoRepositoryBase):
        """
        Inicializa el servicio con un repositorio de alumnos.
        
        Args:
            alumno_repository: Implementación del repositorio de alumnos
        """
        self.alumno_repo = alumno_repository
    
    def crear_alumno(
        self,
        nombre: str,
        apellido: str,
        dni: str,
        email: str,
        cohorte: int
    ) -> Alumno:
        """
        Caso de Uso CU-10: Crear Alumno
        
        Orquesta:
        1. Crear entidad de dominio (con validaciones básicas)
        2. Validar reglas de negocio (email, unicidad de DNI)
        3. Persistir mediante repositorio
        
        Args:
            nombre: Nombre del alumno
            apellido: Apellido del alumno
            dni: DNI del alumno (debe ser único)
            email: Email del alumno
            cohorte: Año de ingreso
        
        Returns:
            Alumno: El alumno creado con ID asignado
        
        Raises:
            EmailInvalidoException: Si el email no tiene formato válido
            DNIDuplicadoException: Si ya existe un alumno con ese DNI
            ValueError: Si algún dato es inválido
        """
        # Paso 1: Crear entidad de dominio
        # La entidad valida sus propios datos en __post_init__
        try:
            alumno = Alumno(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                email=email,
                cohorte=cohorte
            )
        except ValueError as e:
            # Convertir ValueError de la entidad a excepción de dominio apropiada
            if 'email' in str(e).lower():
                raise EmailInvalidoException(str(e))
            raise
        
        # Paso 2: Validar unicidad de DNI
        # Esta validación requiere acceso a BD, por eso va en el servicio
        existente = self.alumno_repo.obtener_por_dni(dni)
        if existente:
            raise DNIDuplicadoException(f"Ya existe un alumno con DNI {dni}")
        
        # Paso 3: Persistir
        alumno_creado = self.alumno_repo.crear(alumno)
        
        return alumno_creado
    
    def obtener_alumno(self, alumno_id: int) -> Alumno:
        """
        Obtiene un alumno por ID.
        
        Args:
            alumno_id: ID del alumno
        
        Returns:
            Alumno: El alumno encontrado
        
        Raises:
            AlumnoNoEncontradoException: Si el alumno no existe
        """
        alumno = self.alumno_repo.obtener_por_id(alumno_id)
        
        if not alumno:
            raise AlumnoNoEncontradoException(f"No existe alumno con ID {alumno_id}")
        
        return alumno
    
    def listar_alumnos(
        self,
        limite: Optional[int] = None,
        offset: int = 0,
        cohorte: Optional[int] = None,
        buscar: Optional[str] = None
    ) -> List[Alumno]:
        """
        Lista alumnos con filtros opcionales.
        
        Args:
            limite: Número máximo de resultados (paginación)
            offset: Número de resultados a saltar (paginación)
            cohorte: Filtrar por cohorte específica
            buscar: Buscar por nombre o apellido
        
        Returns:
            List[Alumno]: Lista de alumnos (puede estar vacía)
        """
        # Aplicar filtros según los parámetros
        if buscar:
            return self.alumno_repo.buscar_por_nombre(buscar)
        elif cohorte:
            return self.alumno_repo.obtener_por_cohorte(cohorte)
        else:
            return self.alumno_repo.obtener_todos(limite=limite, offset=offset)
    
    def actualizar_alumno(
        self,
        alumno_id: int,
        nombre: Optional[str] = None,
        apellido: Optional[str] = None,
        dni: Optional[str] = None,
        email: Optional[str] = None,
        cohorte: Optional[int] = None
    ) -> Alumno:
        """
        Actualiza los datos de un alumno existente.
        
        Decisión de diseño: Actualización parcial
        - Solo se actualizan los campos que se pasan (no None)
        - Esto permite PATCH en la API
        
        Args:
            alumno_id: ID del alumno a actualizar
            nombre: Nuevo nombre (opcional)
            apellido: Nuevo apellido (opcional)
            dni: Nuevo DNI (opcional)
            email: Nuevo email (opcional)
            cohorte: Nueva cohorte (opcional)
        
        Returns:
            Alumno: El alumno actualizado
        
        Raises:
            AlumnoNoEncontradoException: Si el alumno no existe
            DNIDuplicadoException: Si el nuevo DNI ya existe
            EmailInvalidoException: Si el nuevo email es inválido
        """
        # Obtener alumno existente
        alumno = self.obtener_alumno(alumno_id)
        
        # Actualizar solo los campos proporcionados
        if nombre is not None:
            alumno.nombre = nombre
        if apellido is not None:
            alumno.apellido = apellido
        if dni is not None:
            alumno.dni = dni
        if email is not None:
            alumno.email = email
        if cohorte is not None:
            alumno.cohorte = cohorte
        
        # Validar datos actualizados
        try:
            alumno._validar_datos_basicos()
        except ValueError as e:
            if 'email' in str(e).lower():
                raise EmailInvalidoException(str(e))
            raise
        
        # Persistir cambios
        alumno_actualizado = self.alumno_repo.actualizar(alumno)
        
        return alumno_actualizado
    
    def eliminar_alumno(self, alumno_id: int) -> bool:
        """
        Elimina un alumno del sistema.
        
        Args:
            alumno_id: ID del alumno a eliminar
        
        Returns:
            bool: True si se eliminó, False si no existía
        """
        return self.alumno_repo.eliminar(alumno_id)
    
    def contar_alumnos(self, cohorte: Optional[int] = None) -> int:
        """
        Cuenta el total de alumnos (opcionalmente filtrado por cohorte).
        
        Args:
            cohorte: Cohorte para filtrar (opcional)
        
        Returns:
            int: Número de alumnos
        """
        if cohorte:
            return len(self.alumno_repo.obtener_por_cohorte(cohorte))
        else:
            return self.alumno_repo.contar_total()
