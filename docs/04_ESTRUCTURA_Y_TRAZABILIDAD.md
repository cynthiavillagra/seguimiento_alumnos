# Estructura del Proyecto y Trazabilidad

## 1. Estructura de Carpetas Propuesta

```
app-seguimiento-alumnos/
│
├── src/
│   ├── __init__.py
│   │
│   ├── domain/                          # 🎯 Capa de Dominio
│   │   ├── __init__.py
│   │   ├── entities/                    # Entidades de dominio
│   │   │   ├── __init__.py
│   │   │   ├── alumno.py
│   │   │   ├── curso.py
│   │   │   ├── inscripcion.py
│   │   │   ├── clase.py
│   │   │   ├── registro_asistencia.py
│   │   │   ├── registro_participacion.py
│   │   │   ├── trabajo_practico.py
│   │   │   └── entrega_tp.py
│   │   │
│   │   ├── value_objects/               # Value Objects
│   │   │   ├── __init__.py
│   │   │   ├── indicador_riesgo.py
│   │   │   └── enums.py                 # EstadoAsistencia, NivelParticipacion, NivelRiesgo
│   │   │
│   │   └── exceptions/                  # Excepciones de dominio
│   │       ├── __init__.py
│   │       └── domain_exceptions.py
│   │
│   ├── application/                     # ⚙️ Capa de Aplicación
│   │   ├── __init__.py
│   │   ├── services/                    # Servicios de aplicación (casos de uso)
│   │   │   ├── __init__.py
│   │   │   ├── alumno_service.py
│   │   │   ├── curso_service.py
│   │   │   ├── inscripcion_service.py
│   │   │   ├── clase_service.py
│   │   │   ├── asistencia_service.py
│   │   │   ├── participacion_service.py
│   │   │   ├── trabajo_practico_service.py
│   │   │   └── indicador_riesgo_service.py
│   │   │
│   │   └── dtos/                        # Data Transfer Objects
│   │       ├── __init__.py
│   │       ├── alumno_dto.py
│   │       ├── curso_dto.py
│   │       └── indicador_dto.py
│   │
│   ├── infrastructure/                  # 🗄️ Capa de Infraestructura
│   │   ├── __init__.py
│   │   ├── database/                    # Configuración de base de datos
│   │   │   ├── __init__.py
│   │   │   ├── connection.py            # Gestión de conexión SQLite
│   │   │   └── schema.sql               # Script de creación de tablas
│   │   │
│   │   ├── repositories/                # Implementaciones de repositorios
│   │   │   ├── __init__.py
│   │   │   ├── base/                    # Interfaces/clases base
│   │   │   │   ├── __init__.py
│   │   │   │   ├── alumno_repository_base.py
│   │   │   │   ├── curso_repository_base.py
│   │   │   │   ├── asistencia_repository_base.py
│   │   │   │   └── ...
│   │   │   │
│   │   │   └── sqlite/                  # Implementaciones SQLite
│   │   │       ├── __init__.py
│   │   │       ├── alumno_repository_sqlite.py
│   │   │       ├── curso_repository_sqlite.py
│   │   │       ├── inscripcion_repository_sqlite.py
│   │   │       ├── clase_repository_sqlite.py
│   │   │       ├── asistencia_repository_sqlite.py
│   │   │       ├── participacion_repository_sqlite.py
│   │   │       ├── trabajo_practico_repository_sqlite.py
│   │   │       ├── entrega_tp_repository_sqlite.py
│   │   │       └── indicador_riesgo_repository_sqlite.py
│   │   │
│   │   └── config/                      # Configuración
│   │       ├── __init__.py
│   │       └── settings.py              # Variables de entorno, configuración
│   │
│   └── presentation/                    # 📡 Capa de Presentación
│       ├── __init__.py
│       └── api/                         # API HTTP (FastAPI)
│           ├── __init__.py
│           ├── main.py                  # Punto de entrada de FastAPI
│           ├── dependencies.py          # Inyección de dependencias
│           ├── routers/                 # Routers de endpoints
│           │   ├── __init__.py
│           │   ├── alumnos.py
│           │   ├── cursos.py
│           │   ├── inscripciones.py
│           │   ├── clases.py
│           │   ├── asistencias.py
│           │   ├── participaciones.py
│           │   ├── trabajos_practicos.py
│           │   └── alertas.py
│           │
│           ├── schemas/                 # Pydantic schemas (request/response)
│           │   ├── __init__.py
│           │   ├── alumno_schema.py
│           │   ├── curso_schema.py
│           │   ├── asistencia_schema.py
│           │   └── ...
│           │
│           └── middleware/              # Middleware (CORS, autenticación futura)
│               ├── __init__.py
│               └── cors_middleware.py
│
├── tests/                               # 🧪 Tests
│   ├── __init__.py
│   ├── unit/                            # Tests unitarios
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── test_alumno.py
│   │   │   └── test_indicador_riesgo.py
│   │   ├── application/
│   │   │   └── test_alumno_service.py
│   │   └── infrastructure/
│   │       └── test_alumno_repository.py
│   │
│   ├── integration/                     # Tests de integración
│   │   ├── __init__.py
│   │   └── test_api_alumnos.py
│   │
│   └── fixtures/                        # Fixtures y datos de prueba
│       ├── __init__.py
│       └── sample_data.py
│
├── docs/                                # 📚 Documentación
│   ├── 01_CONTEXTO_Y_REQUISITOS.md
│   ├── 02_CASOS_DE_USO_Y_STORIES.md
│   ├── 03_MODELO_Y_API.md
│   ├── 04_ESTRUCTURA_Y_TRAZABILIDAD.md (este archivo)
│   └── API_REFERENCE.md                 # Referencia de API (generada automáticamente)
│
├── scripts/                             # 🛠️ Scripts de utilidad
│   ├── init_db.py                       # Inicializar base de datos
│   ├── seed_data.py                     # Cargar datos de ejemplo
│   └── migrate.py                       # Migraciones (futuro)
│
├── api/                                 # 🚀 Vercel serverless functions
│   └── index.py                         # Entrypoint para Vercel
│
├── .env.example                         # Variables de entorno de ejemplo
├── .gitignore
├── requirements.txt                     # Dependencias de Python
├── pyproject.toml                       # Configuración del proyecto (Poetry/setuptools)
├── README.md                            # Documentación principal
└── vercel.json                          # Configuración de Vercel
```

