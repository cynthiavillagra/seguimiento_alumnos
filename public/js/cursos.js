/**
 * Módulo de Gestión de Cursos
 */

import { fetchCursos, createCurso, updateCurso, deleteCurso } from './api.js';
import { showToast, showModal, closeModal, showConfirmDialog } from './utils.js';

let cursos = [];

// ========================================
// CARGAR Y RENDERIZAR
// ========================================

export async function loadCursosPage() {
    try {
        const data = await fetchCursos();
        cursos = data.clases || [];
        renderCursosTable(cursos);
    } catch (error) {
        console.error('Error al cargar cursos:', error);
        showToast('Error al cargar cursos', 'error');
    }
}

function renderCursosTable(cursosData) {
    const tbody = document.getElementById('tabla-cursos-body');
    const noData = document.getElementById('no-cursos');

    if (!tbody) return;

    if (!cursosData || cursosData.length === 0) {
        tbody.innerHTML = '';
        if (noData) noData.style.display = 'flex';
        return;
    }

    if (noData) noData.style.display = 'none';

    tbody.innerHTML = cursosData.map(curso => `
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
                    <button class="btn-sm btn-edit" onclick="window.editarCurso(${curso.id})" title="Editar">
                        ✏️
                    </button>
                    <button class="btn-sm btn-delete" onclick="window.eliminarCurso(${curso.id}, '${curso.materia}')" title="Eliminar">
                        🗑️
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// ========================================
// FILTRAR
// ========================================

export function filtrarCursos() {
    const busqueda = document.getElementById('buscar-curso')?.value.toLowerCase() || '';
    const anio = document.getElementById('filtro-anio')?.value || '';
    const cuatrimestre = document.getElementById('filtro-cuatrimestre')?.value || '';

    let cursosFiltrados = cursos;

    if (busqueda) {
        cursosFiltrados = cursosFiltrados.filter(c =>
            c.materia.toLowerCase().includes(busqueda) ||
            c.docente.toLowerCase().includes(busqueda)
        );
    }

    if (anio) {
        cursosFiltrados = cursosFiltrados.filter(c => c.cohorte == anio);
    }

    if (cuatrimestre) {
        cursosFiltrados = cursosFiltrados.filter(c => c.cuatrimestre == cuatrimestre);
    }

    renderCursosTable(cursosFiltrados);
}

// ========================================
// CREAR
// ========================================

export function mostrarModalCrearCurso() {
    showModal('modal-crear-curso');
}

export async function crearCurso() {
    const materia = document.getElementById('curso-materia')?.value.trim();
    const anio = parseInt(document.getElementById('curso-anio')?.value);
    const cuatrimestre = parseInt(document.getElementById('curso-cuatrimestre')?.value);
    const docente = document.getElementById('curso-docente')?.value.trim();

    if (!materia || !anio || !cuatrimestre || !docente) {
        showToast('Por favor completa todos los campos', 'error');
        return;
    }

    try {
        const data = await createCurso({
            nombre_materia: materia,
            anio: anio,
            cuatrimestre: cuatrimestre,
            docente_responsable: docente
        });

        if (data.success) {
            showToast('Curso creado exitosamente', 'success');
            closeModal('modal-crear-curso');
            document.getElementById('form-crear-curso')?.reset();
            loadCursosPage();
        } else {
            showToast(data.error || 'Error al crear curso', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al crear curso', 'error');
    }
}

// ========================================
// EDITAR
// ========================================

export async function editarCurso(id) {
    try {
        const curso = cursos.find(c => c.id === id);

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

export async function guardarEdicionCurso() {
    const id = document.getElementById('edit-curso-id')?.value;
    const data = {
        nombre_materia: document.getElementById('edit-curso-materia')?.value.trim(),
        anio: parseInt(document.getElementById('edit-curso-anio')?.value),
        cuatrimestre: parseInt(document.getElementById('edit-curso-cuatrimestre')?.value),
        docente_responsable: document.getElementById('edit-curso-docente')?.value.trim()
    };

    try {
        const result = await updateCurso(id, data);

        if (result.success) {
            showToast('Curso actualizado exitosamente', 'success');
            closeModal('modal-editar-curso');
            loadCursosPage();
        } else {
            showToast(result.error || 'Error al actualizar curso', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al actualizar curso', 'error');
    }
}

// ========================================
// ELIMINAR
// ========================================

export function eliminarCurso(id, nombre) {
    showConfirmDialog(
        `¿Estás seguro de eliminar el curso "${nombre}"?`,
        async () => {
            try {
                const result = await deleteCurso(id);

                if (result.success) {
                    showToast('Curso eliminado exitosamente', 'success');
                    loadCursosPage();
                } else {
                    showToast(result.error || 'Error al eliminar curso', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('Error al eliminar curso', 'error');
            }
        }
    );
}

// Exportar para uso global
window.loadCursosPage = loadCursosPage;
window.filtrarCursos = filtrarCursos;
window.mostrarModalCrearCurso = mostrarModalCrearCurso;
window.crearCurso = crearCurso;
window.editarCurso = editarCurso;
window.guardarEdicionCurso = guardarEdicionCurso;
window.eliminarCurso = eliminarCurso;
