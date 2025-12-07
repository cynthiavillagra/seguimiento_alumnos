"""
Script de Migración: SQLite → PostgreSQL
Convierte el schema y crea las tablas en Vercel Postgres
"""

import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env.local')

# Schema PostgreSQL (convertido desde SQLite)
POSTGRES_SCHEMA = """
-- ============================================================================
-- TABLA: alumno
-- ============================================================================
CREATE TABLE IF NOT EXISTS alumno (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    cohorte INTEGER NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (LENGTH(nombre) > 0),
    CHECK (LENGTH(apellido) > 0),
    CHECK (LENGTH(dni) > 0),
    CHECK (email LIKE '%@%'),
    CHECK (cohorte >= 2000 AND cohorte <= 2100)
);

CREATE INDEX IF NOT EXISTS idx_alumno_dni ON alumno(dni);
CREATE INDEX IF NOT EXISTS idx_alumno_cohorte ON alumno(cohorte);
CREATE INDEX IF NOT EXISTS idx_alumno_apellido ON alumno(apellido);

-- ============================================================================
-- TABLA: curso
-- ============================================================================
CREATE TABLE IF NOT EXISTS curso (
    id SERIAL PRIMARY KEY,
    nombre_materia VARCHAR(200) NOT NULL,
    anio INTEGER NOT NULL,
    cuatrimestre INTEGER NOT NULL,
    docente_responsable VARCHAR(200) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (LENGTH(nombre_materia) > 0),
    CHECK (anio >= 2000 AND anio <= 2100),
    CHECK (cuatrimestre IN (1, 2)),
    CHECK (LENGTH(docente_responsable) > 0)
);

CREATE INDEX IF NOT EXISTS idx_curso_anio_cuatrimestre ON curso(anio, cuatrimestre);
CREATE INDEX IF NOT EXISTS idx_curso_materia ON curso(nombre_materia);

-- ============================================================================
-- TABLA: inscripcion
-- ============================================================================
CREATE TABLE IF NOT EXISTS inscripcion (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES curso(id) ON DELETE CASCADE,
    
    UNIQUE(alumno_id, curso_id)
);

CREATE INDEX IF NOT EXISTS idx_inscripcion_alumno ON inscripcion(alumno_id);
CREATE INDEX IF NOT EXISTS idx_inscripcion_curso ON inscripcion(curso_id);

-- ============================================================================
-- TABLA: clase
-- ============================================================================
CREATE TABLE IF NOT EXISTS clase (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    numero_clase INTEGER NOT NULL,
    tema TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (curso_id) REFERENCES curso(id) ON DELETE CASCADE,
    
    CHECK (numero_clase > 0),
    
    UNIQUE(curso_id, numero_clase)
);

CREATE INDEX IF NOT EXISTS idx_clase_curso ON clase(curso_id);
CREATE INDEX IF NOT EXISTS idx_clase_fecha ON clase(fecha);

-- ============================================================================
-- TABLA: registro_asistencia
-- ============================================================================
CREATE TABLE IF NOT EXISTS registro_asistencia (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    FOREIGN KEY (clase_id) REFERENCES clase(id) ON DELETE CASCADE,
    
    CHECK (estado IN ('Presente', 'Ausente', 'Tardanza', 'Justificada')),
    
    UNIQUE(alumno_id, clase_id)
);

CREATE INDEX IF NOT EXISTS idx_asistencia_alumno ON registro_asistencia(alumno_id);
CREATE INDEX IF NOT EXISTS idx_asistencia_clase ON registro_asistencia(clase_id);
CREATE INDEX IF NOT EXISTS idx_asistencia_estado ON registro_asistencia(estado);

-- ============================================================================
-- TABLA: registro_participacion
-- ============================================================================
CREATE TABLE IF NOT EXISTS registro_participacion (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    nivel VARCHAR(20) NOT NULL,
    comentario TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    FOREIGN KEY (clase_id) REFERENCES clase(id) ON DELETE CASCADE,
    
    CHECK (nivel IN ('Ninguna', 'Baja', 'Media', 'Alta'))
);

CREATE INDEX IF NOT EXISTS idx_participacion_alumno ON registro_participacion(alumno_id);
CREATE INDEX IF NOT EXISTS idx_participacion_clase ON registro_participacion(clase_id);
CREATE INDEX IF NOT EXISTS idx_participacion_nivel ON registro_participacion(nivel);

-- ============================================================================
-- TABLA: trabajo_practico
-- ============================================================================
CREATE TABLE IF NOT EXISTS trabajo_practico (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_entrega DATE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (curso_id) REFERENCES curso(id) ON DELETE CASCADE,
    
    CHECK (LENGTH(titulo) > 0)
);

CREATE INDEX IF NOT EXISTS idx_tp_curso ON trabajo_practico(curso_id);
CREATE INDEX IF NOT EXISTS idx_tp_fecha_entrega ON trabajo_practico(fecha_entrega);

-- ============================================================================
-- TABLA: entrega_tp
-- ============================================================================
CREATE TABLE IF NOT EXISTS entrega_tp (
    id SERIAL PRIMARY KEY,
    trabajo_practico_id INTEGER NOT NULL,
    alumno_id INTEGER NOT NULL,
    fecha_entrega_real DATE,
    entregado BOOLEAN NOT NULL DEFAULT FALSE,
    nota DECIMAL(4,2),
    es_tardia BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (trabajo_practico_id) REFERENCES trabajo_practico(id) ON DELETE CASCADE,
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    
    CHECK (nota IS NULL OR (nota >= 1 AND nota <= 10)),
    
    UNIQUE(trabajo_practico_id, alumno_id)
);

CREATE INDEX IF NOT EXISTS idx_entrega_tp ON entrega_tp(trabajo_practico_id);
CREATE INDEX IF NOT EXISTS idx_entrega_alumno ON entrega_tp(alumno_id);
CREATE INDEX IF NOT EXISTS idx_entrega_estado ON entrega_tp(entregado);

-- ============================================================================
-- TABLA: registro_actitud
-- ============================================================================
CREATE TABLE IF NOT EXISTS registro_actitud (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    actitud VARCHAR(20) NOT NULL,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    FOREIGN KEY (clase_id) REFERENCES clase(id) ON DELETE CASCADE,
    
    CHECK (actitud IN ('Excelente', 'Buena', 'Regular', 'Mala'))
);

CREATE INDEX IF NOT EXISTS idx_actitud_alumno ON registro_actitud(alumno_id);
CREATE INDEX IF NOT EXISTS idx_actitud_clase ON registro_actitud(clase_id);

-- ============================================================================
-- VISTAS
-- ============================================================================

-- Vista: Resumen de asistencias por alumno y curso
CREATE OR REPLACE VIEW vista_resumen_asistencias AS
SELECT 
    ra.alumno_id,
    cl.curso_id,
    COUNT(*) AS total_registros,
    SUM(CASE WHEN ra.estado = 'Presente' THEN 1 ELSE 0 END) AS presentes,
    SUM(CASE WHEN ra.estado = 'Ausente' THEN 1 ELSE 0 END) AS ausentes,
    SUM(CASE WHEN ra.estado = 'Tardanza' THEN 1 ELSE 0 END) AS tardanzas,
    SUM(CASE WHEN ra.estado = 'Justificada' THEN 1 ELSE 0 END) AS justificadas,
    ROUND(
        (SUM(CASE WHEN ra.estado IN ('Presente', 'Tardanza', 'Justificada') THEN 1 ELSE 0 END)::NUMERIC * 100.0) / COUNT(*),
        2
    ) AS porcentaje_asistencia
FROM registro_asistencia ra
JOIN clase cl ON ra.clase_id = cl.id
GROUP BY ra.alumno_id, cl.curso_id;

-- Vista: Resumen de TPs por alumno y curso
CREATE OR REPLACE VIEW vista_resumen_tps AS
SELECT 
    et.alumno_id,
    tp.curso_id,
    COUNT(*) AS total_tps,
    SUM(CASE WHEN et.entregado = TRUE THEN 1 ELSE 0 END) AS tps_entregados,
    SUM(CASE WHEN et.entregado = FALSE THEN 1 ELSE 0 END) AS tps_no_entregados,
    SUM(CASE WHEN et.es_tardia = TRUE THEN 1 ELSE 0 END) AS tps_tardios,
    ROUND(
        (SUM(CASE WHEN et.entregado = TRUE THEN 1 ELSE 0 END)::NUMERIC * 100.0) / COUNT(*),
        2
    ) AS porcentaje_entregados,
    ROUND(AVG(et.nota), 2) AS promedio_notas
FROM entrega_tp et
JOIN trabajo_practico tp ON et.trabajo_practico_id = tp.id
GROUP BY et.alumno_id, tp.curso_id;
"""

