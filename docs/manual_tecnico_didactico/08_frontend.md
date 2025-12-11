# Capítulo 8: Frontend

## 8.1 Lo que Vamos a Construir

Un frontend simple pero funcional que:

- ✅ Muestra lista de alumnos
- ✅ Permite crear alumnos
- ✅ Muestra lista de cursos
- ✅ Permite inscribir alumnos

```
┌─────────────────────────────────────────────────────────────┐
│  📚 Sistema de Gestión                                      │
├─────────────────────────────────────────────────────────────┤
│  [Alumnos] [Cursos] [Inscripciones]                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Lista de Alumnos                    [+ Nuevo]      │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  Pérez, Juan     | 12345678 | juan@mail.com        │   │
│  │  García, María   | 22222222 | maria@mail.com       │   │
│  │  López, Ana      | 33333333 | ana@mail.com         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 8.2 HTML Principal

Crear `public/index.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Gestión - MVP</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <h1>📚 Sistema de Gestión</h1>
        <nav class="nav">
            <button class="nav-btn active" onclick="showSection('alumnos')">
                Alumnos
            </button>
            <button class="nav-btn" onclick="showSection('cursos')">
                Cursos
            </button>
            <button class="nav-btn" onclick="showSection('inscripciones')">
                Inscripciones
            </button>
        </nav>
    </header>

    <!-- Main Content -->
    <main class="container">
        
        <!-- Sección Alumnos -->
        <section id="section-alumnos" class="section active">
            <div class="section-header">
                <h2>Lista de Alumnos</h2>
                <button class="btn btn-primary" onclick="showModal('modal-alumno')">
                    + Nuevo Alumno
                </button>
            </div>
            
            <table class="table" id="tabla-alumnos">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre Completo</th>
                        <th>DNI</th>
                        <th>Email</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody id="tbody-alumnos">
                    <!-- Se llena con JavaScript -->
                </tbody>
            </table>
        </section>

        <!-- Sección Cursos -->
        <section id="section-cursos" class="section">
            <div class="section-header">
                <h2>Lista de Cursos</h2>
                <button class="btn btn-primary" onclick="showModal('modal-curso')">
                    + Nuevo Curso
                </button>
            </div>
            
            <table class="table" id="tabla-cursos">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Materia</th>
                        <th>Año</th>
                        <th>Cuatrimestre</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody id="tbody-cursos">
                    <!-- Se llena con JavaScript -->
                </tbody>
            </table>
        </section>

        <!-- Sección Inscripciones -->
        <section id="section-inscripciones" class="section">
            <div class="section-header">
                <h2>Inscripciones</h2>
            </div>
            
            <div class="inscripcion-form">
                <label>Seleccionar curso:</label>
                <select id="select-curso" onchange="cargarAlumnosCurso()">
                    <option value="">-- Seleccionar --</option>
                </select>
                
                <button class="btn btn-primary" onclick="showModal('modal-inscripcion')">
                    + Inscribir Alumno
                </button>
            </div>
            
            <h3 id="titulo-inscriptos">Alumnos inscriptos</h3>
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>DNI</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody id="tbody-inscriptos">
                </tbody>
            </table>
        </section>

    </main>

    <!-- Modal Nuevo Alumno -->
    <div id="modal-alumno" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('modal-alumno')">&times;</span>
            <h2>Nuevo Alumno</h2>
            <form id="form-alumno" onsubmit="return crearAlumno(event)">
                <div class="form-group">
                    <label>Nombre</label>
                    <input type="text" id="alumno-nombre" required>
                </div>
                <div class="form-group">
                    <label>Apellido</label>
                    <input type="text" id="alumno-apellido" required>
                </div>
                <div class="form-group">
                    <label>DNI</label>
                    <input type="text" id="alumno-dni" required>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="alumno-email" required>
                </div>
                <button type="submit" class="btn btn-primary">Guardar</button>
            </form>
        </div>
    </div>

    <!-- Modal Nuevo Curso -->
    <div id="modal-curso" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('modal-curso')">&times;</span>
            <h2>Nuevo Curso</h2>
            <form id="form-curso" onsubmit="return crearCurso(event)">
                <div class="form-group">
                    <label>Materia</label>
                    <input type="text" id="curso-materia" required>
                </div>
                <div class="form-group">
                    <label>Año</label>
                    <input type="number" id="curso-anio" value="2024" required>
                </div>
                <div class="form-group">
                    <label>Cuatrimestre</label>
                    <select id="curso-cuatrimestre" required>
                        <option value="1">1° Cuatrimestre</option>
                        <option value="2">2° Cuatrimestre</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Guardar</button>
            </form>
        </div>
    </div>

    <!-- Modal Inscribir -->
    <div id="modal-inscripcion" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('modal-inscripcion')">&times;</span>
            <h2>Inscribir Alumno</h2>
            <form id="form-inscripcion" onsubmit="return inscribirAlumno(event)">
                <div class="form-group">
                    <label>Alumno</label>
                    <select id="inscripcion-alumno" required>
                        <option value="">-- Seleccionar --</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Inscribir</button>
            </form>
        </div>
    </div>

    <!-- Toast Container -->
    <div id="toast-container"></div>

    <!-- JavaScript -->
    <script src="app.js"></script>
