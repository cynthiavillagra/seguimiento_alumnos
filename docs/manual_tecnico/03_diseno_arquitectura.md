# Capítulo 3: Diseño y Arquitectura

## 3.1 Decisiones Arquitectónicas

Antes de escribir código, debemos tomar decisiones importantes sobre cómo estructurar el proyecto. Estas decisiones afectarán todo el desarrollo.

### ¿Por qué una arquitectura por capas?

Existen muchos patrones arquitectónicos:

| Patrón | Descripción | Cuándo usarlo |
|--------|-------------|---------------|
| **Monolito simple** | Todo en un archivo/carpeta | Proyectos muy pequeños |
| **MVC** | Model-View-Controller | Apps web tradicionales |
| **Capas (Layered)** | Separación por responsabilidad | APIs, servicios |
| **Microservicios** | Servicios independientes | Sistemas grandes, equipos grandes |
| **Hexagonal** | Puertos y adaptadores | Alta testabilidad |

**Elegimos Arquitectura por Capas** porque:

1. **Educativo**: Es fácil de entender y enseñar
2. **Equilibrado**: No es tan simple como "todo junto" ni tan complejo como microservicios
3. **Testeable**: Cada capa se puede probar por separado
4. **Escalable**: Fácil agregar funcionalidades
5. **Profesional**: Es lo que se usa en empresas reales

## 3.2 Las Cuatro Capas

### Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│     CAPA DE PRESENTACIÓN (src/presentation/)                   │
│     ─────────────────────────────────────────                   │
│     • Routers de FastAPI (endpoints HTTP)                       │
│     • Schemas de Pydantic (validación de entrada/salida)        │
│     • Manejo de errores HTTP                                    │
│                                                                 │
│     Responsabilidad: Recibir requests, devolver responses       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Llama a...
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│     CAPA DE APLICACIÓN (src/application/)                       │
│     ─────────────────────────────────────                       │
│     • Servicios de negocio                                      │
│     • Orquestación de operaciones                               │
│     • Validaciones de negocio                                   │
│                                                                 │
│     Responsabilidad: Lógica de negocio, casos de uso            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Usa entidades de...
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│     CAPA DE DOMINIO (src/domain/)                               │
│     ─────────────────────────────                               │
│     • Entidades (Alumno, Curso, Clase, etc.)                    │
│     • Excepciones de dominio                                    │
│     • Interfaces (contratos de repositorios)                    │
│                                                                 │
│     Responsabilidad: Representar conceptos del negocio          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Implementado por...
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│     CAPA DE INFRAESTRUCTURA (src/infrastructure/)               │
│     ─────────────────────────────────────────────               │
│     • Repositorios (acceso a base de datos)                     │
│     • Conexión a PostgreSQL                                     │
│     • Schemas de base de datos                                  │
│                                                                 │
│     Responsabilidad: Implementar detalles técnicos              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Regla de Dependencia

**Las capas superiores pueden depender de las inferiores, pero NO al revés.**

```
✅ Presentación → Aplicación → Dominio → Infraestructura
❌ Infraestructura → Dominio (NO PERMITIDO)
```

Esto significa:
- Un **Router** puede usar un **Servicio**
- Un **Servicio** puede usar un **Repositorio**
- Un **Repositorio** NO puede usar un **Servicio**

## 3.3 Patrones de Diseño Utilizados

### Patrón Repository

El **Repository Pattern** abstrae el acceso a datos.

**¿Por qué usarlo?**

Sin Repository:
```python
# ❌ MAL: El servicio conoce detalles de la base de datos
class AlumnoService:
    def crear_alumno(self, nombre, apellido, dni):
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO alumno (nombre, apellido, dni) VALUES (?, ?, ?)", 
                      (nombre, apellido, dni))
        conexion.commit()
```

Con Repository:
```python
# ✅ BIEN: El servicio no sabe cómo se guarda
class AlumnoService:
    def __init__(self, alumno_repo):
        self.alumno_repo = alumno_repo
    
    def crear_alumno(self, nombre, apellido, dni):
        alumno = Alumno(nombre=nombre, apellido=apellido, dni=dni)
        return self.alumno_repo.crear(alumno)
```

