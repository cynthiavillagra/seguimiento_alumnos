# 🔌 Plan de Conexión a Base de Datos Real

## 📊 Estado Actual

### ✅ Lo que YA tienes
- Schema SQL completo (`schema.sql`) con 11 tablas
- Entidades de dominio (Alumno, Curso, RegistroAsistencia)
- Repositorios SQLite implementados
- Frontend funcional

### ❌ Lo que FALTA
- Conectar la API de Vercel a la base de datos
- Inicializar la BD con datos reales
- Implementar lógica de alertas automáticas
- Endpoints para TPs con metadata

## 🎯 Funcionalidades Requeridas

### 1. Materias con Cohortes
**Tabla**: `curso`
```sql
CREATE TABLE curso (
    id INTEGER PRIMARY KEY,
    nombre_materia TEXT NOT NULL,
    anio INTEGER NOT NULL,
    cuatrimestre INTEGER NOT NULL,
    docente_responsable TEXT NOT NULL
);
```

**Endpoint necesario**: `GET /cursos`
```json
{
  "cursos": [
    {
      "id": 1,
      "materia": "Programación I",
      "anio": 2024,
      "cuatrimestre": 1,
      "docente": "Prof. García",
      "totalAlumnos": 30,
      "asistenciaPromedio": 85
    }
  ]
}
```

### 2. Alumnos por Cohorte
**Tabla**: `alumno` + `inscripcion`
```sql
SELECT a.*, c.nombre_materia
FROM alumno a
JOIN inscripcion i ON a.id = i.alumno_id
JOIN curso c ON i.curso_id = c.id
WHERE c.id = ?
```

**Endpoint necesario**: `GET /cursos/{id}/alumnos`

### 3. TPs con Metadata
**Tabla**: `trabajo_practico` + `entrega_tp`
```sql
CREATE TABLE trabajo_practico (
    id INTEGER PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    fecha_entrega DATE NOT NULL
);

CREATE TABLE entrega_tp (
    id INTEGER PRIMARY KEY,
    trabajo_practico_id INTEGER NOT NULL,
    alumno_id INTEGER NOT NULL,
    entregado BOOLEAN NOT NULL,
    fecha_entrega_real DATE,
    es_tardia BOOLEAN NOT NULL
);
```

**Endpoint necesario**: `GET /cursos/{id}/tps`
```json
{
  "tps": [
    {
      "id": 1,
      "titulo": "TP1 - Variables y Tipos",
      "descripcion": "Ejercicios de práctica...",
      "fechaEntrega": "2024-12-15",
      "entregados": 25,
      "noEntregados": 5
    }
  ]
}
```

### 4. Alertas Automáticas (2 Faltas Consecutivas)
**Lógica necesaria**:
```sql
-- Detectar 2 faltas consecutivas
WITH faltas_consecutivas AS (
    SELECT 
        ra.alumno_id,
        cl.curso_id,
        cl.fecha,
        ra.estado,
        LAG(ra.estado) OVER (
            PARTITION BY ra.alumno_id, cl.curso_id 
            ORDER BY cl.fecha
        ) AS estado_anterior
    FROM registro_asistencia ra
    JOIN clase cl ON ra.clase_id = cl.id
)
SELECT DISTINCT alumno_id, curso_id
FROM faltas_consecutivas
WHERE estado = 'Ausente' 
  AND estado_anterior = 'Ausente';
```

**Endpoint necesario**: `GET /alertas`
```json
{
  "alertas": [
    {
      "tipo": "faltas_consecutivas",
      "alumno": {
        "id": 1,
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

## 🚀 Plan de Implementación

### Fase 1: Migrar API a Base de Datos (CRÍTICO)
**Problema**: Vercel usa funciones serverless, la BD SQLite es efímera

**Opciones**:

#### Opción A: PostgreSQL en Vercel (RECOMENDADO)
```bash
# 1. Crear BD PostgreSQL en Vercel
vercel postgres create

# 2. Actualizar schema a PostgreSQL
# 3. Conectar API a Vercel Postgres
```

#### Opción B: SQLite con Turso (Alternativa)
```bash
# BD SQLite en la nube
turso db create seguimiento-alumnos
```

#### Opción C: Supabase (Más fácil)
```bash
# PostgreSQL + API REST automática
# Gratis hasta 500MB
```

### Fase 2: Actualizar API de Python
**Archivo**: `api/index.py`

Cambiar de:
```python
# Datos hardcodeados
clases_ejemplo = [...]
```

A:
```python
# Conexión a BD
import psycopg2  # o sqlite3

