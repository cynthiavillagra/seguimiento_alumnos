# Capítulo 4: Capa de Dominio

## 4.1 ¿Qué es la Capa de Dominio?

Es el **corazón** de tu aplicación. Contiene:

- **Entidades:** Las "cosas" del negocio (Alumno, Curso)
- **Excepciones:** Errores de negocio (DNI duplicado, no encontrado)
- **Reglas:** Validaciones que siempre deben cumplirse

### Características

- ✅ Python puro (sin frameworks)
- ✅ No sabe de HTTP ni SQL
- ✅ Fácil de testear
- ✅ Reutilizable

---

## 4.2 Entidad Alumno

Crear `src/domain/entities/alumno.py`:

```python
"""
Entidad Alumno
--------------
Representa un alumno en el sistema.

Esta clase:
- Define qué datos tiene un alumno
- Contiene validaciones de negocio
- No sabe de base de datos ni HTTP
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Alumno:
    """
    Entidad que representa un estudiante.
    
    Usamos @dataclass para que Python genere automáticamente:
    - __init__()  -> constructor
    - __repr__()  -> representación para debug
    - __eq__()    -> comparación entre objetos
    """
    
    # Campos de la entidad
    id: Optional[int]      # None si es nuevo, número si ya existe
    nombre: str
    apellido: str
    dni: str
    email: str
    
    def __post_init__(self):
        """
        Se ejecuta después del __init__.
        Usamos esto para validaciones.
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
        
        # Validar email (básico)
        if not self.email or '@' not in self.email:
            raise ValueError("El email debe contener @")
        
        # Limpiar espacios
        self.nombre = self.nombre.strip()
        self.apellido = self.apellido.strip()
        self.dni = self.dni.strip()
        self.email = self.email.strip()
    
    @property
    def nombre_completo(self) -> str:
        """
        Propiedad calculada: "Apellido, Nombre"
        
        @property permite acceder como alumno.nombre_completo
        en lugar de alumno.nombre_completo()
        """
        return f"{self.apellido}, {self.nombre}"
```

### ¿Qué aprendimos?

| Concepto | Explicación |
|----------|-------------|
| `@dataclass` | Genera código automáticamente (init, repr, eq) |
| `Optional[int]` | Puede ser `int` o `None` |
| `__post_init__` | Se ejecuta después del constructor |
| `@property` | Campo calculado que parece atributo |

### Probar la entidad

```python
# En una terminal de Python
from src.domain.entities.alumno import Alumno

# Crear alumno válido
alumno = Alumno(
    id=None,
    nombre="Juan",
    apellido="Pérez",
    dni="12345678",
    email="juan@mail.com"
)

print(alumno.nombre_completo)  # "Pérez, Juan"

# Intentar crear con nombre vacío (falla)
try:
    Alumno(id=None, nombre="", apellido="Test", dni="123", email="a@b.com")
except ValueError as e:
    print(f"Error esperado: {e}")
```

---

## 4.3 Entidad Curso

Crear `src/domain/entities/curso.py`:

```python
"""
Entidad Curso
--------------
Representa una materia/curso en un cuatrimestre.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Curso:
    """
    Entidad que representa un curso/materia.
    """
    
    id: Optional[int]
    nombre_materia: str
    anio: int
    cuatrimestre: int  # 1 o 2
    
    def __post_init__(self):
        """Validaciones de negocio"""
        
        # Validar nombre de materia
        if not self.nombre_materia or not self.nombre_materia.strip():
            raise ValueError("El nombre de la materia no puede estar vacío")
        
        # Validar cuatrimestre
        if self.cuatrimestre not in [1, 2]:
            raise ValueError("El cuatrimestre debe ser 1 o 2")
        
        # Validar año
        if self.anio < 2000 or self.anio > 2100:
            raise ValueError("El año debe estar entre 2000 y 2100")
        
        # Limpiar
        self.nombre_materia = self.nombre_materia.strip()
    
    @property
    def nombre_completo(self) -> str:
        """Ej: 'Programación I - 1C2024'"""
        return f"{self.nombre_materia} - {self.cuatrimestre}C{self.anio}"
```

