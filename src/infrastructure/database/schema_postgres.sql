-- Schema de Base de Datos PostgreSQL
-- Sistema de Seguimiento de Alumnos
-- Versión: 1.0.0

-- ============================================================================
-- TABLA: alumno
-- Descripción: Almacena información de los estudiantes
-- ============================================================================
CREATE TABLE IF NOT EXISTS alumno (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    cohorte INTEGER NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CHECK (length(nombre) > 0),
    CHECK (length(apellido) > 0),
    CHECK (length(dni) > 0),
    CHECK (email LIKE '%@%'),
    CHECK (cohorte >= 2000 AND cohorte <= 2100)
);

-- Índices para alumno
CREATE INDEX IF NOT EXISTS idx_alumno_dni ON alumno(dni);
CREATE INDEX IF NOT EXISTS idx_alumno_cohorte ON alumno(cohorte);
CREATE INDEX IF NOT EXISTS idx_alumno_apellido ON alumno(apellido);

-- ============================================================================
-- TABLA: curso
-- Descripción: Representa una materia dictada en un período específico
-- ============================================================================
CREATE TABLE IF NOT EXISTS curso (
    id SERIAL PRIMARY KEY,
    nombre_materia TEXT NOT NULL,
    anio INTEGER NOT NULL,
    cuatrimestre INTEGER NOT NULL,
    docente_responsable TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CHECK (length(nombre_materia) > 0),
    CHECK (anio >= 2000 AND anio <= 2100),
    CHECK (cuatrimestre IN (1, 2)),
    CHECK (length(docente_responsable) > 0)
);

-- Índices para curso
CREATE INDEX IF NOT EXISTS idx_curso_anio_cuatrimestre ON curso(anio, cuatrimestre);
CREATE INDEX IF NOT EXISTS idx_curso_materia ON curso(nombre_materia);

-- ============================================================================
-- TABLA: inscripcion
-- Descripción: Relaciona alumnos con cursos
-- ============================================================================
CREATE TABLE IF NOT EXISTS inscripcion (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES curso(id) ON DELETE CASCADE,
    
    -- Constraint: Un alumno no puede inscribirse dos veces en el mismo curso
    UNIQUE(alumno_id, curso_id)
);

-- Índices para inscripcion
CREATE INDEX IF NOT EXISTS idx_inscripcion_alumno ON inscripcion(alumno_id);
CREATE INDEX IF NOT EXISTS idx_inscripcion_curso ON inscripcion(curso_id);

-- ============================================================================
-- TABLA: clase
-- Descripción: Representa una sesión de cursada específica
-- ============================================================================
CREATE TABLE IF NOT EXISTS clase (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    numero_clase INTEGER NOT NULL,
    tema TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (curso_id) REFERENCES curso(id) ON DELETE CASCADE,
    
    -- Constraints
    CHECK (numero_clase > 0),
    
    -- Constraint: El número de clase debe ser único dentro del curso
    UNIQUE(curso_id, numero_clase)
);

-- Índices para clase
CREATE INDEX IF NOT EXISTS idx_clase_curso ON clase(curso_id);
CREATE INDEX IF NOT EXISTS idx_clase_fecha ON clase(fecha);

-- ============================================================================
-- TABLA: registro_asistencia
-- Descripción: Registra la asistencia de un alumno a una clase
-- ============================================================================
CREATE TABLE IF NOT EXISTS registro_asistencia (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    estado TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    FOREIGN KEY (clase_id) REFERENCES clase(id) ON DELETE CASCADE,
    
    -- Constraints
    CHECK (estado IN ('Presente', 'Ausente', 'Tardanza', 'Justificada')),
    
    -- Constraint: Solo un registro de asistencia por alumno por clase
    UNIQUE(alumno_id, clase_id)
);

-- Índices para registro_asistencia
CREATE INDEX IF NOT EXISTS idx_asistencia_alumno ON registro_asistencia(alumno_id);
CREATE INDEX IF NOT EXISTS idx_asistencia_clase ON registro_asistencia(clase_id);
CREATE INDEX IF NOT EXISTS idx_asistencia_estado ON registro_asistencia(estado);

-- ============================================================================
-- TABLA: registro_participacion
-- Descripción: Registra la participación de un alumno en una clase
-- ============================================================================
CREATE TABLE IF NOT EXISTS registro_participacion (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    nivel TEXT NOT NULL,
    comentario TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    FOREIGN KEY (clase_id) REFERENCES clase(id) ON DELETE CASCADE,
    
    -- Constraints
    CHECK (nivel IN ('Ninguna', 'Baja', 'Media', 'Alta'))
);

-- Índices para registro_participacion
CREATE INDEX IF NOT EXISTS idx_participacion_alumno ON registro_participacion(alumno_id);
CREATE INDEX IF NOT EXISTS idx_participacion_clase ON registro_participacion(clase_id);
CREATE INDEX IF NOT EXISTS idx_participacion_nivel ON registro_participacion(nivel);

-- ============================================================================
-- TABLA: trabajo_practico
-- Descripción: Representa un trabajo práctico asignado a un curso
-- ============================================================================
CREATE TABLE IF NOT EXISTS trabajo_practico (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    fecha_entrega DATE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (curso_id) REFERENCES curso(id) ON DELETE CASCADE,
    
    -- Constraints
    CHECK (length(titulo) > 0)
);

