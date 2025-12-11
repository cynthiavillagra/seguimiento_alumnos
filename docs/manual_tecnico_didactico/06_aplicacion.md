# Capítulo 6: Capa de Aplicación

## 6.1 ¿Qué es la Capa de Aplicación?

Es donde vive la **lógica de negocio**. Los "Servicios" orquestan operaciones.

### Responsabilidades

- ✅ Validar reglas de negocio (ej: DNI no duplicado)
- ✅ Orquestar operaciones (ej: crear y luego inscribir)
- ✅ Lanzar excepciones de dominio
- ✅ Usar repositorios para acceder a datos

### Lo que NO hace

- ❌ No sabe de HTTP ni JSON
- ❌ No sabe de SQL
- ❌ No valida formato de datos (eso lo hace Pydantic)

---

## 6.2 Servicio de Alumnos

Crear `src/application/services/alumno_service.py`:

```python
"""
Servicio de Alumnos
-------------------
Contiene la lógica de negocio para operaciones con alumnos.

Este servicio:
- Recibe datos limpios (ya validados por Pydantic)
- Aplica reglas de negocio
- Usa el repositorio para persistir
- Lanza excepciones de dominio cuando corresponde
"""

from typing import List, Optional

from src.domain.entities import Alumno
from src.domain.exceptions import (
    AlumnoNoEncontradoException,
    DNIDuplicadoException
)
from src.infrastructure.repositories import AlumnoRepository


class AlumnoService:
    """
    Servicio de aplicación para Alumnos.
    
    Ejemplo de uso:
        service = AlumnoService()
        alumno = service.crear("Juan", "Pérez", "12345678", "juan@mail.com")
    """
    
    def __init__(self, repo: AlumnoRepository = None):
        """
        Inicializa el servicio.
        
        Args:
            repo: Repositorio de alumnos. Si no se pasa, crea uno.
                  Esto permite inyectar un mock para tests.
        """
        self.repo = repo or AlumnoRepository()
    
    def crear(self, nombre: str, apellido: str, dni: str, email: str) -> Alumno:
        """
        Crea un nuevo alumno.
        
        Args:
            nombre, apellido, dni, email: datos del alumno
        
        Returns:
            Alumno creado con ID
        
        Raises:
            DNIDuplicadoException: si el DNI ya existe
            ValueError: si los datos son inválidos
        """
        # 1. Verificar que el DNI no exista
        existente = self.repo.obtener_por_dni(dni)
        if existente:
            raise DNIDuplicadoException(dni)
        
        # 2. Crear entidad (esto valida los datos)
        alumno = Alumno(
            id=None,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email
        )
        
        # 3. Guardar
        return self.repo.guardar(alumno)
    
    def obtener(self, alumno_id: int) -> Alumno:
        """
        Obtiene un alumno por ID.
        
        Raises:
            AlumnoNoEncontradoException: si no existe
        """
        alumno = self.repo.obtener_por_id(alumno_id)
        
        if not alumno:
            raise AlumnoNoEncontradoException(alumno_id)
        
        return alumno
    
    def listar(self, limite: int = 100) -> List[Alumno]:
        """Lista todos los alumnos."""
        return self.repo.listar(limite)
    
    def actualizar(
        self,
        alumno_id: int,
        nombre: Optional[str] = None,
        apellido: Optional[str] = None,
        dni: Optional[str] = None,
        email: Optional[str] = None
    ) -> Alumno:
        """
        Actualiza un alumno existente.
        
        Solo actualiza los campos que se pasan (no None).
        """
        # 1. Obtener alumno actual
        alumno = self.obtener(alumno_id)  # Lanza excepción si no existe
        
        # 2. Si cambia el DNI, verificar que no exista
        if dni and dni != alumno.dni:
            existente = self.repo.obtener_por_dni(dni)
            if existente:
                raise DNIDuplicadoException(dni)
        
        # 3. Actualizar solo los campos que vienen
        if nombre is not None:
            alumno.nombre = nombre
        if apellido is not None:
            alumno.apellido = apellido
        if dni is not None:
            alumno.dni = dni
        if email is not None:
            alumno.email = email
        
        # 4. Guardar
        return self.repo.actualizar(alumno)
    
    def eliminar(self, alumno_id: int) -> bool:
        """Elimina un alumno por ID."""
        return self.repo.eliminar(alumno_id)
    
    def contar(self) -> int:
        """Cuenta el total de alumnos."""
        return self.repo.contar()
```

