/**
 * Sistema de Seguimiento de Alumnos - JavaScript
 * Maneja la interacción del frontend con la API
 */

// Configuración
// En Vercel, la API está en la raíz (sin /api)
const API_URL = '/api';

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
// Modales
// ============================================================================

function openModal(modalId) {
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

// Exportar funciones de modal
window.openModal = openModal;
window.closeModal = closeModal;

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
        case 'admin':
            loadAdminData();
            break;
    }
}

// ============================================================================
// Dashboard
// ============================================================================

async function loadDashboardData() {
    try {
        const url = `${API_URL}/cursos`;
        console.log('Cargando cursos desde:', url);

        const response = await fetch(url);
        const data = await response.json();

        console.log('Cursos recibidos:', data);

        state.clases = data.cursos || [];
        renderClasesCards(state.clases);

        // Cargar últimas clases registradas de todos los cursos
        cargarUltimasClases();

    } catch (error) {
        console.error('Error al cargar cursos:', error);
        showToast('Error al cargar cursos', 'error');
    }
}

function populateCourseSelects(cursos) {
    const materiaSelect = document.getElementById('select-materia');
    const cohorteSelect = document.getElementById('select-cohorte');

    if (!materiaSelect) return;

    // Guardar opción default
    const defaultOption = materiaSelect.firstElementChild;
    materiaSelect.innerHTML = '';
    materiaSelect.appendChild(defaultOption);

    // Poblar con cursos
    cursos.forEach(curso => {
        const option = document.createElement('option');
        option.value = curso.id;
        option.textContent = `${curso.nombre_materia} - ${curso.anio}`;
        materiaSelect.appendChild(option);
    });

    // Deshabilitar selector de cohorte ya que está integrado en la materia
    if (cohorteSelect) {
        cohorteSelect.style.display = 'none';
        // También ocultar el label si es posible, o el padre
        if (cohorteSelect.parentElement) {
            cohorteSelect.parentElement.style.display = 'none';
        }
    }
}

