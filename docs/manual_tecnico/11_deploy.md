# Capítulo 11: Deploy

## 11.1 Preparación para Producción

Antes de hacer deploy, asegurate de:

### Checklist Pre-Deploy

```
□ Todos los tests pasan
□ No hay errores de linting
□ Variables de entorno documentadas
□ .env.example actualizado
□ README actualizado
□ vercel.json configurado
□ requirements.txt actualizado
□ Código commitado y pusheado
```

## 11.2 Arquitectura de Deploy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ARQUITECTURA DE DEPLOY                             │
└─────────────────────────────────────────────────────────────────────────────┘

     Usuario (Navegador)
            │
            │ HTTPS
            ▼
┌─────────────────────────────────────┐
│            VERCEL                    │
│         (Edge Network)               │
│                                      │
│  ┌───────────────┬───────────────┐  │
│  │   Static      │   Serverless  │  │
│  │   Files       │   Functions   │  │
│  │               │               │  │
│  │  public/      │   api/        │  │
│  │  • index.html │   • index.py  │  │
│  │  • styles.css │     ↓         │  │
│  │  • app.js     │   FastAPI     │  │
│  │               │               │  │
│  └───────────────┴───────────────┘  │
│                                      │
└─────────────────────────────────────┘
            │
            │ PostgreSQL Protocol (SSL)
            ▼
┌─────────────────────────────────────┐
│             NEON                     │
│    (PostgreSQL Serverless)          │
│                                      │
│  ┌───────────────────────────────┐  │
│  │         Base de Datos         │  │
│  │                               │  │
│  │  • alumno                     │  │
│  │  • curso                      │  │
│  │  • clase                      │  │
│  │  • inscripcion                │  │
│  │  • registro_asistencia        │  │
│  │  • trabajo_practico           │  │
│  │  • entrega_tp                 │  │
│  │                               │  │
│  └───────────────────────────────┘  │
│                                      │
└─────────────────────────────────────┘
```

## 11.3 Configurar Neon (Base de Datos)

### Paso 1: Crear Cuenta

1. Ir a https://neon.tech
2. Registrarse con GitHub o email
3. Verificar email si es necesario

### Paso 2: Crear Proyecto

1. Click en "Create a project"
2. Nombre: `seguimiento-alumnos`
3. Región: `South America (São Paulo)` (o la más cercana)
4. Plan: `Free` (10GB gratis)

### Paso 3: Obtener Connection String

1. En el dashboard, ir a "Connection Details"
2. Seleccionar "pg8000" en el dropdown de driver
3. Copiar la URL completa:

```
postgresql://neondb_owner:AbCdEfGh123@ep-cool-fire-123456.sa-east-1.aws.neon.tech/neondb?sslmode=require
```

### Paso 4: Verificar Conexión

```bash
# Crear archivo .env con la URL
echo POSTGRES_URL=postgresql://... > .env

# Probar conexión
python scripts/test_db.py
```

Resultado esperado:
```
--- Test de Conexión a Base de Datos ---
✅ ¡CONEXIÓN EXITOSA!
PostgreSQL: PostgreSQL 16.x ...
```

## 11.4 Configurar Vercel

### Paso 1: Crear Cuenta y Conectar GitHub

1. Ir a https://vercel.com
2. "Sign up with GitHub"
3. Autorizar acceso

### Paso 2: Importar Proyecto

1. Click en "Add New..." → "Project"
2. Seleccionar el repositorio de GitHub
3. Click "Import"

### Paso 3: Configurar Build

| Campo | Valor |
|-------|-------|
| Framework Preset | Other |
| Root Directory | `./` |
| Build Command | (dejar vacío) |
| Output Directory | `public` |
| Install Command | `pip install -r requirements.txt` |

### Paso 4: Agregar Variables de Entorno

1. Expandir "Environment Variables"
2. Agregar:

| Nombre | Valor | Entornos |
|--------|-------|----------|
| `POSTGRES_URL` | (tu URL de Neon) | Production, Preview |
| `VERCEL` | `1` | Production, Preview |

### Paso 5: Deploy

1. Click en "Deploy"
2. Esperar 1-3 minutos
3. Verás el progreso en tiempo real

### Paso 6: Verificar

1. Una vez completado, click en "Visit"
2. Debería cargar la aplicación
3. Verificar: `https://tu-proyecto.vercel.app/api` → Debe responder JSON

## 11.5 Archivo vercel.json

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
  ],
  "functions": {
    "api/**/*.py": {
      "memory": 256,
      "maxDuration": 10
    }
  }
}
```

### Explicación

| Campo | Propósito |
|-------|-----------|
| `builds` | Define cómo se construye cada parte |
| `@vercel/python` | Usa el runtime de Python para la API |
| `@vercel/static` | Sirve archivos estáticos sin procesamiento |
| `routes` | Define cómo se rutean las URLs |
| `functions` | Configuración de las funciones serverless |

## 11.6 Archivo api/index.py

```python
"""
Punto de entrada para Vercel Serverless Functions
Sistema de Seguimiento de Alumnos

Este archivo adapta FastAPI para funcionar en el entorno
serverless de Vercel usando Mangum.
"""