---

## 2. Descripción de Cada Capa

### 🎯 Capa de Dominio (`src/domain/`)

**Propósito**: Contiene la lógica de negocio pura, independiente de frameworks, bases de datos o APIs.

**Contenido**:
- **Entidades** (`entities/`): Clases que representan conceptos del dominio con identidad propia (Alumno, Curso, Clase, etc.)
- **Value Objects** (`value_objects/`): Objetos sin identidad, definidos por sus atributos (IndicadorRiesgo, Enums)
- **Excepciones** (`exceptions/`): Excepciones específicas del dominio (ej: `AlumnoYaInscriptoException`)

**Reglas**:
- ✅ Puede contener lógica de validación y reglas de negocio
- ✅ Puede usar solo librerías estándar de Python (datetime, enum, etc.)
- ❌ NO debe depender de frameworks (FastAPI, SQLite, etc.)
- ❌ NO debe conocer detalles de infraestructura o presentación

**Ejemplo de archivo**: `src/domain/entities/alumno.py`
```python
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class Alumno:
    nombre: str
    apellido: str
    dni: str
    email: str
    cohorte: int
    id: int | None = None
    fecha_creacion: datetime | None = None
    
    def validar_email(self) -> bool:
        """Valida formato de email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, self.email) is not None
    
    def to_dict(self) -> dict:
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'email': self.email,
            'cohorte': self.cohorte,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
```

---

### ⚙️ Capa de Aplicación (`src/application/`)

**Propósito**: Orquesta los casos de uso del sistema, coordinando entidades de dominio y repositorios.

**Contenido**:
- **Servicios** (`services/`): Implementan casos de uso específicos (crear alumno, registrar asistencia, calcular riesgo)
- **DTOs** (`dtos/`): Objetos de transferencia de datos para comunicación entre capas

**Reglas**:
- ✅ Puede usar entidades de dominio
- ✅ Puede usar interfaces de repositorios (NO implementaciones concretas)
- ✅ Contiene lógica de coordinación y orquestación
- ❌ NO debe contener lógica de negocio pura (eso va en dominio)
- ❌ NO debe conocer detalles de HTTP, JSON, SQL

