# Capítulo 10: Deploy

## 10.1 ¿Qué es Deploy?

**Deploy** = poner tu aplicación en internet para que otros la usen.

```
DESARROLLO                       PRODUCCIÓN
───────────                      ──────────

Tu PC                   ───►     Servidores en la nube
localhost:8000                   tu-app.vercel.app

Solo vos podés ver              Todo el mundo puede ver
```

---

## 10.2 Arquitectura de Deploy

```
┌─────────────────────────────────────────────────────────────┐
│                         INTERNET                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                          VERCEL                             │
│                      (Hosting gratis)                       │
│                                                             │
│   ┌─────────────┐              ┌─────────────────────┐      │
│   │   Frontend  │              │    API (FastAPI)    │      │
│   │   (HTML/JS) │              │    Serverless       │      │
│   │             │              │                     │      │
│   │   public/   │              │    api/index.py     │      │
│   └─────────────┘              └─────────────────────┘      │
│                                           │                 │
└─────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────┐
│                           NEON                              │
│                   (PostgreSQL gratis)                       │
│                                                             │
│   Tablas: alumno, curso, inscripcion                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 10.3 Preparar el Proyecto para Deploy

### Paso 1: Crear archivo para Vercel

Crear `api/index.py`:

```python
"""
Punto de entrada para Vercel
"""
import os

# Marcar que estamos en Vercel
os.environ["VERCEL"] = "1"

# Importar la app
from src.presentation.api.main import app
```

### Paso 2: Crear vercel.json

Crear `vercel.json` en la raíz:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
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
      "src": "/(.*\\.(css|js|ico|png|jpg|svg))",
      "dest": "public/$1"
    },
    {
      "src": "/(.*)",
      "dest": "public/index.html"
    }
  ]
}
```

### Paso 3: Asegurar requirements.txt

```
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.6.0
pg8000==1.30.0
email-validator==2.1.0
```

---

## 10.4 Configurar Neon (Base de Datos)

### 1. Crear cuenta

1. Ir a https://neon.tech
2. Registrarse con GitHub
3. Crear proyecto: `mi-proyecto-mvp`

### 2. Obtener URL de conexión

1. Dashboard → Connection Details
2. Copiar URL que empieza con `postgresql://...`

### 3. Guardar localmente

En tu archivo `.env`:
```
POSTGRES_URL=postgresql://usuario:pass@host/database?sslmode=require
```

---

## 10.5 Configurar Vercel

### 1. Crear cuenta

1. Ir a https://vercel.com
2. Registrarse con GitHub

### 2. Subir código a GitHub

```powershell
# Si no tenés repo, crear uno
git init
git add .
git commit -m "Initial commit"

# Conectar a GitHub (crear repo en github.com primero)
git remote add origin https://github.com/tu-usuario/mi-proyecto-mvp.git
git push -u origin main
```

### 3. Importar en Vercel

1. Dashboard de Vercel → "Add New Project"
2. Seleccionar el repositorio de GitHub
3. Click "Import"

### 4. Configurar build

| Campo | Valor |
|-------|-------|
| Framework Preset | Other |
| Root Directory | `./` |
| Build Command | (dejar vacío) |
| Output Directory | `public` |

### 5. Agregar variables de entorno

1. Expandir "Environment Variables"
2. Agregar:

| Nombre | Valor |
|--------|-------|
| `POSTGRES_URL` | (tu URL de Neon) |

### 6. Deploy

1. Click "Deploy"
2. Esperar 1-2 minutos
3. ¡Listo! URL disponible

---

## 10.6 Verificar el Deploy

### Checklist

```
□ La página principal carga
□ /api responde JSON
□ Puedo crear un alumno
□ Puedo crear un curso
□ Los datos persisten al recargar
□ No hay errores en consola
```

### Probar endpoints

```
https://tu-app.vercel.app/api
https://tu-app.vercel.app/api/alumnos/
https://tu-app.vercel.app/api/cursos/
```

---

## 10.7 Actualizar el Deploy

Cada vez que hagas push a GitHub, Vercel re-despliega automáticamente.

```powershell
# Hacer cambios
# ...

# Commitear
git add .
git commit -m "fix: corregir bug"

# Pushear (automáticamente redeploy)
git push
```

---

## 10.8 Troubleshooting

### Error: 500 Internal Server Error

**Ver logs en Vercel:**
1. Dashboard → tu proyecto
2. Deployments → último deploy
3. Functions → Ver logs

**Causa común:** Variable de entorno no configurada

### Error: No se conecta a la BD

**Verificar:**
1. POSTGRES_URL está configurada en Vercel
2. La URL es correcta
3. El proyecto de Neon está activo

### Error: 404 Not Found

**Causa:** Rutas incorrectas en vercel.json

**Verificar:**
1. El archivo vercel.json existe
2. Las rutas apuntan correctamente

---

## 10.9 Dominio Personalizado (Opcional)

1. En Vercel → Settings → Domains
2. Agregar tu dominio
3. Configurar DNS según instrucciones

---

## 10.10 Resumen

### Lo que configuraste

| Servicio | Para qué | Gratis |
|----------|----------|--------|
| **GitHub** | Código fuente | ✅ |
| **Vercel** | Hosting | ✅ |
| **Neon** | Base de datos | ✅ (500MB) |

### Archivos de deploy

```
mi_proyecto/
├── api/
│   └── index.py          ✅ Punto de entrada Vercel
├── vercel.json           ✅ Configuración Vercel
└── requirements.txt      ✅ Dependencias
```

### Flujo de deploy

```
1. Hacer cambios localmente
2. git add . && git commit
3. git push
4. Vercel detecta y redeploy automático
5. ¡Listo en 1-2 minutos!
```

---

## 🎉 ¡Felicitaciones!

Completaste el manual. Ahora tenés:

- ✅ Un proyecto con arquitectura profesional
- ✅ Frontend y backend funcionando
- ✅ Tests automatizados
- ✅ Deploy en producción

### Próximos pasos sugeridos

1. 📱 Agregar más funcionalidades
2. 🔐 Implementar autenticación
3. 📊 Agregar reportes
4. 🎨 Mejorar el diseño

---

**Anterior:** [Capítulo 9 - Testing](./09_testing.md)

**Volver al inicio:** [README](./README.md)
