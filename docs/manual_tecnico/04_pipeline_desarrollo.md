# Capítulo 4: Pipeline de Desarrollo

## 4.1 ¿Qué es un Pipeline de Desarrollo?

Un **pipeline** es una secuencia ordenada de pasos para construir software. Como una línea de producción en una fábrica, cada paso debe completarse antes de pasar al siguiente.

### ¿Por qué es importante?

Sin pipeline:
```
❌ Empezar a codear sin planificar
❌ Agregar funcionalidades al azar
❌ Olvidar documentación
❌ Deploy caótico con errores
```

Con pipeline:
```
✅ Planificación clara
✅ Desarrollo ordenado
✅ Documentación incluida
✅ Deploy controlado
```

## 4.2 Pipeline General del Proyecto

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE DESARROLLO                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1: DISEÑO                                                │
│  ────────────────                                               │
│  • Análisis de requisitos                                       │
│  • Diseño de arquitectura                                       │
│  • Diseño de base de datos                                      │
│  • Diseño de API                                                │
│  • Diseño de UI/UX                                              │
│                                                                 │
│                           ▼                                     │
│                                                                 │
│  FASE 2: SETUP                                                  │
│  ─────────────                                                  │
│  • Crear repositorio Git                                        │
│  • Configurar entorno Python                                    │
│  • Instalar dependencias                                        │
│  • Configurar base de datos                                     │
│  • Estructura de carpetas                                       │
│                                                                 │
│                           ▼                                     │
│                                                                 │
│  FASE 3: BACKEND MVP                                            │
│  ───────────────────                                            │
│  • Capa de Dominio (entidades)                                  │
│  • Capa de Infraestructura (repositorios)                       │
│  • Capa de Aplicación (servicios)                               │
│  • Capa de Presentación (routers)                               │
│                                                                 │
│                           ▼                                     │
│                                                                 │
│  FASE 4: FRONTEND MVP                                           │
│  ────────────────────                                           │
│  • Estructura HTML                                              │
│  • Estilos CSS                                                  │
│  • JavaScript básico                                            │
│  • Conexión con API                                             │
│                                                                 │
│                           ▼                                     │
│                                                                 │
│  FASE 5: INTEGRACIÓN                                            │
│  ───────────────────                                            │
│  • Conectar frontend con backend                                │
│  • Pruebas manuales                                             │
│  • Corrección de bugs                                           │
│                                                                 │
│                           ▼                                     │
│                                                                 │
│  FASE 6: FUNCIONALIDADES COMPLETAS                              │
│  ─────────────────────────────────                              │
│  • Agregar todas las entidades                                  │
│  • Completar todos los endpoints                                │
│  • Completar todas las vistas                                   │
│                                                                 │
│                           ▼                                     │
│                                                                 │
│  FASE 7: PRUEBAS                                                │
│  ───────────────                                                │
│  • Pruebas unitarias                                            │
│  • Pruebas de integración                                       │
│  • Pruebas end-to-end                                           │
│                                                                 │
│                           ▼                                     │
│                                                                 │
│  FASE 8: DEPLOY                                                 │
│  ─────────────                                                  │
│  • Configurar Vercel                                            │
│  • Configurar Neon                                              │
│  • Variables de entorno                                         │
│  • Deploy producción                                            │
│                                                                 │
│                           ▼                                     │
│                                                                 │
│  FASE 9: DOCUMENTACIÓN                                          │
│  ─────────────────────                                          │
│  • README final                                                 │
│  • Documentación de API                                         │
│  • Manual de usuario                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 4.3 Pipeline del Backend (Detallado)

### Fase 1: Diseño del Backend

| Tarea | Entregable | Tiempo Estimado |
|-------|------------|-----------------|
| Definir endpoints | Lista de URLs y métodos | 2 horas |
| Diseñar modelos | Diagrama de entidades | 2 horas |
| Diseñar responses | Ejemplos JSON | 1 hora |
| Definir validaciones | Lista de reglas | 1 hora |
| Diseñar errores | Códigos y mensajes | 1 hora |

