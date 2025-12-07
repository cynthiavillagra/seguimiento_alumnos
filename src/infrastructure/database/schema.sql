-- Schema de Base de Datos SQLite
-- Sistema de Seguimiento de Alumnos
-- Versión: 1.0.0

-- ============================================================================
-- TABLA: alumno
-- Descripción: Almacena información de los estudiantes
-- ============================================================================
CREATE TABLE IF NOT EXISTS alumno (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trabajo_practico_id INTEGER NOT NULL,
    alumno_id INTEGER NOT NULL,
    fecha_entrega_real DATE,
    entregado BOOLEAN NOT NULL DEFAULT 0,
    es_tardia BOOLEAN NOT NULL DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (trabajo_practico_id) REFERENCES trabajo_practico(id) ON DELETE CASCADE,
    FOREIGN KEY (alumno_id) REFERENCES alumno(id) ON DELETE CASCADE,
    
    -- Constraint: Solo una entrega por alumno por TP
    UNIQUE(trabajo_practico_id, alumno_id)
);

-- Índices para entrega_tp
CREATE INDEX IF NOT EXISTS idx_entrega_tp ON entrega_tp(trabajo_practico_id);
CREATE INDEX IF NOT EXISTS idx_entrega_alumno ON entrega_tp(alumno_id);
CREATE INDEX IF NOT EXISTS idx_entrega_estado ON entrega_tp(entregado);

-- ============================================================================
-- TABLA: indicador_riesgo (Opcional - para cachear cálculos)
-- Descripción: Almacena indicadores de riesgo calculados
-- Nota: En el MVP, estos se calculan on-the-fly, pero esta tabla permite
--       cachear los resultados para mejorar performance en el futuro
-- ============================================================================
CREATE TABLE IF NOT EXISTS indicador_riesgo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    porcentaje_asistencia REAL,
    porcentaje_participacion REAL,
    porcentaje_tps_entregados REAL,
    nivel_riesgo TEXT,
    alertas_activas TEXT, -- JSON array de alertas
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
CREATE VIEW IF NOT EXISTS vista_alumnos_cursos AS
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
CREATE VIEW IF NOT EXISTS vista_resumen_asistencias AS
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

-- Vista: Resumen de entregas de TPs por alumno y curso
CREATE VIEW IF NOT EXISTS vista_resumen_tps AS
SELECT 
    et.alumno_id,
    tp.curso_id,
    COUNT(*) AS total_tps,
    SUM(CASE WHEN et.entregado = 1 THEN 1 ELSE 0 END) AS tps_entregados,
    SUM(CASE WHEN et.entregado = 0 THEN 1 ELSE 0 END) AS tps_no_entregados,
    SUM(CASE WHEN et.es_tardia = 1 THEN 1 ELSE 0 END) AS tps_tardios,
    ROUND(
        (SUM(CASE WHEN et.entregado = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*),
        2
    ) AS porcentaje_entregados
FROM entrega_tp et
JOIN trabajo_practico tp ON et.trabajo_practico_id = tp.id
GROUP BY et.alumno_id, tp.curso_id;

-- ============================================================================
-- TRIGGERS (Opcional - para validaciones adicionales)
-- ============================================================================

-- Trigger: Validar que el alumno esté inscripto en el curso de la clase
-- antes de registrar asistencia
CREATE TRIGGER IF NOT EXISTS validar_asistencia_inscripcion
BEFORE INSERT ON registro_asistencia
BEGIN
    SELECT CASE
        WHEN NOT EXISTS (
            SELECT 1 FROM inscripcion i
            JOIN clase c ON c.curso_id = i.curso_id
            WHERE i.alumno_id = NEW.alumno_id
            AND c.id = NEW.clase_id
        )
        THEN RAISE(ABORT, 'El alumno no está inscripto en el curso de esta clase')
    END;
END;

-- Trigger: Validar que el alumno esté inscripto en el curso de la clase
-- antes de registrar participación
CREATE TRIGGER IF NOT EXISTS validar_participacion_inscripcion
BEFORE INSERT ON registro_participacion
BEGIN
    SELECT CASE
        WHEN NOT EXISTS (
            SELECT 1 FROM inscripcion i
            JOIN clase c ON c.curso_id = i.curso_id
            WHERE i.alumno_id = NEW.alumno_id
            AND c.id = NEW.clase_id
        )
        THEN RAISE(ABORT, 'El alumno no está inscripto en el curso de esta clase')
    END;
END;

-- Trigger: Calcular automáticamente si una entrega es tardía
CREATE TRIGGER IF NOT EXISTS calcular_entrega_tardia
BEFORE INSERT ON entrega_tp
BEGIN
    UPDATE entrega_tp
    SET es_tardia = (
        SELECT CASE
            WHEN NEW.fecha_entrega_real > tp.fecha_entrega THEN 1
            ELSE 0
        END
        FROM trabajo_practico tp
        WHERE tp.id = NEW.trabajo_practico_id
    )
    WHERE id = NEW.id;
END;

-- ============================================================================
-- DATOS DE EJEMPLO (Comentados - descomentar para testing)
-- ============================================================================

/*
-- Insertar alumnos de ejemplo
INSERT INTO alumno (nombre, apellido, dni, email, cohorte) VALUES
('Juan', 'Pérez', '12345678', 'juan.perez@example.com', 2024),
('Ana', 'García', '23456789', 'ana.garcia@example.com', 2024),
('Pedro', 'Gómez', '34567890', 'pedro.gomez@example.com', 2023),
('María', 'López', '45678901', 'maria.lopez@example.com', 2024);

-- Insertar cursos de ejemplo
INSERT INTO curso (nombre_materia, anio, cuatrimestre, docente_responsable) VALUES
('Programación I', 2025, 1, 'Prof. García'),
('Matemática I', 2025, 1, 'Prof. Rodríguez'),
('Inglés Técnico', 2025, 1, 'Prof. Smith');

-- Inscribir alumnos a cursos
INSERT INTO inscripcion (alumno_id, curso_id) VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 2),
(3, 1),
(4, 1), (4, 2), (4, 3);
*/
