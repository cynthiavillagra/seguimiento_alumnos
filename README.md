# 🎓 Sistema de Seguimiento de Alumnos

Sistema de seguimiento y detección temprana de riesgo de deserción para Tecnicaturas Superiores.

> ## ⚠️ ADVERTENCIA IMPORTANTE - Base de Datos Efímera en Vercel
> 
> **Si desplegás esta aplicación en Vercel con SQLite:**
> - ❌ **TODOS LOS DATOS SE BORRAN** en cada nuevo despliegue
> - ❌ **Los archivos cargados NO PERSISTEN** (se pierden al reiniciar)
> - ❌ **Los cambios en la BD NO SE GUARDAN** permanentemente
> 
> **¿Por qué?** Vercel usa contenedores efímeros. SQLite se guarda en `/tmp` que se borra constantemente.
> 
> **Soluciones:**
> - ✅ **Para desarrollo/demos**: Usar SQLite (está bien que sea efímero)
> - ✅ **Para producción**: Migrar a PostgreSQL (ver [DESPLIEGUE_VERCEL.md](./DESPLIEGUE_VERCEL.md))
> - ✅ **Para archivos**: Usar almacenamiento externo (Vercel Blob, S3, Cloudinary)
>
> 📖 **Lee la advertencia completa**: [ADVERTENCIA_DATOS_EFIMEROS.md](./ADVERTENCIA_DATOS_EFIMEROS.md)

## 📋 Descripción

Esta aplicación permite a docentes y coordinadores de Tecnicaturas Superiores:

- ✅ Registrar asistencia, participación y entregas de trabajos prácticos clase por clase
- 📊 Calcular automáticamente indicadores de riesgo de deserción
- 🚨 Generar alertas tempranas para intervención oportuna
- 📈 Consultar fichas completas de alumnos con historial académico

### Problema que Resuelve

Las Tecnicaturas Superiores enfrentan tasas de deserción del 40-60% en los primeros años. El seguimiento tradicional (solo con notas de parciales) detecta el riesgo **demasiado tarde**. Este sistema permite:

- **Detección temprana**: Identificar señales de alerta desde las primeras semanas
- **Seguimiento continuo**: Registrar datos clase por clase
- **Visión integral**: Combinar múltiples indicadores (asistencia, participación, TPs)
- **Intervención oportuna**: Actuar antes de que sea irreversible

## 🏗️ Arquitectura

El sistema está construido con **arquitectura por capas** siguiendo principios SOLID:

```
┌─────────────────────────────────────────────┐
│  📡 API (FastAPI)                            │
│  - Endpoints REST                            │
│  - Validación con Pydantic                   │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│  ⚙️  Servicios de Aplicación                │
│  - Casos de uso                              │
│  - Orquestación                              │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│  🎯 Dominio                                  │
│  - Entidades (Alumno, Curso, etc.)           │
│  - Reglas de negocio                         │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│  🗄️  Repositorios (SQLite)                  │
│  - Persistencia                              │
│  - Patrón Repository                         │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│  💾 SQLite Database                          │
└─────────────────────────────────────────────┘
```

### Tecnologías

- **Backend**: Python 3.11+
- **Framework Web**: FastAPI
- **Base de Datos (MVP)**: SQLite
- **Validación**: Pydantic
- **Despliegue**: Vercel (serverless)

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio** (o descargar el código)

```bash
cd "app seguimiento de alumnos"
```