**Ejemplo de archivo**: `src/application/services/alumno_service.py`
```python
from src.domain.entities.alumno import Alumno
from src.infrastructure.repositories.base.alumno_repository_base import AlumnoRepositoryBase
from src.domain.exceptions.domain_exceptions import EmailInvalidoException, DNIDuplicadoException

class AlumnoService:
    def __init__(self, alumno_repository: AlumnoRepositoryBase):
        # Decisión de diseño: Inyección de dependencias
        # El servicio depende de la INTERFAZ, no de la implementación concreta
        self.alumno_repo = alumno_repository
    
    def crear_alumno(self, nombre: str, apellido: str, dni: str, email: str, cohorte: int) -> Alumno:
        """
        Caso de uso: Crear un nuevo alumno
        
        Orquesta:
        1. Crear entidad de dominio
        2. Validar reglas de negocio
        3. Verificar unicidad de DNI
        4. Persistir mediante repositorio
        """
        # Crear entidad
        alumno = Alumno(nombre, apellido, dni, email, cohorte)
        
        # Validar reglas de negocio
        if not alumno.validar_email():
            raise EmailInvalidoException(f"Email inválido: {email}")
        
        # Verificar unicidad de DNI
        existente = self.alumno_repo.obtener_por_dni(dni)
        if existente:
            raise DNIDuplicadoException(f"Ya existe un alumno con DNI {dni}")
        
        # Persistir
        alumno_creado = self.alumno_repo.crear(alumno)
        return alumno_creado
```

---

### 🗄️ Capa de Infraestructura (`src/infrastructure/`)

**Propósito**: Implementa detalles técnicos de persistencia, configuración y acceso a recursos externos.

**Contenido**:
- **Database** (`database/`): Gestión de conexión a SQLite, scripts de schema
- **Repositories** (`repositories/`):
  - `base/`: Interfaces abstractas (contratos)
  - `sqlite/`: Implementaciones concretas con SQLite
- **Config** (`config/`): Configuración, variables de entorno

**Reglas**:
- ✅ Implementa interfaces definidas en `repositories/base/`
- ✅ Contiene código específico de SQLite (SQL, conexiones)
- ✅ Puede usar librerías de terceros (sqlite3, etc.)
- ❌ NO debe contener lógica de negocio
- ❌ NO debe conocer detalles de HTTP o API

**Ejemplo de archivo**: `src/infrastructure/repositories/base/alumno_repository_base.py`
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.alumno import Alumno

class AlumnoRepositoryBase(ABC):
    """
    Decisión de diseño: Patrón Repository + Dependency Inversion
    
    Esta interfaz define el CONTRATO de lo que puede hacer un repositorio de alumnos,
    sin especificar CÓMO lo hace. Esto permite:
    - Cambiar de SQLite a PostgreSQL sin tocar la lógica de negocio
    - Testear servicios con repositorios mock
    - Mantener el dominio independiente de la infraestructura
    """
    
    @abstractmethod
    def crear(self, alumno: Alumno) -> Alumno:
        """Crea un alumno y retorna el alumno con ID asignado"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        """Obtiene un alumno por ID, retorna None si no existe"""
        pass
    
    @abstractmethod
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """Obtiene un alumno por DNI, retorna None si no existe"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Alumno]:
        """Obtiene todos los alumnos"""
        pass
    
    @abstractmethod
    def actualizar(self, alumno: Alumno) -> Alumno:
        """Actualiza un alumno existente"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un alumno, retorna True si se eliminó"""
        pass
```

**Ejemplo de implementación**: `src/infrastructure/repositories/sqlite/alumno_repository_sqlite.py`
```python
import sqlite3
from typing import List, Optional
from src.domain.entities.alumno import Alumno
from src.infrastructure.repositories.base.alumno_repository_base import AlumnoRepositoryBase
from datetime import datetime