### El flujo de crear

```
1. service.crear("Juan", "Pérez", "12345678", "juan@mail.com")
   │
   ├─► 2. ¿El DNI ya existe?
   │       repo.obtener_por_dni("12345678")
   │       │
   │       ├── SÍ existe → raise DNIDuplicadoException
   │       └── NO existe → continuar
   │
   ├─► 3. Crear entidad Alumno
   │       Alumno(nombre="Juan", ...)
   │       (las validaciones se ejecutan aquí)
   │
   └─► 4. Guardar en BD
           repo.guardar(alumno)
           │
           └── return alumno_con_id
```

---

## 6.3 Servicio de Cursos

Crear `src/application/services/curso_service.py`:

```python
"""
Servicio de Cursos
------------------
Lógica de negocio para operaciones con cursos.
"""

from typing import List, Optional

from src.domain.entities import Curso
from src.domain.exceptions import CursoNoEncontradoException
from src.infrastructure.repositories import CursoRepository


class CursoService:
    """Servicio de aplicación para Cursos."""
    
    def __init__(self, repo: CursoRepository = None):
        self.repo = repo or CursoRepository()
    
    def crear(
        self,
        nombre_materia: str,
        anio: int,
        cuatrimestre: int
    ) -> Curso:
        """Crea un nuevo curso."""
        
        # Crear entidad (valida datos)
        curso = Curso(
            id=None,
            nombre_materia=nombre_materia,
            anio=anio,
            cuatrimestre=cuatrimestre
        )
        
        # Guardar
        return self.repo.guardar(curso)
    
    def obtener(self, curso_id: int) -> Curso:
        """
        Obtiene un curso por ID.
        
        Raises:
            CursoNoEncontradoException: si no existe
        """
        curso = self.repo.obtener_por_id(curso_id)
        
        if not curso:
            raise CursoNoEncontradoException(curso_id)
        
        return curso
    
    def listar(self, limite: int = 100) -> List[Curso]:
        """Lista todos los cursos."""
        return self.repo.listar(limite)
    
    def actualizar(
        self,
        curso_id: int,
        nombre_materia: Optional[str] = None,
        anio: Optional[int] = None,
        cuatrimestre: Optional[int] = None
    ) -> Curso:
        """Actualiza un curso existente."""
        
        # Obtener actual
        curso = self.obtener(curso_id)
        
        # Actualizar campos
        if nombre_materia is not None:
            curso.nombre_materia = nombre_materia
        if anio is not None:
            curso.anio = anio
        if cuatrimestre is not None:
            curso.cuatrimestre = cuatrimestre
        
        return self.repo.actualizar(curso)
    
    def eliminar(self, curso_id: int) -> bool:
        """Elimina un curso por ID."""
        return self.repo.eliminar(curso_id)
    
    def contar(self) -> int:
        """Cuenta el total de cursos."""
        return self.repo.contar()
```

---

## 6.4 Servicio de Inscripciones

Crear `src/application/services/inscripcion_service.py`:

```python
"""
Servicio de Inscripciones
-------------------------
Maneja la lógica de inscribir alumnos a cursos.
"""

from typing import List

from src.domain.entities import Alumno, Inscripcion
from src.domain.exceptions import (
    AlumnoNoEncontradoException,
    CursoNoEncontradoException,
    InscripcionDuplicadaException
)
from src.infrastructure.repositories import (
    InscripcionRepository,
    AlumnoRepository,
    CursoRepository
)


class InscripcionService:
    """Servicio para operaciones de inscripción."""
    
    def __init__(
        self,
        inscripcion_repo: InscripcionRepository = None,
        alumno_repo: AlumnoRepository = None,
        curso_repo: CursoRepository = None
    ):
        self.inscripcion_repo = inscripcion_repo or InscripcionRepository()
        self.alumno_repo = alumno_repo or AlumnoRepository()
        self.curso_repo = curso_repo or CursoRepository()
    
    def inscribir(self, alumno_id: int, curso_id: int) -> Inscripcion:
        """
        Inscribe un alumno en un curso.
        
        Args:
            alumno_id: ID del alumno
            curso_id: ID del curso
        
        Returns:
            Inscripción creada
        
        Raises:
            AlumnoNoEncontradoException: si el alumno no existe
            CursoNoEncontradoException: si el curso no existe
            InscripcionDuplicadaException: si ya está inscripto
        """
        # 1. Verificar que el alumno existe
        alumno = self.alumno_repo.obtener_por_id(alumno_id)
        if not alumno:
            raise AlumnoNoEncontradoException(alumno_id)
        
        # 2. Verificar que el curso existe
        curso = self.curso_repo.obtener_por_id(curso_id)
        if not curso:
            raise CursoNoEncontradoException(curso_id)
        
        # 3. Verificar que no esté ya inscripto
        if self.inscripcion_repo.ya_inscripto(alumno_id, curso_id):
            raise InscripcionDuplicadaException(alumno_id, curso_id)
        
        # 4. Inscribir
        return self.inscripcion_repo.inscribir(alumno_id, curso_id)
    
    def alumnos_de_curso(self, curso_id: int) -> List[Alumno]:
        """
        Obtiene los alumnos inscriptos en un curso.
        
        Raises:
            CursoNoEncontradoException: si el curso no existe
        """
        # Verificar que el curso existe
        curso = self.curso_repo.obtener_por_id(curso_id)
        if not curso:
            raise CursoNoEncontradoException(curso_id)
        
        return self.inscripcion_repo.alumnos_de_curso(curso_id)
    
    def desinscribir(self, alumno_id: int, curso_id: int) -> bool:
        """Elimina la inscripción de un alumno en un curso."""
        return self.inscripcion_repo.desinscribir(alumno_id, curso_id)
```

---

## 6.5 Actualizar __init__.py

`src/application/services/__init__.py`:

```python
"""Exportar servicios"""
from .alumno_service import AlumnoService
from .curso_service import CursoService
from .inscripcion_service import InscripcionService
```

---

## 6.6 Por qué los Servicios son Importantes

### Comparación

```python
# ❌ SIN servicio: lógica en el router
@router.post("/alumnos")
def crear_alumno(data: AlumnoSchema):
    # Verificar DNI
    repo = AlumnoRepository()
    if repo.obtener_por_dni(data.dni):
        raise HTTPException(409, "DNI duplicado")
    
    # Crear entidad
    alumno = Alumno(id=None, nombre=data.nombre, ...)
    
    # Guardar
    return repo.guardar(alumno)

# ¿Problemas?
# - El router hace demasiado
# - Difícil de testear
# - Código repetido si otro endpoint necesita crear alumnos


# ✅ CON servicio: router solo maneja HTTP
@router.post("/alumnos")
def crear_alumno(data: AlumnoSchema):
    try:
        return service.crear(data.nombre, data.apellido, data.dni, data.email)
    except DNIDuplicadoException:
        raise HTTPException(409, "DNI duplicado")

# Beneficios:
# - Router solo maneja HTTP
# - Servicio es fácil de testear
# - Lógica reutilizable
```

---

## 6.7 Probar los Servicios

Crear `tests/test_servicios.py`:

```python
"""Tests de la capa de aplicación"""
import pytest
from src.application.services import AlumnoService, CursoService
from src.domain.exceptions import DNIDuplicadoException, AlumnoNoEncontradoException


class MockAlumnoRepository:
    """
    Repositorio falso para tests.
    No usa base de datos real.
    """
    
    def __init__(self):
        self._alumnos = {}
        self._next_id = 1
    
    def guardar(self, alumno):
        alumno.id = self._next_id
        self._alumnos[self._next_id] = alumno
        self._next_id += 1
        return alumno
    
    def obtener_por_id(self, id):
        return self._alumnos.get(id)
    
    def obtener_por_dni(self, dni):
        for a in self._alumnos.values():
            if a.dni == dni:
                return a
        return None
    
    def listar(self, limite=100):
        return list(self._alumnos.values())[:limite]
    
    def actualizar(self, alumno):
        self._alumnos[alumno.id] = alumno
        return alumno
    
    def eliminar(self, id):
        if id in self._alumnos:
            del self._alumnos[id]
            return True
        return False
    
    def contar(self):
        return len(self._alumnos)


class TestAlumnoService:
    """Tests para AlumnoService"""
    
    def test_crear_alumno_exitoso(self):
        """Debe crear un alumno correctamente"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        alumno = service.crear("Juan", "Pérez", "12345678", "juan@mail.com")
        
        assert alumno.id == 1
        assert alumno.nombre == "Juan"
        assert alumno.nombre_completo == "Pérez, Juan"
    
    def test_crear_dni_duplicado_falla(self):
        """Debe fallar si el DNI ya existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        # Crear primer alumno
        service.crear("Juan", "Pérez", "12345678", "juan@mail.com")
        
        # Intentar con mismo DNI
        with pytest.raises(DNIDuplicadoException) as exc:
            service.crear("Otro", "Usuario", "12345678", "otro@mail.com")
        
        assert "12345678" in str(exc.value)
    
    def test_obtener_existente(self):
        """Debe retornar alumno si existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        creado = service.crear("María", "García", "11111111", "maria@mail.com")
        obtenido = service.obtener(creado.id)
        
        assert obtenido.id == creado.id
        assert obtenido.nombre == "María"
    
    def test_obtener_no_existente_falla(self):
        """Debe fallar si el alumno no existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        with pytest.raises(AlumnoNoEncontradoException):
            service.obtener(999)
    
    def test_actualizar_parcial(self):
        """Debe actualizar solo los campos que vienen"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        alumno = service.crear("Juan", "Pérez", "12345678", "juan@mail.com")
        
        # Solo actualizar nombre
        actualizado = service.actualizar(alumno.id, nombre="Juan Carlos")
        
        assert actualizado.nombre == "Juan Carlos"
        assert actualizado.apellido == "Pérez"  # No cambió
```

Ejecutar:

```powershell
pytest tests/test_servicios.py -v
```

---

## 6.8 Resumen

### Archivos creados

```
src/application/
└── services/
    ├── __init__.py
    ├── alumno_service.py     ✅
    ├── curso_service.py      ✅
    └── inscripcion_service.py ✅
```

### Qué aprendiste

| Concepto | Explicación |
|----------|-------------|
| Service | Clase que orquesta lógica de negocio |
| Dependency Injection | Pasar el repo desde afuera |
| Mock | Objeto falso para tests |
| Single Responsibility | El servicio solo hace lógica de negocio |

### Responsabilidades de cada capa (hasta ahora)

| Capa | Responsabilidad |
|------|-----------------|
| **Dominio** | Qué es un Alumno/Curso, validaciones básicas |
| **Infraestructura** | Guardar/recuperar de PostgreSQL |
| **Aplicación** | Reglas de negocio (DNI único, etc.) |
| **Presentación** | (próximo capítulo) |

---

**Anterior:** [Capítulo 5 - Infraestructura](./05_infraestructura.md)

**Siguiente:** [Capítulo 7 - Presentación](./07_presentacion.md)
