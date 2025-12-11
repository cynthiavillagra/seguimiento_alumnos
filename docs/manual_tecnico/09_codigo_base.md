# Capítulo 9: Código Base Completo

## 9.1 Visión General

Este capítulo contiene el código base completo de las principales entidades y componentes del sistema. Usá este código como referencia para entender cómo cada pieza encaja en la arquitectura.

## 9.2 Capa de Dominio - Entidades

### Entidad Curso

```python
# src/domain/entities/curso.py
"""
Entidad Curso - Sistema de Seguimiento de Alumnos
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Curso:
    """
    Representa una materia/curso en un cuatrimestre específico.
    
    Ejemplo: "Programación I" del 1er cuatrimestre de 2024
    """
    id: Optional[int]
    nombre_materia: str
    anio: int
    cuatrimestre: int  # 1 o 2
    docente_responsable: str
    fecha_creacion: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.nombre_materia or not self.nombre_materia.strip():
            raise ValueError("El nombre de la materia no puede estar vacío")
        
        self.nombre_materia = self.nombre_materia.strip()
        
        if self.cuatrimestre not in [1, 2]:
            raise ValueError("El cuatrimestre debe ser 1 o 2")
        
        if self.anio < 2000 or self.anio > 2100:
            raise ValueError("El año debe estar entre 2000 y 2100")
        
        if not self.docente_responsable or not self.docente_responsable.strip():
            raise ValueError("El docente responsable no puede estar vacío")
    
    @property
    def nombre_completo(self) -> str:
        """Ej: 'Programación I - 1C2024'"""
        return f"{self.nombre_materia} - {self.cuatrimestre}C{self.anio}"
```

### Entidad Clase

```python
# src/domain/entities/clase.py
"""
Entidad Clase - Representa una sesión de clase
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Clase:
    """
    Representa una clase dictada en una fecha específica.
    """
    id: Optional[int]
    curso_id: int
    fecha: date
    numero_clase: int
    tema: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    
    def __post_init__(self):
        if self.numero_clase < 1:
            raise ValueError("El número de clase debe ser positivo")
        
        if isinstance(self.fecha, str):
            self.fecha = date.fromisoformat(self.fecha)
```

### Entidad Asistencia

```python
# src/domain/entities/asistencia.py
"""
Entidad Asistencia - Registro de asistencia por alumno por clase
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Estados válidos de asistencia
ESTADOS_ASISTENCIA = ['Presente', 'Ausente', 'Tardanza', 'Justificada']


@dataclass
class Asistencia:
    """
    Representa el estado de asistencia de un alumno a una clase.
    """
    id: Optional[int]
    alumno_id: int
    clase_id: int
    estado: str  # 'Presente', 'Ausente', 'Tardanza', 'Justificada'
    fecha_registro: Optional[datetime] = None
    
    def __post_init__(self):
        if self.estado not in ESTADOS_ASISTENCIA:
            raise ValueError(
                f"Estado inválido: {self.estado}. "
                f"Debe ser uno de: {', '.join(ESTADOS_ASISTENCIA)}"
            )
```

### Entidad TrabajoPractico

```python
# src/domain/entities/trabajo_practico.py
"""
Entidad Trabajo Práctico
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class TrabajoPractico:
    """
    Representa un trabajo práctico asignado a un curso.
    """
    id: Optional[int]
    curso_id: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_entrega: Optional[date] = None
    fecha_creacion: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.titulo or not self.titulo.strip():
            raise ValueError("El título del TP no puede estar vacío")
        
        self.titulo = self.titulo.strip()
        
        if isinstance(self.fecha_entrega, str):
            self.fecha_entrega = date.fromisoformat(self.fecha_entrega)
```

### Entidad EntregaTP

