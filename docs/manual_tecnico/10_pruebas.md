# Capítulo 10: Pruebas

## 10.1 Tipos de Pruebas

En un proyecto profesional, existen varios niveles de pruebas:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIRÁMIDE DE TESTING                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                          ▲                                      │
│                         /│\                                     │
│                        / │ \   End-to-End (E2E)                │
│                       /  │  \  Pocas, lentas, costosas          │
│                      /   │   \                                  │
│                     /────┼────\                                 │
│                    /     │     \  Integración                   │
│                   /      │      \ Moderadas                     │
│                  /───────┼───────\                              │
│                 /        │        \  Unitarias                  │
│                /         │         \ Muchas, rápidas, baratas   │
│               ────────────────────────                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| Tipo | Qué prueba | Cantidad | Velocidad |
|------|------------|----------|-----------|
| **Unitarias** | Una función/clase aislada | Muchas | Muy rápidas |
| **Integración** | Interacción entre componentes | Moderadas | Medias |
| **E2E** | Flujo completo usuario-sistema | Pocas | Lentas |

## 10.2 Configuración de Pytest

### Instalar dependencias de testing

```bash
pip install pytest pytest-asyncio httpx
```

Agregar a `requirements.txt`:
```
pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
```

### Crear archivo de configuración

`pytest.ini`:
```ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
python_functions = test_*
asyncio_mode = auto
```

### Estructura de tests

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartidos
├── unit/                    # Pruebas unitarias
│   ├── __init__.py
│   ├── test_alumno.py
│   ├── test_curso.py
│   └── test_asistencia.py
├── integration/             # Pruebas de integración
│   ├── __init__.py
│   ├── test_alumno_service.py
│   └── test_api_endpoints.py
└── e2e/                     # Pruebas end-to-end
    ├── __init__.py
    └── test_flows.py
```

## 10.3 Pruebas Unitarias

### Probar Entidades

```python
# tests/unit/test_alumno.py
"""
Pruebas unitarias para la entidad Alumno
"""

import pytest
from src.domain.entities.alumno import Alumno


class TestAlumnoCreacion:
    """Grupo de tests para creación de alumnos"""
    
    def test_crear_alumno_valido(self):
        """Debe crear un alumno con datos válidos"""
        alumno = Alumno(
            id=None,
            nombre="María",
            apellido="García",
            dni="12345678",
            email="maria@test.com",
            cohorte=2024
        )
        
        assert alumno.nombre == "María"
        assert alumno.apellido == "García"
        assert alumno.dni == "12345678"
        assert alumno.email == "maria@test.com"
        assert alumno.cohorte == 2024
    
    def test_nombre_completo(self):
        """Debe calcular el nombre completo correctamente"""
        alumno = Alumno(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            dni="11111111",
            email="juan@test.com",
            cohorte=2023
        )
        
        assert alumno.nombre_completo == "Pérez, Juan"
    
    def test_limpiar_espacios(self):
        """Debe limpiar espacios de nombre y apellido"""
        alumno = Alumno(
            id=None,
            nombre="  Ana  ",
            apellido="  López  ",
            dni="22222222",
            email="ana@test.com",
            cohorte=2024
        )
        
        assert alumno.nombre == "Ana"
        assert alumno.apellido == "López"


