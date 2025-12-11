# Capítulo 2: Diseño

## 2.1 Nuestras Entidades

Solo vamos a trabajar con **2 entidades principales** y **1 relación**:

```
┌─────────────────┐                    ┌─────────────────┐
│     ALUMNO      │                    │      CURSO      │
├─────────────────┤                    ├─────────────────┤
│ • id            │                    │ • id            │
│ • nombre        │                    │ • nombre_materia│
│ • apellido      │    INSCRIPCIÓN     │ • año           │
│ • dni           │◄──────────────────►│ • cuatrimestre  │
│ • email         │    (los conecta)   │                 │
└─────────────────┘                    └─────────────────┘
```

### ¿Por qué estas?

| Entidad | Propósito didáctico |
|---------|---------------------|
| **Alumno** | CRUD completo, validaciones |
| **Curso** | Muestra que el patrón se repite |
| **Inscripción** | Enseña relaciones N:M |

---

## 2.2 Los 4 Patrones que Usaremos

### Patrón 1: Repository (Repositorio)

**¿Qué es?** Una clase que se encarga de guardar y recuperar datos.

**¿Por qué?** Separa la lógica de negocio del acceso a datos.

```python
# SIN Repository (malo)
class AlumnoService:
    def crear(self, nombre, dni):
        cursor = conexion.cursor()  # El servicio sabe de SQL
        cursor.execute("INSERT INTO alumno...")  # Acoplado a la BD

# CON Repository (bueno)
class AlumnoService:
    def __init__(self, repo):
        self.repo = repo  # Recibe el repositorio
    
    def crear(self, nombre, dni):
        alumno = Alumno(nombre=nombre, dni=dni)
        return self.repo.guardar(alumno)  # No sabe de SQL
```

**Beneficio:** Si mañana cambiás de PostgreSQL a MongoDB, solo cambiás el repositorio.

---

### Patrón 2: Dependency Injection (Inyección de Dependencias)

**¿Qué es?** Pasarle a un objeto lo que necesita desde afuera.

**¿Por qué?** Hace el código más flexible y testeable.

```python
# SIN Dependency Injection (malo)
class AlumnoService:
    def __init__(self):
        self.repo = AlumnoRepositoryPostgres()  # Crea su propia dependencia
        # ¿Cómo teseo esto sin BD real?

# CON Dependency Injection (bueno)
class AlumnoService:
    def __init__(self, repo):  # Recibe la dependencia
        self.repo = repo

# Uso:
repo = AlumnoRepositoryPostgres(conexion)  # Creo el repo
service = AlumnoService(repo)  # Lo "inyecto" al servicio

# Para tests:
repo_falso = AlumnoRepositoryFake()  # Repo que no usa BD
service = AlumnoService(repo_falso)  # Puedo testear sin BD
```

---

### Patrón 3: DTO (Data Transfer Object)

**¿Qué es?** Objetos simples para transferir datos entre capas.

**¿Por qué?** Controlar qué datos entran y salen de la API.

```python
# DTO de entrada (lo que el cliente envía)
class AlumnoCreateDTO:
    nombre: str
    apellido: str
    dni: str
    email: str

# DTO de salida (lo que devolvemos)
class AlumnoResponseDTO:
    id: int
    nombre: str
    apellido: str
    nombre_completo: str  # Campo calculado
```

**Beneficio:** 
- El cliente no ve datos internos (ej: contraseñas)
- Validamos formato automáticamente
- Podemos tener campos calculados

---

### Patrón 4: Layered Architecture (Arquitectura por Capas)

**¿Qué es?** Organizar el código en capas con responsabilidades claras.

**¿Por qué?** Código más limpio, mantenible y testeable.

```
┌────────────────────────────────────────────────────────┐
│                    PRESENTACIÓN                        │
│                                                        │
│  Responsabilidad: Manejar HTTP                         │
│  Conoce: FastAPI, Request, Response                    │
│  NO conoce: SQL, lógica de negocio compleja            │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                     APLICACIÓN                         │
│                                                        │
│  Responsabilidad: Lógica de negocio                    │
│  Conoce: Entidades, Repositorios (interfaces)          │
│  NO conoce: HTTP, SQL                                  │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                      DOMINIO                           │
│                                                        │
│  Responsabilidad: Reglas de negocio puras              │
│  Conoce: Solo Python puro                              │
│  NO conoce: BD, HTTP, frameworks                       │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                  INFRAESTRUCTURA                       │
│                                                        │
│  Responsabilidad: Detalles técnicos                    │
│  Conoce: SQL, PostgreSQL, archivos                     │
│  NO conoce: Lógica de negocio                          │
└────────────────────────────────────────────────────────┘
```