```python
# src/domain/entities/entrega_tp.py
"""
Entidad Entrega de TP - Registro de entrega por alumno
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

ESTADOS_ENTREGA = ['pendiente', 'entregado', 'tarde', 'no_entregado']


@dataclass
class EntregaTP:
    """
    Representa la entrega de un TP por parte de un alumno.
    """
    id: Optional[int] = None
    trabajo_practico_id: Optional[int] = None
    alumno_id: Optional[int] = None
    fecha_entrega_real: Optional[date] = None
    entregado: bool = False
    es_tardia: bool = False
    estado: str = 'pendiente'
    nota: Optional[float] = None
    observaciones: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    
    def __post_init__(self):
        if self.estado not in ESTADOS_ENTREGA:
            raise ValueError(f"Estado inválido: {self.estado}")
        
        if self.nota is not None:
            if self.nota < 1 or self.nota > 10:
                raise ValueError("La nota debe estar entre 1 y 10")
        
        if isinstance(self.fecha_entrega_real, str):
            self.fecha_entrega_real = date.fromisoformat(self.fecha_entrega_real)
```

### Entidad Inscripción

```python
# src/domain/entities/inscripcion.py
"""
Entidad Inscripción - Relación Alumno-Curso
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Inscripcion:
    """
    Representa la inscripción de un alumno en un curso.
    """
    id: Optional[int]
    alumno_id: int
    curso_id: int
    fecha_inscripcion: Optional[datetime] = None
```

## 9.3 Capa de Infraestructura - Conexión a Base de Datos

```python
# src/infrastructure/database/connection.py
"""
Gestión de conexión a PostgreSQL
"""

import os
from urllib.parse import urlparse
import pg8000
import ssl

# Conexión singleton
_connection = None


def get_db_connection():
    """
    Retorna una conexión a PostgreSQL (singleton).
    
    Usa POSTGRES_URL o DATABASE_URL del entorno.
    """
    global _connection
    
    if _connection is not None:
        try:
            # Verificar que la conexión sigue activa
            cursor = _connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return _connection
        except:
            _connection = None
    
    # Obtener URL de conexión
    db_url = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
    
    if not db_url:
        raise Exception("No se encontró POSTGRES_URL o DATABASE_URL")
    
    # Parsear URL
    parsed = urlparse(db_url)
    
    # Crear contexto SSL
    ssl_context = ssl.create_default_context()
    
    # Conectar
    _connection = pg8000.connect(
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path.lstrip('/'),
        ssl_context=ssl_context
    )
    
    print("✅ Conexión a PostgreSQL exitosa (pg8000)")
    
    return _connection


def close_db_connection():
    """Cierra la conexión a la base de datos."""
    global _connection
    if _connection:
        try:
            _connection.close()
            print("👋 Conexión cerrada")
        except:
            pass
        _connection = None


def inicializar_base_de_datos():
    """
    Crea las tablas si no existen.
    Lee el schema desde postgres_schema.py
    """
    from src.infrastructure.database.postgres_schema import POSTGRES_SCHEMA
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Dividir por statements respetando bloques $$
    statements = []
    current_statement = []
    in_dollar_block = False
    
    for line in POSTGRES_SCHEMA.split('\n'):
        current_statement.append(line)
        
        if '$$' in line:
            in_dollar_block = not in_dollar_block
        
        if not in_dollar_block and line.strip().endswith(';'):
            full_statement = '\n'.join(current_statement).strip()
            if full_statement:
                statements.append(full_statement)
            current_statement = []
    
    ok_count = 0
    error_count = 0
    exist_count = 0
    
    for stmt in statements:
        if not stmt.strip():
            continue
        try:
            cursor.execute(stmt)
            conn.commit()
            ok_count += 1
        except Exception as e:
            conn.rollback()
            error_msg = str(e).lower()
            if 'already exists' in error_msg or 'ya existe' in error_msg:
                exist_count += 1
            else:
                error_count += 1
                print(f"⚠️ Error en statement: {error_msg[:100]}")
    
    cursor.close()
    print(f"✅ Schema inicializado: {ok_count} OK, {exist_count} ya existían, {error_count} errores")
```

## 9.4 Capa de Infraestructura - Schema SQL

