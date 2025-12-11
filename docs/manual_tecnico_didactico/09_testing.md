# Capítulo 9: Testing

## 9.1 ¿Por qué Testear?

Porque queremos **confianza** de que el código funciona.

```
Sin tests:
❌ "Creo que funciona..."
❌ "No sé si rompí algo..."
❌ Miedo a hacer cambios

Con tests:
✅ "Sé que funciona, los tests pasan"
✅ "Si rompo algo, un test falla"
✅ Confianza para refactorizar
```

---

## 9.2 Tipos de Tests

```
      ▲
     /│\    E2E (pocos)
    / │ \   Prueban flujo completo
   /──┼──\  
  /   │   \  Integración (moderados)
 /    │    \ Prueban componentes juntos
/─────┼─────\
      │      Unitarios (muchos)
      │      Prueban una función/clase
```

| Tipo | Qué prueba | Velocidad | Cantidad |
|------|------------|-----------|----------|
| **Unitario** | Una función | Muy rápido | Muchos |
| **Integración** | Varios componentes | Medio | Algunos |
| **E2E** | Todo el flujo | Lento | Pocos |

---

## 9.3 Configurar Pytest

### Instalar

```powershell
pip install pytest
```

Agregar a `requirements.txt`:
```
pytest>=7.0.0
```

### Estructura de tests

```
tests/
├── __init__.py
├── test_dominio.py        # Tests de entidades
├── test_servicios.py      # Tests de servicios (ya lo hicimos)
└── test_api.py            # Tests de endpoints
```

---

## 9.4 Tests de Dominio (Unitarios)

Ya creamos algunos en el capítulo 4. Completemos el archivo `tests/test_dominio.py`:

```python
"""
Tests Unitarios del Dominio
===========================

Estos tests prueban las entidades y sus validaciones.
No necesitan base de datos ni servicios.
"""

import pytest
from src.domain.entities import Alumno, Curso, Inscripcion
from src.domain.exceptions import (
    DNIDuplicadoException,
    AlumnoNoEncontradoException
)


class TestAlumno:
    """Tests para la entidad Alumno"""
    
    def test_crear_alumno_valido(self):
        """Debe crear un alumno con datos válidos"""
        alumno = Alumno(
            id=None,
            nombre="Juan",
            apellido="Pérez",
            dni="12345678",
            email="juan@mail.com"
        )
        
        assert alumno.nombre == "Juan"
        assert alumno.apellido == "Pérez"
        assert alumno.dni == "12345678"
        assert alumno.email == "juan@mail.com"
    
    def test_nombre_completo(self):
        """Debe calcular nombre completo correctamente"""
        alumno = Alumno(
            id=1,
            nombre="María",
            apellido="García",
            dni="11111111",
            email="maria@mail.com"
        )
        
        assert alumno.nombre_completo == "García, María"
    
    def test_limpiar_espacios(self):
        """Debe limpiar espacios en nombre y apellido"""
        alumno = Alumno(
            id=None,
            nombre="  Ana  ",
            apellido="  López  ",
            dni="22222222",
            email="ana@mail.com"
        )
        
        assert alumno.nombre == "Ana"
        assert alumno.apellido == "López"
    
    def test_nombre_vacio_falla(self):
        """Debe fallar con nombre vacío"""
        with pytest.raises(ValueError) as excinfo:
            Alumno(
                id=None,
                nombre="",
                apellido="Test",
                dni="12345678",
                email="test@mail.com"
            )
        
        assert "nombre" in str(excinfo.value).lower()
    
    def test_apellido_vacio_falla(self):
        """Debe fallar con apellido vacío"""
        with pytest.raises(ValueError):
            Alumno(
                id=None,
                nombre="Juan",
                apellido="",
                dni="12345678",
                email="test@mail.com"
            )
    
    def test_email_sin_arroba_falla(self):
        """Debe fallar con email inválido"""
        with pytest.raises(ValueError) as excinfo:
            Alumno(
                id=None,
                nombre="Juan",
                apellido="Pérez",
                dni="12345678",
                email="emailinvalido"
            )
        
        assert "email" in str(excinfo.value).lower()
    
    def test_dni_vacio_falla(self):
        """Debe fallar con DNI vacío"""
        with pytest.raises(ValueError):
            Alumno(
                id=None,
                nombre="Juan",
                apellido="Pérez",
                dni="",
                email="juan@mail.com"
            )


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
        assert curso.anio == 2024
        assert curso.cuatrimestre == 1
    
    def test_nombre_completo_curso(self):
        """Debe generar nombre completo"""
        curso = Curso(
            id=1,
            nombre_materia="Base de Datos",
            anio=2024,
            cuatrimestre=2
        )
        
        assert curso.nombre_completo == "Base de Datos - 2C2024"
    
    def test_cuatrimestre_invalido_falla(self):
        """Debe fallar con cuatrimestre != 1 o 2"""
        with pytest.raises(ValueError) as excinfo:
            Curso(
                id=None,
                nombre_materia="Test",
                anio=2024,
                cuatrimestre=3
            )
        
        assert "cuatrimestre" in str(excinfo.value).lower()
    
    def test_cuatrimestre_cero_falla(self):
        """Debe fallar con cuatrimestre 0"""
        with pytest.raises(ValueError):
            Curso(
                id=None,
                nombre_materia="Test",
                anio=2024,
                cuatrimestre=0
            )
    
    def test_anio_muy_antiguo_falla(self):
        """Debe fallar con año < 2000"""
        with pytest.raises(ValueError):
            Curso(
                id=None,
                nombre_materia="Test",
                anio=1999,
                cuatrimestre=1
            )
    
    def test_materia_vacia_falla(self):
        """Debe fallar con materia vacía"""
        with pytest.raises(ValueError):
            Curso(
                id=None,
                nombre_materia="",
                anio=2024,
                cuatrimestre=1
            )


class TestInscripcion:
    """Tests para la entidad Inscripcion"""
    
    def test_crear_inscripcion_valida(self):
        """Debe crear inscripción válida"""
        inscripcion = Inscripcion(
            id=None,
            alumno_id=1,
            curso_id=1
        )
        
        assert inscripcion.alumno_id == 1
        assert inscripcion.curso_id == 1
    
    def test_alumno_id_cero_falla(self):
        """Debe fallar con alumno_id = 0"""
        with pytest.raises(ValueError):
            Inscripcion(
                id=None,
                alumno_id=0,
                curso_id=1
            )
    
    def test_curso_id_negativo_falla(self):
        """Debe fallar con curso_id negativo"""
        with pytest.raises(ValueError):
            Inscripcion(
                id=None,
                alumno_id=1,
                curso_id=-1
            )


class TestExcepciones:
    """Tests para las excepciones de dominio"""
    
    def test_dni_duplicado_mensaje(self):
        """La excepción debe incluir el DNI"""
        exc = DNIDuplicadoException("12345678")
        
        assert "12345678" in str(exc)
    
    def test_alumno_no_encontrado_mensaje(self):
        """La excepción debe incluir el ID"""
        exc = AlumnoNoEncontradoException(99)
        
        assert "99" in str(exc)
```

### Ejecutar tests de dominio

```powershell
pytest tests/test_dominio.py -v
```

Resultado esperado:
```
tests/test_dominio.py::TestAlumno::test_crear_alumno_valido PASSED
tests/test_dominio.py::TestAlumno::test_nombre_completo PASSED
...
15 passed
```

---

## 9.5 Tests de Servicios (Integración)

Ya creamos una versión básica. Aquí está el archivo completo `tests/test_servicios.py`:

```python
"""
Tests de Servicios
==================

Estos tests prueban la lógica de negocio.
Usan mocks para no depender de la BD real.
"""

import pytest
from src.application.services import AlumnoService, CursoService
from src.domain.entities import Alumno, Curso
from src.domain.exceptions import (
    DNIDuplicadoException,
    AlumnoNoEncontradoException,
    CursoNoEncontradoException
)


class MockAlumnoRepository:
    """
    Repositorio falso para tests.
    Simula guardar en memoria.
    """
    
    def __init__(self):
        self._alumnos = {}
        self._next_id = 1
    
    def guardar(self, alumno: Alumno) -> Alumno:
        alumno.id = self._next_id
        self._alumnos[self._next_id] = alumno
        self._next_id += 1
        return alumno
    
    def obtener_por_id(self, id: int):
        return self._alumnos.get(id)
    
    def obtener_por_dni(self, dni: str):
        for a in self._alumnos.values():
            if a.dni == dni:
                return a
        return None
    
    def listar(self, limite=100):
        return list(self._alumnos.values())[:limite]
    
    def actualizar(self, alumno: Alumno) -> Alumno:
        self._alumnos[alumno.id] = alumno
        return alumno
    
    def eliminar(self, id: int) -> bool:
        if id in self._alumnos:
            del self._alumnos[id]
            return True
        return False
    
    def contar(self):
        return len(self._alumnos)


class MockCursoRepository:
    """Repositorio falso para cursos"""
    
    def __init__(self):
        self._cursos = {}
        self._next_id = 1
    
    def guardar(self, curso: Curso) -> Curso:
        curso.id = self._next_id
        self._cursos[self._next_id] = curso
        self._next_id += 1
        return curso
    
    def obtener_por_id(self, id: int):
        return self._cursos.get(id)
    
    def listar(self, limite=100):
        return list(self._cursos.values())[:limite]
    
    def actualizar(self, curso: Curso) -> Curso:
        self._cursos[curso.id] = curso
        return curso
    
    def eliminar(self, id: int) -> bool:
        if id in self._cursos:
            del self._cursos[id]
            return True
        return False
    
    def contar(self):
        return len(self._cursos)


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
        
        # Intentar crear otro con mismo DNI
        with pytest.raises(DNIDuplicadoException) as exc:
            service.crear("Otro", "Usuario", "12345678", "otro@mail.com")
        
        assert "12345678" in str(exc.value)
    
    def test_obtener_alumno_existente(self):
        """Debe retornar alumno si existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        creado = service.crear("María", "García", "11111111", "maria@mail.com")
        obtenido = service.obtener(creado.id)
        
        assert obtenido.id == creado.id
        assert obtenido.nombre == "María"
    
    def test_obtener_alumno_no_existente_falla(self):
        """Debe fallar si el alumno no existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        with pytest.raises(AlumnoNoEncontradoException):
            service.obtener(999)
    
    def test_listar_alumnos(self):
        """Debe listar todos los alumnos"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        service.crear("Juan", "Pérez", "11111111", "juan@mail.com")
        service.crear("María", "García", "22222222", "maria@mail.com")
        
        alumnos = service.listar()
        
        assert len(alumnos) == 2
    
    def test_actualizar_parcial(self):
        """Debe actualizar solo los campos enviados"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        alumno = service.crear("Juan", "Pérez", "12345678", "juan@mail.com")
        
        # Solo actualizar nombre
        actualizado = service.actualizar(alumno.id, nombre="Juan Carlos")
        
        assert actualizado.nombre == "Juan Carlos"
        assert actualizado.apellido == "Pérez"  # No cambió
    
    def test_actualizar_dni_a_existente_falla(self):
        """Debe fallar al cambiar DNI a uno existente"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        service.crear("Juan", "Pérez", "11111111", "juan@mail.com")
        maria = service.crear("María", "García", "22222222", "maria@mail.com")
        
        # Intentar cambiar DNI de María al de Juan
        with pytest.raises(DNIDuplicadoException):
            service.actualizar(maria.id, dni="11111111")
    
    def test_eliminar_existente(self):
        """Debe eliminar y retornar True"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        alumno = service.crear("Test", "Test", "00000000", "test@mail.com")
        
        resultado = service.eliminar(alumno.id)
        
        assert resultado is True
        assert service.contar() == 0
    
    def test_eliminar_no_existente(self):
        """Debe retornar False si no existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        resultado = service.eliminar(999)
        
        assert resultado is False


class TestCursoService:
    """Tests para CursoService"""
    
    def test_crear_curso_exitoso(self):
        """Debe crear un curso correctamente"""
        repo = MockCursoRepository()
        service = CursoService(repo)
        
        curso = service.crear("Programación I", 2024, 1)
        
        assert curso.id == 1
        assert curso.nombre_materia == "Programación I"
        assert curso.nombre_completo == "Programación I - 1C2024"
    
    def test_obtener_curso_existente(self):
        """Debe retornar curso si existe"""
        repo = MockCursoRepository()
        service = CursoService(repo)
        
        creado = service.crear("Base de Datos", 2024, 2)
        obtenido = service.obtener(creado.id)
        
        assert obtenido.id == creado.id
    
    def test_obtener_curso_no_existente_falla(self):
        """Debe fallar si el curso no existe"""
        repo = MockCursoRepository()
        service = CursoService(repo)
        
        with pytest.raises(CursoNoEncontradoException):
            service.obtener(999)
```