**Entregable final:** Documento de diseño de API

### Fase 2: Implementación por Capas

Orden estricto de implementación:

```
1. DOMINIO (src/domain/)
   │
   ├── entities/
   │   ├── alumno.py          ← Primero
   │   ├── curso.py
   │   ├── inscripcion.py
   │   ├── clase.py
   │   ├── asistencia.py
   │   └── trabajo_practico.py
   │
   └── exceptions/
       └── domain_exceptions.py
   
2. INFRAESTRUCTURA (src/infrastructure/)
   │
   ├── database/
   │   ├── connection.py      ← Conexión a PostgreSQL
   │   └── postgres_schema.py ← SQL de creación
   │
   └── repositories/
       ├── base/              ← Interfaces abstractas
       └── postgres/          ← Implementaciones reales

3. APLICACIÓN (src/application/)
   │
   └── services/
       ├── alumno_service.py
       ├── curso_service.py
       └── ...

4. PRESENTACIÓN (src/presentation/)
   │
   └── api/
       ├── main.py            ← App FastAPI
       ├── routers/           ← Endpoints
       └── schemas/           ← Pydantic DTOs
```

### Fase 3: Pruebas del Backend

```python
# tests/test_alumno_service.py

def test_crear_alumno():
    """Verifica que se puede crear un alumno válido"""
    service = AlumnoService(mock_repo)
    alumno = service.crear_alumno(
        nombre="Juan",
        apellido="Pérez",
        dni="12345678",
        email="juan@test.com",
        cohorte=2024
    )
    assert alumno.nombre == "Juan"
    assert alumno.dni == "12345678"

def test_crear_alumno_dni_duplicado():
    """Verifica que no se pueden crear 2 alumnos con mismo DNI"""
    # ... test de error
```

### Fase 4: Documentación del Backend

FastAPI genera documentación automática:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 4.4 Pipeline del Frontend (Detallado)

### Fase 1: Diseño del Frontend

| Tarea | Entregable |
|-------|------------|
| Wireframes | Bocetos de cada página |
| Componentes | Lista de elementos reutilizables |
| Flujo de usuario | Diagrama de navegación |
| Paleta de colores | Variables CSS |

### Fase 2: Implementación

```
1. ESTRUCTURA HTML
   │
   ├── public/
   │   ├── index.html         ← Layout principal
   │   ├── components/        ← Fragmentos HTML
   │   │   ├── header.html
   │   │   ├── footer.html
   │   │   └── modals/
   │   │       ├── alumno.html
   │   │       └── curso.html
   │
2. ESTILOS CSS
   │
   ├── styles.css             ← Estilos globales
   │   ├── Variables CSS
   │   ├── Reset/Normalize
   │   ├── Layout (header, main, footer)
   │   ├── Componentes (cards, buttons, forms)
   │   └── Utilities (helpers)
   │
3. LÓGICA JAVASCRIPT
   │
   └── app.js
       ├── Estado global (state)
       ├── Inicialización
       ├── Navegación
       ├── Llamadas a API (fetch)
       ├── Renderizado
       └── Event handlers
```

### Fase 3: Conexión con API

```javascript
// Patrón para todas las llamadas API

// 1. Definir URL base
const API_URL = '/api';

// 2. Función genérica de fetch
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`Error en ${endpoint}:`, error);
        throw error;
    }
}

// 3. Uso específico
async function cargarAlumnos() {
    const data = await fetchAPI('/alumnos/');
    return data.alumnos;
}
```

## 4.5 Pipeline de Integración

### Checklist de Integración

```
□ Frontend puede hacer GET a todos los endpoints
□ Frontend puede hacer POST a todos los endpoints
□ Frontend puede hacer PUT a todos los endpoints
□ Frontend puede hacer DELETE a todos los endpoints
□ Errores del backend se muestran correctamente
□ Loading states funcionan
□ Toast notifications funcionan
□ Navegación funciona sin recargar página
```