```python
# src/infrastructure/database/postgres_schema.py
"""
Schema SQL para PostgreSQL
"""

POSTGRES_SCHEMA = """
-- Tabla de Alumnos
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

-- Tabla de Cursos
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

-- Tabla de Inscripciones (alumno <-> curso)
CREATE TABLE IF NOT EXISTS inscripcion (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL REFERENCES alumno(id) ON DELETE CASCADE,
    curso_id INTEGER NOT NULL REFERENCES curso(id) ON DELETE CASCADE,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(alumno_id, curso_id)
);

-- Tabla de Clases
CREATE TABLE IF NOT EXISTS clase (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL REFERENCES curso(id) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    numero_clase INTEGER NOT NULL,
    tema TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (numero_clase > 0),
    UNIQUE(curso_id, numero_clase)
);

-- Tabla de Registro de Asistencia
CREATE TABLE IF NOT EXISTS registro_asistencia (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL REFERENCES alumno(id) ON DELETE CASCADE,
    clase_id INTEGER NOT NULL REFERENCES clase(id) ON DELETE CASCADE,
    estado TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (estado IN ('Presente', 'Ausente', 'Tardanza', 'Justificada')),
    UNIQUE(alumno_id, clase_id)
);

-- Tabla de Trabajos Prácticos
CREATE TABLE IF NOT EXISTS trabajo_practico (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL REFERENCES curso(id) ON DELETE CASCADE,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    fecha_entrega DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (length(titulo) > 0)
);

-- Tabla de Entregas de TP
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

-- Índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_alumno_dni ON alumno(dni);
CREATE INDEX IF NOT EXISTS idx_alumno_cohorte ON alumno(cohorte);
CREATE INDEX IF NOT EXISTS idx_inscripcion_alumno ON inscripcion(alumno_id);
CREATE INDEX IF NOT EXISTS idx_inscripcion_curso ON inscripcion(curso_id);
CREATE INDEX IF NOT EXISTS idx_clase_curso ON clase(curso_id);
CREATE INDEX IF NOT EXISTS idx_clase_fecha ON clase(fecha);
CREATE INDEX IF NOT EXISTS idx_asistencia_alumno ON registro_asistencia(alumno_id);
CREATE INDEX IF NOT EXISTS idx_asistencia_clase ON registro_asistencia(clase_id);
"""
```

## 9.5 Capa de Presentación - Main FastAPI

```python
# src/presentation/api/main.py
"""
Aplicación Principal FastAPI
Sistema de Seguimiento de Alumnos
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importar routers
from src.presentation.api.routers import (
    alumnos, cursos, inscripciones, clases, 
    asistencias, tps, entregas, seed
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación.
    Se ejecuta al iniciar y al cerrar.
    """
    # Startup
    print("🚀 Iniciando aplicación...")
    try:
        from src.infrastructure.database.connection import (
            get_db_connection, 
            inicializar_base_de_datos,
            close_db_connection
        )
        get_db_connection()
        inicializar_base_de_datos()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"❌ Error inicializando BD: {e}")
    
    yield  # La aplicación corre aquí
    
    # Shutdown
    print("👋 Cerrando aplicación...")
    try:
        close_db_connection()
    except:
        pass


# Crear aplicación
app = FastAPI(
    title="Sistema de Seguimiento de Alumnos",
    description="""
    API para gestión académica de alumnos en instituciones educativas.
    
    ## Funcionalidades
    * Gestión de alumnos y cursos
    * Registro de asistencia
    * Seguimiento de trabajos prácticos
    * Inscripciones a cursos
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prefijo para todos los endpoints de API
api_prefix = "/api"

# Registrar routers
app.include_router(alumnos.router, prefix=api_prefix)
app.include_router(cursos.router, prefix=api_prefix)
app.include_router(inscripciones.router, prefix=api_prefix)
app.include_router(clases.router, prefix=api_prefix)
app.include_router(asistencias.router, prefix=api_prefix)
app.include_router(tps.router, prefix=api_prefix)
app.include_router(entregas.router, prefix=api_prefix)
app.include_router(seed.router, prefix=api_prefix)

# Health check
@app.get("/api", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "API funcionando correctamente",
        "version": "1.0.0"
    }

# Servir archivos estáticos (frontend) en desarrollo local
if not os.environ.get("VERCEL"):
    try:
        app.mount("/", StaticFiles(directory="public", html=True), name="public")
    except:
        pass
```

## 9.6 Frontend - HTML Principal (Estructura)

