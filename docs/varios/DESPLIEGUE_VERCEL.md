# 🚀 Guía de Despliegue en Vercel

## 📋 Requisitos Previos

1. **Cuenta en Vercel**: Crear una cuenta gratuita en [vercel.com](https://vercel.com)
2. **Vercel CLI** (opcional pero recomendado): 
   ```bash
   npm install -g vercel
   ```
3. **Git** (opcional): Para despliegue automático desde GitHub

---

## 🎯 Opción 1: Despliegue desde GitHub (Recomendado)

### Paso 1: Subir el Proyecto a GitHub

1. **Crear un repositorio en GitHub**
   - Ve a [github.com/new](https://github.com/new)
   - Nombre: `sistema-seguimiento-alumnos`
   - Visibilidad: Público o Privado

2. **Inicializar Git localmente**
   ```bash
   cd "app seguimiento de alumnos"
   git init
   git add .
   git commit -m "Initial commit: Sistema de Seguimiento de Alumnos"
   ```

3. **Conectar con GitHub**
   ```bash
   git remote add origin https://github.com/TU-USUARIO/sistema-seguimiento-alumnos.git
   git branch -M main
   git push -u origin main
   ```

### Paso 2: Importar en Vercel

1. **Ir a Vercel Dashboard**
   - Acceder a [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click en "Add New..." → "Project"

2. **Importar el repositorio**
   - Seleccionar "Import Git Repository"
   - Autorizar acceso a GitHub
   - Seleccionar el repositorio `sistema-seguimiento-alumnos`

3. **Configurar el proyecto**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (dejar por defecto)
   - **Build Command**: (dejar vacío)
   - **Output Directory**: (dejar vacío)
   - **Install Command**: `pip install -r requirements.txt`

4. **Variables de Entorno** (opcional por ahora)
   - Por ahora no es necesario configurar nada
   - En el futuro, agregar aquí las variables del archivo `.env.example`

5. **Deploy**
   - Click en "Deploy"
   - Esperar 1-2 minutos
   - ✅ ¡Tu API estará en línea!

### Paso 3: Probar la API Desplegada

Una vez desplegado, Vercel te dará una URL como:
```
https://sistema-seguimiento-alumnos-xxx.vercel.app
```

Probar los endpoints:
- **Documentación**: `https://tu-app.vercel.app/docs`
- **Health Check**: `https://tu-app.vercel.app/health`
- **Crear Alumno**: `POST https://tu-app.vercel.app/alumnos`

---

## 🎯 Opción 2: Despliegue con Vercel CLI

### Paso 1: Instalar Vercel CLI

```bash
npm install -g vercel
```

### Paso 2: Iniciar Sesión

```bash
vercel login
```

Esto abrirá el navegador para autenticarte.

### Paso 3: Desplegar

```bash
cd "app seguimiento de alumnos"
vercel
```

**Responder las preguntas**:
- Set up and deploy? → `Y`
- Which scope? → Seleccionar tu cuenta
- Link to existing project? → `N`
- What's your project's name? → `sistema-seguimiento-alumnos`
- In which directory is your code located? → `./` (Enter)
- Want to override the settings? → `N`

Esperar 1-2 minutos y ¡listo!

### Paso 4: Desplegar a Producción

```bash
vercel --prod
```

---

## ⚙️ Configuración Avanzada

### Variables de Entorno en Vercel

1. **Ir a Project Settings**
   - Dashboard → Tu Proyecto → Settings → Environment Variables

2. **Agregar variables** (para futuras versiones):
   ```
   DATABASE_URL=postgresql://...  (cuando migres a PostgreSQL)
   SECRET_KEY=tu-clave-secreta
   CORS_ORIGINS=https://tu-frontend.com
   ```

3. **Aplicar cambios**
   - Las variables estarán disponibles en el próximo despliegue

---

## 🗄️ Limitaciones de SQLite en Vercel

### ⚠️ Importante: SQLite en Vercel es EFÍMERO

**Problema**:
- Vercel ejecuta cada request en un contenedor efímero
- La base de datos SQLite se guarda en `/tmp`
- `/tmp` se borra cuando el contenedor se destruye
- **Los datos NO persisten entre despliegues**

**Solución para Desarrollo/Demo**:
- ✅ Funciona perfectamente para probar la API
- ✅ Cada despliegue inicia con BD vacía (limpia)
- ✅ Ideal para demos y pruebas

**Solución para Producción**:
- 🔄 **Migrar a PostgreSQL** (recomendado)
- Opciones:
  - [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres)
  - [Supabase](https://supabase.com) (gratis hasta cierto límite)
  - [Neon](https://neon.tech) (serverless PostgreSQL)
  - [Railway](https://railway.app)

---

## 🔄 Migración a PostgreSQL (Futuro)

### Paso 1: Crear Base de Datos PostgreSQL

Ejemplo con Supabase (gratis):
1. Crear cuenta en [supabase.com](https://supabase.com)
2. Crear nuevo proyecto
3. Copiar la cadena de conexión

### Paso 2: Actualizar Repositorios

Crear nuevos repositorios en `src/infrastructure/repositories/postgres/`:
- `alumno_repository_postgres.py`
- `curso_repository_postgres.py`
- etc.

### Paso 3: Configurar Variables de Entorno

En Vercel Dashboard:
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Paso 4: Actualizar Dependency Injection

En `src/presentation/api/routers/alumnos.py`:
```python
def get_alumno_service() -> AlumnoService:
    # Detectar si hay DATABASE_URL (PostgreSQL) o usar SQLite
    if os.environ.get("DATABASE_URL"):
        # Usar PostgreSQL
        from src.infrastructure.repositories.postgres.alumno_repository_postgres import AlumnoRepositoryPostgres
        conexion = get_postgres_connection()
        alumno_repo = AlumnoRepositoryPostgres(conexion)
    else:
        # Usar SQLite (desarrollo local)
        from src.infrastructure.repositories.sqlite.alumno_repository_sqlite import AlumnoRepositorySQLite
        conexion = get_db_connection()
        alumno_repo = AlumnoRepositorySQLite(conexion)
    
    return AlumnoService(alumno_repo)
```

---

## 🧪 Probar la API Desplegada

### Con cURL

```bash
# Health check
curl https://tu-app.vercel.app/health

# Crear alumno
curl -X POST "https://tu-app.vercel.app/alumnos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test",
    "apellido": "Vercel",
    "dni": "11111111",
    "email": "test@vercel.com",
    "cohorte": 2024
  }'

# Listar alumnos
curl https://tu-app.vercel.app/alumnos
```

### Con Swagger UI

Acceder a: `https://tu-app.vercel.app/docs`

Probar todos los endpoints desde la interfaz interactiva.

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
vercel logs
```

### Ver Logs en Dashboard

1. Ir a tu proyecto en Vercel
2. Click en "Deployments"
3. Click en el deployment activo
4. Ver logs en la pestaña "Logs"

---

## 🔧 Troubleshooting

### Error: "Module not found"

**Solución**: Verificar que `requirements.txt` esté en la raíz del proyecto.

### Error: "Database locked"

**Solución**: Normal en SQLite serverless. Migrar a PostgreSQL para producción.

### Error: "Function timeout"

**Solución**: Aumentar `maxDuration` en `vercel.json`:
```json
"functions": {
  "api/index.py": {
    "maxDuration": 30
  }
}
```

### La BD se borra en cada despliegue

**Solución**: Esto es esperado con SQLite en Vercel. Usar PostgreSQL para persistencia real.

---

## 🎉 ¡Listo!

Tu API está desplegada y funcionando en Vercel. Ahora puedes:

- ✅ Compartir la URL con otros
- ✅ Conectar un frontend
- ✅ Usar la API desde cualquier lugar
- ✅ Ver logs y métricas en Vercel Dashboard

---

## 📚 Recursos Adicionales

- [Documentación de Vercel](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Mangum (ASGI Adapter)](https://mangum.io/)

---

**Última actualización**: 2025-12-07  
**Versión**: 1.0.0