**Ventajas:**
1. El servicio no conoce SQL ni la base de datos
2. Podemos cambiar de PostgreSQL a MongoDB sin tocar el servicio
3. Podemos crear un "repositorio falso" para tests

### Patrón Dependency Injection

La **Inyección de Dependencias** permite que un objeto reciba sus dependencias desde afuera.

```python
# ❌ MAL: El servicio crea su dependencia
class AlumnoService:
    def __init__(self):
        self.repo = AlumnoRepositoryPostgres()  # Dependencia fija

# ✅ BIEN: La dependencia viene de afuera
class AlumnoService:
    def __init__(self, repo):  # Recibe la dependencia
        self.repo = repo

# Uso:
repo = AlumnoRepositoryPostgres(conexion)
service = AlumnoService(repo)  # "Inyectamos" el repo
```

FastAPI facilita esto con `Depends()`:

```python
def get_alumno_service():
    conexion = get_db_connection()
    repo = AlumnoRepositoryPostgres(conexion)
    return AlumnoService(repo)

@router.get("/")
def listar(service: AlumnoService = Depends(get_alumno_service)):
    return service.listar_alumnos()
```

### Patrón DTO (Data Transfer Object)

Los **DTOs** son objetos simples para transferir datos entre capas.

En FastAPI usamos **Pydantic Schemas** como DTOs:

```python
# Schema para crear (entrada)
class AlumnoCreateSchema(BaseModel):
    nombre: str
    apellido: str
    dni: str
    email: str
    cohorte: int

# Schema para respuesta (salida)
class AlumnoResponseSchema(BaseModel):
    id: int
    nombre: str
    apellido: str
    nombre_completo: str
```

**¿Por qué separar entrada y salida?**

- La **entrada** tiene campos que el usuario envía
- La **salida** puede tener campos calculados (ej: `nombre_completo`)
- No exponemos datos internos (ej: contraseñas hasheadas)

## 3.4 Diseño de la API REST

### Principios REST

REST (Representational State Transfer) define convenciones para APIs web:

| Principio | Descripción | Ejemplo |
|-----------|-------------|---------|
| **Recursos** | URLs representan "cosas" | `/alumnos`, `/cursos` |
| **Verbos HTTP** | Indican la acción | GET=leer, POST=crear |
| **Sin estado** | Cada request es independiente | No hay sesión |
| **Respuestas JSON** | Formato estándar | `{"id": 1, "nombre": "Juan"}` |

### Endpoints Diseñados

#### Alumnos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/alumnos/` | Listar todos los alumnos |
| GET | `/api/alumnos/{id}` | Obtener un alumno |
| POST | `/api/alumnos/` | Crear alumno |
| PUT | `/api/alumnos/{id}` | Actualizar alumno |
| DELETE | `/api/alumnos/{id}` | Eliminar alumno |

#### Cursos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/cursos/` | Listar cursos |
| GET | `/api/cursos/{id}` | Obtener un curso |
| POST | `/api/cursos/` | Crear curso |
| PUT | `/api/cursos/{id}` | Actualizar curso |
| DELETE | `/api/cursos/{id}` | Eliminar curso |

#### Inscripciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/inscripciones/curso/{curso_id}` | Alumnos de un curso |
| GET | `/api/inscripciones/alumno/{alumno_id}` | Cursos de un alumno |
| POST | `/api/inscripciones/` | Inscribir alumno |
| DELETE | `/api/inscripciones/{id}` | Desinscribir |

#### Clases

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/clases/curso/{curso_id}` | Clases de un curso |
| GET | `/api/clases/{id}` | Obtener una clase |
| POST | `/api/clases/` | Crear clase |

#### Asistencias

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/asistencias/clase/{clase_id}` | Asistencias de una clase |
| POST | `/api/asistencias/` | Registrar asistencia |
| PUT | `/api/asistencias/{id}` | Modificar asistencia |

#### Trabajos Prácticos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tps/` | Listar todos los TPs |
| GET | `/api/tps/curso/{curso_id}` | TPs de un curso |
| POST | `/api/tps/` | Crear TP |
| PUT | `/api/tps/{id}` | Actualizar TP |
| DELETE | `/api/tps/{id}` | Eliminar TP |