class AlumnoRepositorySQLite(AlumnoRepositoryBase):
    """
    Decisión de diseño: Implementación concreta con SQLite
    
    Esta clase SÍ conoce detalles de SQLite: SQL, conexiones, cursores.
    Pero implementa la interfaz AlumnoRepositoryBase, por lo que puede
    ser reemplazada por otra implementación (PostgreSQL, MongoDB, etc.)
    sin afectar a los servicios que la usan.
    """
    
    def __init__(self, conexion: sqlite3.Connection):
        self.conexion = conexion
    
    def crear(self, alumno: Alumno) -> Alumno:
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT INTO alumno (nombre, apellido, dni, email, cohorte, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (alumno.nombre, alumno.apellido, alumno.dni, alumno.email, alumno.cohorte, datetime.now()))
        
        self.conexion.commit()
        alumno.id = cursor.lastrowid
        alumno.fecha_creacion = datetime.now()
        return alumno
    
    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM alumno WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_alumno(row)
        return None
    
    def _row_to_alumno(self, row) -> Alumno:
        """Convierte una fila de SQLite a entidad Alumno"""
        return Alumno(
            id=row[0],
            nombre=row[1],
            apellido=row[2],
            dni=row[3],
            email=row[4],
            cohorte=row[5],
            fecha_creacion=datetime.fromisoformat(row[6]) if row[6] else None
        )
```

---

### 📡 Capa de Presentación (`src/presentation/api/`)

**Propósito**: Expone la funcionalidad del sistema mediante una API HTTP REST.

**Contenido**:
- **main.py**: Punto de entrada de FastAPI, configuración de la app
- **routers/**: Endpoints agrupados por recurso (alumnos, cursos, etc.)
- **schemas/**: Pydantic models para validación de request/response
- **dependencies.py**: Inyección de dependencias (conexión DB, servicios)
- **middleware/**: CORS, autenticación (futuro)

**Reglas**:
- ✅ Maneja HTTP: request, response, códigos de estado
- ✅ Valida datos de entrada con Pydantic
- ✅ Delega toda la lógica a servicios de aplicación
- ❌ NO debe contener lógica de negocio
- ❌ NO debe acceder directamente a repositorios (solo a través de servicios)

**Ejemplo de archivo**: `src/presentation/api/routers/alumnos.py`
```python
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.services.alumno_service import AlumnoService
from src.presentation.api.schemas.alumno_schema import AlumnoCreateSchema, AlumnoResponseSchema
from src.presentation.api.dependencies import get_alumno_service
from src.domain.exceptions.domain_exceptions import EmailInvalidoException, DNIDuplicadoException

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

