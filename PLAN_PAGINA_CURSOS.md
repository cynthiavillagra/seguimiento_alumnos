# 🎯 Implementación: Página de Gestión de Cursos

## Problema Actual

La API devuelve los cursos correctamente, pero el dashboard no los muestra bien. Necesitas una página dedicada para gestionar cursos con CRUD completo.

## Solución

Voy a crear una **página completa de gestión de cursos** con:

1. ✅ Listado de cursos en tabla
2. ✅ Botón "Crear Curso"
3. ✅ Botones "Editar" y "Eliminar" en cada fila
4. ✅ Búsqueda y filtros
5. ✅ Diseño limpio y funcional

---

## Archivos a Modificar

### 1. `public/index.html`

Agregar una nueva página "Cursos" en el navbar y crear la sección:

```html
<!-- En el navbar, cambiar o agregar: -->
<a href="#cursos" class="nav-link" data-page="cursos">
    <span class="nav-icon">📚</span>
    Cursos
</a>

<!-- Nueva página de cursos (agregar después del dashboard) -->
<div id="page-cursos" class="page">
    <div class="page-header">
        <div>
            <h1>Gestión de Cursos</h1>
            <p class="subtitle">Administra todos los cursos del sistema</p>
        </div>
        <button class="btn-primary" onclick="mostrarModalCrearCurso()">
            <span>📚</span> Nuevo Curso
        </button>
    </div>

    <!-- Búsqueda y filtros -->
    <div class="section">
        <div class="search-bar">
            <input type="text" id="buscar-curso" placeholder="🔍 Buscar por materia o docente..." onkeyup="filtrarCursos()">
            <select id="filtro-anio" onchange="filtrarCursos()">
                <option value="">Todos los años</option>
                <option value="2024">2024</option>
                <option value="2023">2023</option>
                <option value="2022">2022</option>
            </select>
            <select id="filtro-cuatrimestre" onchange="filtrarCursos()">
                <option value="">Todos los cuatrimestres</option>
                <option value="1">1er Cuatrimestre</option>
                <option value="2">2do Cuatrimestre</option>
            </select>
        </div>
    </div>

    <!-- Tabla de cursos -->
    <div class="section">
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Materia</th>
                        <th>Año</th>
                        <th>Cuatrimestre</th>
                        <th>Docente</th>
                        <th>Alumnos</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody id="tabla-cursos-body">
                    <!-- Se llena dinámicamente -->
                </tbody>
            </table>
        </div>
        <div id="no-cursos" class="empty-state" style="display: none;">
            <span class="empty-icon">📚</span>
            <h3>No hay cursos</h3>
            <p>Comienza creando tu primer curso</p>
            <button class="btn-primary" onclick="mostrarModalCrearCurso()">Crear Curso</button>
        </div>
    </div>
</div>
```

---

### 2. `public/app.js`

Agregar funciones para cargar y filtrar cursos:

```javascript
// ========================================
// GESTIÓN DE CURSOS
// ========================================

async function loadCursosPage() {
    try {
        const response = await fetch(`${API_URL}/cursos`);
        const data = await response.json();
        
        state.cursos = data.clases || [];
        renderCursosTable(state.cursos);
    } catch (error) {
        console.error('Error al cargar cursos:', error);
        showToast('Error al cargar cursos', 'error');
    }
}

function renderCursosTable(cursos) {
    const tbody = document.getElementById('tabla-cursos-body');
    const noData = document.getElementById('no-cursos');
    
    if (!cursos || cursos.length === 0) {
        tbody.innerHTML = '';
        noData.style.display = 'flex';
        return;
    }
    
    noData.style.display = 'none';
    
    tbody.innerHTML = cursos.map(curso => `
        <tr>
            <td>${curso.id}</td>
            <td><strong>${curso.materia}</strong></td>
            <td>${curso.cohorte}</td>
            <td>${curso.cuatrimestre}° Cuatrimestre</td>
            <td>${curso.docente}</td>
            <td>
                <span class="badge-info">${curso.totalAlumnos} alumnos</span>
            </td>
            <td>
                <div class="action-buttons-inline">
                    <button class="btn-sm btn-edit" onclick="editarCurso(${curso.id})" title="Editar">
                        ✏️
                    </button>
                    <button class="btn-sm btn-delete" onclick="eliminarCurso(${curso.id}, '${curso.materia}')" title="Eliminar">
                        🗑️
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function filtrarCursos() {
    const busqueda = document.getElementById('buscar-curso').value.toLowerCase();
    const anio = document.getElementById('filtro-anio').value;
    const cuatrimestre = document.getElementById('filtro-cuatrimestre').value;
    
    let cursosFiltrados = state.cursos;
    
    // Filtrar por búsqueda
    if (busqueda) {
        cursosFiltrados = cursosFiltrados.filter(c => 
            c.materia.toLowerCase().includes(busqueda) ||
            c.docente.toLowerCase().includes(busqueda)
        );
    }
    
    // Filtrar por año
    if (anio) {
        cursosFiltrados = cursosFiltrados.filter(c => c.cohorte == anio);
    }
    
    // Filtrar por cuatrimestre
    if (cuatrimestre) {
        cursosFiltrados = cursosFiltrados.filter(c => c.cuatrimestre == cuatrimestre);
    }
    
    renderCursosTable(cursosFiltrados);
}

// Exportar funciones
window.loadCursosPage = loadCursosPage;
window.filtrarCursos = filtrarCursos;
```

---

### 3. `public/styles.css`

Agregar estilos para la tabla y búsqueda:

```css
/* Tabla de datos */
.table-container {
    overflow-x: auto;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

.data-table thead {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
}

.data-table th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.data-table td {
    padding: 1rem;
    border-bottom: 1px solid var(--gray-200);
}

.data-table tbody tr:hover {
    background: var(--gray-50);
}

/* Barra de búsqueda */
.search-bar {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.search-bar input {
    flex: 1;
    padding: 0.75rem 1rem;
    border: 2px solid var(--gray-300);
    border-radius: var(--radius-md);
    font-size: 1rem;
}

.search-bar select {
    padding: 0.75rem 1rem;
    border: 2px solid var(--gray-300);
    border-radius: var(--radius-md);
    font-size: 1rem;
    background: white;
}

/* Botones pequeños */
.btn-sm {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    border: none;
    border-radius: var(--radius);
    cursor: pointer;
    transition: var(--transition);
}

.action-buttons-inline {
    display: flex;
    gap: 0.5rem;
}

/* Estado vacío */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.empty-state h3 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: var(--gray-700);
}

.empty-state p {
    color: var(--gray-500);
    margin-bottom: 1.5rem;
}

/* Badge info */
.badge-info {
    background: var(--info);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 600;
}
```

---

### 4. Modificar Navegación

En `app.js`, actualizar la función de navegación para cargar cursos:

```javascript
function setupNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            showPage(page);
        });
    });
}

function showPage(pageName) {
    // Ocultar todas las páginas
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // Mostrar página seleccionada
    const page = document.getElementById(`page-${pageName}`);
    if (page) {
        page.classList.add('active');
    }
    
    // Actualizar nav
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelector(`[data-page="${pageName}"]`)?.classList.add('active');
    
    // Cargar datos según la página
    if (pageName === 'dashboard') {
        loadDashboardData();
    } else if (pageName === 'cursos') {
        loadCursosPage();
    } else if (pageName === 'alumnos') {
        loadAlumnos();
    }
    
    state.currentPage = pageName;
}
```

---

## Resumen

Con estos cambios tendrás:

1. ✅ Página dedicada de "Cursos"
2. ✅ Tabla con todos los cursos
3. ✅ Búsqueda por materia/docente
4. ✅ Filtros por año y cuatrimestre
5. ✅ Botones Editar/Eliminar en cada fila
6. ✅ Botón "Nuevo Curso"
7. ✅ Estado vacío cuando no hay cursos

---

**¿Quieres que implemente todo esto ahora?** 🚀