#### Entregas de TPs

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/entregas/` | Registrar entrega |
| GET | `/api/entregas/tp/{tp_id}` | Entregas de un TP |
| GET | `/api/entregas/alumno/{alumno_id}` | Entregas de un alumno |

### Códigos de Estado HTTP

| Código | Significado | Cuándo usarlo |
|--------|-------------|---------------|
| 200 | OK | Operación exitosa |
| 201 | Created | Recurso creado |
| 204 | No Content | Eliminación exitosa |
| 400 | Bad Request | Datos inválidos |
| 404 | Not Found | Recurso no existe |
| 409 | Conflict | Duplicado (ej: DNI) |
| 500 | Server Error | Error interno |

## 3.5 Diseño de la Base de Datos

### Diagrama Entidad-Relación

```
┌─────────────────┐
│     ALUMNO      │
├─────────────────┤
│ PK id           │
│    nombre       │
│    apellido     │
│ UK dni          │
│    email        │
│    cohorte      │
│    fecha_creacion│
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐          ┌─────────────────┐
│  INSCRIPCION    │          │     CURSO       │
├─────────────────┤          ├─────────────────┤
│ PK id           │          │ PK id           │
│ FK alumno_id ───┼──────────│    nombre_materia│
│ FK curso_id  ───┼─────────►│    anio         │
│    fecha_inscr  │          │    cuatrimestre │
└────────┬────────┘          │    docente      │
         │                   │    fecha_creacion│
         │                   └────────┬────────┘
         │                            │
         │                            │ 1:N
         ▼                            ▼
┌─────────────────┐          ┌─────────────────┐
│ REG_ASISTENCIA  │          │     CLASE       │
├─────────────────┤          ├─────────────────┤
│ PK id           │          │ PK id           │
│ FK alumno_id    │          │ FK curso_id     │
│ FK clase_id  ───┼─────────►│    fecha        │
│    estado       │          │    numero_clase │
│    fecha_registro│         │    tema         │
└─────────────────┘          │    fecha_creacion│
                             └─────────────────┘

┌─────────────────┐          ┌─────────────────┐
│   ENTREGA_TP    │          │ TRABAJO_PRACTICO│
├─────────────────┤          ├─────────────────┤
│ PK id           │          │ PK id           │
│ FK tp_id     ───┼─────────►│ FK curso_id     │
│ FK alumno_id    │          │    titulo       │
│    fecha_real   │          │    descripcion  │
│    entregado    │          │    fecha_entrega│
│    es_tardia    │          │    fecha_creacion│
│    estado       │          └─────────────────┘
│    nota         │
│    observaciones│
└─────────────────┘
```

### SQL de Creación (PostgreSQL)

```sql
-- Tabla ALUMNO
CREATE TABLE IF NOT EXISTS alumno (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    cohorte INTEGER NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (length(nombre) > 0),
    CHECK (length(apellido) > 0),
    CHECK (email LIKE '%@%'),
    CHECK (cohorte >= 2000 AND cohorte <= 2100)
);

-- Tabla CURSO
CREATE TABLE IF NOT EXISTS curso (
    id SERIAL PRIMARY KEY,
    nombre_materia TEXT NOT NULL,
    anio INTEGER NOT NULL,
    cuatrimestre INTEGER NOT NULL,
    docente_responsable TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (cuatrimestre IN (1, 2)),
    CHECK (anio >= 2000 AND anio <= 2100)
);

-- Tabla INSCRIPCION (relación N:M entre alumno y curso)
CREATE TABLE IF NOT EXISTS inscripcion (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL REFERENCES alumno(id) ON DELETE CASCADE,
    curso_id INTEGER NOT NULL REFERENCES curso(id) ON DELETE CASCADE,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(alumno_id, curso_id)  -- Un alumno solo puede inscribirse una vez
);

-- Tabla CLASE
CREATE TABLE IF NOT EXISTS clase (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL REFERENCES curso(id) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    numero_clase INTEGER NOT NULL,
    tema TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (numero_clase > 0),
    UNIQUE(curso_id, numero_clase)  -- No repetir número de clase
);

