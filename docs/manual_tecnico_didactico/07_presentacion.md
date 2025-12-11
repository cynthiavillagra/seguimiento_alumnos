# Capítulo 7: Capa de Presentación

## 7.1 ¿Qué es la Capa de Presentación?

Es la **interfaz** con el mundo exterior. En nuestro caso: una API REST.

### Responsabilidades

- ✅ Recibir requests HTTP
- ✅ Validar formato de datos (con Pydantic)
- ✅ Delegar al servicio
- ✅ Devolver responses HTTP
- ✅ Convertir excepciones a códigos HTTP

### Lo que NO hace

- ❌ Lógica de negocio
- ❌ Acceso a base de datos
- ❌ SQL

---

## 7.2 Schemas (DTOs) con Pydantic

Los Schemas definen **qué forma tienen los datos** que entran y salen.

Crear `src/presentation/api/schemas/alumno.py`:

```python
"""
Schemas de Alumno
-----------------
Definen la forma de los datos para la API.

- AlumnoCreateSchema: para crear (entrada)
- AlumnoUpdateSchema: para actualizar (entrada)
- AlumnoResponseSchema: para respuestas (salida)
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from src.domain.entities import Alumno


class AlumnoCreateSchema(BaseModel):
    """
    Schema para crear un alumno.
    
    Pydantic valida automáticamente:
    - Tipos de datos
    - Campos requeridos
    - Formatos especiales (EmailStr)
    - Longitudes (min_length, max_length)
    """
    nombre: str = Field(
        ...,  # ... significa "requerido"
        min_length=1,
        max_length=100,
        description="Nombre del alumno"
    )
    apellido: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Apellido del alumno"
    )
    dni: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="DNI (único)"
    )
    email: EmailStr = Field(
        ...,
        description="Email válido"
    )


class AlumnoUpdateSchema(BaseModel):
    """
    Schema para actualizar un alumno.
    Todos los campos son opcionales.
    """
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    dni: Optional[str] = Field(None, min_length=1, max_length=20)
    email: Optional[EmailStr] = None


class AlumnoResponseSchema(BaseModel):
    """
    Schema para devolver un alumno.
    Incluye campos calculados.
    """
    id: int
    nombre: str
    apellido: str
    dni: str
    email: str
    nombre_completo: str  # Campo calculado
    
    @classmethod
    def from_entity(cls, alumno: Alumno) -> 'AlumnoResponseSchema':
        """
        Crea el schema desde una entidad.
        
        Este método evita repetir la conversión en cada endpoint.
        """
        return cls(
            id=alumno.id,
            nombre=alumno.nombre,
            apellido=alumno.apellido,
            dni=alumno.dni,
            email=alumno.email,
            nombre_completo=alumno.nombre_completo
        )


class AlumnoListResponseSchema(BaseModel):
    """Schema para listar alumnos."""
    total: int
    alumnos: list[AlumnoResponseSchema]
```

### ¿Por qué separar entrada y salida?

```python
# Entrada: lo que el usuario envía
{
    "nombre": "Juan",
    "apellido": "Pérez",
    "dni": "12345678",
    "email": "juan@mail.com"
}

# Salida: lo que devolvemos (incluye campos extra)
{
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "dni": "12345678",
    "email": "juan@mail.com",
    "nombre_completo": "Pérez, Juan"  # ← Calculado
}
```

---

## 7.3 Schema de Cursos

Crear `src/presentation/api/schemas/curso.py`:

```python
"""Schemas de Curso"""

from pydantic import BaseModel, Field
from typing import Optional

from src.domain.entities import Curso


class CursoCreateSchema(BaseModel):
    """Schema para crear un curso."""
    nombre_materia: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre de la materia"
    )
    anio: int = Field(
        ...,
        ge=2000,
        le=2100,
        description="Año del curso"
    )
    cuatrimestre: int = Field(
        ...,
        ge=1,
        le=2,
        description="Cuatrimestre (1 o 2)"
    )


class CursoUpdateSchema(BaseModel):
    """Schema para actualizar un curso."""
    nombre_materia: Optional[str] = Field(None, min_length=1, max_length=100)
    anio: Optional[int] = Field(None, ge=2000, le=2100)
    cuatrimestre: Optional[int] = Field(None, ge=1, le=2)


class CursoResponseSchema(BaseModel):
    """Schema de respuesta de curso."""
    id: int
    nombre_materia: str
    anio: int
    cuatrimestre: int
    nombre_completo: str
    
    @classmethod
    def from_entity(cls, curso: Curso) -> 'CursoResponseSchema':
        return cls(
            id=curso.id,
            nombre_materia=curso.nombre_materia,
            anio=curso.anio,
            cuatrimestre=curso.cuatrimestre,
            nombre_completo=curso.nombre_completo
        )


class CursoListResponseSchema(BaseModel):
    """Schema para listar cursos."""
    total: int
    cursos: list[CursoResponseSchema]
```

---

## 7.4 Schema de Inscripciones

Crear `src/presentation/api/schemas/inscripcion.py`:

```python
"""Schemas de Inscripción"""

from pydantic import BaseModel, Field
from src.presentation.api.schemas.alumno import AlumnoResponseSchema


class InscripcionCreateSchema(BaseModel):
    """Schema para crear una inscripción."""
    alumno_id: int = Field(..., gt=0, description="ID del alumno")
    curso_id: int = Field(..., gt=0, description="ID del curso")


class InscripcionResponseSchema(BaseModel):
    """Schema de respuesta de inscripción."""
    mensaje: str
    alumno_id: int
    curso_id: int


class AlumnosDeCursoResponseSchema(BaseModel):
    """Schema para listar alumnos de un curso."""
    curso_id: int
    total: int
    alumnos: list[AlumnoResponseSchema]
```

---

## 7.5 Router de Alumnos

Crear `src/presentation/api/routers/alumnos.py`:

```python
"""
Router de Alumnos
-----------------
Define los endpoints HTTP para alumnos.

Endpoints:
- GET    /api/alumnos/      → Listar
- GET    /api/alumnos/{id}  → Obtener uno
- POST   /api/alumnos/      → Crear
- PUT    /api/alumnos/{id}  → Actualizar
- DELETE /api/alumnos/{id}  → Eliminar
"""

from fastapi import APIRouter, HTTPException, status

from src.application.services import AlumnoService
from src.domain.exceptions import (
    AlumnoNoEncontradoException,
    DNIDuplicadoException
)
from src.presentation.api.schemas.alumno import (
    AlumnoCreateSchema,
    AlumnoUpdateSchema,
    AlumnoResponseSchema,
    AlumnoListResponseSchema
)


# Crear router con prefijo
router = APIRouter(
    prefix="/alumnos",
    tags=["Alumnos"]  # Agrupa en Swagger
)

# Instancia del servicio
service = AlumnoService()


@router.get(
    "/",
    response_model=AlumnoListResponseSchema,
    summary="Listar alumnos"
)
def listar_alumnos():
    """
    Obtiene la lista de todos los alumnos.
    """
    alumnos = service.listar()
    
    return AlumnoListResponseSchema(
        total=len(alumnos),
        alumnos=[AlumnoResponseSchema.from_entity(a) for a in alumnos]
    )


@router.get(
    "/{alumno_id}",
    response_model=AlumnoResponseSchema,
    summary="Obtener un alumno"
)
def obtener_alumno(alumno_id: int):
    """
    Obtiene un alumno por su ID.
    """
    try:
        alumno = service.obtener(alumno_id)
        return AlumnoResponseSchema.from_entity(alumno)
    
    except AlumnoNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/",
    response_model=AlumnoResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear alumno"
)
def crear_alumno(data: AlumnoCreateSchema):
    """
    Crea un nuevo alumno.
    
    - **nombre**: Nombre del alumno
    - **apellido**: Apellido del alumno
    - **dni**: DNI único
    - **email**: Email válido
    """
    try:
        alumno = service.crear(
            nombre=data.nombre,
            apellido=data.apellido,
            dni=data.dni,
            email=data.email
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


@router.put(
    "/{alumno_id}",
    response_model=AlumnoResponseSchema,
    summary="Actualizar alumno"
)
def actualizar_alumno(alumno_id: int, data: AlumnoUpdateSchema):
    """
    Actualiza un alumno existente.
    Solo los campos enviados se actualizan.
    """
    try:
        alumno = service.actualizar(
            alumno_id=alumno_id,
            nombre=data.nombre,
            apellido=data.apellido,
            dni=data.dni,
            email=data.email
        )
        return AlumnoResponseSchema.from_entity(alumno)
    
    except AlumnoNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DNIDuplicadoException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete(
    "/{alumno_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar alumno"
)
def eliminar_alumno(alumno_id: int):
    """
    Elimina un alumno por su ID.
    """
    eliminado = service.eliminar(alumno_id)
    
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno {alumno_id} no encontrado"
        )
    
    return None
```

