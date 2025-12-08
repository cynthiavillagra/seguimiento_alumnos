/**
 * App Principal - Sistema de Seguimiento de Alumnos
 * Inicialización y coordinación de módulos
 */

import { setupNavigation, showPage } from './utils.js';
import { loadCursosPage } from './cursos.js';

// Estado global de la aplicación
window.appState = {
    currentPage: 'dashboard',
    cursos: [],
    alumnos: [],
    claseActual: {
        materia: null,
        cohorte: null,
        fecha: null,
        registros: {}
    }
};

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎓 Sistema de Seguimiento de Alumnos iniciado');

    // Configurar navegación
    setupNavigation(handlePageChange);

    // Cargar página inicial
    loadDashboardData();
});

// ========================================
// MANEJO DE CAMBIO DE PÁGINA
// ========================================

function handlePageChange(pageName) {
    window.appState.currentPage = pageName;

    switch (pageName) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'cursos':
            loadCursosPage();
            break;
        case 'alumnos':
            // loadAlumnosPage(); // TODO: Implementar
            break;
        case 'alertas':
            // loadAlertasPage(); // TODO: Implementar
            break;
    }
}

// ========================================
// DASHBOARD (Temporal - mantener compatibilidad)
// ========================================

async function loadDashboardData() {
    // TODO: Implementar carga de dashboard
    console.log('Cargando dashboard...');
}

// Exportar para uso global
window.loadDashboardData = loadDashboardData;
window.showPage = showPage;