function renderClasesCards(clases) {
    // Llamar a poblar selectores aquí también o desde loadDashboardData
    populateCourseSelects(clases);

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
                <div class="clase-card-materia">${clase.nombre_materia || clase.materia}</div>
                <div class="clase-card-cohorte">Cohorte ${clase.anio || clase.cohorte} - ${clase.cuatrimestre || ''}°C</div>
            </div>
            <div class="clase-card-stats">
                <div class="clase-stat">
                    <span class="clase-stat-icon">👥</span>
                    <span class="clase-stat-label">Alumnos</span>
                    <span class="clase-stat-value">${clase.totalAlumnos || 0}</span>
                </div>
                <div class="clase-stat">
                    <span class="clase-stat-icon">📊</span>
                    <span class="clase-stat-label">Asistencia</span>
                    <span class="clase-stat-value ${(clase.asistenciaPromedio || 0) >= 80 ? 'success' : (clase.asistenciaPromedio || 0) >= 70 ? 'warning' : 'danger'}">${clase.asistenciaPromedio || 0}%</span>
                </div>
                <div class="clase-stat">
                    <span class="clase-stat-icon">🚨</span>
                    <span class="clase-stat-label">En riesgo</span>
                    <span class="clase-stat-value ${(clase.alumnosEnRiesgo || 0) > 0 ? 'danger' : 'success'}">${clase.alumnosEnRiesgo || 0}</span>
                </div>
                <div class="clase-stat">
                    <span class="clase-stat-icon">📚</span>
                    <span class="clase-stat-label">Clases</span>
                    <span class="clase-stat-value">${clase.totalClases || 0}</span>
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
    document.getElementById('clase-detalle-titulo').textContent = `${clase.nombre_materia || clase.materia} - Cohorte ${clase.anio || clase.cohorte}`;
    document.getElementById('clase-detalle-subtitulo').textContent = `Última clase: ${clase.ultimaClase || 'N/A'}`;

    // Actualizar stats
    document.getElementById('clase-total-alumnos').textContent = clase.totalAlumnos || 0;

    // Estos elementos pueden no existir si el HTML fue modificado
    const asistenciaEl = document.getElementById('clase-asistencia-promedio');
    if (asistenciaEl) asistenciaEl.textContent = `${clase.asistenciaPromedio || 0}%`;

    const tpsEl = document.getElementById('clase-tps-promedio');
    if (tpsEl) tpsEl.textContent = `${clase.tpsPromedio || 0}%`;

    document.getElementById('clase-total-clases').textContent = clase.totalClases || 0;

    // Mostrar página
    showPage('clase-detalle');

    // Cargar historial de clases registradas
    cargarHistorialClases(claseId);
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
    const materiaSelect = document.getElementById('select-materia');
    const materiaVal = (clase.nombre_materia || clase.materia || '').toLowerCase().replace(/ /g, '');

    // Intentar seleccionar si existe la opcion, sino dejar vacio
    if (materiaSelect.querySelector(`option[value="${materiaVal}"]`)) {
        materiaSelect.value = materiaVal;
    }

    document.getElementById('select-cohorte').value = (clase.anio || clase.cohorte || '').toString();

    showToast(`Registrando clase de ${clase.nombre_materia || clase.materia}`, 'info');
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
// Historial de Clases
// ============================================================================

// Cargar últimas clases de TODOS los cursos (para el Dashboard)
async function cargarUltimasClases() {
    const container = document.getElementById('ultimas-clases-container');
    if (!container) return;

    container.innerHTML = '<p class="loading">Cargando últimas clases...</p>';

    try {
        // Obtener clases de todos los cursos
        const cursos = state.clases || [];
        let todasLasClases = [];

        // Crear mapa de cursos para obtener nombres
        const cursosMap = {};
        cursos.forEach(c => cursosMap[c.id] = c);

        // Obtener clases de cada curso
        for (const curso of cursos) {
            const response = await fetch(`${API_URL}/clases/curso/${curso.id}`);
            if (response.ok) {
                const clases = await response.json();
                // Agregar info del curso a cada clase
                clases.forEach(clase => {
                    clase.cursoNombre = curso.nombre_materia || curso.materia;
                    clase.cursoAnio = curso.anio;
                });
                todasLasClases = todasLasClases.concat(clases);
            }
        }

        if (todasLasClases.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>🎓 No hay clases registradas todavía</p>
                    <p>Selecciona un curso arriba y haz click en "Registrar" para agregar tu primera clase</p>
                </div>
            `;
            return;
        }

        // Ordenar por fecha descendente y tomar las últimas 10
        todasLasClases.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
        const ultimasClases = todasLasClases.slice(0, 10);

        container.innerHTML = ultimasClases.map(clase => {
            const fecha = new Date(clase.fecha).toLocaleDateString('es-AR', {
                weekday: 'short',
                day: '2-digit',
                month: 'short'
            });

            return `
                <div class="historial-clase-card" onclick="verDetalleClase(${clase.id})">
                    <div class="clase-card-info">
                        <div class="clase-card-numero">${clase.cursoNombre} - Clase ${clase.numero_clase}</div>
                        <div class="clase-card-fecha">${fecha}</div>
                        <div class="clase-card-tema">${clase.tema || 'Sin tema'}</div>
                    </div>
                    <div class="clase-card-actions">
                        <button class="btn-sm" onclick="event.stopPropagation(); verDetalleClase(${clase.id})">
                            👁️ Ver / Editar
                        </button>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error('Error cargando últimas clases:', error);
        container.innerHTML = '<p class="error">Error al cargar clases</p>';
    }
}

async function cargarHistorialClases(cursoId) {
    const container = document.getElementById('historial-clases-container');
    if (!container) return;

    container.innerHTML = '<p class="loading">Cargando historial...</p>';

    try {
        const response = await fetch(`${API_URL}/clases/curso/${cursoId}`);
        const clases = await response.json();

        if (!clases || clases.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>No hay clases registradas aún</p>
                    <button class="btn-primary" onclick="registrarClaseDirecta()">
                        ✍️ Registrar Primera Clase
                    </button>
                </div>
            `;
            return;
        }

        // Ordenar por fecha descendente
        clases.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));

        container.innerHTML = clases.map(clase => {
            const fecha = new Date(clase.fecha).toLocaleDateString('es-AR', {
                weekday: 'long',
                day: '2-digit',
                month: 'long',
                year: 'numeric'
            });

            return `
                <div class="historial-clase-card" onclick="verDetalleClase(${clase.id})">
                    <div class="clase-card-info">
                        <div class="clase-card-numero">Clase ${clase.numero_clase}</div>
                        <div class="clase-card-fecha">${fecha}</div>
                        <div class="clase-card-tema">${clase.tema || 'Sin tema'}</div>
                    </div>
                    <div class="clase-card-actions">
                        <button class="btn-sm" onclick="event.stopPropagation(); verDetalleClase(${clase.id})">
                            👁️ Ver
                        </button>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error('Error cargando historial:', error);
        container.innerHTML = '<p class="error">Error al cargar historial</p>';
    }
}

async function verDetalleClase(claseId) {
    try {
        // Obtener datos de la clase
        const claseRes = await fetch(`${API_URL}/clases/${claseId}`);
        const clase = await claseRes.json();

        // Obtener asistencias de la clase
        const asistenciasRes = await fetch(`${API_URL}/asistencias/clase/${claseId}`);
        const asistencias = await asistenciasRes.json();

        // Guardar en state para edición
        state.claseVisualizando = { clase, asistencias };

        // Llenar el modal
        document.getElementById('ver-clase-id').value = claseId;
        document.getElementById('modal-clase-titulo').textContent = `Clase ${clase.numero_clase}`;

        const fechaFormateada = new Date(clase.fecha).toLocaleDateString('es-AR', {
            weekday: 'long',
            day: '2-digit',
            month: 'long',
            year: 'numeric'
        });
        document.getElementById('ver-clase-fecha').textContent = fechaFormateada;
        document.getElementById('ver-clase-tema').textContent = clase.tema || 'Sin tema especificado';

        // Contar estados
        let presentes = 0, tardes = 0, ausentes = 0;
        asistencias.forEach(a => {
            if (a.estado === 'Presente') presentes++;
            else if (a.estado === 'Tardanza') tardes++;
            else if (a.estado === 'Ausente') ausentes++;
        });

        document.getElementById('ver-presentes').textContent = presentes;
        document.getElementById('ver-tardes').textContent = tardes;
        document.getElementById('ver-ausentes').textContent = ausentes;

        // Obtener nombres de alumnos
        const alumnosRes = await fetch(`${API_URL}/alumnos`);
        const alumnosData = await alumnosRes.json();
        const alumnos = alumnosData.alumnos || [];
        const alumnosMap = {};
        alumnos.forEach(a => alumnosMap[a.id] = a);

        // Mostrar lista de asistencias
        const asistenciasContainer = document.getElementById('ver-clase-asistencias');

        if (asistencias.length === 0) {
            asistenciasContainer.innerHTML = '<p>No hay registros de asistencia</p>';
        } else {
            asistenciasContainer.innerHTML = asistencias.map(a => {
                const alumno = alumnosMap[a.alumno_id] || { nombre_completo: `Alumno #${a.alumno_id}` };
                const estadoClass = a.estado === 'Presente' ? 'presente' :
                    a.estado === 'Tardanza' ? 'tarde' : 'ausente';
                const estadoIcon = a.estado === 'Presente' ? '✅' :
                    a.estado === 'Tardanza' ? '⏰' : '❌';

                return `
                    <div class="asistencia-item ${estadoClass}">
                        <span class="alumno-nombre">${alumno.nombre_completo}</span>
                        <span class="estado-badge ${estadoClass}">${estadoIcon} ${a.estado}</span>
                    </div>
                `;
            }).join('');
        }

        openModal('modal-ver-clase');

    } catch (error) {
        console.error('Error al cargar detalle de clase:', error);
        showToast('Error al cargar detalle de la clase', 'error');
    }
}

// Activar modo edición
function activarModoEdicion() {
    const { asistencias } = state.claseVisualizando;

    // Obtener nombres de alumnos del state
    const alumnosMap = {};
    if (state.alumnos) {
        state.alumnos.forEach(a => alumnosMap[a.id] = a);
    }

    // Guardar asistencias originales para poder cancelar
    state.asistenciasEditando = JSON.parse(JSON.stringify(asistencias));

    // Mostrar modo edición
    document.getElementById('ver-clase-modo-ver').style.display = 'none';
    document.getElementById('ver-clase-modo-editar').style.display = 'block';
    document.getElementById('btns-modo-ver').style.display = 'none';
    document.getElementById('btns-modo-editar').style.display = 'flex';

    // Llenar lista editable
    const container = document.getElementById('editar-clase-asistencias');

    container.innerHTML = asistencias.map(a => {
        const alumno = alumnosMap[a.alumno_id] || { nombre_completo: `Alumno #${a.alumno_id}` };

        return `
            <div class="asistencia-edit-item" data-asistencia-id="${a.id}" data-alumno-id="${a.alumno_id}">
                <span class="alumno-nombre">${alumno.nombre_completo}</span>
                <div class="estado-buttons">
                    <button class="estado-btn presente ${a.estado === 'Presente' ? 'active' : ''}" 
                            onclick="cambiarEstadoAsistencia(${a.id}, 'Presente')">
                        ✅ Presente
                    </button>
                    <button class="estado-btn tarde ${a.estado === 'Tardanza' ? 'active' : ''}" 
                            onclick="cambiarEstadoAsistencia(${a.id}, 'Tardanza')">
                        ⏰ Tarde
                    </button>
                    <button class="estado-btn ausente ${a.estado === 'Ausente' ? 'active' : ''}" 
                            onclick="cambiarEstadoAsistencia(${a.id}, 'Ausente')">
                        ❌ Ausente
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// Cambiar estado de asistencia (solo visual, no guarda aún)
function cambiarEstadoAsistencia(asistenciaId, nuevoEstado) {
    // Actualizar en el array
    const asistencia = state.asistenciasEditando.find(a => a.id === asistenciaId);
    if (asistencia) {
        asistencia.estado = nuevoEstado;
        asistencia.modificado = true;
    }

    // Actualizar UI
    const item = document.querySelector(`[data-asistencia-id="${asistenciaId}"]`);
    if (item) {
        item.querySelectorAll('.estado-btn').forEach(btn => btn.classList.remove('active'));
        const estadoClass = nuevoEstado === 'Presente' ? 'presente' :
            nuevoEstado === 'Tardanza' ? 'tarde' : 'ausente';
        item.querySelector(`.estado-btn.${estadoClass}`).classList.add('active');
    }

    // Actualizar contadores
    actualizarContadoresEdicion();
}

// Actualizar contadores mientras se edita
function actualizarContadoresEdicion() {
    let presentes = 0, tardes = 0, ausentes = 0;
    state.asistenciasEditando.forEach(a => {
        if (a.estado === 'Presente') presentes++;
        else if (a.estado === 'Tardanza') tardes++;
        else if (a.estado === 'Ausente') ausentes++;
    });

    document.getElementById('ver-presentes').textContent = presentes;
    document.getElementById('ver-tardes').textContent = tardes;
    document.getElementById('ver-ausentes').textContent = ausentes;
}

// Cancelar edición
function cancelarEdicionClase() {
    // Restaurar vista original
    document.getElementById('ver-clase-modo-ver').style.display = 'block';
    document.getElementById('ver-clase-modo-editar').style.display = 'none';
    document.getElementById('btns-modo-ver').style.display = 'flex';
    document.getElementById('btns-modo-editar').style.display = 'none';

    // Restaurar contadores originales
    const { asistencias } = state.claseVisualizando;
    let presentes = 0, tardes = 0, ausentes = 0;
    asistencias.forEach(a => {
        if (a.estado === 'Presente') presentes++;
        else if (a.estado === 'Tardanza') tardes++;
        else if (a.estado === 'Ausente') ausentes++;
    });
    document.getElementById('ver-presentes').textContent = presentes;
    document.getElementById('ver-tardes').textContent = tardes;
    document.getElementById('ver-ausentes').textContent = ausentes;

    delete state.asistenciasEditando;
}

// Guardar cambios de edición
async function guardarEdicionClase() {
    const cambios = state.asistenciasEditando.filter(a => a.modificado);

    if (cambios.length === 0) {
        showToast('No hay cambios para guardar', 'info');
        cancelarEdicionClase();
        return;
    }

    showToast('Guardando cambios...', 'info');

    try {
        let guardados = 0;

        for (const asistencia of cambios) {
            const response = await fetch(`${API_URL}/asistencias/${asistencia.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ estado: asistencia.estado })
            });

            if (response.ok) {
                guardados++;
            } else {
                console.error(`Error al actualizar asistencia ${asistencia.id}`);
            }
        }

        showToast(`${guardados} asistencia(s) actualizada(s)`, 'success');

        // Cerrar modal y recargar
        closeModal('modal-ver-clase');

        // Recargar historial si existe
        if (state.claseSeleccionada) {
            cargarHistorialClases(state.claseSeleccionada.id);
        }

    } catch (error) {
        console.error('Error al guardar cambios:', error);
        showToast('Error al guardar los cambios', 'error');
    }
}

