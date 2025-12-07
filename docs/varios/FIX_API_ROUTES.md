# 🔧 Fix: Rutas de API en Vercel

## ❌ Problema
El frontend recibía HTML en lugar de JSON porque Vercel estaba enviando todas las peticiones (incluyendo `/alumnos`) al `index.html` del frontend.

## ✅ Solución

### `vercel.json` - Orden de Rutas Corregido

```json
{
  "routes": [
    // 1. PRIMERO: Rutas de API → Python
    {
      "src": "/(alumnos|health|ping|docs).*",
      "dest": "api/index.py"
    },
    
    // 2. SEGUNDO: Archivos estáticos → public/
    {
      "src": "/(.*\\.(css|js|png|...))",
      "dest": "/public/$1"
    },
    
    // 3. ÚLTIMO: Todo lo demás → index.html (SPA)
    {
      "src": "/(.*)",
      "dest": "/public/index.html"
    }
  ]
}
```

### Cómo Funciona Ahora

```
Request a Vercel
    ↓
¿Es /alumnos, /health, /ping o /docs?
    ↓ SÍ
    → api/index.py (Python)
    
    ↓ NO
¿Es un archivo estático (.css, .js, etc.)?
    ↓ SÍ
    → public/archivo
    
    ↓ NO
    → public/index.html (Frontend SPA)
```

## 🚀 Redesplegar

```bash
git add vercel.json
git commit -m "Fix API routes in Vercel"
git push
```

## ✅ Qué Esperar

Después del redespliegue:

### 1. Probar API Directamente
```
https://seguimiento-alumnos.vercel.app/alumnos
```
**Debería devolver**: JSON con lista de alumnos

### 2. Probar Frontend
```
https://seguimiento-alumnos.vercel.app/
```
**Debería mostrar**: El dashboard

### 3. Probar Registro de Clase
1. Click en "Registrar Clase"
2. Seleccionar materia/cohorte/fecha
3. Click en "Iniciar Registro"
4. ✅ Debería cargar los alumnos

## 🔍 Debugging

Si sigue fallando, abre la consola (F12) y verás:
```
Cargando alumnos desde: /alumnos
Alumnos recibidos: { total: 2, alumnos: [...] }
```

O si hay error:
```
Error al cargar alumnos: [mensaje de error]
```

---

**¡Redespliegua ahora!** 🚀
