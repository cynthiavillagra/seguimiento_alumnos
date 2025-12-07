# 🔧 Configuración de Vercel - Frontend + API

## ✅ Cambios Realizados

He actualizado la configuración de Vercel para servir **tanto el frontend como la API** en el mismo dominio.

### 1. `vercel.json` - Configuración Actualizada

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "public/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*\\.(css|js|png|jpg|...))",
      "dest": "/public/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/public/index.html"
    }
  ]
}
```

### 2. `public/app.js` - URL de API Actualizada

```javascript
const API_URL = '/api'; // Ruta relativa
```

## 🎯 Cómo Funciona

### Estructura de URLs

Después de redesplegar, las URLs funcionarán así:

#### Frontend (Archivos Estáticos)
- `https://seguimiento-alumnos.vercel.app/` → `public/index.html`
- `https://seguimiento-alumnos.vercel.app/styles.css` → `public/styles.css`
- `https://seguimiento-alumnos.vercel.app/app.js` → `public/app.js`

#### API (Python)
- `https://seguimiento-alumnos.vercel.app/api/` → API Python (info)
- `https://seguimiento-alumnos.vercel.app/api/health` → Health check
- `https://seguimiento-alumnos.vercel.app/api/alumnos` → Lista de alumnos
- `https://seguimiento-alumnos.vercel.app/api/ping` → Ping

### Flujo de Routing

```
Request → Vercel
    ↓
    ├─ /api/* → Python API (api/index.py)
    ├─ /*.css, *.js, *.png, etc. → Archivos estáticos (public/)
    └─ /* (cualquier otra ruta) → public/index.html (SPA)
```

## 🚀 Redesplegar

```bash
git add .
git commit -m "Configure Vercel for frontend + API"
git push
```

O desde Vercel Dashboard → Redeploy

## ✅ Qué Esperar Después del Redespliegue

### 1. Abrir la URL Principal
```
https://seguimiento-alumnos.vercel.app/
```

**Deberías ver**: El frontend con el dashboard hermoso

### 2. Probar la API
```
https://seguimiento-alumnos.vercel.app/api/
```

**Deberías ver**: JSON con info de la API

### 3. Probar Alumnos
```
https://seguimiento-alumnos.vercel.app/api/alumnos
```

**Deberías ver**: JSON con lista de alumnos

### 4. Interactuar con el Frontend
- Click en "Alumnos" en el navbar
- Debería cargar la lista desde `/api/alumnos`
- Click en "Nuevo Alumno"
- Completar formulario
- Debería enviar a `/api/alumnos` (POST)

## 🔍 Verificación

### Verificar Frontend
1. Abrir `https://seguimiento-alumnos.vercel.app/`
2. Deberías ver el dashboard con gradientes
3. Navegar entre páginas
4. Todo debería funcionar

### Verificar API
1. Abrir `https://seguimiento-alumnos.vercel.app/api/`
2. Deberías ver JSON
3. Abrir `https://seguimiento-alumnos.vercel.app/api/alumnos`
4. Deberías ver lista de alumnos

### Verificar Integración
1. En el frontend, ir a "Alumnos"
2. Debería cargar datos desde la API
3. Abrir DevTools (F12) → Network
4. Deberías ver requests a `/api/alumnos`

## 🐛 Troubleshooting

### Problema: Frontend no carga
**Solución**: Verificar que `public/index.html` existe

### Problema: CSS/JS no cargan
**Solución**: Verificar rutas en `index.html`:
```html
<link rel="stylesheet" href="styles.css">
<script src="app.js"></script>
```

### Problema: API no responde
**Solución**: Verificar que `api/index.py` existe y funciona

### Problema: CORS errors
**Solución**: No debería haber CORS porque frontend y API están en el mismo dominio

## 📊 Estructura Final

```
proyecto/
├── api/
│   └── index.py          # API Python
├── public/
│   ├── index.html        # Frontend
│   ├── styles.css        # Estilos
│   └── app.js            # JavaScript
└── vercel.json           # Configuración
```

## 🎯 Ventajas de Esta Configuración

1. ✅ **Un solo dominio** - No hay problemas de CORS
2. ✅ **URLs limpias** - `/api/alumnos` en lugar de `api.example.com/alumnos`
3. ✅ **Fácil de mantener** - Todo en un proyecto
4. ✅ **Despliegue único** - Un solo comando para todo
5. ✅ **Gratis en Vercel** - Plan gratuito cubre ambos

## 📝 Próximos Pasos

Después del redespliegue:

1. ✅ Verificar que el frontend carga
2. ✅ Verificar que la API responde
3. ✅ Probar crear un alumno desde el frontend
4. ✅ Verificar que los datos se guardan (aunque sean efímeros)

---

**¡Redespliegua ahora y todo debería funcionar perfectamente!** 🚀

El frontend y la API estarán integrados en el mismo dominio.
