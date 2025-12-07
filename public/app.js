/**
 * Sistema de Seguimiento de Alumnos - JavaScript
 * Maneja la interacción del frontend con la API
 */

// Configuración
// En Vercel, la API está en la raíz (sin /api)
const API_URL = window.location.hostname.includes('vercel.app') ? '' : '/api';

// Estado de la aplicación
const state = {
    alumnos: [],
    clases: [],
    claseSeleccionada: null,
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
    console.log('API URL:', API_URL || '(raíz)');

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
        const url = `${API_URL}/clases`;
        console.log('Cargando clases desde:', url);

        const response = await fetch(url);
        const data = await response.json();

        console.log('Clases recibidas:', data);

        state.clases = data.clases || [];
        renderClasesCards(state.clases);

    } catch (error) {
        console.error('Error al cargar clases:', error);
        showToast('Error al cargar clases', 'error');
    }
}

function renderClasesCards(clases) {
    const container = document.getElementById('clases-grid');

    if (!clases || clases.length === 0) {
        container.innerHTML = `
            <div class="loading-clases">
                <span style="font-size: 3rem;">📚</span>
                <p>No hay clases registradas</p>
            </div>
        `;
        return;
    }

    container.innerHTML = clases.map(clase => `
        <div class="clase-card" onclick="verClaseDetalle(${clase.id})">
            <div class="clase-card-header">
                <div class="clase-card-materia">${clase.materia}</div>
                <div class="clase-card-cohorte">Cohorte ${clase.cohorte}</div>
            </div>
            <div class="clase-card-stats">
                <div class="clase-stat">
                    <span class="clase-stat-icon">👥</span>
                    <span class="clase-stat-label">Alumnos</span>
                    <span class="clase-stat-value">${clase.totalAlumnos}</span>
                </div>
                <div class="clase-stat">
                    <span class="clase-stat-icon">📊</span>
                    <span class="clase-stat-label">Asistencia</span>
                    <span class="clase-stat-value ${clase.asistenciaPromedio >= 80 ? 'success' : clase.asistenciaPromedio >= 70 ? 'warning' : 'danger'}">${clase.asistenciaPromedio}%</span>
                </div>
                <div class="clase-stat">
                    <span class="clase-stat-icon">🚨</span>
                    <span class="clase-stat-label">En riesgo</span>
                    <span class="clase-stat-value ${clase.alumnosEnRiesgo > 0 ? 'danger' : 'success'}">${clase.alumnosEnRiesgo}</span>
                </div>
                <div class="clase-stat">
                    <span class="clase-stat-icon">📚</span>
                    <span class="clase-stat-label">Clases</span>
                    <span class="clase-stat-value">${clase.totalClases}</span>
                </div>
            </div>
            <div class="clase-card-actions" onclick="event.stopPropagation()">
                <button class="clase-card-btn clase-card-btn-primary" onclick="registrarClaseDirecta(${clase.id})">
                    Registrar
                </button>
                <button class="clase-card-btn clase-card-btn-secondary" onclick="verClaseDetalle(${clase.id})">
                    Ver Detalle
                </button>
            </div>
        </div>
    `).join('');
}

function verClaseDetalle(claseId) {
    const clase = state.clases.find(c => c.id === claseId);

    if (!clase) {
        showToast('Clase no encontrada', 'error');
        return;
    }

    // Guardar clase actual
    state.claseSeleccionada = clase;

    // Actualizar título
    document.getElementById('clase-detalle-titulo').textContent = `${clase.materia} - Cohorte ${clase.cohorte}`;
    document.getElementById('clase-detalle-subtitulo').textContent = `Última clase: ${clase.ultimaClase}`;

    // Actualizar stats
    document.getElementById('clase-total-alumnos').textContent = clase.totalAlumnos;
    document.getElementById('clase-asistencia').textContent = `${clase.asistenciaPromedio}%`;
    document.getElementById('clase-en-riesgo').textContent = clase.alumnosEnRiesgo;
    document.getElementById('clase-total-clases').textContent = clase.totalClases;

    // Mostrar página
    showPage('clase-detalle');
}

