# Capítulo 5: Estructura de Carpetas

## 5.1 Vista General del Proyecto

```
seguimiento_alumnos/
│
├── 📁 api/                      # Adaptador para Vercel (serverless)
│   └── index.py                 # Punto de entrada para Vercel
│
├── 📁 docs/                     # Documentación del proyecto
│   ├── ARQUITECTURA.md
│   ├── DATABASE.md
│   └── manual_tecnico/          # Este manual
│
├── 📁 public/                   # Frontend (archivos estáticos)
│   ├── index.html               # Página principal
│   ├── styles.css               # Estilos globales
│   ├── app.js                   # Lógica JavaScript
│   └── components/              # Fragmentos HTML reutilizables
│       ├── header.html
│       ├── footer.html
│       └── modals/
│
├── 📁 scripts/                  # Scripts de utilidad
│   ├── test_db.py               # Probar conexión a BD
│   └── list_routes.py           # Listar rutas de la API
│
├── 📁 src/                      # Código fuente del backend
│   ├── 📁 domain/               # Capa de Dominio
│   ├── 📁 application/          # Capa de Aplicación
│   ├── 📁 infrastructure/       # Capa de Infraestructura
│   └── 📁 presentation/         # Capa de Presentación
│
├── 📁 tests/                    # Pruebas automatizadas
│
├── .env                         # Variables de entorno (NO commitear)
├── .env.example                 # Ejemplo de variables
├── .gitignore                   # Archivos a ignorar por Git
├── requirements.txt             # Dependencias Python
├── vercel.json                  # Configuración de Vercel
├── run_local.bat               # Script para correr localmente
└── README.md                    # Documentación principal
```

## 5.2 Estructura del Backend (src/)

### Capa de Dominio (src/domain/)

La capa más interna. Contiene la lógica de negocio pura.

```
src/domain/
│
├── __init__.py
│
├── 📁 entities/                 # Entidades del dominio
│   ├── __init__.py
│   ├── alumno.py               # Entidad Alumno
│   ├── curso.py                # Entidad Curso
│   ├── inscripcion.py          # Entidad Inscripcion
│   ├── clase.py                # Entidad Clase
│   ├── asistencia.py           # Entidad Asistencia
│   ├── trabajo_practico.py     # Entidad TrabajoPractico
│   └── entrega_tp.py           # Entidad EntregaTP
│
└── 📁 exceptions/               # Excepciones de dominio
    ├── __init__.py
    └── domain_exceptions.py     # AlumnoNoEncontrado, DNIDuplicado, etc.
```

**¿Qué contiene cada entidad?**

```python
# alumno.py
@dataclass
class Alumno:
    id: Optional[int]
    nombre: str
    apellido: str
    dni: str
    email: str
    cohorte: int
    
    @property
    def nombre_completo(self) -> str:
        return f"{self.apellido}, {self.nombre}"
    
    def __post_init__(self):
        # Validaciones de dominio
        if not self.nombre:
            raise ValueError("Nombre no puede estar vacío")
```

### Capa de Aplicación (src/application/)

Servicios que orquestan la lógica de negocio.

```
src/application/
│
├── __init__.py
│
└── 📁 services/                 # Servicios de aplicación
    ├── __init__.py
    ├── alumno_service.py       # Lógica de negocio de alumnos
    ├── curso_service.py        # Lógica de negocio de cursos
    ├── inscripcion_service.py
    ├── clase_service.py
    ├── asistencia_service.py
    ├── tp_service.py
    └── entrega_service.py
```

**Ejemplo de servicio:**

```python
# alumno_service.py
class AlumnoService:
    def __init__(self, alumno_repo: AlumnoRepositoryBase):
        self.alumno_repo = alumno_repo
    
    def crear_alumno(self, nombre, apellido, dni, email, cohorte) -> Alumno:
        # 1. Validar que el DNI no exista
        existente = self.alumno_repo.obtener_por_dni(dni)
        if existente:
            raise DNIDuplicadoException(dni)
        
        # 2. Crear entidad
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
```

### Capa de Infraestructura (src/infrastructure/)

Implementaciones técnicas: base de datos, APIs externas, etc.