# Datos iniciales
SEED_DATA = """
-- Insertar cursos
INSERT INTO curso (nombre_materia, anio, cuatrimestre, docente_responsable) VALUES
('Programación I', 2024, 2, 'Prof. García'),
('Matemática', 2024, 2, 'Prof. Rodríguez'),
('Física', 2023, 2, 'Prof. López')
ON CONFLICT DO NOTHING;

-- Insertar alumnos
INSERT INTO alumno (nombre, apellido, dni, email, cohorte) VALUES
('Juan', 'Pérez', '12345678', 'juan.perez@example.com', 2024),
('Ana', 'García', '23456789', 'ana.garcia@example.com', 2024),
('Carlos', 'López', '34567890', 'carlos.lopez@example.com', 2024),
('María', 'Rodríguez', '45678901', 'maria.rodriguez@example.com', 2024),
('Pedro', 'Fernández', '56789012', 'pedro.fernandez@example.com', 2024),
('Laura', 'González', '67890123', 'laura.gonzalez@example.com', 2024),
('Diego', 'Sánchez', '78901234', 'diego.sanchez@example.com', 2024),
('Sofía', 'Pérez', '89012345', 'sofia.perez@example.com', 2024)
ON CONFLICT (dni) DO NOTHING;

-- Inscribir alumnos a cursos
INSERT INTO inscripcion (alumno_id, curso_id)
SELECT a.id, c.id
FROM alumno a
CROSS JOIN curso c
WHERE a.cohorte = 2024 AND c.anio = 2024
ON CONFLICT DO NOTHING;

-- Insertar TPs
INSERT INTO trabajo_practico (curso_id, titulo, descripcion, fecha_entrega)
SELECT id, 'TP1 - Variables y Tipos', 'Ejercicios de práctica sobre variables y tipos de datos', '2024-12-15'
FROM curso WHERE nombre_materia = 'Programación I'
ON CONFLICT DO NOTHING;

INSERT INTO trabajo_practico (curso_id, titulo, descripcion, fecha_entrega)
SELECT id, 'TP2 - Funciones', 'Implementar funciones básicas en Python', '2024-12-22'
FROM curso WHERE nombre_materia = 'Programación I'
ON CONFLICT DO NOTHING;
"""

def migrate():
    """Ejecuta la migración a PostgreSQL"""
    
    # Obtener URL de conexión
    postgres_url = os.getenv('POSTGRES_URL')
    
    if not postgres_url:
        print("❌ Error: No se encontró POSTGRES_URL en .env.local")
        print("Ejecuta: vercel env pull .env.local")
        return
    
    print("🔄 Conectando a PostgreSQL...")
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(postgres_url)
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa")
        print("📝 Creando tablas...")
        
        # Ejecutar schema
        cursor.execute(POSTGRES_SCHEMA)
        conn.commit()
        
        print("✅ Tablas creadas")
        print("🌱 Insertando datos iniciales...")
        
        # Insertar datos
        cursor.execute(SEED_DATA)
        conn.commit()
        
        print("✅ Datos insertados")
        
        # Verificar
        cursor.execute("SELECT COUNT(*) FROM alumno")
        count_alumnos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM curso")
        count_cursos = cursor.fetchone()[0]
        
        print(f"\n📊 Resumen:")
        print(f"   - Alumnos: {count_alumnos}")
        print(f"   - Cursos: {count_cursos}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 ¡Migración completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        raise

if __name__ == '__main__':
    migrate()