class TestAlumnoValidaciones:
    """Grupo de tests para validaciones de alumno"""
    
    def test_nombre_vacio_falla(self):
        """Debe fallar si el nombre está vacío"""
        with pytest.raises(ValueError) as exc_info:
            Alumno(
                id=None,
                nombre="",
                apellido="García",
                dni="12345678",
                email="test@test.com",
                cohorte=2024
            )
        
        assert "nombre no puede estar vacío" in str(exc_info.value).lower()
    
    def test_nombre_solo_espacios_falla(self):
        """Debe fallar si el nombre son solo espacios"""
        with pytest.raises(ValueError):
            Alumno(
                id=None,
                nombre="   ",
                apellido="García",
                dni="12345678",
                email="test@test.com",
                cohorte=2024
            )
    
    def test_email_sin_arroba_falla(self):
        """Debe fallar si el email no tiene @"""
        with pytest.raises(ValueError) as exc_info:
            Alumno(
                id=None,
                nombre="Juan",
                apellido="Pérez",
                dni="12345678",
                email="emailinvalido",
                cohorte=2024
            )
        
        assert "email" in str(exc_info.value).lower()
    
    def test_cohorte_muy_antiguo_falla(self):
        """Debe fallar si el cohorte es anterior a 2000"""
        with pytest.raises(ValueError) as exc_info:
            Alumno(
                id=None,
                nombre="Juan",
                apellido="Pérez",
                dni="12345678",
                email="juan@test.com",
                cohorte=1999
            )
        
        assert "cohorte" in str(exc_info.value).lower()
    
    def test_cohorte_futurista_falla(self):
        """Debe fallar si el cohorte es mayor a 2100"""
        with pytest.raises(ValueError):
            Alumno(
                id=None,
                nombre="Juan",
                apellido="Pérez",
                dni="12345678",
                email="juan@test.com",
                cohorte=2101
            )


class TestAlumnoSerializacion:
    """Tests para to_dict y from_dict"""
    
    def test_to_dict(self):
        """Debe convertir a diccionario correctamente"""
        alumno = Alumno(
            id=1,
            nombre="Ana",
            apellido="López",
            dni="33333333",
            email="ana@test.com",
            cohorte=2024
        )
        
        resultado = alumno.to_dict()
        
        assert resultado["id"] == 1
        assert resultado["nombre"] == "Ana"
        assert resultado["apellido"] == "López"
        assert resultado["nombre_completo"] == "López, Ana"
    
    def test_from_dict(self):
        """Debe crear desde diccionario correctamente"""
        datos = {
            "id": 5,
            "nombre": "Pedro",
            "apellido": "Martínez",
            "dni": "44444444",
            "email": "pedro@test.com",
            "cohorte": 2023
        }
        
        alumno = Alumno.from_dict(datos)
        
        assert alumno.id == 5
        assert alumno.nombre == "Pedro"
        assert alumno.nombre_completo == "Martínez, Pedro"
```

### Probar Curso

```python
# tests/unit/test_curso.py
"""
Pruebas unitarias para la entidad Curso
"""

import pytest
from src.domain.entities.curso import Curso


class TestCursoCreacion:
    
    def test_crear_curso_valido(self):
        """Debe crear un curso con datos válidos"""
        curso = Curso(
            id=None,
            nombre_materia="Programación I",
            anio=2024,
            cuatrimestre=1,
            docente_responsable="Prof. García"
        )
        
        assert curso.nombre_materia == "Programación I"
        assert curso.anio == 2024
        assert curso.cuatrimestre == 1
    
    def test_nombre_completo_curso(self):
        """Debe generar el nombre completo correctamente"""
        curso = Curso(
            id=1,
            nombre_materia="Base de Datos",
            anio=2024,
            cuatrimestre=2,
            docente_responsable="Prof. López"
        )
        
        assert curso.nombre_completo == "Base de Datos - 2C2024"


class TestCursoValidaciones:
    
    def test_cuatrimestre_invalido(self):
        """Debe fallar si el cuatrimestre no es 1 o 2"""
        with pytest.raises(ValueError) as exc_info:
            Curso(
                id=None,
                nombre_materia="Test",
                anio=2024,
                cuatrimestre=3,  # Inválido
                docente_responsable="Prof. X"
            )
        
        assert "cuatrimestre" in str(exc_info.value).lower()
    
    def test_materia_vacia(self):
        """Debe fallar si la materia está vacía"""
        with pytest.raises(ValueError):
            Curso(
                id=None,
                nombre_materia="",
                anio=2024,
                cuatrimestre=1,
                docente_responsable="Prof. X"
            )
```

### Probar Asistencia

```python
# tests/unit/test_asistencia.py
"""
Pruebas unitarias para la entidad Asistencia
"""

import pytest
from src.domain.entities.asistencia import Asistencia, ESTADOS_ASISTENCIA


