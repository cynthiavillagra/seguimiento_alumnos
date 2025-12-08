/**
 * Módulo de Utilidades - Funciones helper reutilizables
 */

// ========================================
// TOAST NOTIFICATIONS
// ========================================

export function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span>${getToastIcon(type)}</span>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // Auto-remove después de 3 segundos
    setTimeout(() => {
        toast.style.animation = 'toastSlideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function getToastIcon(type) {
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    return icons[type] || icons.info;
}

// ========================================
// MODALES
// ========================================

export function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

export function closeModal(modalId) {
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

// Cerrar modal con ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
    }
});

// ========================================
// NAVEGACIÓN
// ========================================

export function setupNavigation(onPageChange) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            showPage(page, onPageChange);
        });
    });
}

export function showPage(pageName, callback) {
    // Ocultar todas las páginas
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));

    // Mostrar página seleccionada
    const page = document.getElementById(`page-${pageName}`);
    if (page) {
        page.classList.add('active');
    }

    // Actualizar nav
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    const activeLink = document.querySelector(`[data-page="${pageName}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }

    // Callback para cargar datos
    if (callback) {
        callback(pageName);
    }
}

// ========================================
// VALIDACIONES
// ========================================

export function validateEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}

export function validateDNI(dni) {
    return dni && dni.length >= 7 && dni.length <= 8 && /^\d+$/.test(dni);
}

export function validateRequired(value) {
    return value && value.trim().length > 0;
}

// ========================================
// FORMATEO
// ========================================

export function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-AR');
}

export function formatDateTime(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('es-AR');
}

// ========================================
// CONFIRMACIÓN
// ========================================

let confirmCallback = null;

export function showConfirmDialog(message, onConfirm) {
    const modal = document.getElementById('modal-confirmar-eliminar');
    const messageEl = document.getElementById('mensaje-confirmar-eliminar');

    if (modal && messageEl) {
        messageEl.textContent = message;
        confirmCallback = onConfirm;
        showModal('modal-confirmar-eliminar');
    }
}

export function confirmarEliminacion() {
    if (confirmCallback) {
        confirmCallback();
        confirmCallback = null;
    }
    closeModal('modal-confirmar-eliminar');
}

// Exportar para uso global
window.cerrarModal = closeModal;
window.confirmarEliminacion = confirmarEliminacion;