```
src/infrastructure/
│
├── __init__.py
│
├── 📁 database/                 # Acceso a base de datos
│   ├── __init__.py
│   ├── connection.py           # Conexión a PostgreSQL
│   └── postgres_schema.py      # SQL de creación de tablas
│
└── 📁 repositories/             # Repositorios
    │
    ├── 📁 base/                 # Interfaces abstractas
    │   ├── __init__.py
    │   ├── alumno_repository_base.py
    │   ├── curso_repository_base.py
    │   └── ...
    │
    └── 📁 postgres/             # Implementaciones PostgreSQL
        ├── __init__.py
        ├── alumno_repository_postgres.py
        ├── curso_repository_postgres.py
        └── ...
```

**Ejemplo de repositorio base (interfaz):**

```python
# alumno_repository_base.py
from abc import ABC, abstractmethod

class AlumnoRepositoryBase(ABC):
    """Contrato que deben cumplir los repositorios de Alumno"""
    
    @abstractmethod
    def crear(self, alumno: Alumno) -> Alumno:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        pass
    
    @abstractmethod
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        pass
    
    @abstractmethod
    def listar(self, limite=None, offset=0) -> List[Alumno]:
        pass
    
    @abstractmethod
    def actualizar(self, alumno: Alumno) -> Alumno:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
```

**Ejemplo de repositorio concreto:**

```python
# alumno_repository_postgres.py
class AlumnoRepositoryPostgres(AlumnoRepositoryBase):
    def __init__(self, conexion):
        self.conexion = conexion
    
    def crear(self, alumno: Alumno) -> Alumno:
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT INTO alumno (nombre, apellido, dni, email, cohorte)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (alumno.nombre, alumno.apellido, alumno.dni, 
              alumno.email, alumno.cohorte))
        
        row = cursor.fetchone()
        self.conexion.commit()
        alumno.id = row[0]
        return alumno
```

### Capa de Presentación (src/presentation/)

APIs HTTP, interfaces de usuario, etc.

```
src/presentation/
│
├── __init__.py
│
└── 📁 api/                      # API FastAPI
    ├── __init__.py
    ├── main.py                  # Aplicación FastAPI principal
    │
    ├── 📁 routers/              # Endpoints por recurso
    │   ├── __init__.py
    │   ├── alumnos.py           # /api/alumnos
    │   ├── cursos.py            # /api/cursos
    │   ├── inscripciones.py     # /api/inscripciones
    │   ├── clases.py            # /api/clases
    │   ├── asistencias.py       # /api/asistencias
    │   ├── tps.py               # /api/tps
    │   └── entregas.py          # /api/entregas
    │
    └── 📁 schemas/              # DTOs Pydantic
        ├── __init__.py
        ├── alumno_schema.py
        ├── curso_schema.py
        └── ...
```

**Ejemplo de router:**

```python
# routers/alumnos.py
router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

@router.get("/", response_model=AlumnoListResponseSchema)
def listar_alumnos(
    limite: int = Query(None),
    service: AlumnoService = Depends(get_alumno_service)
):
    alumnos = service.listar_alumnos(limite=limite)
    return AlumnoListResponseSchema(
        total=len(alumnos),
        alumnos=[AlumnoResponseSchema.from_entity(a) for a in alumnos]
    )
```

**Ejemplo de schema:**

```python
# schemas/alumno_schema.py
class AlumnoCreateSchema(BaseModel):
    nombre: str
    apellido: str
    dni: str
    email: EmailStr
    cohorte: int = Field(ge=2000, le=2100)

class AlumnoResponseSchema(BaseModel):
    id: int
    nombre: str
    apellido: str
    dni: str
    email: str
    cohorte: int
    nombre_completo: str
    
    @classmethod
    def from_entity(cls, alumno: Alumno):
        return cls(
            id=alumno.id,
            nombre=alumno.nombre,
            apellido=alumno.apellido,
            dni=alumno.dni,
            email=alumno.email,
            cohorte=alumno.cohorte,
            nombre_completo=alumno.nombre_completo
        )
```

## 5.3 Estructura del Frontend (public/)

```
public/
│
├── index.html                   # HTML principal (SPA)
├── styles.css                   # Estilos globales
├── app.js                       # Lógica JavaScript
│
├── 📁 components/               # Fragmentos HTML reutilizables
│   ├── header.html              # Cabecera
│   ├── footer.html              # Pie de página
│   │
│   └── 📁 modals/               # Ventanas modales
│       ├── alumno.html          # Modal crear/editar alumno
│       ├── curso.html           # Modal crear/editar curso
│       ├── tp.html              # Modal crear/editar TP
│       └── inscripcion.html     # Modal gestionar inscripciones
│
└── 📁 images/                   # Recursos gráficos (si hay)
    └── logo.png
```