class TestAsistenciaCreacion:
    
    def test_crear_asistencia_presente(self):
        """Debe crear asistencia con estado Presente"""
        asistencia = Asistencia(
            id=None,
            alumno_id=1,
            clase_id=1,
            estado="Presente"
        )
        
        assert asistencia.estado == "Presente"
    
    def test_todos_los_estados_validos(self):
        """Debe aceptar todos los estados válidos"""
        for estado in ESTADOS_ASISTENCIA:
            asistencia = Asistencia(
                id=None,
                alumno_id=1,
                clase_id=1,
                estado=estado
            )
            assert asistencia.estado == estado


class TestAsistenciaValidaciones:
    
    def test_estado_invalido(self):
        """Debe fallar con estado inválido"""
        with pytest.raises(ValueError) as exc_info:
            Asistencia(
                id=None,
                alumno_id=1,
                clase_id=1,
                estado="Invalido"
            )
        
        assert "Estado inválido" in str(exc_info.value)
```

## 10.4 Pruebas de Integración

### Fixtures Compartidos

```python
# tests/conftest.py
"""
Fixtures compartidos para todos los tests
"""

import pytest
from src.domain.entities.alumno import Alumno


@pytest.fixture
def alumno_valido():
    """Fixture que retorna un alumno válido para tests"""
    return Alumno(
        id=None,
        nombre="Test",
        apellido="Usuario",
        dni="99999999",
        email="test@test.com",
        cohorte=2024
    )


@pytest.fixture
def lista_alumnos():
    """Fixture con lista de alumnos para tests"""
    return [
        Alumno(id=1, nombre="Ana", apellido="García", 
               dni="11111111", email="ana@test.com", cohorte=2024),
        Alumno(id=2, nombre="Juan", apellido="Pérez", 
               dni="22222222", email="juan@test.com", cohorte=2024),
        Alumno(id=3, nombre="María", apellido="López", 
               dni="33333333", email="maria@test.com", cohorte=2023),
    ]


class MockAlumnoRepository:
    """
    Repositorio falso para tests.
    No usa base de datos real.
    """
    
    def __init__(self):
        self._alumnos = {}
        self._next_id = 1
    
    def crear(self, alumno: Alumno) -> Alumno:
        alumno.id = self._next_id
        self._alumnos[self._next_id] = alumno
        self._next_id += 1
        return alumno
    
    def obtener_por_id(self, id: int):
        return self._alumnos.get(id)
    
    def obtener_por_dni(self, dni: str):
        for alumno in self._alumnos.values():
            if alumno.dni == dni:
                return alumno
        return None
    
    def listar(self, limite=None, offset=0, cohorte=None, buscar=None):
        resultado = list(self._alumnos.values())
        if cohorte:
            resultado = [a for a in resultado if a.cohorte == cohorte]
        return resultado[offset:offset+limite] if limite else resultado[offset:]
    
    def actualizar(self, alumno: Alumno) -> Alumno:
        self._alumnos[alumno.id] = alumno
        return alumno
    
    def eliminar(self, id: int) -> bool:
        if id in self._alumnos:
            del self._alumnos[id]
            return True
        return False
    
    def contar(self, cohorte=None) -> int:
        if cohorte:
            return len([a for a in self._alumnos.values() if a.cohorte == cohorte])
        return len(self._alumnos)


@pytest.fixture
def mock_repo():
    """Fixture que retorna un repositorio mock vacío"""
    return MockAlumnoRepository()
```

### Probar Servicio con Mock

```python
# tests/integration/test_alumno_service.py
"""
Pruebas de integración para AlumnoService
"""

import pytest
from src.application.services.alumno_service import AlumnoService
from src.domain.exceptions.domain_exceptions import (
    AlumnoNoEncontradoException,
    DNIDuplicadoException
)
from tests.conftest import MockAlumnoRepository


