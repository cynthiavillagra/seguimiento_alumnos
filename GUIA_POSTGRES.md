# 🚀 Guía de Implementación: Vercel Postgres

## 📋 Pasos a Seguir

### Paso 1: Instalar Vercel CLI (si no lo tienes)

Abre PowerShell y ejecuta:

```powershell
npm install -g vercel
```

Luego inicia sesión:
```powershell
vercel login
```

### Paso 2: Crear Base de Datos PostgreSQL en Vercel

```powershell
# Navegar al proyecto
cd "C:\Users\Cynthia\OneDrive\Escritorio\EDUCACION\00 Pedagogia\app seguimiento de alumnos"

# Crear BD PostgreSQL
vercel postgres create
```

Te preguntará:
- **Database name**: `seguimiento-alumnos-db`
- **Region**: Elegir la más cercana (ej: `iad1` para US East)

### Paso 3: Conectar la BD al Proyecto

```powershell
# Link la BD al proyecto
vercel link

# Descargar variables de entorno
vercel env pull .env.local
```

Esto creará un archivo `.env.local` con las credenciales de la BD.

### Paso 4: Ver las Credenciales

Abre `.env.local` y verás algo como:

```env
POSTGRES_URL="postgres://default:..."
POSTGRES_PRISMA_URL="postgres://default:..."
POSTGRES_URL_NON_POOLING="postgres://default:..."
POSTGRES_USER="default"
POSTGRES_HOST="..."
POSTGRES_PASSWORD="..."
POSTGRES_DATABASE="verceldb"
```

### Paso 5: Instalar Dependencias de PostgreSQL

Actualiza `requirements.txt`:

```txt
# Agregar al final
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

Instalar localmente:
```powershell
pip install psycopg2-binary python-dotenv
```

### Paso 6: Crear Script de Migración

Voy a crear un script que:
1. Convierte el schema SQLite a PostgreSQL
2. Crea las tablas
3. Inserta datos iniciales

### Paso 7: Ejecutar Migración

```powershell
# Ejecutar script de migración
python scripts/migrate_to_postgres.py
```

### Paso 8: Actualizar API para Usar PostgreSQL

Modificaré `api/index.py` para conectarse a PostgreSQL en lugar de usar datos hardcodeados.

### Paso 9: Redesplegar en Vercel

```powershell
git add .
git commit -m "Migrate to PostgreSQL"
git push
```

Vercel detectará las variables de entorno automáticamente.

### Paso 10: Verificar

```
https://seguimiento-alumnos.vercel.app/cursos
→ Debería devolver datos reales de PostgreSQL
```

---

## ⏱️ Tiempo Estimado

- Paso 1-3: 5 minutos
- Paso 4-6: 10 minutos (yo creo los scripts)
- Paso 7-9: 5 minutos
- **Total: ~20 minutos**

---

## 🎯 ¿Estás listo?

**Ejecuta el Paso 1 y 2** (instalar Vercel CLI y crear BD) y avísame cuando esté listo.

Mientras tanto, voy a preparar:
- ✅ Script de migración SQLite → PostgreSQL
- ✅ API actualizada para PostgreSQL
- ✅ Datos iniciales (seed)

**¿Tienes Vercel CLI instalado? ¿Quieres que continúe preparando los scripts?**