### Estructura del index.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Sistema de Seguimiento de Alumnos</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header -->
    <header id="main-header">...</header>
    
    <!-- Main Content - Páginas -->
    <main id="main-content">
        <section id="page-dashboard" class="page">...</section>
        <section id="page-registro" class="page">...</section>
        <section id="page-alumnos" class="page">...</section>
        <section id="page-admin" class="page">...</section>
    </main>
    
    <!-- Footer -->
    <footer id="main-footer">...</footer>
    
    <!-- Modales -->
    <div id="modales">...</div>
    
    <!-- Toasts -->
    <div id="toast-container"></div>
    
    <!-- JavaScript -->
    <script src="app.js"></script>
</body>
</html>
```

### Estructura del app.js

```javascript
// ============================================================================
// CONFIGURACIÓN
// ============================================================================
const API_URL = '/api';

// ============================================================================
// ESTADO GLOBAL
// ============================================================================
const state = {
    alumnos: [],
    cursos: [],
    clases: [],
    currentPage: 'dashboard',
    claseActual: {
        id: null,
        registros: {},
        entregasTPs: {}
    }
};

// ============================================================================
// INICIALIZACIÓN
// ============================================================================
document.addEventListener('DOMContentLoaded', init);

async function init() {
    setupNavigation();
    await loadDashboardData();
}

// ============================================================================
// NAVEGACIÓN
// ============================================================================
function showPage(pageId) { ... }

// ============================================================================
// DASHBOARD
// ============================================================================
async function loadDashboardData() { ... }

// ============================================================================
// REGISTRO DE ASISTENCIA
// ============================================================================
async function iniciarRegistroClase() { ... }
async function marcarAsistencia(alumnoId, estado) { ... }

// ============================================================================
// ALUMNOS
// ============================================================================
async function loadAlumnos() { ... }
async function crearAlumno() { ... }

// ============================================================================
// ADMIN
// ============================================================================
async function loadAdminCursos() { ... }
async function loadAdminAlumnos() { ... }
async function loadAdminTPs() { ... }

// ============================================================================
// UTILIDADES
// ============================================================================
function showToast(mensaje, tipo) { ... }
function showModal(modalId) { ... }
function closeModal(modalId) { ... }

// ============================================================================
// EXPORTAR FUNCIONES GLOBALES
// ============================================================================
window.showPage = showPage;
window.marcarAsistencia = marcarAsistencia;
// ... etc
```

## 5.4 Archivos de Configuración

### requirements.txt

```
fastapi>=0.109.0
uvicorn>=0.27.0
pydantic>=2.6.0
python-multipart>=0.0.9
pg8000>=1.30.0
email-validator>=2.0.0
```

### vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "public/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "public/$1"
    }
  ]
}
```

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
venv/
.env
.env.local

# IDE
.vscode/
.idea/

# Vercel
.vercel/

# Local
*.db
*.sqlite
```

### .env.example

```env
# Base de datos PostgreSQL (Neon)
POSTGRES_URL=postgresql://user:password@host/database?sslmode=require

# Entorno
ENVIRONMENT=development
```

## 5.5 Justificación de la Estructura

### ¿Por qué tantas carpetas?

| Estructura | Ventaja |
|------------|---------|
| Separar por capas | Cambios aislados, fácil testing |
| Separar por entidad | Fácil encontrar código relacionado |
| Schemas separados | Validación clara y documentable |
| Routers separados | Endpoints organizados lógicamente |

### ¿Cuándo agregar más estructura?

```
Si tienes < 5 entidades:
  → Esta estructura es suficiente

Si tienes > 10 entidades:
  → Considera agrupar por módulo/feature
  → Ej: src/modules/academico/, src/modules/reportes/

Si tienes múltiples APIs:
  → Considera separar en v1/, v2/
```

---

**Capítulo anterior**: [Pipeline de Desarrollo](./04_pipeline_desarrollo.md)

**Siguiente capítulo**: [Diagramas UML](./06_uml.md)