</body>
</html>
```

---

## 8.3 CSS

Crear `public/styles.css`:

```css
/* ============================================
   VARIABLES
   ============================================ */
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --success: #10b981;
    --danger: #ef4444;
    --bg-dark: #1e293b;
    --bg-card: #334155;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --border: #475569;
    --radius: 8px;
}

/* ============================================
   RESET
   ============================================ */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #0f172a;
    color: var(--text);
    min-height: 100vh;
}

/* ============================================
   HEADER
   ============================================ */
.header {
    background: var(--bg-dark);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
}

.header h1 {
    font-size: 1.5rem;
}

.nav {
    display: flex;
    gap: 0.5rem;
}

.nav-btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 0.5rem 1rem;
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.2s;
}

.nav-btn:hover {
    background: var(--bg-card);
    color: var(--text);
}

.nav-btn.active {
    background: var(--primary);
    border-color: var(--primary);
    color: white;
}

/* ============================================
   CONTAINER
   ============================================ */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

/* ============================================
   SECTIONS
   ============================================ */
.section {
    display: none;
}

.section.active {
    display: block;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.section-header h2 {
    font-size: 1.5rem;
}

/* ============================================
   BUTTONS
   ============================================ */
.btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: var(--radius);
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-dark);
}

.btn-danger {
    background: var(--danger);
    color: white;
}

.btn-danger:hover {
    background: #dc2626;
}

.btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.8rem;
}

/* ============================================
   TABLE
   ============================================ */
.table {
    width: 100%;
    border-collapse: collapse;
    background: var(--bg-dark);
    border-radius: var(--radius);
    overflow: hidden;
}

.table th,
.table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

.table th {
    background: var(--bg-card);
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    font-size: 0.8rem;
}

.table tr:hover {
    background: rgba(99, 102, 241, 0.1);
}

/* ============================================
   MODAL
   ============================================ */
.modal {
    display: none;
    position: fixed;
    z-index: 100;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    animation: fadeIn 0.2s ease;
}

.modal.show {
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background: var(--bg-dark);
    padding: 2rem;
    border-radius: var(--radius);
    width: 90%;
    max-width: 400px;
    position: relative;
}

.modal-content h2 {
    margin-bottom: 1.5rem;
}

.close {
    position: absolute;
    right: 1rem;
    top: 1rem;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text-muted);
}

.close:hover {
    color: var(--text);
}

/* ============================================
   FORM
   ============================================ */
.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: var(--text-muted);
    font-size: 0.9rem;
}

.form-group input,
.form-group select {
    width: 100%;
    padding: 0.75rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
    outline: none;
    border-color: var(--primary);
}

/* ============================================
   INSCRIPCION
   ============================================ */
.inscripcion-form {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}

.inscripcion-form select {
    padding: 0.5rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    min-width: 200px;
}

/* ============================================
   TOAST
   ============================================ */
#toast-container {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 200;
}

.toast {
    background: var(--bg-dark);
    color: var(--text);
    padding: 1rem 1.5rem;
    border-radius: var(--radius);
    margin-bottom: 0.5rem;
    border-left: 4px solid var(--primary);
    animation: slideIn 0.3s ease;
}

.toast.success {
    border-color: var(--success);
}

.toast.error {
    border-color: var(--danger);
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
```

---

## 8.4 JavaScript

Crear `public/app.js`:

```javascript
/**
 * App.js - Frontend del Sistema de Gestión
 * =========================================
 * 
 * Este archivo contiene toda la lógica del frontend:
 * - Navegación entre secciones
 * - Llamadas a la API
 * - Renderizado de datos
 * - Manejo de formularios
 */

// ============================================
// CONFIGURACIÓN
// ============================================
const API_URL = '/api';

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Iniciando aplicación...');
    
    // Cargar datos iniciales
    await cargarAlumnos();
    await cargarCursos();
});