class TestAlumnoServiceCrear:
    
    def test_crear_alumno_exitoso(self):
        """Debe crear un alumno correctamente"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        alumno = service.crear_alumno(
            nombre="Juan",
            apellido="Pérez",
            dni="12345678",
            email="juan@test.com",
            cohorte=2024
        )
        
        assert alumno.id is not None
        assert alumno.nombre == "Juan"
        assert alumno.dni == "12345678"
    
    def test_crear_alumno_dni_duplicado(self):
        """Debe fallar si el DNI ya existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        # Crear primer alumno
        service.crear_alumno(
            nombre="Juan",
            apellido="Pérez",
            dni="12345678",
            email="juan@test.com",
            cohorte=2024
        )
        
        # Intentar crear con mismo DNI
        with pytest.raises(DNIDuplicadoException) as exc_info:
            service.crear_alumno(
                nombre="Otro",
                apellido="Usuario",
                dni="12345678",  # Mismo DNI
                email="otro@test.com",
                cohorte=2024
            )
        
        assert "12345678" in str(exc_info.value)


class TestAlumnoServiceObtener:
    
    def test_obtener_alumno_existente(self):
        """Debe retornar alumno si existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        creado = service.crear_alumno(
            nombre="María",
            apellido="García",
            dni="11111111",
            email="maria@test.com",
            cohorte=2024
        )
        
        obtenido = service.obtener_alumno(creado.id)
        
        assert obtenido.id == creado.id
        assert obtenido.nombre == "María"
    
    def test_obtener_alumno_no_existente(self):
        """Debe lanzar excepción si no existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        with pytest.raises(AlumnoNoEncontradoException) as exc_info:
            service.obtener_alumno(999)
        
        assert "999" in str(exc_info.value)


class TestAlumnoServiceActualizar:
    
    def test_actualizar_parcial(self):
        """Debe actualizar solo los campos proporcionados"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        alumno = service.crear_alumno(
            nombre="Juan",
            apellido="Pérez",
            dni="12345678",
            email="juan@test.com",
            cohorte=2024
        )
        
        # Solo actualizar nombre
        actualizado = service.actualizar_alumno(
            alumno_id=alumno.id,
            nombre="Juan Carlos"
        )
        
        assert actualizado.nombre == "Juan Carlos"
        assert actualizado.apellido == "Pérez"  # No cambió
        assert actualizado.email == "juan@test.com"  # No cambió


class TestAlumnoServiceEliminar:
    
    def test_eliminar_existente(self):
        """Debe eliminar y retornar True"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        alumno = service.crear_alumno(
            nombre="Test",
            apellido="Test",
            dni="00000000",
            email="test@test.com",
            cohorte=2024
        )
        
        resultado = service.eliminar_alumno(alumno.id)
        
        assert resultado is True
        assert service.contar_alumnos() == 0
    
    def test_eliminar_no_existente(self):
        """Debe retornar False si no existe"""
        repo = MockAlumnoRepository()
        service = AlumnoService(repo)
        
        resultado = service.eliminar_alumno(999)
        
        assert resultado is False
```

## 10.5 Pruebas de API (Endpoints)

```python
# tests/integration/test_api_endpoints.py
"""
Pruebas de integración para endpoints de la API
"""

import pytest
from fastapi.testclient import TestClient
from src.presentation.api.main import app


@pytest.fixture
def client():
    """Cliente de prueba para la API"""
    return TestClient(app)


class TestHealthCheck:
    
    def test_health_check(self, client):
        """Debe responder con status ok"""
        response = client.get("/api")
        
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestAlumnosEndpoints:
    
    def test_listar_alumnos(self, client):
        """Debe listar alumnos"""
        response = client.get("/api/alumnos/")
        
        assert response.status_code == 200
        assert "alumnos" in response.json()
        assert "total" in response.json()
    
    def test_crear_alumno(self, client):
        """Debe crear un alumno"""
        datos = {
            "nombre": "Test",
            "apellido": "API",
            "dni": "98765432",
            "email": "test@api.com",
            "cohorte": 2024
        }
        
        response = client.post("/api/alumnos/", json=datos)
        
        # Puede ser 201 (creado) o 409 (ya existe)
        assert response.status_code in [201, 409]
        
        if response.status_code == 201:
            resultado = response.json()
            assert resultado["nombre"] == "Test"
            assert resultado["nombre_completo"] == "API, Test"
    
    def test_crear_alumno_datos_invalidos(self, client):
        """Debe fallar con datos inválidos"""
        datos = {
            "nombre": "",  # Vacío
            "apellido": "Test",
            "dni": "12345678",
            "email": "invalido",  # Sin @
            "cohorte": 1900  # Muy antiguo
        }
        
        response = client.post("/api/alumnos/", json=datos)
        
        assert response.status_code == 422  # Validation error
    
    def test_obtener_alumno_no_existente(self, client):
        """Debe retornar 404 para alumno inexistente"""
        response = client.get("/api/alumnos/99999")
        
        assert response.status_code == 404


