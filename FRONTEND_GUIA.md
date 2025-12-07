# 🎨 Frontend - Sistema de Seguimiento de Alumnos

## ✅ Archivos Creados

1. **`public/index.html`** - Estructura HTML de la SPA
2. **`public/styles.css`** - Estilos modernos con gradientes y animaciones
3. **`public/app.js`** - Lógica JavaScript y conexión con la API

## 🎯 Características del Frontend

### Diseño Moderno
- ✅ **Gradientes vibrantes** (púrpura y azul)
- ✅ **Glassmorphism** en la navbar
- ✅ **Animaciones suaves** en hover y transiciones
- ✅ **Sombras profundas** para dar sensación de profundidad
- ✅ **Tipografía moderna** (Inter font)
- ✅ **Responsive** para móviles y tablets

### Páginas Implementadas

#### 1. Dashboard
- 4 tarjetas de estadísticas con iconos
- Acciones rápidas
- Animación de números

#### 2. Alumnos
- Tabla con lista de alumnos
- Búsqueda en tiempo real
- Filtro por cohorte
- Modal para crear nuevo alumno
- Botones de acción (Ver, Editar)

#### 3. Alertas
- Tarjetas de alumnos en riesgo
- Niveles de riesgo (Alto, Medio, Bajo)
- Información de asistencia y TPs

#### 4. Reportes
- Placeholder "Próximamente"

### Componentes

#### Navbar
- Logo animado
- Links de navegación con iconos
- Badge de notificaciones
- Sticky (se queda arriba al hacer scroll)

#### Modales
- Modal para crear alumno
- Animación de entrada
- Cierre al hacer click fuera
- Formulario con validación

#### Toasts
- Notificaciones temporales
- 3 tipos: success, error, info
- Auto-desaparecen después de 3 segundos
- Animación de entrada/salida

## 🚀 Cómo Usar

### Opción 1: Abrir Directamente
```bash
# Navegar a la carpeta public
cd "app seguimiento de alumnos/public"

# Abrir index.html en el navegador
start index.html  # Windows
open index.html   # Mac
xdg-open index.html  # Linux
```

### Opción 2: Con Servidor Local (Recomendado)

#### Con Python:
```bash
cd "app seguimiento de alumnos/public"
python -m http.server 8080
```
Luego abrir: `http://localhost:8080`

#### Con Node.js (http-server):
```bash
npm install -g http-server
cd "app seguimiento de alumnos/public"
http-server -p 8080
```
Luego abrir: `http://localhost:8080`

#### Con VS Code Live Server:
1. Instalar extensión "Live Server"
2. Click derecho en `index.html`
3. "Open with Live Server"

## 📱 Funcionalidades Interactivas

### Dashboard
- ✅ Contador animado de alumnos
- ✅ Botones de acciones rápidas
- ✅ Navegación entre páginas

### Alumnos
- ✅ **Crear alumno**: Click en "Nuevo Alumno"
  - Completa el formulario
  - Click en "Crear Alumno"
  - Se envía a la API
  - Muestra notificación de éxito/error

- ✅ **Buscar alumno**: Escribe en el campo de búsqueda
  - Filtra en tiempo real
  - Busca por nombre, DNI o email

- ✅ **Ver/Editar**: Botones en cada fila
  - Por ahora muestran toast (próximamente implementar)

### Navegación
- Click en los links del navbar
- Transición suave entre páginas
- Highlight del link activo

## 🎨 Personalización de Estilos

### Colores Principales
Edita las variables CSS en `styles.css`:

```css
:root {
    --primary: #6366f1;      /* Azul principal */
    --secondary: #8b5cf6;    /* Púrpura */
    --accent: #ec4899;       /* Rosa */
    --success: #10b981;      /* Verde */
    --warning: #f59e0b;      /* Naranja */
    --danger: #ef4444;       /* Rojo */
}
```

### Gradientes
```css
/* Gradiente principal (navbar, botones) */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Gradiente de fondo */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 🔌 Conexión con la API

El frontend se conecta automáticamente a:
```javascript
const API_URL = 'https://seguimiento-alumnos.vercel.app';
```

### Endpoints Usados

1. **GET /alumnos** - Listar alumnos
   ```javascript
   fetch(`${API_URL}/alumnos`)
   ```

2. **POST /alumnos** - Crear alumno
   ```javascript
   fetch(`${API_URL}/alumnos`, {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify(alumnoData)
   })
   ```

## 🎯 Próximas Mejoras

### Corto Plazo
- [ ] Vista de detalle de alumno
- [ ] Edición de alumno
- [ ] Eliminación de alumno
- [ ] Paginación de tabla
- [ ] Ordenamiento de columnas

### Mediano Plazo
- [ ] Gestión de cursos
- [ ] Registro de asistencia
- [ ] Visualización de indicadores de riesgo
- [ ] Gráficos y estadísticas
- [ ] Exportar a PDF/Excel

### Largo Plazo
- [ ] Autenticación de usuarios
- [ ] Roles y permisos
- [ ] Notificaciones en tiempo real
- [ ] Dashboard personalizable
- [ ] Modo oscuro

## 📊 Estructura de Archivos

```
public/
├── index.html      # Estructura HTML (SPA)
├── styles.css      # Estilos modernos
└── app.js          # Lógica JavaScript
```

## 🎓 Conceptos Aplicados

### HTML
- Estructura semántica
- Accesibilidad (labels, alt text)
- SEO (meta tags, títulos)

### CSS
- Variables CSS (custom properties)
- Flexbox y Grid
- Animaciones y transiciones
- Media queries (responsive)
- Gradientes y sombras

### JavaScript
- Fetch API (llamadas HTTP)
- DOM manipulation
- Event listeners
- Async/await
- Modularización de código

## ✅ Checklist de Funcionalidad

- [x] Navegación entre páginas
- [x] Dashboard con estadísticas
- [x] Lista de alumnos desde API
- [x] Búsqueda de alumnos
- [x] Modal para crear alumno
- [x] Formulario con validación
- [x] Envío a API
- [x] Notificaciones toast
- [x] Diseño responsive
- [x] Animaciones suaves

---

**¡El frontend está listo para usar!** 🎉

Abre `public/index.html` en tu navegador y empieza a interactuar con el sistema.