```html
<!-- public/index.html (estructura principal) -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Seguimiento de Alumnos</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <h1>📚 Seguimiento de Alumnos</h1>
            <nav class="nav-principal">
                <button class="nav-btn active" onclick="showPage('dashboard')">
                    🏠 Dashboard
                </button>
                <button class="nav-btn" onclick="showPage('registro')">
                    ✍️ Registro
                </button>
                <button class="nav-btn" onclick="showPage('alumnos')">
                    👥 Alumnos
                </button>
                <button class="nav-btn" onclick="showPage('admin')">
                    ⚙️ Admin
                </button>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        <!-- Dashboard Page -->
        <section id="page-dashboard" class="page active">
            <h2>Dashboard</h2>
            <div id="clases-container" class="cards-grid">
                <!-- Cursos cargados dinámicamente -->
            </div>
        </section>

        <!-- Registro Page -->
        <section id="page-registro" class="page">
            <h2>Registro de Clase</h2>
            <!-- Formulario de registro -->
        </section>

        <!-- Alumnos Page -->
        <section id="page-alumnos" class="page">
            <h2>Lista de Alumnos</h2>
            <table id="alumnos-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>DNI</th>
                        <th>Email</th>
                        <th>Cohorte</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody id="alumnos-tbody">
                    <!-- Filas cargadas dinámicamente -->
                </tbody>
            </table>
        </section>

        <!-- Admin Page -->
        <section id="page-admin" class="page">
            <h2>Administración</h2>
            <!-- Tabs y contenido de admin -->
        </section>
    </main>

    <!-- Modales -->
    <div id="modal-container"></div>

    <!-- Toasts -->
    <div id="toast-container"></div>

    <!-- Scripts -->
    <script src="app.js"></script>
</body>
</html>
```

## 9.7 Frontend - JavaScript Principal (Estructura)

```javascript
// public/app.js (estructura principal)

// ============================================================================
// CONFIGURACIÓN
// ============================================================================
const API_URL = '/api';

// ============================================================================
// ESTADO GLOBAL
// ============================================================================
const state = {
    clases: [],
    alumnos: [],
    cursos: [],
    currentPage: 'dashboard',
    claseActual: {
        id: null,
        cursoId: null,
        registros: {},
        entregasTPs: {}
    }
};

// ============================================================================
// INICIALIZACIÓN
// ============================================================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Iniciando aplicación...');
    setupNavigation();
    await loadDashboardData();
});

function setupNavigation() {
    // Configurar navegación SPA
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const pageName = btn.getAttribute('onclick')
                .match(/showPage\('(.+)'\)/)?.[1];
            if (pageName) showPage(pageName);
        });
    });
}

// ============================================================================
// NAVEGACIÓN
// ============================================================================
function showPage(pageId) {
    // Ocultar todas las páginas
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // Mostrar la seleccionada
    const page = document.getElementById(`page-${pageId}`);
    if (page) page.classList.add('active');
    
    // Actualizar navegación
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.querySelector(`.nav-btn[onclick="showPage('${pageId}')"]`);
    if (activeBtn) activeBtn.classList.add('active');
    
    // Cargar datos según la página
    switch(pageId) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'alumnos':
            loadAlumnos();
            break;
        case 'admin':
            loadAdminCursos();
            break;
    }
    
    state.currentPage = pageId;
}

// ============================================================================
// DASHBOARD
// ============================================================================
async function loadDashboardData() {
    try {
        const response = await fetch(`${API_URL}/cursos/`);
        const data = await response.json();
        state.clases = data.cursos || [];
        renderClasesCards(state.clases);
    } catch (error) {
        console.error('Error cargando cursos:', error);
        showToast('Error al cargar cursos', 'error');
    }
}

function renderClasesCards(cursos) {
    const container = document.getElementById('clases-container');
    
    if (!cursos.length) {
        container.innerHTML = '<p>No hay cursos registrados</p>';
        return;
    }
    
    container.innerHTML = cursos.map(curso => `
        <div class="card curso-card" data-id="${curso.id}">
            <h3>${curso.nombre_materia}</h3>
            <p>${curso.cuatrimestre}° Cuatrimestre ${curso.anio}</p>
            <p>Docente: ${curso.docente_responsable}</p>
            <button onclick="verCurso(${curso.id})">Ver detalle</button>
        </div>
    `).join('');
}

// ============================================================================
// ALUMNOS
// ============================================================================
async function loadAlumnos() {
    try {
        const response = await fetch(`${API_URL}/alumnos/`);
        const data = await response.json();
        state.alumnos = data.alumnos || [];
        renderAlumnos(state.alumnos);
    } catch (error) {
        console.error('Error cargando alumnos:', error);
        showToast('Error al cargar alumnos', 'error');
    }
}

function renderAlumnos(alumnos) {
    const tbody = document.getElementById('alumnos-tbody');
    
    if (!alumnos.length) {
        tbody.innerHTML = '<tr><td colspan="6">No hay alumnos registrados</td></tr>';
        return;
    }
    
    tbody.innerHTML = alumnos.map(a => `
        <tr>
            <td>${a.id}</td>
            <td>${a.nombre_completo}</td>
            <td>${a.dni}</td>
            <td>${a.email}</td>
            <td>${a.cohorte}</td>
            <td>
                <button onclick="editarAlumno(${a.id})">Editar</button>
                <button onclick="eliminarAlumno(${a.id})">Eliminar</button>
            </td>
        </tr>
    `).join('');
}

// ============================================================================
// UTILIDADES
// ============================================================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// ============================================================================
// EXPORTAR FUNCIONES GLOBALES
// ============================================================================
window.showPage = showPage;
window.showToast = showToast;
// ... más funciones exportadas
```