def get_clases():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.id,
            c.nombre_materia,
            c.anio,
            COUNT(DISTINCT i.alumno_id) as total_alumnos,
            AVG(vra.porcentaje_asistencia) as asistencia_promedio
        FROM curso c
        LEFT JOIN inscripcion i ON c.id = i.curso_id
        LEFT JOIN vista_resumen_asistencias vra 
            ON i.alumno_id = vra.alumno_id 
            AND c.id = vra.curso_id
        GROUP BY c.id
    """)
    return cursor.fetchall()
```

### Fase 3: Implementar Alertas
**Archivo**: `api/alertas.py` (nuevo)

```python
def detectar_faltas_consecutivas():
    """Detecta alumnos con 2 faltas consecutivas"""
    query = """
        WITH clases_ordenadas AS (
            SELECT 
                ra.alumno_id,
                cl.curso_id,
                cl.fecha,
                ra.estado,
                LAG(ra.estado, 1) OVER (
                    PARTITION BY ra.alumno_id, cl.curso_id 
                    ORDER BY cl.fecha
                ) AS estado_anterior,
                LAG(cl.fecha, 1) OVER (
                    PARTITION BY ra.alumno_id, cl.curso_id 
                    ORDER BY cl.fecha
                ) AS fecha_anterior
            FROM registro_asistencia ra
            JOIN clase cl ON ra.clase_id = cl.id
        )
        SELECT 
            alumno_id,
            curso_id,
            fecha_anterior,
            fecha
        FROM clases_ordenadas
        WHERE estado = 'Ausente' 
          AND estado_anterior = 'Ausente'
    """
    return ejecutar_query(query)
```

### Fase 4: Seed Data (Datos Iniciales)
**Archivo**: `scripts/seed_production.py`

```python
# Insertar datos reales
cursos = [
    ('Programación I', 2024, 1, 'Prof. García'),
    ('Matemática', 2024, 1, 'Prof. Rodríguez'),
    ('Física', 2023, 2, 'Prof. López')
]

alumnos = [
    ('Juan', 'Pérez', '12345678', 'juan@example.com', 2024),
    ('Ana', 'García', '23456789', 'ana@example.com', 2024),
    # ... más alumnos
]

tps = [
    (1, 'TP1 - Variables', 'Ejercicios...', '2024-12-15'),
    (1, 'TP2 - Funciones', 'Implementar...', '2024-12-22'),
]
```

## 📋 Checklist de Implementación

### Corto Plazo (1-2 días)
- [ ] Decidir BD (PostgreSQL/Turso/Supabase)
- [ ] Crear BD en producción
- [ ] Migrar schema SQL
- [ ] Conectar API a BD
- [ ] Cargar datos iniciales (seed)

### Mediano Plazo (3-5 días)
- [ ] Endpoint `/cursos` con datos reales
- [ ] Endpoint `/cursos/{id}/alumnos`
- [ ] Endpoint `/cursos/{id}/tps`
- [ ] Endpoint `/alertas` con lógica de faltas
- [ ] Guardar registro de clase en BD

### Largo Plazo (1-2 semanas)
- [ ] Dashboard con alertas en tiempo real
- [ ] Cálculo automático de indicadores
- [ ] Notificaciones por email
- [ ] Reportes y exportación

## 🎯 Recomendación Inmediata

### Opción 1: Vercel Postgres (Más Profesional)
```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Crear BD
vercel postgres create

# 3. Obtener connection string
vercel env pull

# 4. Actualizar api/index.py
import psycopg2
conn = psycopg2.connect(os.getenv('POSTGRES_URL'))
```

**Ventajas**:
- ✅ Integración nativa con Vercel
- ✅ Backups automáticos
- ✅ Escalable
- ✅ Gratis hasta 256MB

### Opción 2: Supabase (Más Rápido)
```bash
# 1. Crear cuenta en supabase.com
# 2. Crear proyecto
# 3. Copiar connection string
# 4. Pegar schema SQL en SQL Editor
```

**Ventajas**:
- ✅ Setup en 5 minutos
- ✅ UI para ver datos
- ✅ API REST automática
- ✅ Gratis hasta 500MB

## ❓ ¿Qué prefieres?

1. **Vercel Postgres** - Más integrado, profesional
2. **Supabase** - Más rápido, con UI
3. **Turso** - SQLite en la nube (compatible con código actual)

Dime cuál prefieres y te ayudo a implementarlo paso a paso.

---

**IMPORTANTE**: Mientras tanto, puedo hacer que la API use SQLite local para desarrollo, pero en Vercel se perderán los datos en cada deploy.