@router.post("/", response_model=AlumnoResponseSchema, status_code=status.HTTP_201_CREATED)
def crear_alumno(
    alumno_data: AlumnoCreateSchema,
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """
    Endpoint: POST /alumnos
    
    Decisión de diseño: Este endpoint SOLO se encarga de:
    1. Recibir y validar datos HTTP (Pydantic lo hace automáticamente)
    2. Delegar al servicio de aplicación
    3. Convertir el resultado a formato HTTP (JSON)
    4. Manejar errores y convertirlos a códigos HTTP apropiados
    
    NO contiene lógica de negocio, NO accede a la BD directamente.
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
    
    except EmailInvalidoException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except DNIDuplicadoException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
```

---

## 3. Comunicación Entre Capas

### Flujo de una Request HTTP

```
1. Cliente HTTP
   ↓ (HTTP Request)
2. FastAPI Router (Presentación)
   ↓ (Llama a)
3. Servicio de Aplicación
   ↓ (Usa)
4. Entidades de Dominio + Repositorio (Interfaz)
   ↓ (Implementado por)
5. Repositorio SQLite (Infraestructura)
   ↓ (Accede a)
6. SQLite Database
   ↓ (Retorna datos)
5. Repositorio SQLite
   ↓ (Retorna entidad)
4. Servicio de Aplicación
   ↓ (Retorna entidad)
3. FastAPI Router
   ↓ (Serializa a JSON)
2. Cliente HTTP
```

### Principio de Inversión de Dependencias

```
┌─────────────────────────────────────────────┐
│  Capa de Aplicación (AlumnoService)         │
│  - Depende de AlumnoRepositoryBase          │
│    (INTERFAZ, no implementación)            │
└─────────────────┬───────────────────────────┘
                  │ depende de (interfaz)
                  ↓
┌─────────────────────────────────────────────┐
│  AlumnoRepositoryBase (Interfaz/ABC)        │
│  - Define el contrato                       │
└─────────────────┬───────────────────────────┘
                  ↑ implementa
                  │
┌─────────────────────────────────────────────┐
│  Capa de Infraestructura                    │
│  AlumnoRepositorySQLite                     │
│  - Implementación concreta con SQLite       │
└─────────────────────────────────────────────┘
```

**Ventaja**: Si mañana queremos usar PostgreSQL, solo creamos `AlumnoRepositoryPostgreSQL` que implemente `AlumnoRepositoryBase`, y cambiamos la inyección de dependencias. **No tocamos ni dominio ni aplicación**.

---

## 4. Matriz de Trazabilidad

### Tabla Completa: RF → CU → US → Endpoints → Tests

| **ID RF** | **Requisito Funcional** | **Caso de Uso** | **User Story** | **Endpoint(s)** | **Test(s)** |
|-----------|------------------------|-----------------|----------------|-----------------|-------------|
| **RF-01** | Gestión de Alumnos | CU-10 | US-01 (indirecta) | `POST /alumnos`<br>`GET /alumnos/{id}`<br>`GET /alumnos`<br>`PUT /alumnos/{id}`<br>`DELETE /alumnos/{id}` | `test_crear_alumno`<br>`test_obtener_alumno`<br>`test_listar_alumnos`<br>`test_actualizar_alumno`<br>`test_eliminar_alumno` |
| **RF-02** | Gestión de Cursos | CU-06 | - | `POST /cursos`<br>`GET /cursos/{id}`<br>`GET /cursos` | `test_crear_curso`<br>`test_obtener_curso`<br>`test_listar_cursos` |
| **RF-03** | Gestión de Clases | CU-07 | - | `POST /clases`<br>`GET /clases/{id}`<br>`GET /cursos/{curso_id}/clases` | `test_crear_clase`<br>`test_obtener_clase`<br>`test_listar_clases_curso` |
| **RF-04** | Registro de Asistencia | CU-01 | US-01 | `POST /asistencias`<br>`GET /clases/{clase_id}/asistencias`<br>`PUT /asistencias/{id}` | `test_registrar_asistencia`<br>`test_registrar_asistencias_multiples`<br>`test_obtener_asistencias_clase`<br>`test_actualizar_asistencia` |
| **RF-05** | Registro de Participación | CU-02 | US-03 | `POST /participaciones`<br>`GET /clases/{clase_id}/participaciones` | `test_registrar_participacion`<br>`test_obtener_participaciones_clase` |
| **RF-06** | Registro de TPs | CU-03, CU-08 | - | `POST /trabajos-practicos`<br>`GET /trabajos-practicos/{id}`<br>`GET /cursos/{curso_id}/trabajos-practicos`<br>`POST /entregas-tp`<br>`GET /trabajos-practicos/{tp_id}/entregas` | `test_crear_tp`<br>`test_obtener_tp`<br>`test_listar_tps_curso`<br>`test_registrar_entrega_tp`<br>`test_listar_entregas_tp` |
| **RF-07** | Consulta de Ficha de Alumno | CU-04 | US-04 | `GET /alumnos/{id}/ficha` | `test_obtener_ficha_alumno_completa`<br>`test_obtener_ficha_sin_datos` |
| **RF-08** | Cálculo de Indicadores | CU-04, CU-05 | US-02, US-04, US-05 | (Automático al registrar datos)<br>`GET /alumnos/{id}/ficha`<br>`GET /cursos/{curso_id}/indicadores` | `test_calcular_indicadores_asistencia`<br>`test_calcular_indicadores_participacion`<br>`test_calcular_indicadores_tps`<br>`test_determinar_nivel_riesgo` |
| **RF-09** | Generación de Alertas | CU-05 | US-05 | `GET /alertas/alumnos-en-riesgo` | `test_generar_alertas_asistencia`<br>`test_generar_alertas_tps`<br>`test_listar_alumnos_en_riesgo` |
| **RF-10** | Consulta de Listados | CU-04, CU-05 | US-02, US-05, US-06 | `GET /alumnos`<br>`GET /cursos/{curso_id}/alumnos`<br>`GET /alertas/alumnos-en-riesgo`<br>`GET /clases/{clase_id}/asistencias` | `test_listar_alumnos_por_curso`<br>`test_listar_alumnos_en_riesgo_filtrado`<br>`test_listar_asistencias_clase` |
| **RF-API-01** | Endpoint Crear Alumno | CU-10 | - | `POST /alumnos` | `test_api_crear_alumno_exitoso`<br>`test_api_crear_alumno_dni_duplicado`<br>`test_api_crear_alumno_email_invalido` |
| **RF-API-02** | Endpoint Obtener Alumno | CU-04 | - | `GET /alumnos/{id}` | `test_api_obtener_alumno_existente`<br>`test_api_obtener_alumno_no_existe` |
| **RF-API-03** | Endpoint Listar Alumnos | CU-04 | - | `GET /alumnos` | `test_api_listar_alumnos`<br>`test_api_listar_alumnos_filtro_cohorte` |
| **RF-API-04** | Endpoint Crear Curso | CU-06 | - | `POST /cursos` | `test_api_crear_curso_exitoso`<br>`test_api_crear_curso_datos_invalidos` |
| **RF-API-05** | Endpoint Crear Clase | CU-07 | - | `POST /clases` | `test_api_crear_clase_exitosa`<br>`test_api_crear_clase_curso_no_existe` |
| **RF-API-06** | Endpoint Registrar Asistencia | CU-01 | US-01 | `POST /asistencias` | `test_api_registrar_asistencia_exitosa`<br>`test_api_registrar_asistencias_multiples`<br>`test_api_registrar_asistencia_alumno_no_inscripto` |
| **RF-API-07** | Endpoint Registrar Participación | CU-02 | US-03 | `POST /participaciones` | `test_api_registrar_participacion_exitosa`<br>`test_api_registrar_participacion_nivel_invalido` |
| **RF-API-08** | Endpoint Crear TP | CU-08 | - | `POST /trabajos-practicos` | `test_api_crear_tp_exitoso` |
| **RF-API-09** | Endpoint Registrar Entrega TP | CU-03 | - | `POST /entregas-tp` | `test_api_registrar_entrega_tp_exitosa`<br>`test_api_registrar_entrega_tp_tardia` |
| **RF-API-10** | Endpoint Ficha de Alumno | CU-04 | US-04 | `GET /alumnos/{id}/ficha` | `test_api_obtener_ficha_completa`<br>`test_api_obtener_ficha_con_indicadores` |
| **RF-API-11** | Endpoint Alumnos en Riesgo | CU-05 | US-05 | `GET /alertas/alumnos-en-riesgo` | `test_api_listar_alumnos_riesgo_alto`<br>`test_api_listar_alumnos_riesgo_filtro_curso` |

---

### Matriz de Trazabilidad: User Stories → Criterios de Aceptación → Endpoints

| **User Story** | **Criterios de Aceptación (BDD)** | **Endpoint(s) Relacionados** |
|----------------|-----------------------------------|------------------------------|
| **US-01**: Tomar asistencia rápidamente | - Given clase con 30 alumnos<br>- When accedo al registro<br>- Then veo lista completa<br>- And puedo marcar todos en <2min | `POST /asistencias`<br>`GET /clases/{clase_id}/asistencias` |
| **US-02**: Ver quién está en riesgo en mi materia | - Given alumnos con diferentes niveles<br>- When consulto estado del curso<br>- Then veo listado destacando riesgo alto/medio | `GET /alertas/alumnos-en-riesgo?curso_id={id}`<br>`GET /cursos/{curso_id}/indicadores` |
| **US-03**: Registrar participación destacada | - Given estoy en una clase<br>- When alumno participa<br>- Then puedo registrar nivel + comentario<br>- And se refleja en ficha | `POST /participaciones`<br>`GET /alumnos/{id}/ficha` |
| **US-04**: Consultar historial de un alumno | - Given alumno inscripto<br>- When consulto ficha<br>- Then veo asistencia, participación, TPs, indicadores | `GET /alumnos/{id}/ficha` |
| **US-05**: Identificar alumnos en riesgo de deserción | - Given alumnos con diferentes riesgos<br>- When accedo a dashboard de alertas<br>- Then veo listado ordenado por riesgo<br>- And puedo filtrar por carrera/cohorte/materia | `GET /alertas/alumnos-en-riesgo`<br>`GET /alertas/alumnos-en-riesgo?nivel=Alto`<br>`GET /alertas/alumnos-en-riesgo?curso_id={id}` |
| **US-06**: Analizar tendencias por materia | - Given múltiples cursos con datos<br>- When consulto reporte por materia<br>- Then veo % asistencia, % riesgo, % TPs<br>- And puedo comparar | `GET /cursos/{curso_id}/indicadores`<br>`GET /cursos` (con estadísticas agregadas - futuro) |
| **US-07**: Exportar datos para análisis | - Given datos en el sistema<br>- When solicito exportar<br>- Then puedo elegir qué exportar<br>- And filtrar por fecha/curso/cohorte<br>- And descargo archivo estándar | (Futuro: `GET /exportar/alumnos`, `GET /exportar/asistencias`, etc.) |

---

## 5. Plan de Implementación por Fases

### **Fase 1: Fundamentos (MVP Core)** ✅
**Duración estimada**: 2-3 semanas

**Objetivos**:
- Estructura de proyecto completa
- Capa de dominio con entidades principales
- Capa de infraestructura con SQLite
- Capa de aplicación con servicios básicos
- API mínima funcional

**Tareas**:
1. ✅ Crear estructura de carpetas
2. ✅ Implementar entidades de dominio:
   - Alumno, Curso, Inscripcion, Clase
   - RegistroAsistencia, RegistroParticipacion
   - TrabajoPractico, EntregaTP
   - Enums (EstadoAsistencia, NivelParticipacion, NivelRiesgo)
3. ✅ Crear schema de SQLite (`schema.sql`)
4. ✅ Implementar repositorios base (interfaces)
5. ✅ Implementar repositorios SQLite
6. ✅ Implementar servicios de aplicación:
   - AlumnoService
   - CursoService
   - InscripcionService
   - ClaseService
   - AsistenciaService
   - ParticipacionService
   - TrabajoPracticoService
7. ✅ Crear API con FastAPI:
   - Routers para alumnos, cursos, clases, asistencias, participaciones, TPs
   - Schemas de Pydantic
   - Inyección de dependencias
8. ✅ Tests unitarios básicos

**Entregable**: API funcional que permite CRUD de alumnos, cursos, clases, y registro de asistencia/participación/TPs.

---

### **Fase 2: Cálculo de Indicadores y Alertas** 🔄
**Duración estimada**: 1-2 semanas

**Objetivos**:
- Implementar cálculo automático de indicadores de riesgo
- Generar alertas
- Endpoint de ficha completa de alumno
- Endpoint de alumnos en riesgo

**Tareas**:
1. ✅ Implementar `IndicadorRiesgo` (value object)
2. ✅ Implementar `IndicadorRiesgoService`:
   - `calcular_indicadores(alumno_id, curso_id)`
   - `determinar_nivel_riesgo()`
   - `generar_alertas()`
   - `obtener_alumnos_en_riesgo(filtros)`
   - `obtener_estadisticas_curso(curso_id)`
3. ✅ Integrar cálculo automático al registrar asistencia/participación/TPs
4. ✅ Crear endpoints:
   - `GET /alumnos/{id}/ficha`
   - `GET /alertas/alumnos-en-riesgo`
   - `GET /cursos/{curso_id}/indicadores`
5. ✅ Tests de cálculo de indicadores
6. ✅ Tests de generación de alertas

**Entregable**: Sistema completo de detección de riesgo funcionando.

---

### **Fase 3: Preparación para Vercel** 🚀
**Duración estimada**: 1 semana

**Objetivos**:
- Adaptar código para despliegue serverless en Vercel
- Configurar variables de entorno
- Documentación de despliegue

**Tareas**:
1. ✅ Crear `api/index.py` (entrypoint para Vercel)
2. ✅ Configurar `vercel.json`
3. ✅ Adaptar gestión de conexión SQLite para serverless
4. ✅ Configurar variables de entorno (`.env.example`)
5. ✅ Documentar proceso de despliegue
6. ✅ Probar despliegue en Vercel

**Entregable**: API desplegada y funcionando en Vercel.

---

### **Fase 4: Autenticación y Roles** 🔐 (Futuro)
**Duración estimada**: 2-3 semanas

**Objetivos**:
- Sistema de login con JWT
- Roles: Docente, Coordinación, Estudiante, Admin
- Permisos por rol (RBAC)

**Tareas**:
1. Implementar entidad `Usuario`
2. Implementar `UsuarioService` y `AuthService`
3. Crear endpoints de autenticación:
   - `POST /auth/login`
   - `POST /auth/register`
   - `POST /auth/refresh`
4. Implementar middleware de autenticación JWT
5. Implementar middleware de autorización por roles
6. Proteger endpoints según roles
7. Permitir a estudiantes ver su propia ficha

**Entregable**: Sistema con login completo y control de acceso.

---

### **Fase 5: Frontend Web** 🎨 (Futuro)
**Duración estimada**: 4-6 semanas

**Objetivos**:
- Interfaz web completa para docentes y coordinación
- Dashboard de alertas
- Portal de estudiantes

**Tareas**:
1. Elegir stack frontend (React/Vue/Svelte)
2. Implementar componentes:
   - Login
   - Dashboard de coordinación
   - Registro de asistencia para docentes
   - Ficha de alumno
   - Portal de estudiantes
3. Integrar con API
4. Desplegar frontend en Vercel

**Entregable**: Aplicación web completa.

---

### **Fase 6: Funcionalidades Avanzadas** 🚀 (Futuro)
**Duración estimada**: Variable

**Objetivos**:
- Notificaciones automáticas
- Reportes y gráficos
- Predicción de riesgo con ML
- Exportación de datos

**Tareas**:
1. Implementar sistema de notificaciones (email/SMS)
2. Crear reportes PDF/Excel
3. Implementar gráficos y visualizaciones
4. Entrenar modelo de ML para predicción de riesgo
5. Crear endpoints de exportación

**Entregable**: Sistema con funcionalidades avanzadas.

---

### **Fase 7: Migración a BBDD Externa** 🗄️ (Futuro)
**Duración estimada**: 2-3 semanas

**Objetivos**:
- Migrar de SQLite a PostgreSQL
- Despliegue en servidor dedicado o cloud

**Tareas**:
1. Crear `AlumnoRepositoryPostgreSQL` (y demás repositorios)
2. Implementar migraciones de schema
3. Configurar conexión a PostgreSQL
4. Cambiar inyección de dependencias
5. Probar migración con datos reales
6. Configurar backups automáticos

**Entregable**: Sistema funcionando con PostgreSQL.

---

## 6. Resumen de Decisiones de Arquitectura

### ✅ Decisiones Tomadas

1. **Arquitectura por Capas (Layered Architecture)**
   - **Por qué**: Separación clara de responsabilidades, fácil de entender y mantener
   - **Capas**: Domain, Application, Infrastructure, Presentation

2. **Patrón Repository**
   - **Por qué**: Abstrae el acceso a datos, permite cambiar de BD sin tocar lógica de negocio
   - **Implementación**: Interfaces en `repositories/base/`, implementaciones en `repositories/sqlite/`

3. **Inversión de Dependencias (Dependency Inversion)**
   - **Por qué**: Servicios dependen de interfaces, no de implementaciones concretas
   - **Beneficio**: Facilita testing, permite cambiar implementaciones

4. **Inyección de Dependencias**
   - **Por qué**: Facilita testing, desacopla componentes
   - **Implementación**: FastAPI Depends + `dependencies.py`

5. **SQLite para MVP, preparado para PostgreSQL**
   - **Por qué**: SQLite es simple para MVP, pero el diseño permite migrar fácilmente
   - **Preparación**: Uso de repositorios abstractos

6. **FastAPI como framework web**
   - **Por qué**: Moderno, rápido, con validación automática (Pydantic), compatible con Vercel
   - **Beneficio**: Documentación automática (Swagger), type hints nativos

7. **Value Objects para Indicadores**
   - **Por qué**: Los indicadores se calculan, no se persisten directamente (en el MVP)
   - **Beneficio**: Lógica de cálculo centralizada

8. **Enums para Estados**
   - **Por qué**: Evita strings mágicos, facilita validación
   - **Implementación**: `EstadoAsistencia`, `NivelParticipacion`, `NivelRiesgo`

---

**Siguiente paso**: [Implementación en Python (Prompt 2)](./05_IMPLEMENTACION_PYTHON.md)
