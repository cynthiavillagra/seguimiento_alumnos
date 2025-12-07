# 🏗️ Arquitectura del Sistema

Documentación técnica de la arquitectura del Sistema de Seguimiento de Alumnos.

## 📊 Visión General

### Stack Tecnológico

```
┌─────────────────────────────────────────┐
│           FRONTEND (SPA)                │
│  HTML5 + CSS3 + Vanilla JavaScript      │
│  - index.html (estructura)              │
│  - app.js (lógica)                      │
│  - styles.css (diseño)                  │
└─────────────────────────────────────────┘
                    ↓ HTTP/JSON
┌─────────────────────────────────────────┐
│      VERCEL (Hosting + Routing)         │
│  - Archivos estáticos (public/)         │
│  - Serverless Functions (api/)          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│        BACKEND (Python 3.12)            │
│  - api/index.py (API REST)              │
│  - api/db.py (conexión BD)              │
└─────────────────────────────────────────┘
                    ↓ SQL
┌─────────────────────────────────────────┐
│    BASE DE DATOS (PostgreSQL)           │
│  Neon Database (Serverless Postgres)    │
│  - 9 tablas principales                 │
│  - 2 vistas de resumen                  │
└─────────────────────────────────────────┘
```

---

## 🗄️ Modelo de Datos

### Tablas Principales

#### 1. **alumno**
Información de estudiantes.