// ============================================
// NAVEGACIÓN
// ============================================
function showSection(sectionId) {
    // Ocultar todas las secciones
    document.querySelectorAll('.section').forEach(s => {
        s.classList.remove('active');
    });
    
    // Mostrar la seleccionada
    document.getElementById(`section-${sectionId}`).classList.add('active');
    
    // Actualizar navegación
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Cargar datos si es necesario
    if (sectionId === 'inscripciones') {
        cargarSelectCursos();
    }
}

// ============================================
// MODALES
// ============================================
function showModal(modalId) {
    document.getElementById(modalId).classList.add('show');
    
    // Si es modal de inscripción, cargar alumnos
    if (modalId === 'modal-inscripcion') {
        cargarSelectAlumnos();
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

// ============================================
// TOASTS (Notificaciones)
// ============================================
function showToast(mensaje, tipo = 'info') {
    const container = document.getElementById('toast-container');
    
    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    toast.textContent = mensaje;
    
    container.appendChild(toast);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// ============================================
// ALUMNOS
// ============================================
async function cargarAlumnos() {
    try {
        const response = await fetch(`${API_URL}/alumnos/`);
        const data = await response.json();
        
        renderizarAlumnos(data.alumnos);
        
    } catch (error) {
        console.error('Error cargando alumnos:', error);
        showToast('Error al cargar alumnos', 'error');
    }
}

function renderizarAlumnos(alumnos) {
    const tbody = document.getElementById('tbody-alumnos');
    
    if (!alumnos.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; color: var(--text-muted);">
                    No hay alumnos registrados
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = alumnos.map(a => `
        <tr>
            <td>${a.id}</td>
            <td>${a.nombre_completo}</td>
            <td>${a.dni}</td>
            <td>${a.email}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="eliminarAlumno(${a.id})">
                    Eliminar
                </button>
            </td>
        </tr>
    `).join('');
}

async function crearAlumno(event) {
    event.preventDefault();
    
    const datos = {
        nombre: document.getElementById('alumno-nombre').value,
        apellido: document.getElementById('alumno-apellido').value,
        dni: document.getElementById('alumno-dni').value,
        email: document.getElementById('alumno-email').value
    };
    
    try {
        const response = await fetch(`${API_URL}/alumnos/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al crear alumno');
        }
        
        showToast('Alumno creado correctamente', 'success');
        closeModal('modal-alumno');
        document.getElementById('form-alumno').reset();
        await cargarAlumnos();
        
    } catch (error) {
        showToast(error.message, 'error');
    }
    
    return false;
}

async function eliminarAlumno(id) {
    if (!confirm('¿Eliminar este alumno?')) return;
    
    try {
        await fetch(`${API_URL}/alumnos/${id}`, { method: 'DELETE' });
        showToast('Alumno eliminado', 'success');
        await cargarAlumnos();
        
    } catch (error) {
        showToast('Error al eliminar', 'error');
    }
}

// ============================================
// CURSOS
// ============================================
async function cargarCursos() {
    try {
        const response = await fetch(`${API_URL}/cursos/`);
        const data = await response.json();
        
        renderizarCursos(data.cursos);
        
    } catch (error) {
        console.error('Error cargando cursos:', error);
    }
}

function renderizarCursos(cursos) {
    const tbody = document.getElementById('tbody-cursos');
    
    if (!cursos.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; color: var(--text-muted);">
                    No hay cursos registrados
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = cursos.map(c => `
        <tr>
            <td>${c.id}</td>
            <td>${c.nombre_materia}</td>
            <td>${c.anio}</td>
            <td>${c.cuatrimestre}°</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="eliminarCurso(${c.id})">
                    Eliminar
                </button>
            </td>
        </tr>
    `).join('');
}

async function crearCurso(event) {
    event.preventDefault();
    
    const datos = {
        nombre_materia: document.getElementById('curso-materia').value,
        anio: parseInt(document.getElementById('curso-anio').value),
        cuatrimestre: parseInt(document.getElementById('curso-cuatrimestre').value)
    };
    
    try {
        const response = await fetch(`${API_URL}/cursos/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });
        
        if (!response.ok) {
            throw new Error('Error al crear curso');
        }
        
        showToast('Curso creado correctamente', 'success');
        closeModal('modal-curso');
        document.getElementById('form-curso').reset();
        await cargarCursos();
        
    } catch (error) {
        showToast(error.message, 'error');
    }
    
    return false;
}

async function eliminarCurso(id) {
    if (!confirm('¿Eliminar este curso?')) return;
    
    try {
        await fetch(`${API_URL}/cursos/${id}`, { method: 'DELETE' });
        showToast('Curso eliminado', 'success');
        await cargarCursos();
        
    } catch (error) {
        showToast('Error al eliminar', 'error');
    }
}

// ============================================
// INSCRIPCIONES
// ============================================
async function cargarSelectCursos() {
    try {
        const response = await fetch(`${API_URL}/cursos/`);
        const data = await response.json();
        
        const select = document.getElementById('select-curso');
        select.innerHTML = '<option value="">-- Seleccionar --</option>';
        
        data.cursos.forEach(c => {
            select.innerHTML += `
                <option value="${c.id}">${c.nombre_completo}</option>
            `;
        });
        
    } catch (error) {
        console.error('Error:', error);
    }
}

async function cargarSelectAlumnos() {
    try {
        const response = await fetch(`${API_URL}/alumnos/`);
        const data = await response.json();
        
        const select = document.getElementById('inscripcion-alumno');
        select.innerHTML = '<option value="">-- Seleccionar --</option>';
        
        data.alumnos.forEach(a => {
            select.innerHTML += `
                <option value="${a.id}">${a.nombre_completo}</option>
            `;
        });
        
    } catch (error) {
        console.error('Error:', error);
    }
}

async function cargarAlumnosCurso() {
    const cursoId = document.getElementById('select-curso').value;
    const tbody = document.getElementById('tbody-inscriptos');
    const titulo = document.getElementById('titulo-inscriptos');
    
    if (!cursoId) {
        tbody.innerHTML = '';
        titulo.textContent = 'Alumnos inscriptos';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/inscripciones/curso/${cursoId}`);
        const data = await response.json();
        
        titulo.textContent = `Alumnos inscriptos (${data.total})`;
        
        if (!data.alumnos.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" style="text-align: center; color: var(--text-muted);">
                        No hay alumnos inscriptos
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = data.alumnos.map(a => `
            <tr>
                <td>${a.id}</td>
                <td>${a.nombre_completo}</td>
                <td>${a.dni}</td>
                <td>
                    <button class="btn btn-danger btn-sm" 
                            onclick="desinscribir(${a.id}, ${cursoId})">
                        Desinscribir
                    </button>
                </td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error:', error);
    }
}

async function inscribirAlumno(event) {
    event.preventDefault();
    
    const cursoId = document.getElementById('select-curso').value;
    const alumnoId = document.getElementById('inscripcion-alumno').value;
    
    if (!cursoId) {
        showToast('Seleccione un curso primero', 'error');
        return false;
    }
    
    try {
        const response = await fetch(`${API_URL}/inscripciones/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                alumno_id: parseInt(alumnoId),
                curso_id: parseInt(cursoId)
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al inscribir');
        }
        
        showToast('Alumno inscripto correctamente', 'success');
        closeModal('modal-inscripcion');
        await cargarAlumnosCurso();
        
    } catch (error) {
        showToast(error.message, 'error');
    }
    
    return false;
}

async function desinscribir(alumnoId, cursoId) {
    if (!confirm('¿Desinscribir a este alumno?')) return;
    
    try {
        await fetch(`${API_URL}/inscripciones/${alumnoId}/${cursoId}`, {
            method: 'DELETE'
        });
        
        showToast('Alumno desinscripto', 'success');
        await cargarAlumnosCurso();
        
    } catch (error) {
        showToast('Error al desinscribir', 'error');
    }
}

// ============================================
// EXPORTAR FUNCIONES GLOBALES
// ============================================
window.showSection = showSection;
window.showModal = showModal;
window.closeModal = closeModal;
window.crearAlumno = crearAlumno;
window.eliminarAlumno = eliminarAlumno;
window.crearCurso = crearCurso;
window.eliminarCurso = eliminarCurso;
window.cargarAlumnosCurso = cargarAlumnosCurso;
window.inscribirAlumno = inscribirAlumno;
window.desinscribir = desinscribir;
```

---

## 8.5 Probar el Frontend

1. Ejecutar el servidor:
   ```powershell
   uvicorn src.presentation.api.main:app --reload
   ```

2. Abrir http://localhost:8000

3. Probar:
   - Crear alumnos
   - Crear cursos
   - Inscribir alumnos en cursos
   - Verificar que los datos persisten

---

## 8.6 Resumen

### Archivos creados

```
public/
├── index.html    ✅
├── styles.css    ✅
└── app.js        ✅
```

### Conceptos aplicados

| Concepto | Dónde |
|----------|-------|
| SPA (Single Page App) | Navegación sin recargar |
| Fetch API | Llamadas al backend |
| async/await | Código asíncrono limpio |
| Template literals | HTML dinámico |
| Event handlers | onclick, onsubmit |

---

**Anterior:** [Capítulo 7 - Presentación](./07_presentacion.md)

**Siguiente:** [Capítulo 9 - Testing](./09_testing.md)