function registrarClaseDirecta(claseId) {
    const clase = state.clases.find(c => c.id === claseId);

    if (!clase) {
        showToast('Clase no encontrada', 'error');
        return;
    }

    // Pre-seleccionar materia y cohorte
    state.claseSeleccionada = clase;

    // Ir a página de registro
    showPage('registro-clase');

    // Pre-llenar formulario
    document.getElementById('select-materia').value = clase.materia.toLowerCase().replace(' ', '');
    document.getElementById('select-cohorte').value = clase.cohorte.toString();

    showToast(`Registrando clase de ${clase.materia}`, 'info');
}

function verAlumnosClase() {
    if (!state.claseSeleccionada) {
        showToast('No hay clase seleccionada', 'error');
        return;
    }
    showPage('alumnos');
}

function verAlertasClase() {
    if (!state.claseSeleccionada) {
        showToast('No hay clase seleccionada', 'error');
        return;
    }
    showPage('alertas');
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
        const url = `${API_URL}/alumnos`;
        console.log('Cargando alumnos desde:', url);

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Alumnos recibidos:', data);

        const alumnos = data.alumnos || [];

        if (alumnos.length === 0) {
            showToast('No hay alumnos registrados', 'error');
            return;
        }

        const container = document.getElementById('lista-registro-alumnos');
        container.innerHTML = '';

        alumnos.forEach(alumno => {
            const card = crearCardRegistroAlumno(alumno);
            container.appendChild(card);

            // Inicializar registro vacío con todas las variables
            state.claseActual.registros[alumno.id] = {
                asistencia: null,
                participacion: null,
                tpEntregado: null,
                notaTP: null,
                actitud: null,
                observaciones: ''
            };
        });

        actualizarContadores();

    } catch (error) {
        console.error('Error al cargar alumnos:', error);
        showToast(`Error al cargar alumnos: ${error.message}`, 'error');
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
        
        <!-- Participación -->
        <div class="registro-section">
            <label class="registro-label">Participación:</label>
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

        <!-- Trabajo Práctico -->
        <div class="registro-section">
            <label class="registro-label">Trabajo Práctico:</label>
            <div class="tp-container">
                <div class="tp-entrega">
                    <button class="tp-btn" onclick="marcarTPEntregado(${alumno.id}, true)">
                        ✓ Entregado
                    </button>
                    <button class="tp-btn" onclick="marcarTPEntregado(${alumno.id}, false)">
                        ✗ No Entregado
                    </button>
                </div>
                <div class="tp-calificacion">
                    <label class="tp-label">Nota:</label>
                    <input 
                        type="number" 
                        min="1" 
                        max="10" 
                        step="0.5"
                        class="tp-nota-input" 
                        placeholder="1-10"
                        onchange="guardarNotaTP(${alumno.id}, this.value)"
                    />
                </div>
            </div>
        </div>

        <!-- Actitud -->
        <div class="registro-section">
            <label class="registro-label">Actitud en Clase:</label>
            <div class="actitud-buttons">
                <button class="actitud-btn" onclick="marcarActitud(${alumno.id}, 'excelente')">
                    😊 Excelente
                </button>
                <button class="actitud-btn" onclick="marcarActitud(${alumno.id}, 'buena')">
                    🙂 Buena
                </button>
                <button class="actitud-btn" onclick="marcarActitud(${alumno.id}, 'regular')">
                    😐 Regular
                </button>
                <button class="actitud-btn" onclick="marcarActitud(${alumno.id}, 'mala')">
                    😞 Mala
                </button>
            </div>
        </div>

        <!-- Observaciones -->
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

function marcarTPEntregado(alumnoId, entregado) {
    // Actualizar estado
    state.claseActual.registros[alumnoId].tpEntregado = entregado;

    // Actualizar UI
    const card = event.target.closest('.alumno-registro-card');
    card.querySelectorAll('.tp-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    showToast(`TP ${entregado ? 'entregado' : 'no entregado'}`, 'info');
}

function guardarNotaTP(alumnoId, nota) {
    const notaNum = parseFloat(nota);

    if (nota && (notaNum < 1 || notaNum > 10)) {
        showToast('La nota debe estar entre 1 y 10', 'error');
        return;
    }

    state.claseActual.registros[alumnoId].notaTP = nota ? notaNum : null;

    if (nota) {
        showToast(`Nota TP registrada: ${notaNum}`, 'success');
    }
}

function marcarActitud(alumnoId, actitud) {
    // Actualizar estado
    state.claseActual.registros[alumnoId].actitud = actitud;

    // Actualizar UI
    const card = event.target.closest('.alumno-registro-card');
    card.querySelectorAll('.actitud-btn').forEach(btn => {
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

        const url = `${API_URL}/alumnos`;
        const response = await fetch(url);
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
        const url = `${API_URL}/alumnos`;
        const response = await fetch(url, {
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
// Nuevas funciones de clases
window.verClaseDetalle = verClaseDetalle;
window.registrarClaseDirecta = registrarClaseDirecta;
window.verAlumnosClase = verAlumnosClase;
window.verAlertasClase = verAlertasClase;
// Nuevas funciones de registro completo
window.marcarTPEntregado = marcarTPEntregado;
window.guardarNotaTP = guardarNotaTP;
window.marcarActitud = marcarActitud;

// ========================================
// FUNCIONES DE CREACIÓN
// ========================================

function mostrarModalCrearAlumno() {
    showModal('modal-nuevo-alumno');
}

function mostrarModalCrearCurso() {
    showModal('modal-crear-curso');
}

async function mostrarModalCrearTP() {
    // Cargar cursos en el select
    try {
        const response = await fetch(`${API_BASE_URL}/cursos`);
        const data = await response.json();

        const select = document.getElementById('tp-curso');
        select.innerHTML = '<option value="">Selecciona un curso...</option>';

        data.clases.forEach(curso => {
            const option = document.createElement('option');
            option.value = curso.id;
            option.textContent = `${curso.materia} - ${curso.cohorte}`;
            select.appendChild(option);
        });

        showModal('modal-crear-tp');
    } catch (error) {
        console.error('Error al cargar cursos:', error);
        showToast('Error al cargar cursos', 'error');
    }
}

function cerrarModal(modalId) {
    closeModal(modalId);
}

async function crearCurso() {
    const materia = document.getElementById('curso-materia').value.trim();
    const anio = parseInt(document.getElementById('curso-anio').value);
    const cuatrimestre = parseInt(document.getElementById('curso-cuatrimestre').value);
    const docente = document.getElementById('curso-docente').value.trim();

    if (!materia || !anio || !cuatrimestre || !docente) {
        showToast('Por favor completa todos los campos', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/cursos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre_materia: materia,
                anio: anio,
                cuatrimestre: cuatrimestre,
                docente_responsable: docente
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showToast('Curso creado exitosamente', 'success');
            cerrarModal('modal-crear-curso');
            document.getElementById('form-crear-curso').reset();
            // Recargar dashboard
            if (state.currentPage === 'dashboard') {
                loadDashboardData();
            }
        } else {
            showToast(data.error || 'Error al crear curso', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al crear curso', 'error');
    }
}

async function crearTP() {
    const cursoId = parseInt(document.getElementById('tp-curso').value);
    const titulo = document.getElementById('tp-titulo').value.trim();
    const descripcion = document.getElementById('tp-descripcion').value.trim();
    const fecha = document.getElementById('tp-fecha').value;

    if (!cursoId || !titulo || !fecha) {
        showToast('Por favor completa todos los campos requeridos', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/trabajos-practicos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                curso_id: cursoId,
                titulo: titulo,
                descripcion: descripcion,
                fecha_entrega: fecha
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showToast('Trabajo Práctico creado exitosamente', 'success');
            cerrarModal('modal-crear-tp');
            document.getElementById('form-crear-tp').reset();
        } else {
            showToast(data.error || 'Error al crear TP', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al crear TP', 'error');
    }
}

// Exportar nuevas funciones
window.mostrarModalCrearAlumno = mostrarModalCrearAlumno;
window.mostrarModalCrearCurso = mostrarModalCrearCurso;
window.mostrarModalCrearTP = mostrarModalCrearTP;
window.cerrarModal = cerrarModal;
window.crearCurso = crearCurso;
window.crearTP = crearTP;

// ========================================
// FUNCIONES DE EDICI�N Y ELIMINACI�N
// ========================================

// Variable global para manejar confirmaci�n de eliminaci�n
let accionEliminar = null;

// EDITAR ALUMNO
async function editarAlumno(id) {
    try {
        const response = await fetch(`{API_URL}/alumnos`);
        const data = await response.json();
        const alumno = data.alumnos.find(a => a.id === id);
        
        if (!alumno) {
            showToast('Alumno no encontrado', 'error');
            return;
        }
        
        document.getElementById('edit-alumno-id').value = alumno.id;
        document.getElementById('edit-alumno-nombre').value = alumno.nombre;
        document.getElementById('edit-alumno-apellido').value = alumno.apellido;
        document.getElementById('edit-alumno-dni').value = alumno.dni;
        document.getElementById('edit-alumno-email').value = alumno.email;
        document.getElementById('edit-alumno-cohorte').value = alumno.cohorte;
        
        showModal('modal-editar-alumno');
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar alumno', 'error');
    }
}

async function guardarEdicionAlumno() {
    const id = document.getElementById('edit-alumno-id').value;
    const data = {
        nombre: document.getElementById('edit-alumno-nombre').value.trim(),
        apellido: document.getElementById('edit-alumno-apellido').value.trim(),
        dni: document.getElementById('edit-alumno-dni').value.trim(),
        email: document.getElementById('edit-alumno-email').value.trim(),
        cohorte: parseInt(document.getElementById('edit-alumno-cohorte').value)
    };
    
    try {
        const response = await fetch(`/alumnos/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showToast('Alumno actualizado exitosamente', 'success');
            cerrarModal('modal-editar-alumno');
            loadAlumnos();
        } else {
            showToast(result.error || 'Error al actualizar alumno', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al actualizar alumno', 'error');
    }
}

// EDITAR CURSO
async function editarCurso(id) {
    try {
        const response = await fetch(`/cursos`);
        const data = await response.json();
        const curso = data.clases.find(c => c.id === id);
        
        if (!curso) {
            showToast('Curso no encontrado', 'error');
            return;
        }
        
        document.getElementById('edit-curso-id').value = curso.id;
        document.getElementById('edit-curso-materia').value = curso.materia;
        document.getElementById('edit-curso-anio').value = curso.cohorte;
        document.getElementById('edit-curso-cuatrimestre').value = curso.cuatrimestre;
        document.getElementById('edit-curso-docente').value = curso.docente;
        
        showModal('modal-editar-curso');
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar curso', 'error');
    }
}

async function guardarEdicionCurso() {
    const id = document.getElementById('edit-curso-id').value;
    const data = {
        nombre_materia: document.getElementById('edit-curso-materia').value.trim(),
        anio: parseInt(document.getElementById('edit-curso-anio').value),
        cuatrimestre: parseInt(document.getElementById('edit-curso-cuatrimestre').value),
        docente_responsable: document.getElementById('edit-curso-docente').value.trim()
    };
    
    try {
        const response = await fetch(`/cursos/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showToast('Curso actualizado exitosamente', 'success');
            cerrarModal('modal-editar-curso');
            loadDashboardData();
        } else {
            showToast(result.error || 'Error al actualizar curso', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al actualizar curso', 'error');
    }
}

// EDITAR TP
async function editarTP(id) {
    try {
        const response = await fetch(`/trabajos-practicos`);
        const data = await response.json();
        const tp = data.tps.find(t => t.id === id);
        
        if (!tp) {
            showToast('TP no encontrado', 'error');
            return;
        }
        
        document.getElementById('edit-tp-id').value = tp.id;
        document.getElementById('edit-tp-titulo').value = tp.titulo;
        document.getElementById('edit-tp-descripcion').value = tp.descripcion || '';
        document.getElementById('edit-tp-fecha').value = tp.fecha_entrega;
        
        showModal('modal-editar-tp');
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar TP', 'error');
    }
}

async function guardarEdicionTP() {
    const id = document.getElementById('edit-tp-id').value;
    const data = {
        titulo: document.getElementById('edit-tp-titulo').value.trim(),
        descripcion: document.getElementById('edit-tp-descripcion').value.trim(),
        fecha_entrega: document.getElementById('edit-tp-fecha').value
    };
    
    try {
        const response = await fetch(`/trabajos-practicos/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showToast('TP actualizado exitosamente', 'success');
            cerrarModal('modal-editar-tp');
        } else {
            showToast(result.error || 'Error al actualizar TP', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al actualizar TP', 'error');
    }
}

// ELIMINAR CON CONFIRMACI�N
function eliminarAlumno(id, nombre) {
    document.getElementById('mensaje-confirmar-eliminar').textContent = 
        `�Est�s seguro de eliminar al alumno ?`;
    
    accionEliminar = async () => {
        try {
            const response = await fetch(`/alumnos/`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                showToast('Alumno eliminado exitosamente', 'success');
                cerrarModal('modal-confirmar-eliminar');
                loadAlumnos();
            } else {
                showToast(result.error || 'Error al eliminar alumno', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Error al eliminar alumno', 'error');
        }
    };
    
    showModal('modal-confirmar-eliminar');
}

function eliminarCurso(id, nombre) {
    document.getElementById('mensaje-confirmar-eliminar').textContent = 
        `�Est�s seguro de eliminar el curso ?`;
    
    accionEliminar = async () => {
        try {
            const response = await fetch(`/cursos/`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                showToast('Curso eliminado exitosamente', 'success');
                cerrarModal('modal-confirmar-eliminar');
                loadDashboardData();
            } else {
                showToast(result.error || 'Error al eliminar curso', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Error al eliminar curso', 'error');
        }
    };
    
    showModal('modal-confirmar-eliminar');
}

function eliminarTP(id, titulo) {
    document.getElementById('mensaje-confirmar-eliminar').textContent = 
        `�Est�s seguro de eliminar el TP ""?`;
    
    accionEliminar = async () => {
        try {
            const response = await fetch(`/trabajos-practicos/`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                showToast('TP eliminado exitosamente', 'success');
                cerrarModal('modal-confirmar-eliminar');
            } else {
                showToast(result.error || 'Error al eliminar TP', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Error al eliminar TP', 'error');
        }
    };
    
    showModal('modal-confirmar-eliminar');
}

function confirmarEliminacion() {
    if (accionEliminar) {
        accionEliminar();
        accionEliminar = null;
    }
}

// Exportar funciones
window.editarAlumno = editarAlumno;
window.guardarEdicionAlumno = guardarEdicionAlumno;
window.eliminarAlumno = eliminarAlumno;
window.editarCurso = editarCurso;
window.guardarEdicionCurso = guardarEdicionCurso;
window.eliminarCurso = eliminarCurso;
window.editarTP = editarTP;
window.guardarEdicionTP = guardarEdicionTP;
window.eliminarTP = eliminarTP;
window.confirmarEliminacion = confirmarEliminacion;