-- Tabla REGISTRO_ASISTENCIA
CREATE TABLE IF NOT EXISTS registro_asistencia (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL REFERENCES alumno(id) ON DELETE CASCADE,
    clase_id INTEGER NOT NULL REFERENCES clase(id) ON DELETE CASCADE,
    estado TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (estado IN ('Presente', 'Ausente', 'Tardanza', 'Justificada')),
    UNIQUE(alumno_id, clase_id)  -- Un registro por alumno por clase
);

-- Tabla TRABAJO_PRACTICO
CREATE TABLE IF NOT EXISTS trabajo_practico (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL REFERENCES curso(id) ON DELETE CASCADE,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    fecha_entrega DATE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (length(titulo) > 0)
);

-- Tabla ENTREGA_TP
CREATE TABLE IF NOT EXISTS entrega_tp (
    id SERIAL PRIMARY KEY,
    trabajo_practico_id INTEGER NOT NULL REFERENCES trabajo_practico(id) ON DELETE CASCADE,
    alumno_id INTEGER NOT NULL REFERENCES alumno(id) ON DELETE CASCADE,
    fecha_entrega_real DATE,
    entregado BOOLEAN NOT NULL DEFAULT FALSE,
    es_tardia BOOLEAN NOT NULL DEFAULT FALSE,
    estado TEXT DEFAULT 'pendiente',
    nota DECIMAL(3,1),
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (estado IN ('pendiente', 'entregado', 'tarde', 'no_entregado')),
    CHECK (nota IS NULL OR (nota >= 1 AND nota <= 10)),
    UNIQUE(trabajo_practico_id, alumno_id)
);
```

## 3.6 Diseño del Frontend

### Estructura de Páginas

```
┌─────────────────────────────────────────────────────────┐
│                      HEADER                             │
│  [Logo] Sistema de Seguimiento           [Usuario]      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │              NAVEGACIÓN                         │   │
│  │  [Dashboard] [Registro] [Alumnos] [Admin]       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │                                                 │   │
│  │              CONTENIDO PRINCIPAL                │   │
│  │                                                 │   │
│  │    (Cambia según la página seleccionada)        │   │
│  │                                                 │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                      FOOTER                             │
└─────────────────────────────────────────────────────────┘
```

### Páginas Principales

1. **Dashboard**: Vista general de cursos y últimas clases
2. **Registro**: Crear clase y registrar asistencia
3. **Alumnos**: Lista y búsqueda de alumnos
4. **Admin**: CRUD de cursos, alumnos, TPs, inscripciones

### Flujo de Usuario

```
Dashboard
    │
    ├──► Ver cursos activos
    │       │
    │       └──► Click en curso
    │               │
    │               └──► Ver clases del curso
    │                       │
    │                       └──► Ver detalle de clase
    │
    ├──► Ir a Registro
    │       │
    │       └──► Seleccionar curso
    │               │
    │               └──► Seleccionar/crear clase
    │                       │
    │                       └──► Marcar asistencia por alumno
    │                               │
    │                               └──► Guardar (automático)
    │
    └──► Ir a Admin
            │
            ├──► Tab Cursos → CRUD cursos
            ├──► Tab Alumnos → CRUD alumnos
            ├──► Tab TPs → CRUD trabajos prácticos
            └──► Tab Datos → Seed/Clear
```

### Diseño Visual

**Paleta de colores:**
```css
:root {
    --primary: #6366f1;      /* Indigo - color principal */
    --primary-dark: #4f46e5;
    --secondary: #8b5cf6;    /* Violeta */
    --success: #10b981;      /* Verde */
    --warning: #f59e0b;      /* Naranja */
    --danger: #ef4444;       /* Rojo */
    --bg-dark: #0f172a;      /* Fondo oscuro */
    --bg-card: #1e293b;      /* Fondo tarjetas */
    --text-primary: #f8fafc; /* Texto principal */
    --text-secondary: #94a3b8;/* Texto secundario */
}
```

**Principios de diseño:**
- Modo oscuro (reduce fatiga visual)
- Botones grandes y claros
- Feedback visual inmediato (toasts)
- Responsive (funciona en móvil)

---

**Capítulo anterior**: [Requisitos](./02_requisitos.md)

**Siguiente capítulo**: [Pipeline de Desarrollo](./04_pipeline_desarrollo.md)