2. **Crear entorno virtual** (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Inicializar base de datos**

```bash
python scripts/init_db.py
```

5. **Cargar datos de ejemplo** (opcional)

```bash
python scripts/seed_data.py
```

6. **Ejecutar la aplicación**

```bash
# Opción 1: Usando uvicorn directamente
uvicorn src.presentation.api.main:app --reload --host 0.0.0.0 --port 8000

# Opción 2: Ejecutando el archivo main.py
python src/presentation/api/main.py
```

7. **Acceder a la API**

- **Swagger UI (Documentación interactiva)**: http://localhost:8000/docs
- **ReDoc (Documentación alternativa)**: http://localhost:8000/redoc
- **API Base**: http://localhost:8000

## 📚 Documentación

La documentación completa del proyecto está en la carpeta `docs/`:

- **[README.md](docs/README.md)** - Índice de documentación
- **[01_CONTEXTO_Y_REQUISITOS.md](docs/01_CONTEXTO_Y_REQUISITOS.md)** - Contexto, objetivos y requisitos
- **[02_CASOS_DE_USO_Y_STORIES.md](docs/02_CASOS_DE_USO_Y_STORIES.md)** - Casos de uso y user stories
- **[03_MODELO_Y_API.md](docs/03_MODELO_Y_API.md)** - Modelo de dominio, API y diagramas UML
- **[04_ESTRUCTURA_Y_TRAZABILIDAD.md](docs/04_ESTRUCTURA_Y_TRAZABILIDAD.md)** - Estructura del proyecto y trazabilidad

## 🔌 Endpoints Principales

### Alumnos

- `POST /alumnos` - Crear alumno
- `GET /alumnos/{id}` - Obtener alumno
- `GET /alumnos` - Listar alumnos (con filtros y paginación)
- `PUT /alumnos/{id}` - Actualizar alumno
- `DELETE /alumnos/{id}` - Eliminar alumno

### Próximamente

- Cursos (`/cursos`)
- Clases (`/clases`)
- Asistencias (`/asistencias`)
- Participaciones (`/participaciones`)
- Trabajos Prácticos (`/trabajos-practicos`)
- Alertas (`/alertas/alumnos-en-riesgo`)

## 🧪 Testing

```bash
# Ejecutar tests unitarios
pytest tests/unit

# Ejecutar tests de integración
pytest tests/integration

# Ejecutar todos los tests con coverage
pytest --cov=src tests/
```

## � Despliegue en Vercel

El sistema está preparado para desplegarse en Vercel como función serverless.

### Opción 1: Despliegue desde GitHub (Recomendado)

1. Subir el proyecto a GitHub
2. Importar en Vercel desde el dashboard
3. Vercel detectará automáticamente la configuración
4. ¡Listo! Tu API estará en línea

### Opción 2: Despliegue con Vercel CLI

```bash
# Instalar Vercel CLI
npm install -g vercel

# Iniciar sesión
vercel login

# Desplegar
vercel

# Desplegar a producción
vercel --prod
```

### 📖 Guía Completa

Ver [DESPLIEGUE_VERCEL.md](./DESPLIEGUE_VERCEL.md) para instrucciones detalladas, configuración avanzada y troubleshooting.

### ⚠️ IMPORTANTE: SQLite en Vercel es EFÍMERO

**🚨 ADVERTENCIA CRÍTICA:**

Cuando desplegás en Vercel con SQLite:

1. **Cada despliegue = Base de datos NUEVA y VACÍA**
   - Si hacés cambios en el código y redespliegás → Se pierden TODOS los datos
   - Si Vercel reinicia el contenedor → Se pierden TODOS los datos
   
2. **Los datos NO persisten entre requests**
   - Cada función serverless puede tener su propia copia de `/tmp`
   - Los datos que guardás pueden no estar disponibles en el próximo request
   
3. **NO usar para datos importantes**
   - ❌ NO guardar datos de alumnos reales
   - ❌ NO usar como base de datos de producción
   - ❌ NO esperar que los datos se mantengan

**✅ Casos de uso válidos con SQLite en Vercel:**
- Demos y presentaciones (los datos se resetean automáticamente)
- Testing de la API (cada test inicia limpio)
- Desarrollo y pruebas (no importa perder los datos)

**✅ Para producción REAL:**
- **Migrar a PostgreSQL** (Vercel Postgres, Supabase, Neon, Railway)
- Ver guía completa en [DESPLIEGUE_VERCEL.md](./DESPLIEGUE_VERCEL.md)
- Los datos SÍ persistirán y estarán disponibles siempre


## �📁 Estructura del Proyecto

```
app-seguimiento-alumnos/
├── docs/                           # Documentación completa
├── src/
│   ├── domain/                     # Capa de Dominio
│   │   ├── entities/               # Entidades (Alumno, Curso, etc.)
│   │   ├── value_objects/          # Value Objects (IndicadorRiesgo, Enums)
│   │   └── exceptions/             # Excepciones de dominio
│   ├── application/                # Capa de Aplicación
│   │   └── services/               # Servicios (casos de uso)
│   ├── infrastructure/             # Capa de Infraestructura
│   │   ├── database/               # Gestión de BD
│   │   └── repositories/           # Repositorios (SQLite)
│   └── presentation/               # Capa de Presentación
│       └── api/                    # API FastAPI
│           ├── routers/            # Endpoints
│           └── schemas/            # Schemas Pydantic
├── scripts/                        # Scripts de utilidad
│   ├── init_db.py                  # Inicializar BD
│   └── seed_data.py                # Cargar datos de ejemplo
├── tests/                          # Tests
├── requirements.txt                # Dependencias
└── README.md                       # Este archivo
```

## 🎯 Decisiones de Diseño

### 1. Arquitectura por Capas

- **Domain**: Lógica de negocio pura, independiente de frameworks
- **Application**: Casos de uso, orquestación
- **Infrastructure**: Persistencia, acceso a datos
- **Presentation**: API HTTP, validación de entrada

### 2. Patrón Repository

- Abstrae el acceso a datos
- Permite cambiar de SQLite a PostgreSQL sin tocar lógica de negocio
- Facilita testing con repositorios mock

### 3. Inversión de Dependencias

- Servicios dependen de interfaces, no de implementaciones
- Inyección de dependencias con FastAPI
- Bajo acoplamiento entre capas

### 4. Validación en Múltiples Capas

- **Pydantic**: Validación de entrada HTTP
- **Entidades**: Validación de reglas de dominio
- **Servicios**: Validación de reglas de negocio que requieren BD

## 🔮 Roadmap

### Fase 1: MVP Core ✅ (Completado)
- ✅ Arquitectura por capas
- ✅ CRUD de alumnos
- ✅ API con FastAPI
- ✅ Persistencia con SQLite

### Fase 2: Funcionalidades Completas (En progreso)
- ⏳ CRUD de cursos, clases, asistencias, participaciones, TPs
- ⏳ Cálculo de indicadores de riesgo
- ⏳ Generación de alertas

### Fase 3: Autenticación y Roles
- 🔮 Sistema de login con JWT
- 🔮 Roles: Docente, Coordinación, Estudiante
- 🔮 Permisos por rol (RBAC)

### Fase 4: Frontend Web
- 🔮 Interfaz web con React/Vue
- 🔮 Dashboard de coordinación
- 🔮 Portal de estudiantes

### Fase 5: Funcionalidades Avanzadas
- 🔮 Notificaciones automáticas
- 🔮 Reportes y gráficos
- 🔮 Predicción de riesgo con ML

### Fase 6: Migración a PostgreSQL
- 🔮 Cambio de SQLite a PostgreSQL
- 🔮 Despliegue en servidor dedicado

## 🤝 Contribuciones

Este proyecto es de código abierto y está diseñado con fines educativos. Las contribuciones son bienvenidas.

## 📄 Licencia

MIT License (pendiente de definir)

## 👥 Contacto

**Equipo de Desarrollo**
- Email: dev@seguimiento-alumnos.edu

---

**Última actualización**: 2025-12-07  
**Versión**: 1.0.0