---

## 4.4 Entidad Inscripción

Crear `src/domain/entities/inscripcion.py`:

```python
"""
Entidad Inscripción
-------------------
Representa la inscripción de un alumno en un curso.
Es la relación N:M entre Alumno y Curso.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Inscripcion:
    """
    Entidad que representa una inscripción.
    """
    
    id: Optional[int]
    alumno_id: int
    curso_id: int
    fecha_inscripcion: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones"""
        if not self.alumno_id or self.alumno_id < 1:
            raise ValueError("alumno_id debe ser un número positivo")
        
        if not self.curso_id or self.curso_id < 1:
            raise ValueError("curso_id debe ser un número positivo")
```

---

## 4.5 Excepciones de Dominio

Crear `src/domain/exceptions/exceptions.py`:

```python
"""
Excepciones de Dominio
----------------------
Errores de NEGOCIO, no errores técnicos.

¿Por qué crear excepciones propias?
- Son más descriptivas que Exception genérico
- Permiten manejar errores específicos
- Documentan qué puede fallar
"""


class DomainException(Exception):
    """Clase base para excepciones de dominio"""
    pass


class AlumnoNoEncontradoException(DomainException):
    """
    Se lanza cuando buscamos un alumno que no existe.
    
    Ejemplo de uso:
        raise AlumnoNoEncontradoException(123)
        # Mensaje: "No se encontró alumno con ID 123"
    """
    def __init__(self, alumno_id: int):
        self.alumno_id = alumno_id
        super().__init__(f"No se encontró alumno con ID {alumno_id}")


class DNIDuplicadoException(DomainException):
    """
    Se lanza cuando intentamos crear un alumno con DNI existente.
    
    Ejemplo:
        raise DNIDuplicadoException("12345678")
    """
    def __init__(self, dni: str):
        self.dni = dni
        super().__init__(f"Ya existe un alumno con DNI {dni}")


class CursoNoEncontradoException(DomainException):
    """Se lanza cuando buscamos un curso que no existe."""
    def __init__(self, curso_id: int):
        self.curso_id = curso_id
        super().__init__(f"No se encontró curso con ID {curso_id}")


class InscripcionDuplicadaException(DomainException):
    """Se lanza cuando un alumno ya está inscripto en un curso."""
    def __init__(self, alumno_id: int, curso_id: int):
        self.alumno_id = alumno_id
        self.curso_id = curso_id
        super().__init__(
            f"El alumno {alumno_id} ya está inscripto en el curso {curso_id}"
        )
```

### ¿Por qué excepciones propias?

```python
# ❌ MAL: Excepción genérica
raise Exception("Alumno no encontrado")

# ¿Cómo sé qué tipo de error es?
# ¿Cómo manejo este error específico?

# ✅ BIEN: Excepción específica
raise AlumnoNoEncontradoException(123)

# Puedo manejar errores específicos:
try:
    alumno = service.obtener(123)
except AlumnoNoEncontradoException:
    return {"error": "No existe"}, 404
except DNIDuplicadoException:
    return {"error": "DNI ya existe"}, 409
```

---

## 4.6 Actualizar __init__.py

Para poder importar fácilmente, actualizar los `__init__.py`:

`src/domain/entities/__init__.py`:

```python
"""Exportar entidades del dominio"""
from .alumno import Alumno
from .curso import Curso
from .inscripcion import Inscripcion
```

`src/domain/exceptions/__init__.py`:

```python
"""Exportar excepciones del dominio"""
from .exceptions import (
    DomainException,
    AlumnoNoEncontradoException,
    DNIDuplicadoException,
    CursoNoEncontradoException,
    InscripcionDuplicadaException
)
```