### Ejecutar tests de servicios

```powershell
pytest tests/test_servicios.py -v
```

---

## 9.6 Tests de API (Integración)

Crear `tests/test_api.py`:

```python
"""
Tests de API
============

Estos tests prueban los endpoints HTTP.
Usan TestClient de FastAPI.
"""

import pytest
from fastapi.testclient import TestClient
from src.presentation.api.main import app


@pytest.fixture
def client():
    """Cliente de prueba para la API"""
    return TestClient(app)


class TestHealthCheck:
    """Tests del endpoint de health"""
    
    def test_health_check(self, client):
        """Debe responder con status ok"""
        response = client.get("/api")
        
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestAlumnosAPI:
    """Tests de endpoints de alumnos"""
    
    def test_listar_alumnos(self, client):
        """Debe listar alumnos"""
        response = client.get("/api/alumnos/")
        
        assert response.status_code == 200
        assert "alumnos" in response.json()
        assert "total" in response.json()
    
    def test_crear_alumno_valido(self, client):
        """Debe crear un alumno"""
        datos = {
            "nombre": "Test",
            "apellido": "API",
            "dni": "99999999",
            "email": "test@api.com"
        }
        
        response = client.post("/api/alumnos/", json=datos)
        
        # Puede ser 201 (creado) o 409 (ya existe)
        assert response.status_code in [201, 409]
    
    def test_crear_alumno_sin_nombre_falla(self, client):
        """Debe fallar sin nombre"""
        datos = {
            "nombre": "",
            "apellido": "Test",
            "dni": "88888888",
            "email": "test@mail.com"
        }
        
        response = client.post("/api/alumnos/", json=datos)
        
        assert response.status_code == 422  # Validation error
    
    def test_crear_alumno_email_invalido_falla(self, client):
        """Debe fallar con email inválido"""
        datos = {
            "nombre": "Test",
            "apellido": "Test",
            "dni": "77777777",
            "email": "emailinvalido"
        }
        
        response = client.post("/api/alumnos/", json=datos)
        
        assert response.status_code == 422
    
    def test_obtener_alumno_no_existente(self, client):
        """Debe retornar 404 para ID inexistente"""
        response = client.get("/api/alumnos/99999")
        
        assert response.status_code == 404


class TestCursosAPI:
    """Tests de endpoints de cursos"""
    
    def test_listar_cursos(self, client):
        """Debe listar cursos"""
        response = client.get("/api/cursos/")
        
        assert response.status_code == 200
        assert "cursos" in response.json()
    
    def test_crear_curso_valido(self, client):
        """Debe crear un curso"""
        datos = {
            "nombre_materia": "Test API",
            "anio": 2024,
            "cuatrimestre": 1
        }
        
        response = client.post("/api/cursos/", json=datos)
        
        assert response.status_code == 201
        assert response.json()["nombre_materia"] == "Test API"
    
    def test_crear_curso_cuatrimestre_invalido_falla(self, client):
        """Debe fallar con cuatrimestre 3"""
        datos = {
            "nombre_materia": "Test",
            "anio": 2024,
            "cuatrimestre": 3
        }
        
        response = client.post("/api/cursos/", json=datos)
        
        assert response.status_code == 422
```