```sql
CREATE TABLE alumno (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    cohorte INTEGER NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Índices:**
- `idx_alumno_dni` (dni)
- `idx_alumno_cohorte` (cohorte)
- `idx_alumno_apellido` (apellido)

---

#### 2. **curso**
Materias dictadas en un período.

```sql
CREATE TABLE curso (
    id SERIAL PRIMARY KEY,
    nombre_materia VARCHAR(200) NOT NULL,
    anio INTEGER NOT NULL,
    cuatrimestre INTEGER NOT NULL,
    docente_responsable VARCHAR(200) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

#### 3. **inscripcion**
Relación alumno-curso.

```sql
CREATE TABLE inscripcion (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alumno_id) REFERENCES alumno(id),
    FOREIGN KEY (curso_id) REFERENCES curso(id),
    UNIQUE(alumno_id, curso_id)
);
```

---

#### 4. **clase**
Sesiones de cursada.

```sql
CREATE TABLE clase (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    numero_clase INTEGER NOT NULL,
    tema TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (curso_id) REFERENCES curso(id),
    UNIQUE(curso_id, numero_clase)
);
```

---

#### 5. **registro_asistencia**
Asistencia por clase.

```sql
CREATE TABLE registro_asistencia (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alumno_id) REFERENCES alumno(id),
    FOREIGN KEY (clase_id) REFERENCES clase(id),
    CHECK (estado IN ('Presente', 'Ausente', 'Tardanza', 'Justificada')),
    UNIQUE(alumno_id, clase_id)
);
```

---

#### 6. **registro_participacion**
Participación en clase.

```sql
CREATE TABLE registro_participacion (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    nivel VARCHAR(20) NOT NULL,
    comentario TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alumno_id) REFERENCES alumno(id),
    FOREIGN KEY (clase_id) REFERENCES clase(id),
    CHECK (nivel IN ('Ninguna', 'Baja', 'Media', 'Alta'))
);
```

---

#### 7. **trabajo_practico**
TPs asignados.

```sql
CREATE TABLE trabajo_practico (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_entrega DATE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (curso_id) REFERENCES curso(id)
);
```

---

#### 8. **entrega_tp**
Entregas de TPs por alumno.

```sql
CREATE TABLE entrega_tp (
    id SERIAL PRIMARY KEY,
    trabajo_practico_id INTEGER NOT NULL,
    alumno_id INTEGER NOT NULL,
    fecha_entrega_real DATE,
    entregado BOOLEAN NOT NULL DEFAULT FALSE,
    nota DECIMAL(4,2),
    es_tardia BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trabajo_practico_id) REFERENCES trabajo_practico(id),
    FOREIGN KEY (alumno_id) REFERENCES alumno(id),
    CHECK (nota IS NULL OR (nota >= 1 AND nota <= 10)),
    UNIQUE(trabajo_practico_id, alumno_id)
);
```

---

#### 9. **registro_actitud**
Actitud en clase.

```sql
CREATE TABLE registro_actitud (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    actitud VARCHAR(20) NOT NULL,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alumno_id) REFERENCES alumno(id),
    FOREIGN KEY (clase_id) REFERENCES clase(id),
    CHECK (actitud IN ('Excelente', 'Buena', 'Regular', 'Mala'))
);
```

---

### Vistas

#### vista_resumen_asistencias
Estadísticas de asistencia por alumno y curso.

```sql
CREATE VIEW vista_resumen_asistencias AS
SELECT 
    ra.alumno_id,
    cl.curso_id,
    COUNT(*) AS total_registros,
    SUM(CASE WHEN ra.estado = 'Presente' THEN 1 ELSE 0 END) AS presentes,
    SUM(CASE WHEN ra.estado = 'Ausente' THEN 1 ELSE 0 END) AS ausentes,
    ROUND(
        (SUM(CASE WHEN ra.estado IN ('Presente', 'Tardanza', 'Justificada') 
             THEN 1 ELSE 0 END)::NUMERIC * 100.0) / COUNT(*),
        2
    ) AS porcentaje_asistencia
FROM registro_asistencia ra
JOIN clase cl ON ra.clase_id = cl.id
GROUP BY ra.alumno_id, cl.curso_id;
```

#### vista_resumen_tps
Estadísticas de TPs por alumno y curso.

```sql
CREATE VIEW vista_resumen_tps AS
SELECT 
    et.alumno_id,
    tp.curso_id,
    COUNT(*) AS total_tps,
    SUM(CASE WHEN et.entregado = TRUE THEN 1 ELSE 0 END) AS tps_entregados,
    ROUND(AVG(et.nota), 2) AS promedio_notas
FROM entrega_tp et
JOIN trabajo_practico tp ON et.trabajo_practico_id = tp.id
GROUP BY et.alumno_id, tp.curso_id;
```

---

## 🔌 API REST

### Endpoints Implementados

#### GET /health
Health check del sistema.

**Response:**
```json
{
  "status": "ok",
  "message": "Working!"
}
```

---

#### GET /cursos (o /clases)
Lista todos los cursos con estadísticas.

**Response:**
```json
{
  "total": 3,
  "clases": [
    {
      "id": 1,
      "materia": "Programación I",
      "cohorte": 2024,
      "cuatrimestre": 2,
      "docente": "Prof. García",
      "totalAlumnos": 8,
      "asistenciaPromedio": 85,
      "alumnosEnRiesgo": 2,
      "totalClases": 15,
      "ultimaClase": "2024-12-07"
    }
  ]
}
```

---

#### GET /alumnos
Lista todos los alumnos.

**Response:**
```json
{
  "total": 8,
  "alumnos": [
    {
      "id": 1,
      "nombre": "Juan",
      "apellido": "Pérez",
      "nombre_completo": "Pérez, Juan",
      "dni": "12345678",
      "email": "juan@example.com",
      "cohorte": 2024
    }
  ]
}
```

---

#### GET /alertas
Alertas de alumnos en riesgo.

**Response:**
```json
{
  "total": 2,
  "alertas": [
    {
      "tipo": "faltas_consecutivas",
      "nivel": "alto",
      "alumno": {
        "id": 2,
        "nombre": "García, Ana"
      },
      "curso": {
        "id": 1,
        "materia": "Programación I"
      },
      "mensaje": "2 faltas consecutivas (05/12 y 07/12)"
    }
  ]
}
```

---

## 🎨 Frontend (SPA)

### Estructura de Archivos

```
public/
├── index.html          # Estructura HTML
├── app.js              # Lógica JavaScript
└── styles.css          # Estilos CSS
```

### Componentes JavaScript

#### Estado Global
```javascript
const state = {
    currentPage: 'dashboard',
    clases: [],
    claseSeleccionada: null,
    alumnos: [],
    claseActual: {
        materia: '',
        cohorte: '',
        fecha: '',
        tema: '',
        registros: {}
    }
};
```

#### Navegación
```javascript
function showPage(pageId)
function loadDashboardData()
function loadAlumnos()
```

#### Registro de Clase
```javascript
function iniciarRegistroClase()
function marcarAsistencia(alumnoId, estado)
function marcarParticipacion(alumnoId, nivel)
function marcarTPEntregado(alumnoId, entregado)
function guardarNotaTP(alumnoId, nota)
function marcarActitud(alumnoId, actitud)
function guardarClase()
```

---

## 🚀 Despliegue

### Vercel

**Configuración (`vercel.json`):**
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
      "src": "/(alumnos|clases|cursos|health|alertas).*",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*\\.(css|js|png|jpg|svg|ico))",
      "dest": "/public/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/public/index.html"
    }
  ]
}
```

### Variables de Entorno

Configuradas automáticamente por Neon:
- `DATABASE_URL` - Connection string de PostgreSQL

---

## 🔒 Seguridad

### CORS
Configurado en la API para permitir requests desde cualquier origen.

### Validaciones
- Checks en base de datos (constraints)
- Validación de notas (1-10)
- Validación de estados (enums)

---

## 📈 Escalabilidad

### Actual
- Serverless Functions (escala automáticamente)
- PostgreSQL serverless (Neon)
- Archivos estáticos en CDN (Vercel)

### Futuro
- Cache de queries frecuentes
- Paginación en listados
- Índices adicionales según uso

---

**Para más detalles técnicos, consulta el código fuente en `/api` y `/public`.**