---

## 4.7 Probar las Entidades

Crear `tests/test_dominio.py`:

```python
"""Tests de la capa de dominio"""
import pytest
from src.domain.entities import Alumno, Curso


class TestAlumno:
    """Tests para la entidad Alumno"""
    
    def test_crear_alumno_valido(self):
        """Debe crear un alumno con datos válidos"""
        alumno = Alumno(
            id=None,
            nombre="María",
            apellido="García",
            dni="12345678",
            email="maria@test.com"
        )
        
        assert alumno.nombre == "María"
        assert alumno.nombre_completo == "García, María"
    
    def test_limpiar_espacios(self):
        """Debe limpiar espacios en nombre y apellido"""
        alumno = Alumno(
            id=None,
            nombre="  Juan  ",
            apellido="  Pérez  ",
            dni="11111111",
            email="juan@test.com"
        )
        
        assert alumno.nombre == "Juan"
        assert alumno.apellido == "Pérez"
    
    def test_nombre_vacio_falla(self):
        """Debe fallar si el nombre está vacío"""
        with pytest.raises(ValueError) as exc:
            Alumno(
                id=None,
                nombre="",
                apellido="Test",
                dni="12345678",
                email="test@test.com"
            )
        
        assert "nombre" in str(exc.value).lower()
    
    def test_email_sin_arroba_falla(self):
        """Debe fallar si el email no tiene @"""
        with pytest.raises(ValueError) as exc:
            Alumno(
                id=None,
                nombre="Juan",
                apellido="Test",
                dni="12345678",
                email="emailinvalido"
            )
        
        assert "email" in str(exc.value).lower()


class TestCurso:
    """Tests para la entidad Curso"""
    
    def test_crear_curso_valido(self):
        """Debe crear un curso válido"""
        curso = Curso(
            id=None,
            nombre_materia="Programación I",
            anio=2024,
            cuatrimestre=1
        )
        
        assert curso.nombre_materia == "Programación I"
        assert curso.nombre_completo == "Programación I - 1C2024"
    
    def test_cuatrimestre_invalido(self):
        """Debe fallar con cuatrimestre 3"""
        with pytest.raises(ValueError) as exc:
            Curso(
                id=None,
                nombre_materia="Test",
                anio=2024,
                cuatrimestre=3
            )
        
        assert "cuatrimestre" in str(exc.value).lower()
```

Ejecutar tests:

```powershell
pip install pytest
pytest tests/test_dominio.py -v
```

Resultado esperado:

```
tests/test_dominio.py::TestAlumno::test_crear_alumno_valido PASSED
tests/test_dominio.py::TestAlumno::test_limpiar_espacios PASSED
tests/test_dominio.py::TestAlumno::test_nombre_vacio_falla PASSED
tests/test_dominio.py::TestAlumno::test_email_sin_arroba_falla PASSED
tests/test_dominio.py::TestCurso::test_crear_curso_valido PASSED
tests/test_dominio.py::TestCurso::test_cuatrimestre_invalido PASSED

6 passed
```

---

## 4.8 Resumen

### Archivos creados

```
src/domain/
├── entities/
│   ├── __init__.py
│   ├── alumno.py        ✅
│   ├── curso.py         ✅
│   └── inscripcion.py   ✅
└── exceptions/
    ├── __init__.py
    └── exceptions.py    ✅
```

### Qué aprendiste

| Concepto | Explicación |
|----------|-------------|
| `@dataclass` | Genera constructor y otros métodos automáticamente |
| `__post_init__` | Ejecutar validaciones después de crear objeto |
| `@property` | Campos calculados que parecen atributos |
| Excepciones propias | Errores de negocio específicos |
| Tests | Verificar que las validaciones funcionan |

---

**Anterior:** [Capítulo 3 - Setup](./03_setup.md)

**Siguiente:** [Capítulo 5 - Infraestructura](./05_infraestructura.md)