### Ejecutar tests de API

```powershell
pytest tests/test_api.py -v
```

---

## 9.7 Ejecutar Todos los Tests

```powershell
# Todos los tests
pytest -v

# Con resumen corto
pytest

# Solo tests que fallaron antes
pytest --lf

# Parar en el primer fallo
pytest -x
```

### Resultado esperado

```
========================= test session starts ==========================
collected 30 items

tests/test_dominio.py ............                                [40%]
tests/test_servicios.py ..........                                [73%]
tests/test_api.py ........                                        [100%]

========================== 30 passed in 2.5s ===========================
```

---

## 9.8 Cobertura de Código

Instalar pytest-cov:

```powershell
pip install pytest-cov
```

Ejecutar con cobertura:

```powershell
pytest --cov=src --cov-report=term-missing
```

Resultado:
```
----------- coverage: platform win32 -----------
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
src/domain/entities/alumno.py                   25      2    92%
src/domain/entities/curso.py                    20      1    95%
src/application/services/alumno_service.py     35      3    91%
...
----------------------------------------------------------------
TOTAL                                          200     15    93%
```

---

## 9.9 Buenas Prácticas de Testing

### 1. Un assert por test (idealmente)

```python
# ❌ MAL
def test_alumno():
    alumno = crear_alumno()
    assert alumno.nombre == "Juan"
    assert alumno.email == "juan@mail.com"
    assert alumno.id is not None

# ✅ BIEN
def test_alumno_tiene_nombre():
    alumno = crear_alumno()
    assert alumno.nombre == "Juan"

def test_alumno_tiene_email():
    alumno = crear_alumno()
    assert alumno.email == "juan@mail.com"
```

### 2. Nombres descriptivos

```python
# ❌ MAL
def test_1():
def test_alumno():

# ✅ BIEN
def test_crear_alumno_con_dni_duplicado_falla():
def test_obtener_alumno_no_existente_retorna_404():
```

### 3. Preparación con fixtures

```python
# ❌ MAL - Repetición
def test_actualizar():
    repo = MockRepo()
    service = Service(repo)
    alumno = service.crear(...)

def test_eliminar():
    repo = MockRepo()
    service = Service(repo)
    alumno = service.crear(...)

# ✅ BIEN - Fixture
@pytest.fixture
def service():
    return AlumnoService(MockRepo())

def test_actualizar(service):
    alumno = service.crear(...)

def test_eliminar(service):
    alumno = service.crear(...)
```

---

## 9.10 Resumen

### Archivos creados

```
tests/
├── __init__.py
├── test_dominio.py     ✅ (unitarios)
├── test_servicios.py   ✅ (integración - con mocks)
└── test_api.py         ✅ (integración - HTTP)
```

### Qué aprendiste

| Concepto | Explicación |
|----------|-------------|
| pytest | Framework de testing para Python |
| Fixtures | Preparar datos para tests |
| Mocks | Objetos falsos para simular dependencias |
| Cobertura | Medir qué % del código tienen tests |
| TestClient | Probar API sin servidor real |

---

**Anterior:** [Capítulo 8 - Frontend](./08_frontend.md)

**Siguiente:** [Capítulo 10 - Deploy](./10_deploy.md)
