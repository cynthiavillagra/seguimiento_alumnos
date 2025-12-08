/**
 * Módulo API - Maneja todas las llamadas a la API REST
 */

const API_URL = window.location.hostname.includes('vercel.app') ? '' : '/api';

// ========================================
// CURSOS
// ========================================

export async function fetchCursos() {
    const response = await fetch(`${API_URL}/cursos`);
    if (!response.ok) throw new Error('Error al cargar cursos');
    return response.json();
}

export async function createCurso(data) {
    const response = await fetch(`${API_URL}/cursos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Error al crear curso');
    return response.json();
}

export async function updateCurso(id, data) {
    const response = await fetch(`${API_URL}/cursos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Error al actualizar curso');
    return response.json();
}

export async function deleteCurso(id) {
    const response = await fetch(`${API_URL}/cursos/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) throw new Error('Error al eliminar curso');
    return response.json();
}

// ========================================
// ALUMNOS
// ========================================

export async function fetchAlumnos() {
    const response = await fetch(`${API_URL}/alumnos`);
    if (!response.ok) throw new Error('Error al cargar alumnos');
    return response.json();
}

export async function createAlumno(data) {
    const response = await fetch(`${API_URL}/alumnos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Error al crear alumno');
    return response.json();
}

export async function updateAlumno(id, data) {
    const response = await fetch(`${API_URL}/alumnos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Error al actualizar alumno');
    return response.json();
}

export async function deleteAlumno(id) {
    const response = await fetch(`${API_URL}/alumnos/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) throw new Error('Error al eliminar alumno');
    return response.json();
}

// ========================================
// TRABAJOS PRÁCTICOS
// ========================================

export async function fetchTPs(cursoId = null) {
    const url = cursoId
        ? `${API_URL}/trabajos-practicos?curso_id=${cursoId}`
        : `${API_URL}/trabajos-practicos`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Error al cargar TPs');
    return response.json();
}

export async function createTP(data) {
    const response = await fetch(`${API_URL}/trabajos-practicos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Error al crear TP');
    return response.json();
}

export async function updateTP(id, data) {
    const response = await fetch(`${API_URL}/trabajos-practicos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Error al actualizar TP');
    return response.json();
}

export async function deleteTP(id) {
    const response = await fetch(`${API_URL}/trabajos-practicos/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) throw new Error('Error al eliminar TP');
    return response.json();
}

// ========================================
// ALERTAS
// ========================================

export async function fetchAlertas() {
    const response = await fetch(`${API_URL}/alertas`);
    if (!response.ok) throw new Error('Error al cargar alertas');
    return response.json();
}
