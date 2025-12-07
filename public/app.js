/**
 * Sistema de Seguimiento de Alumnos - JavaScript
 * Maneja la interacción del frontend con la API
 */

// Configuración
const API_URL = 'https://seguimiento-alumnos.vercel.app';

// Estado de la aplicación
const state = {
    alumnos: [],
    currentPage: 'dashboard'
};

// ============================================================================
// Inicialización
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎓 Sistema de Seguimiento de Alumnos iniciado');

    // Configurar navegación
    setupNavigation();

    // Cargar datos iniciales
    loadDashboardData();

    // Configurar búsqueda
    setupSearch();
});

// ============================================================================
// Navegación
// ============================================================================

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            showPage(page);
        });
    });
}

function showPage(pageName) {
    // Actualizar estado
    state.currentPage = pageName;

    // Ocultar todas las páginas
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Mostrar página seleccionada
    const targetPage = document.getElementById(`page-${pageName}`);
    if (targetPage) {
        targetPage.classList.add('active');
    }

    // Actualizar nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageName) {
            link.classList.add('active');
        }
    });

    // Cargar datos específicos de la página
    loadPageData(pageName);
}

function loadPageData(pageName) {
    switch (pageName) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'alumnos':
            loadAlumnos();
            break;
        case 'alertas':
            // Cargar alertas
            break;
        case 'reportes':
            // Cargar reportes
            break;
    }
}

// ============================================================================
// Dashboard
// ============================================================================

async function loadDashboardData() {
    try {
        // Cargar alumnos para contar
        const response = await fetch(`${API_URL}/alumnos`);
        const data = await response.json();

        // Actualizar contador
        const totalElement = document.getElementById('total-alumnos');
        if (totalElement) {
            totalElement.textContent = data.total || 0;
            animateNumber(totalElement, 0, data.total || 0, 1000);
        }

    } catch (error) {
        console.error('Error al cargar dashboard:', error);
        showToast('Error al cargar datos del dashboard', 'error');
    }
}

function animateNumber(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            element.textContent = end;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// ============================================================================
// Alumnos
// ============================================================================

async function loadAlumnos() {
    try {
        showLoading('alumnos-tbody');

        const response = await fetch(`${API_URL}/alumnos`);
        const data = await response.json();

        state.alumnos = data.alumnos || [];
        renderAlumnos(state.alumnos);

    } catch (error) {
        console.error('Error al cargar alumnos:', error);
        showError('alumnos-tbody', 'Error al cargar alumnos');
        showToast('Error al cargar la lista de alumnos', 'error');
    }
}

function renderAlumnos(alumnos) {
    const tbody = document.getElementById('alumnos-tbody');

    if (!alumnos || alumnos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="loading">No hay alumnos registrados</td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = alumnos.map(alumno => `
        <tr>
            <td>${alumno.id}</td>
            <td><strong>${alumno.nombre_completo}</strong></td>
            <td>${alumno.dni}</td>
            <td>${alumno.email}</td>
            <td>${alumno.cohorte}</td>
            <td>
                <span class="badge" style="background: var(--success);">Activo</span>
            </td>
            <td>
                <button class="btn-sm" onclick="verAlumno(${alumno.id})">Ver</button>
                <button class="btn-sm" onclick="editarAlumno(${alumno.id})" style="background: var(--warning);">Editar</button>
            </td>
        </tr>
    `).join('');
}

async function crearAlumno() {
    const form = document.getElementById('form-nuevo-alumno');
    const formData = new FormData(form);

    const alumnoData = {
        nombre: formData.get('nombre'),
        apellido: formData.get('apellido'),
        dni: formData.get('dni'),
        email: formData.get('email'),
        cohorte: parseInt(formData.get('cohorte'))
    };

    // Validar
    if (!alumnoData.nombre || !alumnoData.apellido || !alumnoData.dni || !alumnoData.email || !alumnoData.cohorte) {
        showToast('Por favor completa todos los campos', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/alumnos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(alumnoData)
        });

        const data = await response.json();

        if (response.ok) {
            showToast('Alumno creado exitosamente', 'success');
            closeModal('modal-nuevo-alumno');
            form.reset();
            loadAlumnos(); // Recargar lista
        } else {
            showToast(data.error || 'Error al crear alumno', 'error');
        }

    } catch (error) {
        console.error('Error al crear alumno:', error);
        showToast('Error al crear alumno', 'error');
    }
}

function verAlumno(id) {
    showToast(`Ver detalles del alumno ${id}`, 'info');
    // TODO: Implementar vista de detalle
}

function editarAlumno(id) {
    showToast(`Editar alumno ${id}`, 'info');
    // TODO: Implementar edición
}

// ============================================================================
// Búsqueda
// ============================================================================

function setupSearch() {
    const searchInput = document.getElementById('search-alumnos');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            filterAlumnos(query);
        });
    }
}

function filterAlumnos(query) {
    if (!query) {
        renderAlumnos(state.alumnos);
        return;
    }

    const filtered = state.alumnos.filter(alumno => {
        return alumno.nombre_completo.toLowerCase().includes(query) ||
            alumno.dni.includes(query) ||
            alumno.email.toLowerCase().includes(query);
    });

    renderAlumnos(filtered);
}

// ============================================================================
// Modales
// ============================================================================

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Cerrar modal al hacer click fuera
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// ============================================================================
// Notificaciones Toast
// ============================================================================

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span style="font-size: 1.5rem;">
            ${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}
        </span>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // Auto-remover después de 3 segundos
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s';
        setTimeout(() => {
            container.removeChild(toast);
        }, 300);
    }, 3000);
}

// ============================================================================
// Utilidades
// ============================================================================

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <tr>
                <td colspan="7" class="loading">
                    <span style="font-size: 2rem;">⏳</span>
                    <br>Cargando...
                </td>
            </tr>
        `;
    }
}

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <tr>
                <td colspan="7" class="loading" style="color: var(--danger);">
                    <span style="font-size: 2rem;">❌</span>
                    <br>${message}
                </td>
            </tr>
        `;
    }
}

// ============================================================================
// Exportar funciones globales
// ============================================================================

window.showPage = showPage;
window.showModal = showModal;
window.closeModal = closeModal;
window.crearAlumno = crearAlumno;
window.verAlumno = verAlumno;
window.editarAlumno = editarAlumno;