---

## 7.6 Router de Cursos

Crear `src/presentation/api/routers/cursos.py`:

```python
"""Router de Cursos"""

from fastapi import APIRouter, HTTPException, status

from src.application.services import CursoService
from src.domain.exceptions import CursoNoEncontradoException
from src.presentation.api.schemas.curso import (
    CursoCreateSchema,
    CursoUpdateSchema,
    CursoResponseSchema,
    CursoListResponseSchema
)


router = APIRouter(prefix="/cursos", tags=["Cursos"])
service = CursoService()


@router.get("/", response_model=CursoListResponseSchema, summary="Listar cursos")
def listar_cursos():
    """Obtiene la lista de todos los cursos."""
    cursos = service.listar()
    return CursoListResponseSchema(
        total=len(cursos),
        cursos=[CursoResponseSchema.from_entity(c) for c in cursos]
    )


@router.get("/{curso_id}", response_model=CursoResponseSchema, summary="Obtener curso")
def obtener_curso(curso_id: int):
    """Obtiene un curso por ID."""
    try:
        curso = service.obtener(curso_id)
        return CursoResponseSchema.from_entity(curso)
    except CursoNoEncontradoException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/",
    response_model=CursoResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear curso"
)
def crear_curso(data: CursoCreateSchema):
    """Crea un nuevo curso."""
    try:
        curso = service.crear(
            nombre_materia=data.nombre_materia,
            anio=data.anio,
            cuatrimestre=data.cuatrimestre
        )
        return CursoResponseSchema.from_entity(curso)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{curso_id}", response_model=CursoResponseSchema, summary="Actualizar curso")
def actualizar_curso(curso_id: int, data: CursoUpdateSchema):
    """Actualiza un curso existente."""
    try:
        curso = service.actualizar(
            curso_id=curso_id,
            nombre_materia=data.nombre_materia,
            anio=data.anio,
            cuatrimestre=data.cuatrimestre
        )
        return CursoResponseSchema.from_entity(curso)
    except CursoNoEncontradoException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{curso_id}", status_code=204, summary="Eliminar curso")
def eliminar_curso(curso_id: int):
    """Elimina un curso por ID."""
    if not service.eliminar(curso_id):
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return None
```

---

## 7.7 Router de Inscripciones

Crear `src/presentation/api/routers/inscripciones.py`:

```python
"""Router de Inscripciones"""

from fastapi import APIRouter, HTTPException, status

from src.application.services import InscripcionService
from src.domain.exceptions import (
    AlumnoNoEncontradoException,
    CursoNoEncontradoException,
    InscripcionDuplicadaException
)
from src.presentation.api.schemas.inscripcion import (
    InscripcionCreateSchema,
    InscripcionResponseSchema,
    AlumnosDeCursoResponseSchema
)
from src.presentation.api.schemas.alumno import AlumnoResponseSchema


router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])
service = InscripcionService()


@router.post(
    "/",
    response_model=InscripcionResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Inscribir alumno"
)
def inscribir(data: InscripcionCreateSchema):
    """Inscribe un alumno en un curso."""
    try:
        inscripcion = service.inscribir(data.alumno_id, data.curso_id)
        return InscripcionResponseSchema(
            mensaje="Inscripción exitosa",
            alumno_id=inscripcion.alumno_id,
            curso_id=inscripcion.curso_id
        )
    
    except AlumnoNoEncontradoException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except CursoNoEncontradoException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except InscripcionDuplicadaException as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get(
    "/curso/{curso_id}",
    response_model=AlumnosDeCursoResponseSchema,
    summary="Alumnos de un curso"
)
def alumnos_de_curso(curso_id: int):
    """Obtiene los alumnos inscriptos en un curso."""
    try:
        alumnos = service.alumnos_de_curso(curso_id)
        return AlumnosDeCursoResponseSchema(
            curso_id=curso_id,
            total=len(alumnos),
            alumnos=[AlumnoResponseSchema.from_entity(a) for a in alumnos]
        )
    
    except CursoNoEncontradoException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{alumno_id}/{curso_id}", status_code=204, summary="Desinscribir")
def desinscribir(alumno_id: int, curso_id: int):
    """Elimina la inscripción de un alumno en un curso."""
    if not service.desinscribir(alumno_id, curso_id):
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return None
```

---

## 7.8 Actualizar main.py

Modificar `src/presentation/api/main.py`:

```python
"""
Aplicación Principal FastAPI
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.presentation.api.routers import alumnos, cursos, inscripciones


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicación."""
    print("🚀 Iniciando aplicación...")
    
    # Cargar .env si existe
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip().strip('"')
    except FileNotFoundError:
        pass
    
    # Inicializar BD
    try:
        from src.infrastructure.database.connection import inicializar_tablas
        inicializar_tablas()
    except Exception as e:
        print(f"⚠️ Error BD: {e}")
    
    yield
    
    print("👋 Cerrando aplicación...")


# Crear app
app = FastAPI(
    title="Sistema de Gestión - MVP",
    description="API para gestión de alumnos y cursos",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(alumnos.router, prefix="/api")
app.include_router(cursos.router, prefix="/api")
app.include_router(inscripciones.router, prefix="/api")


# Health check
@app.get("/api", tags=["Health"])
def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "endpoints": {
            "alumnos": "/api/alumnos/",
            "cursos": "/api/cursos/",
            "inscripciones": "/api/inscripciones/"
        }
    }


# Frontend (si existe)
if not os.environ.get("VERCEL"):
    try:
        app.mount("/", StaticFiles(directory="public", html=True), name="public")
    except:
        pass
```

---

## 7.9 Actualizar __init__.py

`src/presentation/api/routers/__init__.py`:

```python
"""Exportar routers"""
from . import alumnos, cursos, inscripciones
```

`src/presentation/api/schemas/__init__.py`:

```python
"""Exportar schemas"""
from .alumno import *
from .curso import *
from .inscripcion import *
```

---

## 7.10 Probar la API

Ejecutar servidor:

```powershell
uvicorn src.presentation.api.main:app --reload
```

Abrir http://localhost:8000/docs y probar:

1. **POST /api/alumnos/** - Crear alumno
2. **GET /api/alumnos/** - Listar alumnos
3. **POST /api/cursos/** - Crear curso
4. **POST /api/inscripciones/** - Inscribir alumno

---

## 7.11 Resumen

### Archivos creados

```
src/presentation/
└── api/
    ├── main.py                 ✅
    ├── routers/
    │   ├── alumnos.py          ✅
    │   ├── cursos.py           ✅
    │   └── inscripciones.py    ✅
    └── schemas/
        ├── alumno.py           ✅
        ├── curso.py            ✅
        └── inscripcion.py      ✅
```

### Códigos HTTP usados

| Código | Cuándo |
|--------|--------|
| 200 | OK (GET, PUT) |
| 201 | Creado (POST) |
| 204 | Sin contenido (DELETE) |
| 400 | Datos inválidos |
| 404 | No encontrado |
| 409 | Conflicto (duplicado) |

---

**Anterior:** [Capítulo 6 - Aplicación](./06_aplicacion.md)

**Siguiente:** [Capítulo 8 - Frontend](./08_frontend.md)
