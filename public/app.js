/**
 * Sistema de Seguimiento de Alumnos - JavaScript
 * Maneja la interacción del frontend con la API
 */

// Configuración
const API_URL = '/api'; // Ruta relativa para Vercel

// Estado de la aplicación
const state = {
    alumnos: [],
    currentPage: 'dashboard',
    claseActual: {
        materia: null,
        cohorte: null,
        fecha: null,
        registros: {} // { alumnoId: { asistencia, participacion, observaciones } }
    }
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

    // Configurar fecha actual
    const fechaInput = document.getElementById('fecha-clase');
    if (fechaInput) {
        fechaInput.valueAsDate = new Date();
    }
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
        case 'registro-clase':
            // No cargar nada hasta que seleccione la clase
            break;
        case 'alertas':
            // Cargar alertas
            break;
    }
}

// ============================================================================
// Dashboard
// ============================================================================

async function loadDashboardData() {
    try {
        const response = await fetch(`${API_URL}/alumnos`);
        const data = await response.json();

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
// Registro de Clase
// ============================================================================

async function iniciarRegistroClase() {
    const materia = document.getElementById('select-materia').value;
    const cohorte = document.getElementById('select-cohorte').value;
    const fecha = document.getElementById('fecha-clase').value;

    if (!materia || !cohorte || !fecha) {
        showToast('Por favor completa todos los campos', 'error');
        return;
    }

    // Guardar datos de la clase
    state.claseActual = {
        materia,
        cohorte,
        fecha,
        registros: {}
    };

    // Ocultar selección, mostrar registro
    document.getElementById('seleccion-clase').style.display = 'none';
    document.getElementById('registro-asistencia').style.display = 'block';

    // Actualizar título
    const materiaTexto = document.querySelector(`#select-materia option[value="${materia}"]`).textContent;
    document.getElementById('clase-titulo').textContent = `${materiaTexto} - Cohorte ${cohorte}`;

    // Formatear fecha
    const fechaObj = new Date(fecha + 'T00:00:00');
    const fechaFormateada = fechaObj.toLocaleDateString('es-AR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });
    document.getElementById('clase-fecha').textContent = fechaFormateada;

    // Cargar alumnos
    await cargarAlumnosParaRegistro();
}

async function cargarAlumnosParaRegistro() {
    try {
        const response = await fetch(`${API_URL}/alumnos`);
        const data = await response.json();

        const container = document.getElementById('lista-registro-alumnos');
        container.innerHTML = '';

        data.alumnos.forEach(alumno => {
            const card = crearCardRegistroAlumno(alumno);
            container.appendChild(card);

            // Inicializar registro vacío
            state.claseActual.registros[alumno.id] = {
                asistencia: null,
                participacion: null,
                observaciones: ''
            };
        });

        actualizarContadores();

    } catch (error) {
        console.error('Error al cargar alumnos:', error);
        showToast('Error al cargar alumnos', 'error');
    }
}

function crearCardRegistroAlumno(alumno) {
    const card = document.createElement('div');
    card.className = 'alumno-registro-card';
    card.innerHTML = `
        <div class="alumno-registro-header">
            <div class="alumno-registro-nombre">${alumno.nombre_completo}</div>
            <div class="asistencia-buttons">
                <button class="asistencia-btn" onclick="marcarAsistencia(${alumno.id}, 'presente')">
                    ✓ Presente
                </button>
                <button class="asistencia-btn" onclick="marcarAsistencia(${alumno.id}, 'ausente')">
                    ✗ Ausente
                </button>
                <button class="asistencia-btn" onclick="marcarAsistencia(${alumno.id}, 'tarde')">
                    ⏰ Tarde
                </button>
            </div>
        </div>
        <div>
            <label style="font-size: 0.875rem; color: var(--gray-600); margin-bottom: 0.5rem; display: block;">
                Participación:
            </label>
            <div class="participacion-buttons">
                <button class="participacion-btn" onclick="marcarParticipacion(${alumno.id}, 'alta')">
                    Alta
                </button>
                <button class="participacion-btn" onclick="marcarParticipacion(${alumno.id}, 'media')">
                    Media
                </button>
                <button class="participacion-btn" onclick="marcarParticipacion(${alumno.id}, 'baja')">
                    Baja
                </button>
                <button class="participacion-btn" onclick="marcarParticipacion(${alumno.id}, 'nula')">
                    Nula
                </button>
            </div>
        </div>
        <textarea 
            class="observaciones-input" 
            placeholder="Observaciones (opcional)..."
            onchange="guardarObservacion(${alumno.id}, this.value)"
        ></textarea>
    `;
    return card;
}

function marcarAsistencia(alumnoId, estado) {
    // Actualizar estado
    state.claseActual.registros[alumnoId].asistencia = estado;

    // Actualizar UI - remover clase activa de todos los botones
    const card = event.target.closest('.alumno-registro-card');
    card.querySelectorAll('.asistencia-btn').forEach(btn => {
        btn.classList.remove('presente', 'ausente', 'tarde');
    });

    // Agregar clase al botón clickeado
    event.target.classList.add(estado);

    // Actualizar contadores
    actualizarContadores();

    showToast(`Asistencia registrada: ${estado}`, 'success');
}

function marcarParticipacion(alumnoId, nivel) {
    // Actualizar estado
    state.claseActual.registros[alumnoId].participacion = nivel;

    // Actualizar UI
    const card = event.target.closest('.alumno-registro-card');
    card.querySelectorAll('.participacion-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

function guardarObservacion(alumnoId, texto) {
    state.claseActual.registros[alumnoId].observaciones = texto;
}

function actualizarContadores() {
    let presentes = 0;
    let ausentes = 0;

    Object.values(state.claseActual.registros).forEach(registro => {
        if (registro.asistencia === 'presente' || registro.asistencia === 'tarde') {
            presentes++;
        } else if (registro.asistencia === 'ausente') {
            ausentes++;
        }
    });

    document.getElementById('count-presentes').textContent = presentes;
    document.getElementById('count-ausentes').textContent = ausentes;
}

async function guardarClase() {
    // Validar que al menos se haya tomado asistencia
    const registrosCompletos = Object.values(state.claseActual.registros).filter(
        r => r.asistencia !== null
    ).length;

    if (registrosCompletos === 0) {
        showToast('Debes registrar al menos la asistencia de un alumno', 'error');
        return;
    }

    try {
        // TODO: Enviar a la API
        console.log('Guardando clase:', state.claseActual);

        showToast(`Clase guardada exitosamente (${registrosCompletos} registros)`, 'success');

        // Resetear formulario
        cancelarRegistro();
        showPage('dashboard');

    } catch (error) {
        console.error('Error al guardar clase:', error);
        showToast('Error al guardar la clase', 'error');
    }
}

function cancelarRegistro() {
    document.getElementById('seleccion-clase').style.display = 'block';
    document.getElementById('registro-asistencia').style.display = 'none';

    // Limpiar formulario
    document.getElementById('select-materia').value = '';
    document.getElementById('select-cohorte').value = '';

    // Resetear estado
    state.claseActual = {
        materia: null,
        cohorte: null,
        fecha: null,
        registros: {}
    };
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
                <button class="btn-sm" onclick="verFichaAlumno(${alumno.id})">Ver Ficha</button>
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
            loadAlumnos();
        } else {
            showToast(data.error || 'Error al crear alumno', 'error');
        }

    } catch (error) {
        console.error('Error al crear alumno:', error);
        showToast('Error al crear alumno', 'error');
    }
}

function verFichaAlumno(id) {
    // Cargar datos del alumno
    const alumno = state.alumnos.find(a => a.id === id);

    if (!alumno) {
        showToast('Alumno no encontrado', 'error');
        return;
    }

    // Actualizar página de ficha
    document.getElementById('ficha-nombre').textContent = alumno.nombre_completo;
    document.getElementById('ficha-dni').textContent = `DNI: ${alumno.dni}`;

    // Mostrar página
    showPage('ficha-alumno');
}

function editarAlumno(id) {
    showToast(`Editar alumno ${id}`, 'info');
    // TODO: Implementar edición
}

function aplicarFiltroFechas() {
    const desde = document.getElementById('filtro-desde').value;
    const hasta = document.getElementById('filtro-hasta').value;

    if (!desde || !hasta) {
        showToast('Selecciona ambas fechas', 'error');
        return;
    }

    showToast(`Filtrando desde ${desde} hasta ${hasta}`, 'info');
    // TODO: Implementar filtro
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
window.verFichaAlumno = verFichaAlumno;
window.editarAlumno = editarAlumno;
window.iniciarRegistroClase = iniciarRegistroClase;
window.marcarAsistencia = marcarAsistencia;
window.marcarParticipacion = marcarParticipacion;
window.guardarObservacion = guardarObservacion;
window.guardarClase = guardarClase;
window.cancelarRegistro = cancelarRegistro;
window.aplicarFiltroFechas = aplicarFiltroFechas;