class TestCursosEndpoints:
    
    def test_listar_cursos(self, client):
        """Debe listar cursos"""
        response = client.get("/api/cursos/")
        
        assert response.status_code == 200
        assert "cursos" in response.json()
    
    def test_crear_curso(self, client):
        """Debe crear un curso"""
        datos = {
            "nombre_materia": "Test API",
            "anio": 2024,
            "cuatrimestre": 1,
            "docente_responsable": "Prof. Test"
        }
        
        response = client.post("/api/cursos/", json=datos)
        
        assert response.status_code == 201
        assert response.json()["nombre_materia"] == "Test API"
    
    def test_crear_curso_cuatrimestre_invalido(self, client):
        """Debe fallar con cuatrimestre inválido"""
        datos = {
            "nombre_materia": "Test",
            "anio": 2024,
            "cuatrimestre": 3,  # Inválido
            "docente_responsable": "Prof. Test"
        }
        
        response = client.post("/api/cursos/", json=datos)
        
        assert response.status_code == 422
```

## 10.6 Ejecutar Tests

### Comandos básicos

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con output detallado
pytest -v

# Ejecutar solo una carpeta
pytest tests/unit/

# Ejecutar solo un archivo
pytest tests/unit/test_alumno.py

# Ejecutar solo una clase
pytest tests/unit/test_alumno.py::TestAlumnoCreacion

# Ejecutar solo un test específico
pytest tests/unit/test_alumno.py::TestAlumnoCreacion::test_crear_alumno_valido

# Ver tests que fallan solamente
pytest --tb=short

# Con cobertura de código
pip install pytest-cov
pytest --cov=src --cov-report=html
```

### Resultado esperado

```
================================ test session starts =================================
platform win32 -- Python 3.11.x, pytest-7.x.x
rootdir: /path/to/proyecto
collected 25 items

tests/unit/test_alumno.py ........                                            [ 32%]
tests/unit/test_curso.py ....                                                 [ 48%]
tests/unit/test_asistencia.py ...                                             [ 60%]
tests/integration/test_alumno_service.py .......                              [ 88%]
tests/integration/test_api_endpoints.py ...                                   [100%]

================================= 25 passed in 2.35s =================================
```

## 10.7 Mejores Prácticas de Testing

### Nombrar tests descriptivamente

```python
# ❌ MAL
def test_1():
def test_alumno():

# ✅ BIEN
def test_crear_alumno_con_datos_validos():
def test_crear_alumno_falla_si_dni_duplicado():
```

### Un assert por test (idealmente)

```python
# ❌ MAL - Difícil saber qué falló
def test_alumno():
    alumno = crear_alumno()
    assert alumno.nombre == "Juan"
    assert alumno.email == "juan@test.com"
    assert alumno.cohorte == 2024

# ✅ BIEN - Tests específicos
def test_alumno_tiene_nombre_correcto():
    alumno = crear_alumno()
    assert alumno.nombre == "Juan"

def test_alumno_tiene_email_correcto():
    alumno = crear_alumno()
    assert alumno.email == "juan@test.com"
```

### Usar fixtures para setup

```python
# ❌ MAL - Repetición
def test_actualizar():
    alumno = Alumno(id=1, nombre="Test", ...)
    # ...

def test_eliminar():
    alumno = Alumno(id=1, nombre="Test", ...)
    # ...

# ✅ BIEN - Fixture reutilizable
@pytest.fixture
def alumno_test():
    return Alumno(id=1, nombre="Test", ...)

def test_actualizar(alumno_test):
    # usa alumno_test

def test_eliminar(alumno_test):
    # usa alumno_test
```

---

**Capítulo anterior**: [Código Base](./09_codigo_base.md)

**Siguiente capítulo**: [Deploy](./11_deploy.md)