### Pruebas End-to-End

| Flujo | Pasos | Resultado Esperado |
|-------|-------|-------------------|
| Crear alumno | 1. Ir a Admin 2. Click Nuevo Alumno 3. Llenar form 4. Guardar | Alumno aparece en lista |
| Registrar asistencia | 1. Ir a Registro 2. Seleccionar curso 3. Crear clase 4. Marcar presente | Asistencia guardada |
| Ver historial | 1. Ir a Alumnos 2. Click en alumno 3. Ver ficha | Datos correctos |

## 4.6 Pipeline de Deploy

### Configuración de Vercel

```
1. CONECTAR REPOSITORIO
   │
   ├── Ir a vercel.com
   ├── Importar proyecto de GitHub
   └── Seleccionar repositorio
   
2. CONFIGURAR BUILD
   │
   ├── Framework: Other
   ├── Build Command: (vacío o python build.py)
   ├── Output Directory: public
   └── Install Command: pip install -r requirements.txt
   
3. VARIABLES DE ENTORNO
   │
   ├── POSTGRES_URL = (URL de Neon)
   └── VERCEL = 1
   
4. DEPLOY
   │
   ├── Click en Deploy
   └── Esperar ~2 minutos
```

### Configuración de Neon

```
1. Crear cuenta en neon.tech
2. Crear nuevo proyecto
3. Copiar connection string
4. Pegar en variables de Vercel
5. Ejecutar /api/setup para crear tablas
```

## 4.7 Cronograma Sugerido

### Para un desarrollador trabajando solo

| Fase | Duración | Días |
|------|----------|------|
| Diseño | 1 semana | Día 1-5 |
| Setup | 1 día | Día 6 |
| Backend MVP | 1 semana | Día 7-12 |
| Frontend MVP | 1 semana | Día 13-18 |
| Integración | 3 días | Día 19-21 |
| Funcionalidades completas | 1 semana | Día 22-28 |
| Pruebas y bugs | 3 días | Día 29-31 |
| Deploy | 1 día | Día 32 |
| Documentación | 2 días | Día 33-34 |

**Total: ~5 semanas trabajando medio tiempo**

### Hitos Clave

```
Semana 1: Diseño completo ✓
Semana 2: Backend funcionando (probado con Swagger) ✓
Semana 3: Frontend conectado a API ✓
Semana 4: Todas las funcionalidades ✓
Semana 5: Pruebas, deploy, docs ✓
```

## 4.8 Control de Versiones (Git)

### Flujo de trabajo

```
main ─────●─────●─────●─────●─────●─────
          │     │     │     │     │
          │     │     │     │     └── v1.0.0 (release)
          │     │     │     │
          │     │     │     └── merge feature/tps
          │     │     │
          │     │     └── merge feature/asistencia
          │     │
          │     └── merge feature/alumnos
          │
          └── Initial commit
```

### Commits Significativos

```bash
# Estructura inicial
git commit -m "feat: setup inicial del proyecto"

# Por cada entidad
git commit -m "feat(domain): agregar entidad Alumno"
git commit -m "feat(infra): agregar repositorio Alumno"
git commit -m "feat(app): agregar servicio Alumno"
git commit -m "feat(api): agregar endpoints de Alumno"

# Frontend
git commit -m "feat(frontend): agregar página Dashboard"
git commit -m "feat(frontend): agregar registro de asistencia"

# Deploy
git commit -m "chore: configurar Vercel"
git commit -m "docs: agregar README"
```

### Convención de Commits

```
<tipo>(<alcance>): <descripción>

Tipos:
- feat: Nueva funcionalidad
- fix: Corrección de bug
- docs: Documentación
- style: Formato (no afecta código)
- refactor: Refactorización
- test: Agregar tests
- chore: Tareas de mantenimiento
```

---

**Capítulo anterior**: [Diseño y Arquitectura](./03_diseno_arquitectura.md)

**Siguiente capítulo**: [Estructura de Carpetas](./05_estructura_carpetas.md)