---

## 2.3 Diseño de la API REST

### ¿Qué es REST?

**REST** = Representational State Transfer

Es una forma estándar de diseñar APIs web:

| Concepto | Significado |
|----------|-------------|
| **Recursos** | Las "cosas" que manejamos (alumnos, cursos) |
| **URLs** | Identifican recursos (`/alumnos`, `/cursos`) |
| **Verbos HTTP** | Indican qué hacer (GET=leer, POST=crear) |
| **JSON** | Formato de datos |

### Nuestra API

#### Alumnos

| Método | URL | Qué hace |
|--------|-----|----------|
| `GET` | `/api/alumnos/` | Listar todos |
| `GET` | `/api/alumnos/{id}` | Obtener uno |
| `POST` | `/api/alumnos/` | Crear nuevo |
| `PUT` | `/api/alumnos/{id}` | Actualizar |
| `DELETE` | `/api/alumnos/{id}` | Eliminar |

#### Cursos

| Método | URL | Qué hace |
|--------|-----|----------|
| `GET` | `/api/cursos/` | Listar todos |
| `GET` | `/api/cursos/{id}` | Obtener uno |
| `POST` | `/api/cursos/` | Crear nuevo |
| `PUT` | `/api/cursos/{id}` | Actualizar |
| `DELETE` | `/api/cursos/{id}` | Eliminar |

#### Inscripciones

| Método | URL | Qué hace |
|--------|-----|----------|
| `GET` | `/api/inscripciones/curso/{id}` | Alumnos de un curso |
| `POST` | `/api/inscripciones/` | Inscribir alumno |
| `DELETE` | `/api/inscripciones/{id}` | Desinscribir |

---

## 2.4 Diseño de la Base de Datos

### Tablas

```sql
-- Tabla de alumnos
CREATE TABLE alumno (
    id SERIAL PRIMARY KEY,         -- ID autoincremental
    nombre TEXT NOT NULL,          -- Nombre (obligatorio)
    apellido TEXT NOT NULL,        -- Apellido (obligatorio)
    dni TEXT NOT NULL UNIQUE,      -- DNI (único)
    email TEXT NOT NULL            -- Email
);

-- Tabla de cursos
CREATE TABLE curso (
    id SERIAL PRIMARY KEY,
    nombre_materia TEXT NOT NULL,
    anio INTEGER NOT NULL,
    cuatrimestre INTEGER NOT NULL CHECK (cuatrimestre IN (1, 2))
);

-- Tabla de inscripciones (relaciona alumno <-> curso)
CREATE TABLE inscripcion (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER REFERENCES alumno(id) ON DELETE CASCADE,
    curso_id INTEGER REFERENCES curso(id) ON DELETE CASCADE,
    UNIQUE(alumno_id, curso_id)   -- Un alumno no puede inscribirse 2 veces
);
```

### Diagrama

```
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│    alumno     │          │  inscripcion  │          │    curso      │
├───────────────┤          ├───────────────┤          ├───────────────┤
│ PK id         │◄─────────│ FK alumno_id  │          │ PK id         │
│    nombre     │          │ FK curso_id   │─────────►│    nombre_mat │
│    apellido   │          │    (UK)       │          │    anio       │
│ UK dni        │          └───────────────┘          │    cuatrimest │
│    email      │                                     └───────────────┘
└───────────────┘
```

**Explicación:**
- `PK` = Primary Key (identificador único)
- `FK` = Foreign Key (referencia a otra tabla)
- `UK` = Unique (valor único)

---

## 2.5 Flujo de una Petición

Cuando el usuario hace click en "Crear Alumno":