import os

# Forzar variable de entorno para saber que estamos en Vercel
os.environ["VERCEL"] = "1"

# Importar la app de FastAPI
from src.presentation.api.main import app

# En Vercel, no necesitamos Mangum ya que Vercel
# soporta FastAPI directamente
# Solo exportamos la app

# Para compatibilidad con otros entornos serverless,
# podríamos usar:
# from mangum import Mangum
# handler = Mangum(app, lifespan="off")
```

## 11.7 Dominio Personalizado (Opcional)

### Agregar Dominio Propio

1. En Vercel, ir a "Settings" → "Domains"
2. Click "Add"
3. Ingresar tu dominio (ej: `alumnos.tudominio.com`)
4. Seguir instrucciones para configurar DNS

### Configuración DNS

En tu proveedor de dominio, agregar:

| Tipo | Nombre | Valor |
|------|--------|-------|
| CNAME | alumnos | cname.vercel-dns.com |

O para dominio raíz:

| Tipo | Nombre | Valor |
|------|--------|-------|
| A | @ | 76.76.21.21 |

## 11.8 Variables de Entorno

### En Desarrollo (.env)

```env
# Base de datos
POSTGRES_URL=postgresql://user:pass@host/db?sslmode=require

# Entorno (development, production, test)
ENVIRONMENT=development

# Debug (solo desarrollo)
DEBUG=true
```

### En Producción (Vercel Dashboard)

1. Ir a Settings → Environment Variables
2. Agregar cada variable
3. Seleccionar entornos (Production, Preview)

**⚠️ NUNCA commitear el archivo .env con credenciales reales**

## 11.9 CI/CD Automático

### Flujo de Deploy Automático

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Push   │────►│  Build  │────►│  Test   │────►│ Deploy  │
│  GitHub │     │ Vercel  │     │ (auto)  │     │  Live   │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
```

### Cada push a main:
1. Vercel detecta el cambio
2. Construye automáticamente
3. Despliega a producción

### Cada push a otras branches:
1. Vercel crea un "Preview Deployment"
2. URL única para probar
3. Útil para revisar PRs

## 11.10 Monitoreo

### Logs en Vercel

1. Dashboard → Functions → View Logs
2. Ver errores y requests en tiempo real

### Métricas de Neon

1. Dashboard de Neon → Monitoring
2. Ver queries, conexiones, storage

## 11.11 Troubleshooting

### Error: "Module not found"

**Causa:** Falta dependencia en requirements.txt

**Solución:**
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "fix: update dependencies"
git push
```

### Error: "Connection refused" (base de datos)

**Causa:** Variable de entorno incorrecta o faltante

**Solución:**
1. Verificar que `POSTGRES_URL` esté configurada en Vercel
2. Verificar que la URL sea correcta
3. Verificar que el IP de Vercel esté permitido en Neon

### Error: "500 Internal Server Error"

**Causa:** Error en el código del servidor

**Solución:**
1. Ver logs en Vercel
2. Reproducir localmente
3. Agregar más logging
4. Revisar traceback

### Error: "404 Not Found" para archivos estáticos

**Causa:** Rutas incorrectas en vercel.json

**Solución:**
1. Verificar que `public/` contenga los archivos
2. Verificar rutas en vercel.json
3. Verificar que index.html exista

### La base de datos no tiene tablas

**Causa:** No se ejecutó la inicialización

**Solución:**
1. La app inicializa automáticamente en startup
2. Si falla, revisar logs
3. Ejecutar manualmente: GET `/api/setup`

## 11.12 Comandos Útiles

```bash
# Ver estado de deploy
vercel --prod

# Ver logs en tiempo real
vercel logs

# Listar deployments
vercel ls

# Rollback a versión anterior
vercel rollback [deployment-url]

# Ver variables de entorno
vercel env ls

# Agregar variable de entorno
vercel env add POSTGRES_URL
```

## 11.13 Checklist Post-Deploy

```
□ La página principal carga
□ El endpoint /api responde
□ Se pueden crear alumnos
□ Se pueden crear cursos
□ La asistencia se guarda
□ Los datos persisten al recargar
□ No hay errores en consola del navegador
□ No hay errores en logs de Vercel
□ La base de datos tiene las tablas
□ HTTPS funciona correctamente
```

---

**Capítulo anterior**: [Pruebas](./10_pruebas.md)

**Siguiente capítulo**: [README Final](./12_readme_final.md)