// ============================================================================
// Registro de Clase
// ============================================================================

async function iniciarRegistroClase() {
    const cursoId = document.getElementById('select-materia').value;
    const fecha = document.getElementById('fecha-clase').value;

    if (!cursoId || !fecha) {
        showToast('Por favor completa todos los campos', 'error');
        return;
    }

    // Buscar curso seleccionado
    const curso = state.clases.find(c => c.id == cursoId);
    if (!curso) {
        showToast('Curso no encontrado', 'error');
        return;
    }

    // Guardar datos de la clase
    state.claseActual = {
        cursoId: cursoId,
        materia: curso.nombre_materia,
        cohorte: curso.anio,
        fecha: fecha,
        registros: {},
        entregasTPs: {}  // Nuevo: para guardar entregas de TPs
    };

    // Ocultar selección, mostrar registro
    document.getElementById('seleccion-clase').style.display = 'none';
    document.getElementById('registro-asistencia').style.display = 'block';

    // Actualizar título
    document.getElementById('clase-titulo').textContent = `${curso.nombre_materia} - Cohorte ${curso.anio}`;

    // Formatear fecha
    const fechaObj = new Date(fecha + 'T00:00:00');
    const fechaFormateada = fechaObj.toLocaleDateString('es-AR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });
    document.getElementById('clase-fecha').textContent = fechaFormateada;

    // Cargar alumnos filtrados por cohorte del curso
    await cargarAlumnosParaRegistro(curso.anio);

    // Cargar TPs de la materia
    await cargarTPsParaRegistro(cursoId);
}

async function cargarAlumnosParaRegistro(cohorte) {
    try {
        let url = `${API_URL}/alumnos`;
        if (cohorte) {
            url += `?cohorte=${cohorte}`;
        }
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
    card.setAttribute('data-alumno-id', alumno.id);
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

// Cargar TPs de la materia para registro de entregas
async function cargarTPsParaRegistro(cursoId) {
    const container = document.getElementById('lista-tps-clase');
    const seccion = document.getElementById('seccion-tps');

    if (!container || !seccion) return;

    try {
        const response = await fetch(`${API_URL}/tps/curso/${cursoId}`);
        const data = await response.json();
        const tps = Array.isArray(data) ? data : (data.tps || []);

        if (tps.length === 0) {
            seccion.style.display = 'none';
            return;
        }

        // Guardar TPs en el state
        state.claseActual.tps = tps;

        // Mostrar sección de TPs
        seccion.style.display = 'block';

        // Obtener alumnos registrados
        const alumnosIds = Object.keys(state.claseActual.registros);

        container.innerHTML = tps.map(tp => `
            <div class="tp-registro-card" data-tp-id="${tp.id}">
                <div class="tp-registro-header">
                    <div class="tp-info">
                        <h4>${tp.titulo}</h4>
                        <span class="tp-fecha">Entrega: ${tp.fecha_entrega || 'Sin fecha'}</span>
                    </div>
                </div>
                <div class="tp-alumnos-entregas" id="entregas-tp-${tp.id}">
                    ${alumnosIds.map(alumnoId => {
            const registro = state.claseActual.registros[alumnoId];
            // Buscar nombre del alumno
            const alumnoCard = document.querySelector(`[data-alumno-id="${alumnoId}"]`);
            const nombreAlumno = alumnoCard ? alumnoCard.querySelector('.alumno-registro-nombre').textContent : `Alumno ${alumnoId}`;
            return `
                            <div class="entrega-row" data-alumno-id="${alumnoId}">
                                <span class="alumno-nombre">${nombreAlumno}</span>
                                <div class="entrega-buttons">
                                    <button class="entrega-btn" onclick="marcarEntregaTP(${tp.id}, ${alumnoId}, 'a_tiempo')">⏰ A tiempo</button>
                                    <button class="entrega-btn" onclick="marcarEntregaTP(${tp.id}, ${alumnoId}, 'tarde')">⚠️ Tarde</button>
                                    <button class="entrega-btn" onclick="marcarEntregaTP(${tp.id}, ${alumnoId}, 'muy_tarde')">🕙 Muy tarde</button>
                                    <button class="entrega-btn entrega-no" onclick="marcarEntregaTP(${tp.id}, ${alumnoId}, 'no_entrego')">✗ No entregó</button>
                                </div>
                            </div>
                        `;
        }).join('')}
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error al cargar TPs:', error);
        seccion.style.display = 'none';
    }
}

// Marcar entrega de TP por alumno
function marcarEntregaTP(tpId, alumnoId, estado) {
    // Inicializar objeto de entregas si no existe
    if (!state.claseActual.entregasTPs[tpId]) {
        state.claseActual.entregasTPs[tpId] = {};
    }

    // Guardar estado de entrega
    state.claseActual.entregasTPs[tpId][alumnoId] = estado;

    // Actualizar UI
    const row = document.querySelector(`#entregas-tp-${tpId} [data-alumno-id="${alumnoId}"]`);
    if (row) {
        row.querySelectorAll('.entrega-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
    }

    const estadoTexto = {
        'a_tiempo': 'a tiempo',
        'tarde': 'tarde',
        'muy_tarde': 'muy tarde',
        'no_entrego': 'no entregado'
    };

    showToast(`TP marcado como ${estadoTexto[estado]}`, 'info');
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
        showToast('Guardando clase...', 'info');

        // 1. Obtener número de clase (contando las existentes)
        const cursoId = state.claseActual.cursoId;
        const clasesResponse = await fetch(`${API_URL}/clases/curso/${cursoId}`);
        const clasesAnteriores = await clasesResponse.json();
        const numeroClase = (clasesAnteriores.length || 0) + 1;

        // 2. Crear la Clase
        const claseData = {
            curso_id: parseInt(cursoId),
            fecha: state.claseActual.fecha,
            numero_clase: numeroClase,
            tema: `Clase ${numeroClase}`
        };

        const createClaseResponse = await fetch(`${API_URL}/clases`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(claseData)
        });

        if (!createClaseResponse.ok) {
            const err = await createClaseResponse.json();
            throw new Error(err.detail || 'Error al crear la clase');
        }

        const nuevaClase = await createClaseResponse.json();
        console.log('Clase creada:', nuevaClase);
        const claseId = nuevaClase.id;

        // 3. Registrar Asistencias
        // Mapeo de estados frontend -> backend
        const mapEstado = {
            'presente': 'Presente',
            'ausente': 'Ausente',
            'tarde': 'Tardanza'
        };

        const registros = Object.entries(state.claseActual.registros);
        let asistenciasGuardadas = 0;

        for (const [alumnoIdStr, registro] of registros) {
            if (!registro.asistencia) continue;

            const alumnoId = parseInt(alumnoIdStr);
            const estado = mapEstado[registro.asistencia];

            const asistenciaData = {
                alumno_id: alumnoId,
                clase_id: claseId,
                estado: estado
            };

            const asistenciaRes = await fetch(`${API_URL}/asistencias`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(asistenciaData)
            });

            if (asistenciaRes.ok) {
                asistenciasGuardadas++;

                // 4. Registrar Participación (si existe y es válida)
                if (registro.participacion) {
                    const mapNivel = {
                        'alta': 'Alta',
                        'media': 'Media',
                        'baja': 'Baja',
                        'nula': 'Nula'
                    };
                    const participacionData = {
                        alumno_id: alumnoId,
                        clase_id: claseId,
                        nivel: mapNivel[registro.participacion],
                        comentario: registro.observaciones || null
                    };
                    await fetch(`${API_URL}/participaciones`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(participacionData)
                    });
                }
            } else {
                console.error(`Error al guardar asistencia para alumno ${alumnoId}`);
            }
        }

        showToast(`Clase guardada exitosamente (${asistenciasGuardadas} asistencias)`, 'success');

        // Resetear formulario
        cancelarRegistro();
        // Recargar dashboard para ver la nueva clase (aumentará contador)
        loadDashboardData();
        showPage('dashboard');

    } catch (error) {
        console.error('Error al guardar clase:', error);
        showToast(`Error al guardar la clase: ${error.message}`, 'error');
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
// Admin functions
window.showAdminTab = showAdminTab;
window.abrirModalCurso = abrirModalCurso;
window.editarCurso = editarCurso;
window.eliminarCurso = eliminarCurso;
window.guardarCurso = guardarCurso;
window.abrirModalTP = abrirModalTP;
window.editarTP = editarTP;
window.eliminarTP = eliminarTP;
window.guardarTP = guardarTP;
window.crearAlumno = crearAlumno;
window.editarAlumno = editarAlumno;
window.eliminarAlumno = eliminarAlumno;
// Inscripciones
window.gestionarInscripciones = gestionarInscripciones;
window.agregarInscripcion = agregarInscripcion;
window.eliminarInscripcion = eliminarInscripcion;
// Seed functions
window.cargarDatosPrueba = cargarDatosPrueba;
window.borrarDatosPrueba = borrarDatosPrueba;
window.borrarTodo = borrarTodo;

// ============================================================================
// ADMIN PANEL
// ============================================================================

function showAdminTab(tabName) {
    // Ocultar todos los tabs
    document.querySelectorAll('.admin-tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.admin-tab').forEach(btn => {
        btn.classList.remove('active');
    });

    // Mostrar tab seleccionado
    const targetTab = document.getElementById(`admin-tab-${tabName}`);
    if (targetTab) {
        targetTab.classList.add('active');
    }

    // Activar botón
    event.target.classList.add('active');

    // Cargar datos del tab
    if (tabName === 'cursos') loadAdminCursos();
    if (tabName === 'alumnos-admin') loadAdminAlumnos();
    if (tabName === 'tps') loadAdminTPs();
}

async function loadAdminData() {
    loadAdminCursos();
}

// --- CURSOS ---
async function loadAdminCursos() {
    const container = document.getElementById('admin-cursos-list');
    if (!container) return;

    container.innerHTML = '<p class="loading">Cargando cursos...</p>';

    try {
        const response = await fetch(`${API_URL}/cursos`);
        const data = await response.json();
        const cursos = data.cursos || [];

        if (cursos.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📚</div>
                    <p>No hay cursos registrados</p>
                </div>
            `;
            return;
        }

        container.innerHTML = cursos.map(curso => `
            <div class="admin-card">
                <div class="admin-card-info">
                    <div class="admin-card-title">${curso.nombre_materia}</div>
                    <div class="admin-card-subtitle">
                        ${curso.anio} - ${curso.cuatrimestre}° Cuatrimestre | ${curso.docente_responsable || 'Sin docente'}
                    </div>
                </div>
                <div class="admin-card-actions">
                    <button class="btn-edit" onclick="editarCurso(${curso.id})">✏️ Editar</button>
                    <button class="btn-delete" onclick="eliminarCurso(${curso.id})">🗑️ Eliminar</button>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error cargando cursos:', error);
        container.innerHTML = '<p class="loading">Error al cargar cursos</p>';
    }
}

function abrirModalCurso(curso = null) {
    document.getElementById('modal-curso-titulo').textContent = curso ? 'Editar Curso' : 'Nuevo Curso';
    document.getElementById('curso-id').value = curso?.id || '';
    document.getElementById('curso-nombre').value = curso?.nombre_materia || '';
    document.getElementById('curso-anio').value = curso?.anio || new Date().getFullYear();
    document.getElementById('curso-cuatrimestre').value = curso?.cuatrimestre || 1;
    document.getElementById('curso-docente').value = curso?.docente_responsable || '';
    openModal('modal-curso');
}

async function editarCurso(id) {
    try {
        const response = await fetch(`${API_URL}/cursos/${id}`);
        const curso = await response.json();
        abrirModalCurso(curso);
    } catch (error) {
        showToast('Error al cargar curso', 'error');
    }
}

async function guardarCurso() {
    const id = document.getElementById('curso-id').value;
    const data = {
        nombre_materia: document.getElementById('curso-nombre').value,
        anio: parseInt(document.getElementById('curso-anio').value),
        cuatrimestre: parseInt(document.getElementById('curso-cuatrimestre').value),
        docente_responsable: document.getElementById('curso-docente').value
    };

    try {
        const url = id ? `${API_URL}/cursos/${id}` : `${API_URL}/cursos`;
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showToast(id ? 'Curso actualizado' : 'Curso creado', 'success');
            closeModal('modal-curso');
            loadAdminCursos();
            loadDashboardData();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Error al guardar', 'error');
        }
    } catch (error) {
        showToast('Error al guardar curso', 'error');
    }
}

async function eliminarCurso(id) {
    if (!confirm('¿Estás seguro de eliminar este curso? Esto eliminará también las clases y registros asociados.')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/cursos/${id}`, { method: 'DELETE' });
        if (response.ok) {
            showToast('Curso eliminado', 'success');
            loadAdminCursos();
            loadDashboardData();
        } else {
            showToast('Error al eliminar', 'error');
        }
    } catch (error) {
        showToast('Error al eliminar curso', 'error');
    }
}

// --- ALUMNOS (Admin) ---
async function loadAdminAlumnos() {
    const container = document.getElementById('admin-alumnos-list');
    if (!container) return;

    container.innerHTML = '<p class="loading">Cargando alumnos...</p>';

    try {
        const response = await fetch(`${API_URL}/alumnos`);
        const data = await response.json();
        const alumnos = data.alumnos || [];

        if (alumnos.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">👥</div>
                    <p>No hay alumnos registrados</p>
                </div>
            `;
            return;
        }

        container.innerHTML = alumnos.map(alumno => `
            <div class="admin-card">
                <div class="admin-card-info">
                    <div class="admin-card-title">${alumno.apellido}, ${alumno.nombre}</div>
                    <div class="admin-card-subtitle">
                        DNI: ${alumno.dni} | Email: ${alumno.email || '-'} | Cohorte: ${alumno.cohorte || '-'}
                    </div>
                </div>
                <div class="admin-card-actions">
                    <button class="btn-edit" onclick="gestionarInscripciones(${alumno.id}, '${alumno.apellido}, ${alumno.nombre}')">📚 Materias</button>
                    <button class="btn-edit" onclick="editarAlumno(${alumno.id})">✏️ Editar</button>
                    <button class="btn-delete" onclick="eliminarAlumno(${alumno.id})">🗑️ Eliminar</button>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error cargando alumnos:', error);
        container.innerHTML = '<p class="loading">Error al cargar alumnos</p>';
    }
}

async function eliminarAlumno(id) {
    if (!confirm('¿Estás seguro de eliminar este alumno? Esto eliminará también sus registros de asistencia y participación.')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/alumnos/${id}`, { method: 'DELETE' });
        if (response.ok) {
            showToast('Alumno eliminado', 'success');
            loadAdminAlumnos();
            loadAlumnos();
        } else {
            showToast('Error al eliminar', 'error');
        }
    } catch (error) {
        showToast('Error al eliminar alumno', 'error');
    }
}

async function editarAlumno(id) {
    try {
        const response = await fetch(`${API_URL}/alumnos/${id}`);
        const alumno = await response.json();

        // Llenar el modal con los datos del alumno (IDs correctos del HTML)
        document.getElementById('nombre').value = alumno.nombre || '';
        document.getElementById('apellido').value = alumno.apellido || '';
        document.getElementById('dni').value = alumno.dni || '';
        document.getElementById('email').value = alumno.email || '';
        document.getElementById('cohorte').value = alumno.cohorte || '';

        // Guardar el ID para la actualización
        window.currentEditAlumnoId = id;

        // Cambiar título y abrir modal
        const modalTitle = document.querySelector('#modal-nuevo-alumno .modal-header h2');
        if (modalTitle) modalTitle.textContent = 'Editar Alumno';

        // Cambiar texto del botón
        const btn = document.querySelector('#modal-nuevo-alumno .modal-footer .btn-primary');
        if (btn) btn.textContent = 'Guardar Cambios';

        openModal('modal-nuevo-alumno');
    } catch (error) {
        showToast('Error al cargar alumno', 'error');
    }
}

async function crearAlumno() {
    const data = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        dni: document.getElementById('dni').value,
        email: document.getElementById('email').value,
        cohorte: parseInt(document.getElementById('cohorte').value)
    };

    if (!data.nombre || !data.apellido || !data.dni) {
        showToast('Completa los campos obligatorios', 'error');
        return;
    }

    try {
        let url = `${API_URL}/alumnos`;
        let method = 'POST';

        // Si hay un ID de edición, hacer PUT
        if (window.currentEditAlumnoId) {
            url = `${API_URL}/alumnos/${window.currentEditAlumnoId}`;
            method = 'PUT';
        }

        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showToast(window.currentEditAlumnoId ? 'Alumno actualizado' : 'Alumno creado', 'success');
            closeModal('modal-nuevo-alumno');

            // Limpiar formulario y estado
            document.getElementById('form-nuevo-alumno').reset();
            window.currentEditAlumnoId = null;

            // Restaurar título y botón
            const modalTitle = document.querySelector('#modal-nuevo-alumno .modal-header h2');
            if (modalTitle) modalTitle.textContent = 'Nuevo Alumno';
            const btn = document.querySelector('#modal-nuevo-alumno .modal-footer .btn-primary');
            if (btn) btn.textContent = 'Crear Alumno';

            loadAdminAlumnos();
        } else {
            const errorData = await response.json();
            let errorMsg = 'Error al guardar';
            if (errorData.detail) {
                errorMsg = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
            }
            showToast(errorMsg, 'error');
        }
    } catch (error) {
        showToast('Error al guardar alumno', 'error');
        console.error(error);
    }
}

// --- TPs ---
async function loadAdminTPs() {
    const container = document.getElementById('admin-tps-list');
    if (!container) return;

    container.innerHTML = '<p class="loading">Cargando TPs...</p>';

    try {
        // Cargar cursos para tener los nombres
        const cursosRes = await fetch(`${API_URL}/cursos`);
        const cursosData = await cursosRes.json();
        const cursos = cursosData.cursos || [];
        const cursosMap = {};
        cursos.forEach(c => cursosMap[c.id] = c);

        // Actualizar select de cursos en modal
        const tpCursoSelect = document.getElementById('tp-curso');
        if (tpCursoSelect) {
            tpCursoSelect.innerHTML = '<option value="">Seleccionar curso...</option>' +
                cursos.map(c => `<option value="${c.id}">${c.nombre_materia} (${c.anio})</option>`).join('');
        }

        // Cargar todos los TPs con un solo request
        const tpsRes = await fetch(`${API_URL}/tps`);
        const tpsData = await tpsRes.json();
        // La API puede devolver un array directamente o un objeto
        const allTPs = Array.isArray(tpsData) ? tpsData : (tpsData.tps || []);

        if (allTPs.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📝</div>
                    <p>No hay trabajos prácticos registrados</p>
                </div>
            `;
            return;
        }

        container.innerHTML = allTPs.map(tp => {
            const curso = cursosMap[tp.curso_id] || {};
            return `
                <div class="admin-card">
                    <div class="admin-card-info">
                        <div class="admin-card-title">${tp.titulo}</div>
                        <div class="admin-card-subtitle">
                            ${curso.nombre_materia || 'Curso #' + tp.curso_id} | Entrega: ${tp.fecha_entrega || 'Sin fecha'}
                        </div>
                    </div>
                    <div class="admin-card-actions">
                        <button class="btn-edit" onclick="editarTP(${tp.id})">✏️ Editar</button>
                        <button class="btn-delete" onclick="eliminarTP(${tp.id})">🗑️ Eliminar</button>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error('Error cargando TPs:', error);
        container.innerHTML = '<p class="loading">Error al cargar TPs</p>';
    }
}

async function abrirModalTP(tp = null) {
    // Primero cargar cursos en el select
    try {
        const cursosRes = await fetch(`${API_URL}/cursos`);
        const cursosData = await cursosRes.json();
        const cursos = cursosData.cursos || [];

        const select = document.getElementById('tp-curso');
        if (select) {
            select.innerHTML = '<option value="">Seleccionar curso...</option>' +
                cursos.map(c => `<option value="${c.id}">${c.nombre_materia} (${c.anio})</option>`).join('');
        }
    } catch (e) {
        console.error('Error cargando cursos para TP:', e);
    }

    document.getElementById('modal-tp-titulo').textContent = tp ? 'Editar TP' : 'Nuevo TP';
    document.getElementById('tp-id').value = tp?.id || '';
    document.getElementById('tp-curso').value = tp?.curso_id || '';
    document.getElementById('tp-titulo').value = tp?.titulo || '';
    document.getElementById('tp-descripcion').value = tp?.descripcion || '';
    document.getElementById('tp-fecha').value = tp?.fecha_entrega || '';
    openModal('modal-tp');
}

async function editarTP(id) {
    try {
        const response = await fetch(`${API_URL}/tps/${id}`);
        const tp = await response.json();
        abrirModalTP(tp);
    } catch (error) {
        showToast('Error al cargar TP', 'error');
    }
}

async function guardarTP() {
    const id = document.getElementById('tp-id').value;
    const data = {
        curso_id: parseInt(document.getElementById('tp-curso').value),
        titulo: document.getElementById('tp-titulo').value,
        descripcion: document.getElementById('tp-descripcion').value,
        fecha_entrega: document.getElementById('tp-fecha').value
    };

    if (!data.curso_id || !data.titulo) {
        showToast('Completa los campos obligatorios', 'error');
        return;
    }

    try {
        const url = id ? `${API_URL}/tps/${id}` : `${API_URL}/tps`;
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showToast(id ? 'TP actualizado' : 'TP creado', 'success');
            closeModal('modal-tp');
            loadAdminTPs();
        } else {
            const errorData = await response.json();
            let errorMsg = 'Error al guardar TP';
            if (errorData.detail) {
                errorMsg = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
            }
            showToast(errorMsg, 'error');
        }
    } catch (error) {
        console.error('Error guardarTP:', error);
        showToast('Error al guardar TP', 'error');
    }
}

async function eliminarTP(id) {
    if (!confirm('¿Estás seguro de eliminar este TP?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tps/${id}`, { method: 'DELETE' });
        if (response.ok) {
            showToast('TP eliminado', 'success');
            loadAdminTPs();
        } else {
            showToast('Error al eliminar', 'error');
        }
    } catch (error) {
        showToast('Error al eliminar TP', 'error');
    }
}

// ============================================================================
// SEED DATA FUNCTIONS
// ============================================================================

async function cargarDatosPrueba() {
    if (!confirm('¿Cargar datos de prueba? Esto creará cursos, alumnos y TPs de ejemplo.')) {
        return;
    }

    showToast('Cargando datos de prueba...', 'info');

    try {
        const response = await fetch(`${API_URL}/seed`);
        const data = await response.json();

        if (data.status === 'success') {
            showToast(`✅ Datos cargados: ${data.results.cursos} cursos, ${data.results.alumnos} alumnos, ${data.results.tps} TPs`, 'success');
            // Recargar datos
            loadAdminCursos();
            loadAdminAlumnos();
            loadAdminTPs();
            loadDashboardData();
        } else {
            showToast('Error: ' + data.message, 'error');
        }
    } catch (error) {
        showToast('Error al cargar datos de prueba', 'error');
        console.error(error);
    }
}

async function borrarDatosPrueba() {
    if (!confirm('¿Borrar TODOS los datos de prueba? Esta acción no se puede deshacer.')) {
        return;
    }

    showToast('Borrando datos de prueba...', 'info');

    try {
        const response = await fetch(`${API_URL}/seed`, { method: 'DELETE' });
        const data = await response.json();

        if (data.status === 'success') {
            showToast(`✅ Datos eliminados: ${data.results.cursos} cursos, ${data.results.alumnos} alumnos`, 'success');
            // Recargar datos
            loadAdminCursos();
            loadAdminAlumnos();
            loadAdminTPs();
            loadDashboardData();
        } else {
            showToast('Error: ' + data.message, 'error');
        }
    } catch (error) {
        showToast('Error al borrar datos de prueba', 'error');
        console.error(error);
    }
}

async function borrarTodo() {
    if (!confirm('⚠️ ¿Estás SEGURO de BORRAR TODOS los datos?\n\nEsto incluye:\n- Todos los cursos\n- Todos los alumnos\n- Todos los TPs\n- Todas las asistencias\n\n¡Esta acción NO se puede deshacer!')) {
        return;
    }

    if (!confirm('⚠️ ÚLTIMA CONFIRMACIÓN\n\n¿Realmente quieres borrar TODO?')) {
        return;
    }

    showToast('Borrando todos los datos...', 'info');

    try {
        const response = await fetch(`${API_URL}/clear-all`, { method: 'DELETE' });
        const data = await response.json();

        if (data.status === 'success') {
            showToast('✅ Todos los datos han sido eliminados', 'success');
            // Recargar datos
            loadAdminCursos();
            loadAdminAlumnos();
            loadAdminTPs();
            loadDashboardData();
        } else {
            showToast('Error: ' + data.message, 'error');
        }
    } catch (error) {
        showToast('Error al borrar datos', 'error');
        console.error(error);
    }
}

// ============================================================================
// INSCRIPCIONES (Materias del alumno)
// ============================================================================

async function gestionarInscripciones(alumnoId, alumnoNombre) {
    document.getElementById('inscripcion-alumno-id').value = alumnoId;
    document.getElementById('modal-inscripciones-titulo').textContent = `Materias de ${alumnoNombre}`;

    // Cargar cursos disponibles
    try {
        const cursosRes = await fetch(`${API_URL}/cursos`);
        const cursosData = await cursosRes.json();
        const cursos = cursosData.cursos || [];

        const select = document.getElementById('inscripcion-curso');
        select.innerHTML = '<option value="">Seleccionar curso...</option>' +
            cursos.map(c => `<option value="${c.id}">${c.nombre_materia} (${c.anio})</option>`).join('');
    } catch (e) {
        console.error('Error cargando cursos:', e);
    }

    // Cargar inscripciones actuales
    await cargarInscripcionesAlumno(alumnoId);

    openModal('modal-inscripciones');
}

async function cargarInscripcionesAlumno(alumnoId) {
    const container = document.getElementById('inscripciones-list');
    container.innerHTML = '<p class="loading">Cargando inscripciones...</p>';

    try {
        const response = await fetch(`${API_URL}/inscripciones/alumno/${alumnoId}`);
        const data = await response.json();
        // La API devuelve un array directamente
        const inscripciones = Array.isArray(data) ? data : (data.inscripciones || []);

        if (inscripciones.length === 0) {
            container.innerHTML = `
                <div class="empty-state" style="padding: 1rem;">
                    <p>No está inscrito en ninguna materia</p>
                </div>
            `;
            return;
        }

        // Obtener nombres de cursos
        const cursosRes = await fetch(`${API_URL}/cursos`);
        const cursosData = await cursosRes.json();
        const cursos = cursosData.cursos || [];
        const cursosMap = {};
        cursos.forEach(c => cursosMap[c.id] = c);

        container.innerHTML = inscripciones.map(insc => {
            const curso = cursosMap[insc.curso_id] || {};
            return `
                <div class="admin-card" style="padding: 0.75rem;">
                    <div class="admin-card-info">
                        <div class="admin-card-title">${curso.nombre_materia || 'Curso #' + insc.curso_id}</div>
                        <div class="admin-card-subtitle">${curso.anio || ''} - ${curso.cuatrimestre ? curso.cuatrimestre + '° cuatrimestre' : ''}</div>
                    </div>
                    <div class="admin-card-actions">
                        <button class="btn-delete" onclick="eliminarInscripcion(${insc.id})">🗑️</button>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error('Error cargando inscripciones:', error);
        container.innerHTML = '<p class="loading">Error al cargar inscripciones</p>';
    }
}

async function agregarInscripcion() {
    const alumnoId = document.getElementById('inscripcion-alumno-id').value;
    const cursoId = document.getElementById('inscripcion-curso').value;

    if (!cursoId) {
        showToast('Selecciona un curso', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/inscripciones`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                alumno_id: parseInt(alumnoId),
                curso_id: parseInt(cursoId)
            })
        });

        if (response.ok) {
            showToast('Inscripción agregada', 'success');
            document.getElementById('inscripcion-curso').value = '';
            await cargarInscripcionesAlumno(alumnoId);
        } else {
            const errorData = await response.json();
            let errorMsg = 'Error al inscribir';
            if (errorData.detail) {
                errorMsg = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
            }
            showToast(errorMsg, 'error');
        }
    } catch (error) {
        showToast('Error al agregar inscripción', 'error');
        console.error(error);
    }
}

async function eliminarInscripcion(inscripcionId) {
    if (!confirm('¿Eliminar esta inscripción?')) return;

    const alumnoId = document.getElementById('inscripcion-alumno-id').value;

    try {
        const response = await fetch(`${API_URL}/inscripciones/${inscripcionId}`, { method: 'DELETE' });

        if (response.ok) {
            showToast('Inscripción eliminada', 'success');
            await cargarInscripcionesAlumno(alumnoId);
        } else {
            showToast('Error al eliminar', 'error');
        }
    } catch (error) {
        showToast('Error al eliminar inscripción', 'error');
        console.error(error);
    }
}