```
1. FRONTEND (app.js)
   │
   │  const response = await fetch('/api/alumnos/', {
   │      method: 'POST',
   │      body: JSON.stringify({nombre: "Juan", ...})
   │  });
   │
   ▼
2. ROUTER (alumnos.py)
   │
   │  @router.post("/")
   │  def crear(data: AlumnoCreateSchema):
   │      return service.crear(data)
   │
   ▼
3. SERVICE (alumno_service.py)
   │
   │  def crear(self, datos):
   │      # Verificar que DNI no exista
   │      if self.repo.buscar_por_dni(datos.dni):
   │          raise DNIDuplicado()
   │      
   │      alumno = Alumno(**datos)
   │      return self.repo.guardar(alumno)
   │
   ▼
4. REPOSITORY (alumno_repo.py)
   │
   │  def guardar(self, alumno):
   │      cursor.execute("INSERT INTO alumno...")
   │      return alumno_con_id
   │
   ▼
5. BASE DE DATOS
   │
   │  INSERT INTO alumno (nombre, apellido, dni, email)
   │  VALUES ('Juan', 'Pérez', '12345678', 'juan@mail.com')
   │
   ▼
6. RESPUESTA (vuelve por el mismo camino)
   │
   │  {
   │      "id": 1,
   │      "nombre": "Juan",
   │      "apellido": "Pérez",
   │      "nombre_completo": "Pérez, Juan"
   │  }
   │
   ▼
7. FRONTEND muestra "Alumno creado" ✅
```

---

## 2.6 Diagrama de Clases Simplificado

```
┌─────────────────────────────────────────────────────────────────┐
│                          DOMINIO                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐      ┌─────────────────────┐          │
│  │       Alumno        │      │        Curso        │          │
│  ├─────────────────────┤      ├─────────────────────┤          │
│  │ - id: int           │      │ - id: int           │          │
│  │ - nombre: str       │      │ - nombre_materia: str│         │
│  │ - apellido: str     │      │ - anio: int         │          │
│  │ - dni: str          │      │ - cuatrimestre: int │          │
│  │ - email: str        │      ├─────────────────────┤          │
│  ├─────────────────────┤      │ + nombre_completo   │          │
│  │ + nombre_completo   │      └─────────────────────┘          │
│  └─────────────────────┘                                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Excepciones                           │   │
│  │  • DNIDuplicadoException                                 │   │
│  │  • AlumnoNoEncontradoException                           │   │
│  │  • CursoNoEncontradoException                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       APLICACIÓN                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐      ┌─────────────────────┐          │
│  │   AlumnoService     │      │    CursoService     │          │
│  ├─────────────────────┤      ├─────────────────────┤          │
│  │ - repo: AlumnoRepo  │      │ - repo: CursoRepo   │          │
│  ├─────────────────────┤      ├─────────────────────┤          │
│  │ + crear()           │      │ + crear()           │          │
│  │ + obtener()         │      │ + obtener()         │          │
│  │ + listar()          │      │ + listar()          │          │
│  │ + actualizar()      │      │ + actualizar()      │          │
│  │ + eliminar()        │      │ + eliminar()        │          │
│  └─────────────────────┘      └─────────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFRAESTRUCTURA                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐      ┌─────────────────────┐          │
│  │ AlumnoRepoPostgres  │      │  CursoRepoPostgres  │          │
│  ├─────────────────────┤      ├─────────────────────┤          │
│  │ - conexion          │      │ - conexion          │          │
│  ├─────────────────────┤      ├─────────────────────┤          │
│  │ + guardar()         │      │ + guardar()         │          │
│  │ + obtener_por_id()  │      │ + obtener_por_id()  │          │
│  │ + listar()          │      │ + listar()          │          │
│  │ + actualizar()      │      │ + actualizar()      │          │
│  │ + eliminar()        │      │ + eliminar()        │          │
│  └─────────────────────┘      └─────────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2.7 Resumen

| Concepto | Qué aprendiste |
|----------|----------------|
| **Entidades** | Alumno, Curso, Inscripción |
| **Repository** | Separar acceso a datos |
| **Dependency Injection** | Pasar dependencias desde afuera |
| **DTO** | Controlar datos de entrada/salida |
| **Capas** | Presentación → Aplicación → Dominio → Infraestructura |
| **REST** | GET, POST, PUT, DELETE + URLs claras |

---

**Anterior:** [Capítulo 1 - Introducción](./01_introduccion.md)

**Siguiente:** [Capítulo 3 - Setup](./03_setup.md)