-- Índices para trabajo_practico
CREATE INDEX IF NOT EXISTS idx_tp_curso ON trabajo_practico(curso_id);
CREATE INDEX IF NOT EXISTS idx_tp_fecha_entrega ON trabajo_practico(fecha_entrega);

-- ============================================================================
-- TABLA: entrega_tp
-- Descripción: Registra la entrega de un TP por parte de un alumno
-- ============================================================================
CREATE TABLE IF NOT EXISTS entrega_tp (
    id SERIAL PRIMARY KEY,
    trabajo_practico_id INTEGER NOT NULL,
    alumno_id INTEGER NOT NULL,
    fecha_entrega_real DATE,
    entregado BOOLEAN NOT NULL DEFAULT FALSE,
    es_tardia BOOLEAN NOT NULL DEFAULT FALSE,
    estado TEXT DEFAULT 'pendiente',  -- pendiente, entregado, tarde, no_entregado
    nota REAL,                        -- Nota del TP (1-10)
    observaciones TEXT,               -- Comentarios del docente
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (trabajo_practico_id) REFERENCES trabajo_practico(id) ON DELETE CASCADE,
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    
    -- Constraints
    CHECK (nota IS NULL OR (nota >= 1 AND nota <= 10)),
    CHECK (estado IN ('pendiente', 'entregado', 'tarde', 'no_entregado')),
    
    -- Constraint: Solo una entrega por alumno por TP
    UNIQUE(trabajo_practico_id, alumno_id)
);

-- Índices para entrega_tp
CREATE INDEX IF NOT EXISTS idx_entrega_tp ON entrega_tp(trabajo_practico_id);
CREATE INDEX IF NOT EXISTS idx_entrega_alumno ON entrega_tp(alumno_id);
CREATE INDEX IF NOT EXISTS idx_entrega_estado ON entrega_tp(entregado);

-- ============================================================================
-- TABLA: indicador_riesgo
-- Descripción: Almacena indicadores de riesgo calculados
-- ============================================================================
CREATE TABLE IF NOT EXISTS indicador_riesgo (
    id SERIAL PRIMARY KEY,
    alumno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    porcentaje_asistencia REAL,
    porcentaje_participacion REAL,
    porcentaje_tps_entregados REAL,
    nivel_riesgo TEXT,
    alertas_activas TEXT, -- JSON almacenado como texto
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES curso(id) ON DELETE CASCADE,
    
    -- Constraints
    CHECK (nivel_riesgo IN ('Bajo', 'Medio', 'Alto')),
    CHECK (porcentaje_asistencia >= 0 AND porcentaje_asistencia <= 100),
    CHECK (porcentaje_participacion >= 0 AND porcentaje_participacion <= 100),
    CHECK (porcentaje_tps_entregados >= 0 AND porcentaje_tps_entregados <= 100),
    
    -- Constraint: Un indicador por alumno por curso
    UNIQUE(alumno_id, curso_id)
);

-- Índices para indicador_riesgo
CREATE INDEX IF NOT EXISTS idx_indicador_alumno ON indicador_riesgo(alumno_id);
CREATE INDEX IF NOT EXISTS idx_indicador_curso ON indicador_riesgo(curso_id);
CREATE INDEX IF NOT EXISTS idx_indicador_nivel_riesgo ON indicador_riesgo(nivel_riesgo);

-- ============================================================================
-- VISTAS ÚTILES
-- ============================================================================

-- Vista: Alumnos con sus cursos inscriptos
CREATE OR REPLACE VIEW vista_alumnos_cursos AS
SELECT 
    a.id AS alumno_id,
    a.nombre,
    a.apellido,
    a.dni,
    a.cohorte,
    c.id AS curso_id,
    c.nombre_materia,
    c.anio,
    c.cuatrimestre,
    i.fecha_inscripcion
FROM alumno a
JOIN inscripcion i ON a.id = i.alumno_id
JOIN curso c ON i.curso_id = c.id;

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
        (SUM(CASE WHEN ra.estado IN ('Presente', 'Tardanza', 'Justificada') THEN 1 ELSE 0 END) * 100.0) / COUNT(*),
        2
    ) AS porcentaje_asistencia
FROM registro_asistencia ra
JOIN clase cl ON ra.clase_id = cl.id
GROUP BY ra.alumno_id, cl.curso_id;

-- ============================================================================
-- FUNCIONES Y TRIGGERS (PostgreSQL Style)
-- ============================================================================

-- Función: Calcular entrega tardía
CREATE OR REPLACE FUNCTION fn_calcular_entrega_tardia()
RETURNS TRIGGER AS $$
BEGIN
    NEW.es_tardia := (
        SELECT CASE
            WHEN NEW.fecha_entrega_real > tp.fecha_entrega THEN TRUE
            ELSE FALSE
        END
        FROM trabajo_practico tp
        WHERE tp.id = NEW.trabajo_practico_id
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Insertar valor calculado
DROP TRIGGER IF EXISTS trg_calcular_entrega_tardia ON entrega_tp;
CREATE TRIGGER trg_calcular_entrega_tardia
BEFORE INSERT ON entrega_tp
FOR EACH ROW
EXECUTE FUNCTION fn_calcular_entrega_tardia();
