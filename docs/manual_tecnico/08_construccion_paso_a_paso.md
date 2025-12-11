# Capítulo 8: Construcción Paso a Paso

## 8.1 Orden de Construcción

Vamos a construir el proyecto siguiendo un orden lógico, desde lo más básico hasta lo más complejo.

```
PASO 1: Dominio (Entidad Alumno)
   ↓
PASO 2: Infraestructura (Repositorio Alumno)
   ↓
PASO 3: Aplicación (Servicio Alumno)
   ↓
PASO 4: Presentación (Router Alumno)
   ↓
PASO 5: Probar con Swagger
   ↓
PASO 6: Repetir para otras entidades
   ↓
PASO 7: Frontend básico
   ↓
PASO 8: Conectar Frontend con API
```

## 8.2 Paso 1: Crear la Entidad Alumno

### ¿Por qué empezamos por el dominio?

El dominio es el **corazón** de la aplicación. Define qué es un "Alumno" en nuestro sistema, sin preocuparse por bases de datos o interfaces.

### Crear `src/domain/entities/alumno.py`

```python
"""
Entidad Alumno - Capa de Dominio
Sistema de Seguimiento de Alumnos

Esta clase representa un alumno en el sistema.
Contiene validaciones de negocio y propiedades calculadas.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Alumno:
    """
    Entidad que representa un estudiante en el sistema.
    
    Usamos @dataclass para que Python genere automáticamente:
    - __init__() con todos los campos
    - __repr__() para debugging
    - __eq__() para comparación
    
    Attributes:
        id: Identificador único (None si es nuevo)
        nombre: Nombre del alumno
        apellido: Apellido del alumno
        dni: Documento Nacional de Identidad (único)
        email: Correo electrónico
        cohorte: Año de ingreso a la carrera
        fecha_creacion: Cuándo se creó el registro
    """
    id: Optional[int]
    nombre: str
    apellido: str
    dni: str
    email: str
    cohorte: int
    fecha_creacion: Optional[datetime] = None
    
    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el objeto.
        
        Esto garantiza que NUNCA exista un Alumno inválido en memoria.
        Si algo está mal, lanza una excepción inmediatamente.
        """
        # Validar nombre
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        # Validar apellido
        if not self.apellido or not self.apellido.strip():
            raise ValueError("El apellido no puede estar vacío")
        
        # Validar DNI
        if not self.dni or not self.dni.strip():
            raise ValueError("El DNI no puede estar vacío")
        
        # Limpiar espacios
        self.nombre = self.nombre.strip()
        self.apellido = self.apellido.strip()
        self.dni = self.dni.strip()
        
        # Validar email (básico)
        if not self.email or '@' not in self.email:
            raise ValueError("El email debe contener @")
        
        # Validar cohorte
        if self.cohorte < 2000 or self.cohorte > 2100:
            raise ValueError("El cohorte debe estar entre 2000 y 2100")
    
    @property
    def nombre_completo(self) -> str:
        """
        Propiedad calculada que devuelve "Apellido, Nombre".
        
        Se usa @property para que se acceda como alumno.nombre_completo
        en lugar de alumno.nombre_completo()
        """
        return f"{self.apellido}, {self.nombre}"
    
    def to_dict(self) -> dict:
        """
        Convierte la entidad a diccionario.
        Útil para serialización JSON.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "email": self.email,
            "cohorte": self.cohorte,
            "nombre_completo": self.nombre_completo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Alumno':
        """
        Crea un Alumno desde un diccionario.
        
        @classmethod permite llamar Alumno.from_dict(datos)
        sin necesidad de tener una instancia.
        """
        return cls(
            id=data.get("id"),
            nombre=data["nombre"],
            apellido=data["apellido"],
            dni=data["dni"],
            email=data["email"],
            cohorte=data["cohorte"],
            fecha_creacion=data.get("fecha_creacion")
        )
```

### Crear excepciones de dominio

Crear `src/domain/exceptions/domain_exceptions.py`:

```python
"""
Excepciones de Dominio
Sistema de Seguimiento de Alumnos

Estas excepciones representan errores de NEGOCIO, no errores técnicos.
Permiten que las capas superiores manejen los errores apropiadamente.
"""


class DomainException(Exception):
    """Excepción base para errores de dominio"""
    pass


class AlumnoNoEncontradoException(DomainException):
    """Se lanza cuando no se encuentra un alumno"""
    def __init__(self, alumno_id: int):
        self.alumno_id = alumno_id
        super().__init__(f"No se encontró alumno con ID {alumno_id}")


class DNIDuplicadoException(DomainException):
    """Se lanza cuando se intenta crear un alumno con DNI existente"""
    def __init__(self, dni: str):
        self.dni = dni
        super().__init__(f"Ya existe un alumno con DNI {dni}")


class EmailInvalidoException(DomainException):
    """Se lanza cuando el email tiene formato inválido"""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email inválido: {email}")


class CursoNoEncontradoException(DomainException):
    """Se lanza cuando no se encuentra un curso"""
    def __init__(self, curso_id: int):
        self.curso_id = curso_id
        super().__init__(f"No se encontró curso con ID {curso_id}")


class CuatrimestreInvalidoException(DomainException):
    """Se lanza cuando el cuatrimestre no es 1 o 2"""
    def __init__(self, cuatrimestre: int):
        self.cuatrimestre = cuatrimestre
        super().__init__(f"Cuatrimestre inválido: {cuatrimestre}. Debe ser 1 o 2")


class ClaseNoEncontradaException(DomainException):
    """Se lanza cuando no se encuentra una clase"""
    def __init__(self, clase_id: int):
        self.clase_id = clase_id
        super().__init__(f"No se encontró clase con ID {clase_id}")


class TrabajoPracticoNoEncontradoException(DomainException):
    """Se lanza cuando no se encuentra un TP"""
    def __init__(self, tp_id: int):
        self.tp_id = tp_id
        super().__init__(f"No se encontró TP con ID {tp_id}")


class InscripcionDuplicadaException(DomainException):
    """Se lanza cuando se intenta inscribir un alumno que ya está inscripto"""
    def __init__(self, alumno_id: int, curso_id: int):
        self.alumno_id = alumno_id
        self.curso_id = curso_id
        super().__init__(f"El alumno {alumno_id} ya está inscripto en el curso {curso_id}")
```

### Probar la entidad

Crear `tests/test_alumno.py`:

```python
"""Test de la entidad Alumno"""
import pytest
from src.domain.entities.alumno import Alumno


def test_crear_alumno_valido():
    """Debe crear un alumno con datos válidos"""
    alumno = Alumno(
        id=None,
        nombre="Juan",
        apellido="Pérez",
        dni="12345678",
        email="juan@test.com",
        cohorte=2024
    )
    
    assert alumno.nombre == "Juan"
    assert alumno.apellido == "Pérez"
    assert alumno.nombre_completo == "Pérez, Juan"


def test_alumno_nombre_vacio_falla():
    """Debe fallar si el nombre está vacío"""
    with pytest.raises(ValueError):
        Alumno(
            id=None,
            nombre="",
            apellido="Pérez",
            dni="12345678",
            email="juan@test.com",
            cohorte=2024
        )


def test_alumno_email_invalido_falla():
    """Debe fallar si el email no tiene @"""
    with pytest.raises(ValueError):
        Alumno(
            id=None,
            nombre="Juan",
            apellido="Pérez",
            dni="12345678",
            email="invalido",
            cohorte=2024
        )
```

Ejecutar tests:
```bash
pip install pytest
pytest tests/test_alumno.py -v
```

## 8.3 Paso 2: Crear el Repositorio

### Crear interfaz base

`src/infrastructure/repositories/base/alumno_repository_base.py`:

```python
"""
Interfaz del Repositorio de Alumnos
Sistema de Seguimiento de Alumnos

Esta clase abstracta define el CONTRATO que deben cumplir
todas las implementaciones de repositorio de alumnos.

¿Por qué usar una interfaz?
1. Desacoplamiento: El servicio no sabe qué base de datos usamos
2. Testabilidad: Podemos crear un mock para tests
3. Flexibilidad: Podemos cambiar de PostgreSQL a MongoDB sin tocar el servicio
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.alumno import Alumno


class AlumnoRepositoryBase(ABC):
    """
    Interfaz abstracta para repositorios de Alumno.
    
    ABC = Abstract Base Class
    Los métodos con @abstractmethod DEBEN ser implementados
    por las clases hijas.
    """
    
    @abstractmethod
    def crear(self, alumno: Alumno) -> Alumno:
        """
        Crea un nuevo alumno en la base de datos.
        
        Args:
            alumno: Entidad Alumno (sin id)
        
        Returns:
            Alumno con id asignado
        """
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        """
        Busca un alumno por su ID.
        
        Args:
            id: ID del alumno
        
        Returns:
            Alumno si existe, None si no
        """
        pass
    
    @abstractmethod
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """
        Busca un alumno por su DNI.
        
        Args:
            dni: DNI del alumno
        
        Returns:
            Alumno si existe, None si no
        """
        pass
    
    @abstractmethod
    def listar(self, limite: Optional[int] = None, offset: int = 0) -> List[Alumno]:
        """
        Lista alumnos con paginación.
        
        Args:
            limite: Cantidad máxima de resultados
            offset: Cuántos saltar (para paginación)
        
        Returns:
            Lista de Alumnos
        """
        pass
    
    @abstractmethod
    def actualizar(self, alumno: Alumno) -> Alumno:
        """
        Actualiza un alumno existente.
        
        Args:
            alumno: Alumno con datos actualizados (debe tener id)
        
        Returns:
            Alumno actualizado
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina un alumno por ID.
        
        Args:
            id: ID del alumno a eliminar
        
        Returns:
            True si se eliminó, False si no existía
        """
        pass
    
    @abstractmethod
    def contar(self, cohorte: Optional[int] = None) -> int:
        """
        Cuenta alumnos, opcionalmente filtrados por cohorte.
        
        Args:
            cohorte: Filtrar por año de cohorte
        
        Returns:
            Cantidad de alumnos
        """
        pass
```

### Crear implementación PostgreSQL

`src/infrastructure/repositories/postgres/alumno_repository_postgres.py`:

```python
"""
Repositorio PostgreSQL de Alumnos
Sistema de Seguimiento de Alumnos

Esta clase implementa la interfaz AlumnoRepositoryBase
usando PostgreSQL como base de datos.
"""

from typing import List, Optional
from datetime import datetime

from src.domain.entities.alumno import Alumno
from src.infrastructure.repositories.base.alumno_repository_base import AlumnoRepositoryBase


class AlumnoRepositoryPostgres(AlumnoRepositoryBase):
    """
    Implementación del repositorio de Alumnos usando PostgreSQL.
    
    Recibe una conexión ya establecida (Dependency Injection).
    NO crea la conexión, solo la usa.
    """
    
    def __init__(self, conexion):
        """
        Inicializa el repositorio con una conexión.
        
        Args:
            conexion: Conexión pg8000 a PostgreSQL
        """
        self.conexion = conexion
    
    def _row_to_alumno(self, row: tuple) -> Alumno:
        """
        Convierte una fila de la BD a entidad Alumno.
        
        Método privado (comienza con _) que transforma
        los datos de la BD al objeto de dominio.
        """
        return Alumno(
            id=row[0],
            nombre=row[1],
            apellido=row[2],
            dni=row[3],
            email=row[4],
            cohorte=row[5],
            fecha_creacion=row[6] if len(row) > 6 else None
        )
    
    def crear(self, alumno: Alumno) -> Alumno:
        """Crea un alumno en la BD y retorna con ID asignado"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO alumno (nombre, apellido, dni, email, cohorte, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, fecha_creacion
            """, (
                alumno.nombre,
                alumno.apellido,
                alumno.dni,
                alumno.email,
                alumno.cohorte,
                datetime.now()
            ))
            
            row = cursor.fetchone()
            self.conexion.commit()
            
            alumno.id = row[0]
            alumno.fecha_creacion = row[1]
            return alumno
            
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()
    
    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        """Busca alumno por ID"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre, apellido, dni, email, cohorte, fecha_creacion
                FROM alumno
                WHERE id = %s
            """, (id,))
            
            row = cursor.fetchone()
            self.conexion.commit()
            
            if row:
                return self._row_to_alumno(row)
            return None
            
        finally:
            cursor.close()
    
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """Busca alumno por DNI"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre, apellido, dni, email, cohorte, fecha_creacion
                FROM alumno
                WHERE dni = %s
            """, (dni,))
            
            row = cursor.fetchone()
            self.conexion.commit()
            
            if row:
                return self._row_to_alumno(row)
            return None
            
        finally:
            cursor.close()
    
    def listar(self, limite: Optional[int] = None, offset: int = 0, 
               cohorte: Optional[int] = None, buscar: Optional[str] = None) -> List[Alumno]:
        """Lista alumnos con filtros opcionales"""
        cursor = self.conexion.cursor()
        try:
            # Construcción dinámica de la consulta
            query = """
                SELECT id, nombre, apellido, dni, email, cohorte, fecha_creacion
                FROM alumno
                WHERE 1=1
            """
            params = []
            
            if cohorte:
                query += " AND cohorte = %s"
                params.append(cohorte)
            
            if buscar:
                query += " AND (LOWER(nombre) LIKE %s OR LOWER(apellido) LIKE %s)"
                buscar_like = f"%{buscar.lower()}%"
                params.extend([buscar_like, buscar_like])
            
            query += " ORDER BY apellido, nombre"
            
            if limite:
                query += f" LIMIT {limite} OFFSET {offset}"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            self.conexion.commit()
            
            return [self._row_to_alumno(row) for row in rows]
            
        finally:
            cursor.close()
    
    def actualizar(self, alumno: Alumno) -> Alumno:
        """Actualiza datos de un alumno existente"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute("""
                UPDATE alumno
                SET nombre = %s, apellido = %s, dni = %s, email = %s, cohorte = %s
                WHERE id = %s
                RETURNING id, nombre, apellido, dni, email, cohorte, fecha_creacion
            """, (
                alumno.nombre,
                alumno.apellido,
                alumno.dni,
                alumno.email,
                alumno.cohorte,
                alumno.id
            ))
            
            row = cursor.fetchone()
            self.conexion.commit()
            
            if row:
                return self._row_to_alumno(row)
            return alumno
            
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()
    
    def eliminar(self, id: int) -> bool:
        """Elimina un alumno por ID"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute("DELETE FROM alumno WHERE id = %s", (id,))
            eliminados = cursor.rowcount
            self.conexion.commit()
            return eliminados > 0
            
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()
    
    def contar(self, cohorte: Optional[int] = None) -> int:
        """Cuenta alumnos, filtrados opcionalmente por cohorte"""
        cursor = self.conexion.cursor()
        try:
            if cohorte:
                cursor.execute("SELECT COUNT(*) FROM alumno WHERE cohorte = %s", (cohorte,))
            else:
                cursor.execute("SELECT COUNT(*) FROM alumno")
            
            row = cursor.fetchone()
            self.conexion.commit()
            return row[0] if row else 0
            
        finally:
            cursor.close()
```

## 8.4 Paso 3: Crear el Servicio

`src/application/services/alumno_service.py`:

```python
"""
Servicio de Alumnos - Capa de Aplicación
Sistema de Seguimiento de Alumnos

Este servicio orquesta la lógica de negocio para operaciones con alumnos.
NO sabe de HTTP, bases de datos, o interfaces de usuario.
"""

from typing import List, Optional

from src.domain.entities.alumno import Alumno
from src.domain.exceptions.domain_exceptions import (
    AlumnoNoEncontradoException,
    DNIDuplicadoException
)
from src.infrastructure.repositories.base.alumno_repository_base import AlumnoRepositoryBase


class AlumnoService:
    """
    Servicio de aplicación para operaciones con Alumnos.
    
    Responsabilidades:
    - Validar reglas de negocio
    - Orquestar operaciones
    - Lanzar excepciones de dominio cuando corresponde
    
    NO es responsable de:
    - Conocer cómo se guardan los datos
    - Manejar HTTP o respuestas JSON
    - Validar formato de datos (eso lo hace Pydantic)
    """
    
    def __init__(self, alumno_repo: AlumnoRepositoryBase):
        """
        Inyección de dependencias: el servicio recibe su repositorio.
        
        Args:
            alumno_repo: Repositorio de alumnos (cualquier implementación)
        """
        self.alumno_repo = alumno_repo
    
    def crear_alumno(self, nombre: str, apellido: str, dni: str, 
                      email: str, cohorte: int) -> Alumno:
        """
        Crea un nuevo alumno.
        
        Validaciones:
        1. El DNI no debe existir
        2. Los datos deben ser válidos (la entidad lo valida)
        
        Args:
            nombre, apellido, dni, email, cohorte: datos del alumno
        
        Returns:
            Alumno creado con ID
        
        Raises:
            DNIDuplicadoException: si el DNI ya existe
            ValueError: si los datos son inválidos
        """
        # 1. Verificar que el DNI no exista
        existente = self.alumno_repo.obtener_por_dni(dni)
        if existente:
            raise DNIDuplicadoException(dni)
        
        # 2. Crear entidad (esto valida los datos)
        alumno = Alumno(
            id=None,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            cohorte=cohorte
        )
        
        # 3. Persistir
        return self.alumno_repo.crear(alumno)
    
    def obtener_alumno(self, alumno_id: int) -> Alumno:
        """
        Obtiene un alumno por ID.
        
        Raises:
            AlumnoNoEncontradoException: si no existe
        """
        alumno = self.alumno_repo.obtener_por_id(alumno_id)
        if not alumno:
            raise AlumnoNoEncontradoException(alumno_id)
        return alumno
    
    def listar_alumnos(self, limite: Optional[int] = None, offset: int = 0,
                        cohorte: Optional[int] = None, buscar: Optional[str] = None) -> List[Alumno]:
        """
        Lista alumnos con filtros opcionales.
        """
        return self.alumno_repo.listar(
            limite=limite, 
            offset=offset,
            cohorte=cohorte,
            buscar=buscar
        )
    
    def actualizar_alumno(self, alumno_id: int, nombre: Optional[str] = None,
                           apellido: Optional[str] = None, dni: Optional[str] = None,
                           email: Optional[str] = None, cohorte: Optional[int] = None) -> Alumno:
        """
        Actualiza un alumno existente.
        Solo actualiza los campos proporcionados (no None).
        """
        # 1. Obtener alumno actual
        alumno = self.obtener_alumno(alumno_id)  # Lanza excepción si no existe
        
        # 2. Si cambia el DNI, verificar que no exista
        if dni and dni != alumno.dni:
            existente = self.alumno_repo.obtener_por_dni(dni)
            if existente:
                raise DNIDuplicadoException(dni)
        
        # 3. Actualizar campos (solo los que vienen)
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
        
        # 4. Persistir
        return self.alumno_repo.actualizar(alumno)
    
    def eliminar_alumno(self, alumno_id: int) -> bool:
        """Elimina un alumno por ID."""
        return self.alumno_repo.eliminar(alumno_id)
    
    def contar_alumnos(self, cohorte: Optional[int] = None) -> int:
        """Cuenta alumnos, opcionalmente filtrados por cohorte."""
        return self.alumno_repo.contar(cohorte)
```

## 8.5 Paso 4: Crear el Router

### Crear Schemas

`src/presentation/api/schemas/alumno_schema.py`:

```python
"""
Schemas Pydantic para Alumnos
Sistema de Seguimiento de Alumnos

Los schemas definen la FORMA de los datos que entran y salen de la API.
Pydantic valida automáticamente los tipos y formatos.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

from src.domain.entities.alumno import Alumno


class AlumnoCreateSchema(BaseModel):
    """
    Schema para crear un alumno (entrada).
    
    Define qué campos debe enviar el cliente.
    Pydantic valida automáticamente:
    - Tipos de datos
    - Campos requeridos vs opcionales
    - Formatos especiales (EmailStr verifica formato de email)
    - Rangos (Field con ge/le para cohorte)
    """
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del alumno")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del alumno")
    dni: str = Field(..., min_length=1, max_length=20, description="DNI único")
    email: EmailStr = Field(..., description="Email válido")
    cohorte: int = Field(..., ge=2000, le=2100, description="Año de ingreso")


class AlumnoUpdateSchema(BaseModel):
    """
    Schema para actualizar un alumno.
    
    Todos los campos son opcionales porque puede ser
    una actualización parcial.
    """
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    dni: Optional[str] = Field(None, min_length=1, max_length=20)
    email: Optional[EmailStr] = None
    cohorte: Optional[int] = Field(None, ge=2000, le=2100)


class AlumnoResponseSchema(BaseModel):
    """
    Schema para devolver datos de un alumno (salida).
    
    Incluye campos calculados como nombre_completo.
    """
    id: int
    nombre: str
    apellido: str
    dni: str
    email: str
    cohorte: int
    nombre_completo: str
    fecha_creacion: Optional[str] = None
    
    @classmethod
    def from_entity(cls, alumno: Alumno) -> 'AlumnoResponseSchema':
        """
        Factory method para crear el schema desde la entidad.
        
        Esto evita duplicar la lógica de conversión en cada endpoint.
        """
        return cls(
            id=alumno.id,
            nombre=alumno.nombre,
            apellido=alumno.apellido,
            dni=alumno.dni,
            email=alumno.email,
            cohorte=alumno.cohorte,
            nombre_completo=alumno.nombre_completo,
            fecha_creacion=alumno.fecha_creacion.isoformat() if alumno.fecha_creacion else None
        )


class AlumnoListResponseSchema(BaseModel):
    """Schema para listar alumnos con paginación."""
    total: int = Field(..., description="Total de alumnos")
    limite: Optional[int] = Field(None, description="Límite aplicado")
    offset: int = Field(0, description="Offset aplicado")
    alumnos: List[AlumnoResponseSchema]
```

### Crear Router

`src/presentation/api/routers/alumnos.py`:

```python
"""
Router de Alumnos - Capa de Presentación
Sistema de Seguimiento de Alumnos

Este router define los endpoints HTTP para alumnos.
Solo se encarga de:
- Recibir requests HTTP
- Delegar al servicio
- Retornar responses HTTP
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from src.application.services.alumno_service import AlumnoService
from src.presentation.api.schemas.alumno_schema import (
    AlumnoCreateSchema,
    AlumnoUpdateSchema,
    AlumnoResponseSchema,
    AlumnoListResponseSchema
)
from src.domain.exceptions.domain_exceptions import (
    AlumnoNoEncontradoException,
    DNIDuplicadoException
)


# Crear router con prefijo y tags
router = APIRouter(
    prefix="/alumnos",
    tags=["Alumnos"],
    responses={
        404: {"description": "Alumno no encontrado"},
        409: {"description": "DNI duplicado"}
    }
)


def get_alumno_service() -> AlumnoService:
    """
    Función de inyección de dependencias.
    
    FastAPI llama a esta función para obtener el servicio.
    Aquí creamos la cadena de dependencias:
    Conexión → Repositorio → Servicio
    """
    from src.infrastructure.database.connection import get_db_connection
    from src.infrastructure.repositories.postgres.alumno_repository_postgres import AlumnoRepositoryPostgres
    
    conexion = get_db_connection()
    alumno_repo = AlumnoRepositoryPostgres(conexion)
    return AlumnoService(alumno_repo)


@router.post(
    "/",
    response_model=AlumnoResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo alumno"
)
def crear_alumno(
    alumno_data: AlumnoCreateSchema,
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """
    Crea un nuevo alumno en el sistema.
    
    - **nombre**: Nombre del alumno
    - **apellido**: Apellido del alumno
    - **dni**: DNI único
    - **email**: Email válido
    - **cohorte**: Año de ingreso (2000-2100)
    """
    try:
        alumno = alumno_service.crear_alumno(
            nombre=alumno_data.nombre,
            apellido=alumno_data.apellido,
            dni=alumno_data.dni,
            email=alumno_data.email,
            cohorte=alumno_data.cohorte
        )
        return AlumnoResponseSchema.from_entity(alumno)
    
    except DNIDuplicadoException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/{alumno_id}",
    response_model=AlumnoResponseSchema,
    summary="Obtener un alumno por ID"
)
def obtener_alumno(
    alumno_id: int,
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """Obtiene los datos de un alumno específico."""
    try:
        alumno = alumno_service.obtener_alumno(alumno_id)
        return AlumnoResponseSchema.from_entity(alumno)
    
    except AlumnoNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=AlumnoListResponseSchema,
    summary="Listar alumnos"
)
def listar_alumnos(
    limite: Optional[int] = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    cohorte: Optional[int] = Query(None, ge=2000, le=2100),
    buscar: Optional[str] = Query(None, min_length=1),
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """
    Lista alumnos con filtros y paginación.
    
    - **limite**: Cantidad máxima (1-100)
    - **offset**: Cuántos saltar
    - **cohorte**: Filtrar por año
    - **buscar**: Buscar por nombre/apellido
    """
    alumnos = alumno_service.listar_alumnos(
        limite=limite,
        offset=offset,
        cohorte=cohorte,
        buscar=buscar
    )
    total = alumno_service.contar_alumnos(cohorte=cohorte)
    
    return AlumnoListResponseSchema(
        total=total,
        limite=limite,
        offset=offset,
        alumnos=[AlumnoResponseSchema.from_entity(a) for a in alumnos]
    )


@router.put(
    "/{alumno_id}",
    response_model=AlumnoResponseSchema,
    summary="Actualizar un alumno"
)
def actualizar_alumno(
    alumno_id: int,
    alumno_data: AlumnoUpdateSchema,
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """Actualiza los datos de un alumno existente."""
    try:
        alumno = alumno_service.actualizar_alumno(
            alumno_id=alumno_id,
            nombre=alumno_data.nombre,
            apellido=alumno_data.apellido,
            dni=alumno_data.dni,
            email=alumno_data.email,
            cohorte=alumno_data.cohorte
        )
        return AlumnoResponseSchema.from_entity(alumno)
    
    except AlumnoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DNIDuplicadoException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete(
    "/{alumno_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un alumno"
)
def eliminar_alumno(
    alumno_id: int,
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """Elimina un alumno del sistema."""
    eliminado = alumno_service.eliminar_alumno(alumno_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe alumno con ID {alumno_id}"
        )
    return None
```