## 9.8 Frontend - CSS Principal (Estructura)

```css
/* public/styles.css (estructura principal) */

/* ============================================================================
   VARIABLES
   ============================================================================ */
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #8b5cf6;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --bg-dark: #0f172a;
    --bg-card: #1e293b;
    --bg-hover: #334155;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --border: #334155;
    --radius: 12px;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}

/* ============================================================================
   RESET
   ============================================================================ */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg-dark);
    color: var(--text-primary);
    min-height: 100vh;
}

/* ============================================================================
   LAYOUT
   ============================================================================ */
.header {
    background: var(--bg-card);
    padding: 1rem 2rem;
    border-bottom: 1px solid var(--border);
}

.header-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-principal {
    display: flex;
    gap: 0.5rem;
}

.nav-btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-secondary);
    padding: 0.5rem 1rem;
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.2s;
}

.nav-btn:hover {
    background: var(--bg-hover);
    color: var(--text-primary);
}

.nav-btn.active {
    background: var(--primary);
    border-color: var(--primary);
    color: white;
}

.main-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

/* ============================================================================
   PÁGINAS
   ============================================================================ */
.page {
    display: none;
}

.page.active {
    display: block;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ============================================================================
   CARDS
   ============================================================================ */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

.card {
    background: var(--bg-card);
    border-radius: var(--radius);
    padding: 1.5rem;
    border: 1px solid var(--border);
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}

/* ============================================================================
   TABLAS
   ============================================================================ */
table {
    width: 100%;
    border-collapse: collapse;
    background: var(--bg-card);
    border-radius: var(--radius);
    overflow: hidden;
}

th, td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

th {
    background: var(--bg-hover);
    font-weight: 600;
}

tr:hover {
    background: var(--bg-hover);
}

/* ============================================================================
   BOTONES
   ============================================================================ */
button {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: var(--radius);
    cursor: pointer;
    font-size: 0.9rem;
    transition: background 0.2s;
}

button:hover {
    background: var(--primary-dark);
}

/* ============================================================================
   TOASTS
   ============================================================================ */
#toast-container {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.toast {
    background: var(--bg-card);
    padding: 1rem 1.5rem;
    border-radius: var(--radius);
    border-left: 4px solid var(--primary);
    animation: slideIn 0.3s ease;
}

.toast.success { border-color: var(--success); }
.toast.error { border-color: var(--danger); }
.toast.warning { border-color: var(--warning); }

@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
```

---

**Capítulo anterior**: [Construcción Paso a Paso](./08_construccion_paso_a_paso.md)

**Siguiente capítulo**: [Pruebas](./10_pruebas.md)
