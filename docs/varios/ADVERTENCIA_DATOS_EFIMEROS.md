# ⚠️ ADVERTENCIA CRÍTICA - DATOS EFÍMEROS EN VERCEL

## 🚨 LEE ESTO ANTES DE USAR EN PRODUCCIÓN

Si estás desplegando esta aplicación en **Vercel con SQLite**, debes saber que:

### ❌ LOS DATOS NO PERSISTEN

1. **Cada despliegue = Base de datos NUEVA y VACÍA**
   ```
   Despliegue 1: Creás 10 alumnos → ✅ Funcionan
   Despliegue 2: Actualizás el código → ❌ Los 10 alumnos DESAPARECEN
   ```

2. **Los datos pueden NO estar disponibles entre requests**
   ```
   Request 1: POST /alumnos → Creás alumno con ID 1
   Request 2: GET /alumnos/1 → ❌ Puede que NO exista
   ```

3. **Vercel reinicia contenedores constantemente**
   ```
   Guardás datos → Vercel reinicia → ❌ Datos PERDIDOS
   ```

### 🤔 ¿Por qué pasa esto?

Vercel usa **contenedores efímeros** (serverless):
- Cada función se ejecuta en un contenedor temporal
- SQLite se guarda en `/tmp` (directorio temporal)
- `/tmp` se borra cuando el contenedor se destruye
- Los contenedores se destruyen constantemente (cada pocos minutos o en cada despliegue)

### ✅ Casos de uso VÁLIDOS con SQLite en Vercel

**Está bien usar SQLite en Vercel para:**

1. **Demos y presentaciones**
   - Los datos se resetean automáticamente
   - Cada demo inicia limpio
   - No importa perder los datos

2. **Testing de la API**
   - Probar endpoints
   - Verificar que funciona
   - Desarrollo y pruebas

3. **Prototipos y MVPs de demostración**
   - Mostrar funcionalidad
   - No guardar datos reales
   - Solo para validar la idea

### ❌ NO usar SQLite en Vercel para:

1. **Datos de producción reales**
   - ❌ Alumnos reales de una institución
   - ❌ Datos que deben persistir
   - ❌ Información importante

2. **Aplicaciones en uso**
   - ❌ Usuarios reales
   - ❌ Datos que no pueden perderse
   - ❌ Cualquier cosa que necesite guardarse

### ✅ SOLUCIÓN: Migrar a PostgreSQL

Para usar esta aplicación en **producción REAL**, debes migrar a PostgreSQL:

#### Opciones Recomendadas (todas tienen plan gratuito):

1. **Vercel Postgres** (integrado con Vercel)
   - https://vercel.com/docs/storage/vercel-postgres
   - Gratis hasta 256 MB
   - Integración perfecta

2. **Supabase** (recomendado para empezar)
   - https://supabase.com
   - Gratis hasta 500 MB
   - Fácil de usar
   - Incluye autenticación

3. **Neon** (serverless PostgreSQL)
   - https://neon.tech
   - Gratis hasta 3 GB
   - Serverless como Vercel

4. **Railway**
   - https://railway.app
   - Fácil de configurar
   - Buen plan gratuito

#### Pasos para Migrar:

1. **Crear base de datos PostgreSQL** en uno de los servicios
2. **Copiar la cadena de conexión** (DATABASE_URL)
3. **Crear repositorios PostgreSQL** (ver plantilla en documentación)
4. **Configurar variable de entorno** en Vercel:
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```
5. **Actualizar dependency injection** para usar PostgreSQL
6. **Redesplegar**

Ver guía completa en: [DESPLIEGUE_VERCEL.md](./DESPLIEGUE_VERCEL.md)

### 📊 Comparación: SQLite vs PostgreSQL en Vercel

| Característica | SQLite en Vercel | PostgreSQL |
|----------------|------------------|------------|
| **Persistencia** | ❌ Efímera | ✅ Permanente |
| **Entre despliegues** | ❌ Se pierde | ✅ Se mantiene |
| **Entre requests** | ⚠️ Puede fallar | ✅ Siempre disponible |
| **Costo** | ✅ Gratis | ✅ Gratis (planes básicos) |
| **Configuración** | ✅ Automática | ⚠️ Requiere setup |
| **Uso en producción** | ❌ NO | ✅ SÍ |
| **Ideal para** | Demos, testing | Producción real |

### 🎯 Decisión Rápida

**¿Qué estás haciendo?**

- 🎨 **Demo/Presentación** → SQLite está bien
- 🧪 **Testing/Desarrollo** → SQLite está bien
- 🏫 **Producción real con alumnos** → ⚠️ USAR POSTGRESQL
- 💼 **Aplicación en uso** → ⚠️ USAR POSTGRESQL

### 📞 ¿Necesitas Ayuda?

Si necesitás ayuda para migrar a PostgreSQL:
1. Lee [DESPLIEGUE_VERCEL.md](./DESPLIEGUE_VERCEL.md)
2. Revisa la documentación de Supabase/Neon
3. Busca "FastAPI + PostgreSQL + Vercel" en Google

### ✅ Resumen

- ✅ **SQLite en Vercel = EFÍMERO** (datos se borran)
- ✅ **Para demos/testing** = Usar SQLite
- ✅ **Para producción** = Migrar a PostgreSQL
- ✅ **Guía completa** = Ver DESPLIEGUE_VERCEL.md

---

**¿Entendiste las limitaciones?** Entonces podés continuar con confianza sabiendo qué esperar.

**¿Necesitás persistencia real?** Migrá a PostgreSQL antes de usar en producción.

---

**Última actualización**: 2025-12-07