## 8.6 Paso 5: Crear la Aplicación FastAPI

`src/presentation/api/main.py` (versión simplificada inicial):

```python
"""
Aplicación Principal FastAPI
Sistema de Seguimiento de Alumnos
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.presentation.api.routers import alumnos

# Crear aplicación
app = FastAPI(
    title="Sistema de Seguimiento de Alumnos",
    description="API para gestión de alumnos en instituciones educativas",
    version="1.0.0"
)

# Configurar CORS (permite requests desde cualquier origen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(alumnos.router, prefix="/api")

# Servir archivos estáticos (frontend) en desarrollo
if not os.environ.get("VERCEL"):
    try:
        app.mount("/", StaticFiles(directory="public", html=True), name="public")
    except:
        pass

# Health check
@app.get("/api", tags=["Health"])
def root():
    return {"message": "API funcionando", "version": "1.0.0"}
```

## 8.7 Paso 6: Probar con Swagger

1. Ejecutar el servidor:
   ```bash
   .\run_local.bat
   ```

2. Abrir http://localhost:8000/docs

3. Probar endpoints:
   - POST /api/alumnos/ → Crear alumno
   - GET /api/alumnos/ → Listar
   - GET /api/alumnos/{id} → Obtener uno
   - PUT /api/alumnos/{id} → Actualizar
   - DELETE /api/alumnos/{id} → Eliminar

## 8.8 Resumen del Proceso

```
1. DOMINIO
   └── Crear entidad con validaciones
   
2. INFRAESTRUCTURA
   ├── Crear interfaz del repositorio
   └── Implementar para PostgreSQL
   
3. APLICACIÓN
   └── Crear servicio con lógica de negocio
   
4. PRESENTACIÓN
   ├── Crear schemas Pydantic
   ├── Crear router con endpoints
   └── Registrar en main.py
   
5. PROBAR
   └── Verificar en Swagger UI
```

Este proceso se repite para cada entidad: Curso, Clase, Asistencia, TP, etc.

---

**Capítulo anterior**: [Instalación del Entorno](./07_instalacion_entorno.md)

**Siguiente capítulo**: [Código Base Completo](./09_codigo_base.md)
