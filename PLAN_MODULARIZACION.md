# 🏗️ Reestructuración del Proyecto - Modular

## 🎯 Problema Actual

Los archivos están creciendo demasiado:
- `app.js` - Más de 1400 líneas
- `index.html` - Más de 600 líneas
- `styles.css` - Más de 1400 líneas

**Esto dificulta el mantenimiento.**

---

## ✅ Solución: Modularizar

### Nueva Estructura Propuesta

```
public/
├── index.html                 # Solo estructura básica
├── css/
│   ├── variables.css         # Variables CSS
│   ├── base.css              # Estilos base
│   ├── components.css        # Componentes (botones, modales)
│   ├── pages.css             # Estilos de páginas
│   └── table.css             # Estilos de tablas
├── js/
│   ├── app.js                # Inicialización
│   ├── api.js                # Llamadas a la API
│   ├── cursos.js             # Gestión de cursos
│   ├── alumnos.js            # Gestión de alumnos
│   ├── tps.js                # Gestión de TPs
│   ├── modals.js             # Gestión de modales
│   └── utils.js              # Funciones utilitarias
└── pages/
    ├── dashboard.html        # Página dashboard
    ├── cursos.html           # Página cursos
    ├── alumnos.html          # Página alumnos
    └── alertas.html          # Página alertas
```

---

## 🔧 Implementación

### 1. Separar CSS

**css/variables.css**
```css
:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    /* ... todas las variables */
}
```

**css/base.css**
```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; }
/* ... estilos base */
```

**css/components.css**
```css
.btn-primary { }
.btn-secondary { }
.modal { }
/* ... componentes */
```

**css/table.css**
```css
.data-table { }
.search-bar { }
/* ... estilos de tablas */
```

### 2. Separar JavaScript

**js/api.js**
```javascript
const API_URL = window.location.hostname.includes('vercel.app') ? '' : '/api';

export async function fetchCursos() {
    const response = await fetch(`${API_URL}/cursos`);
    return response.json();
}

export async function createCurso(data) {
    const response = await fetch(`${API_URL}/cursos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return response.json();
}

export async function updateCurso(id, data) {
    const response = await fetch(`${API_URL}/cursos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return response.json();
}

export async function deleteCurso(id) {
    const response = await fetch(`${API_URL}/cursos/${id}`, {
        method: 'DELETE'
    });
    return response.json();
}
```

**js/cursos.js**
```javascript
import { fetchCursos, createCurso, updateCurso, deleteCurso } from './api.js';
import { showToast } from './utils.js';

let cursos = [];

export async function loadCursosPage() {
    try {
        const data = await fetchCursos();
        cursos = data.clases || [];
        renderCursosTable(cursos);
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar cursos', 'error');
    }
}

export function renderCursosTable(cursos) {
    // ... código de renderizado
}

export function filtrarCursos() {
    // ... código de filtrado
}
```

**js/utils.js**
```javascript
export function showToast(message, type = 'info') {
    // ... código de toast
}

export function showModal(modalId) {
    // ... código de modal
}

export function closeModal(modalId) {
    // ... código de cerrar modal
}
```

**js/app.js**
```javascript
import { loadCursosPage } from './cursos.js';
import { loadAlumnosPage } from './alumnos.js';
import { loadDashboardData } from './dashboard.js';

document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    loadDashboardData();
});

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
    if (page) page.classList.add('active');
    
    // Cargar datos
    switch(pageName) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'cursos':
            loadCursosPage();
            break;
        case 'alumnos':
            loadAlumnosPage();
            break;
    }
}
```

### 3. index.html Simplificado

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Seguimiento de Alumnos</title>
    
    <!-- CSS Modular -->
    <link rel="stylesheet" href="css/variables.css">
    <link rel="stylesheet" href="css/base.css">
    <link rel="stylesheet" href="css/components.css">
    <link rel="stylesheet" href="css/pages.css">
    <link rel="stylesheet" href="css/table.css">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <!-- ... navbar content ... -->
    </nav>

    <!-- Main Content -->
    <main class="main-content">
        <!-- Las páginas se cargan dinámicamente -->
        <div id="page-container"></div>
    </main>

    <!-- Modales -->
    <div id="modals-container"></div>

    <!-- Toast Container -->
    <div id="toast-container"></div>

    <!-- JavaScript Modular -->
    <script type="module" src="js/app.js"></script>
</body>
</html>
```

---

## 🎯 Ventajas de la Modularización

### 1. **Mantenibilidad**
- Archivos pequeños y enfocados
- Fácil encontrar código específico
- Menos conflictos en Git

### 2. **Escalabilidad**
- Agregar nuevas funcionalidades sin tocar código existente
- Reutilizar componentes

### 3. **Performance**
- Carga solo lo necesario
- Posibilidad de lazy loading

### 4. **Organización**
- Código limpio y estructurado
- Separación de responsabilidades
- Más fácil de testear

---

## 🚀 Plan de Migración

### Fase 1: Separar CSS (30 min)
1. Crear carpeta `public/css/`
2. Dividir `styles.css` en archivos temáticos
3. Actualizar `index.html` para importar todos los CSS

### Fase 2: Separar JavaScript (45 min)
1. Crear carpeta `public/js/`
2. Dividir `app.js` en módulos
3. Usar ES6 modules (import/export)
4. Actualizar `index.html`

### Fase 3: Separar HTML (opcional) (30 min)
1. Crear carpeta `public/pages/`
2. Extraer cada página a su archivo
3. Cargar dinámicamente con JavaScript

### Fase 4: Testing (15 min)
1. Verificar que todo funciona
2. Probar en local
3. Deploy a Vercel

**Total: ~2 horas**

---

## ⚠️ Consideraciones

### Vercel Compatibility
- Vercel soporta ES6 modules
- No requiere build step
- Los imports funcionan directamente

### Browser Support
- ES6 modules funcionan en todos los navegadores modernos
- Si necesitas IE11, necesitarías un bundler (Webpack/Vite)

---

## 🤔 ¿Qué Prefieres?

### Opción A: Modularizar Ahora
- Mejor a largo plazo
- Más trabajo inicial
- Código más limpio

### Opción B: Continuar Monolítico
- Más rápido ahora
- Más difícil después
- Archivos grandes

---

**¿Quieres que modularice el proyecto ahora o prefieres terminar las funcionalidades primero y modularizar después?** 🤔
