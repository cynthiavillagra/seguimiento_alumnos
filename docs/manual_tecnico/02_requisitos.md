# Capítulo 2: Requisitos y Análisis

## 2.1 Análisis del Problema

### El contexto educativo

En las Tecnicaturas Superiores y otras instituciones de educación superior, los docentes enfrentan desafíos específicos:

1. **Grupos grandes**: 20-40 alumnos por materia
2. **Múltiples materias**: Un docente puede tener 3-5 materias diferentes
3. **Seguimiento manual**: Planillas en papel o Excel dispersas
4. **Deserción silenciosa**: Alumnos que dejan de venir sin aviso
5. **Falta de datos históricos**: Difícil ver patrones a lo largo del tiempo

### ¿Qué necesita el docente?

Entrevistando a docentes, identificamos estas necesidades:

| Necesidad | Prioridad | Descripción |
|-----------|-----------|-------------|
| Registro rápido de asistencia | Alta | Marcar presente/ausente en segundos |
| Ver historial por alumno | Alta | Cuántas veces faltó, cuándo |
| Gestión de TPs | Media | Qué TPs entregó, cuáles debe |
| Alertas de riesgo | Media | Saber quién está faltando mucho |
| Notas y observaciones | Baja | Comentarios sobre el alumno |

## 2.2 Requisitos Funcionales

Los **requisitos funcionales** describen QUÉ debe hacer el sistema.

### RF-01: Gestión de Alumnos
```
El sistema debe permitir:
- Crear alumno (nombre, apellido, DNI, email, cohorte)
- Editar datos del alumno
- Eliminar alumno
- Listar alumnos con búsqueda y filtros
- Ver ficha individual del alumno
```

### RF-02: Gestión de Cursos
```
El sistema debe permitir:
- Crear curso (materia, año, cuatrimestre, docente)
- Editar curso
- Eliminar curso
- Listar cursos activos
```

### RF-03: Inscripciones
```
El sistema debe permitir:
- Inscribir alumno a curso
- Desinscribir alumno de curso
- Ver alumnos inscriptos en un curso
- Ver cursos en los que está inscripto un alumno
```

### RF-04: Gestión de Clases
```
El sistema debe permitir:
- Crear clase (curso, fecha, número, tema)
- Ver clases de un curso
- Ver detalle de una clase
```

### RF-05: Registro de Asistencia
```
El sistema debe permitir:
- Marcar asistencia: Presente, Ausente, Tardanza
- Modificar asistencia ya registrada
- Ver resumen de asistencias por clase
- Ver historial de asistencias por alumno
```

### RF-06: Gestión de Trabajos Prácticos
```
El sistema debe permitir:
- Crear TP (curso, título, fecha de entrega, descripción)
- Editar TP
- Eliminar TP
- Registrar entrega de TP por alumno
- Marcar estado: Entregado, Tarde, No entregado
- Asignar nota al TP
```

### RF-07: Participación
```
El sistema debe permitir:
- Registrar nivel de participación por alumno por clase
- Niveles: Alta, Media, Baja, Nula
```

## 2.3 Requisitos No Funcionales

Los **requisitos no funcionales** describen CÓMO debe comportarse el sistema.

### RNF-01: Usabilidad
```
- La interfaz debe ser intuitiva
- Un docente debe poder registrar asistencia de 30 alumnos en menos de 2 minutos
- Debe funcionar en celular (responsive)
```

### RNF-02: Rendimiento
```
- Las páginas deben cargar en menos de 3 segundos
- Las operaciones deben responder en menos de 1 segundo
```

### RNF-03: Disponibilidad
```
- El sistema debe estar disponible 24/7
- Debe funcionar con conexión a internet
```

### RNF-04: Seguridad
```
- Los datos deben estar protegidos
- Solo usuarios autorizados pueden acceder (futuro)
- Validación de todos los datos de entrada
```

### RNF-05: Mantenibilidad
```
- Código documentado
- Arquitectura modular
- Fácil de extender
```

## 2.4 Casos de Uso Principales

### CU-01: Registrar Asistencia de Clase

```
Nombre: Registrar Asistencia
Actor: Docente
Precondición: Existe el curso con alumnos inscriptos

Flujo Principal:
1. Docente selecciona curso
2. Sistema muestra alumnos inscriptos
3. Docente selecciona o crea clase
4. Para cada alumno:
   4.1. Docente marca: Presente/Ausente/Tarde
   4.2. Sistema guarda inmediatamente
5. Docente finaliza registro
6. Sistema muestra resumen

Flujo Alternativo:
4a. Si alumno ya tiene asistencia registrada:
    4a.1. Sistema muestra estado actual
    4a.2. Docente puede modificarlo
```

### CU-02: Consultar Historial de Alumno

```
Nombre: Ver Ficha de Alumno
Actor: Docente
Precondición: Alumno existe en el sistema

Flujo Principal:
1. Docente busca alumno por nombre o DNI
2. Sistema muestra lista de coincidencias
3. Docente selecciona alumno
4. Sistema muestra ficha con:
   - Datos personales
   - Cursos inscriptos
   - Porcentaje de asistencia por curso
   - TPs entregados
   - Indicador de riesgo
```

### CU-03: Gestionar Trabajo Práctico

```
Nombre: Registrar Entrega de TP
Actor: Docente
Precondición: Existe TP asignado al curso

Flujo Principal:
1. Docente selecciona curso
2. Sistema muestra TPs del curso
3. Docente selecciona TP
4. Sistema muestra alumnos y estado de entrega
5. Para cada alumno:
   5.1. Docente marca estado de entrega
   5.2. Opcionalmente asigna nota
6. Sistema guarda cambios
```

## 2.5 Modelo de Datos Conceptual

### Entidades Principales

```
ALUMNO
├── id (único)
├── nombre
├── apellido  
├── dni (único)
├── email
└── cohorte (año de ingreso)

CURSO
├── id (único)
├── nombre_materia
├── año
├── cuatrimestre (1 o 2)
└── docente_responsable

INSCRIPCION (relaciona Alumno con Curso)
├── id (único)
├── alumno_id → ALUMNO
├── curso_id → CURSO
└── fecha_inscripcion

CLASE
├── id (único)
├── curso_id → CURSO
├── fecha
├── numero_clase
└── tema

REGISTRO_ASISTENCIA
├── id (único)
├── alumno_id → ALUMNO
├── clase_id → CLASE
└── estado (Presente/Ausente/Tardanza)

TRABAJO_PRACTICO
├── id (único)
├── curso_id → CURSO
├── titulo
├── descripcion
└── fecha_entrega

ENTREGA_TP
├── id (único)
├── trabajo_practico_id → TRABAJO_PRACTICO
├── alumno_id → ALUMNO
├── fecha_entrega_real
├── estado (pendiente/entregado/tarde/no_entregado)
├── nota
└── observaciones
```

### Diagrama de Relaciones

```
┌─────────┐         ┌─────────────┐         ┌─────────┐
│ ALUMNO  │────────<│ INSCRIPCION │>────────│  CURSO  │
└─────────┘         └─────────────┘         └─────────┘
     │                                           │
     │                                           │
     │         ┌─────────────────┐               │
     └────────<│ REG_ASISTENCIA  │>──────────────┤
     │         └─────────────────┘               │
     │                  │                        │
     │                  ▼                        │
     │            ┌─────────┐                    │
     │            │  CLASE  │<───────────────────┘
     │            └─────────┘
     │
     │         ┌─────────────┐         ┌────────────────┐
     └────────<│  ENTREGA_TP │>────────│ TRABAJO_PRACTICO│
               └─────────────┘         └────────────────┘
                                              │
                                              │
                                        ┌─────────┐
                                        │  CURSO  │
                                        └─────────┘
```

## 2.6 Reglas de Negocio

### Validaciones

| Entidad | Campo | Regla |
|---------|-------|-------|
| Alumno | DNI | Único, no vacío |
| Alumno | Email | Formato válido, contiene @ |
| Alumno | Cohorte | Año entre 2000 y 2100 |
| Curso | Cuatrimestre | Solo 1 o 2 |
| Curso | Año | Entre 2000 y 2100 |
| Inscripción | alumno+curso | Combinación única |
| Asistencia | estado | Solo: Presente, Ausente, Tardanza, Justificada |
| Asistencia | alumno+clase | Solo un registro por combinación |
| TP | nota | Entre 1 y 10 (si existe) |
| Entrega TP | estado | Solo: pendiente, entregado, tarde, no_entregado |

### Cálculos

```python
# Porcentaje de asistencia
porcentaje = (presentes + tardanzas) / total_clases * 100

# Indicador de riesgo
if porcentaje_asistencia < 50:
    riesgo = "Alto"
elif porcentaje_asistencia < 75:
    riesgo = "Medio"
else:
    riesgo = "Bajo"

# Entrega tardía
es_tardia = fecha_entrega_real > fecha_entrega_limite
```

## 2.7 Priorización de Funcionalidades

Usamos el método **MoSCoW** para priorizar:

### Must Have (Debe tener) - MVP
- ✅ CRUD de Alumnos
- ✅ CRUD de Cursos
- ✅ Inscripciones
- ✅ CRUD de Clases
- ✅ Registro de Asistencia

### Should Have (Debería tener)
- ✅ Gestión de TPs
- ✅ Registro de entregas
- ⏳ Historial por alumno

### Could Have (Podría tener)
- ⏳ Indicadores de riesgo automáticos
- ⏳ Alertas por email
- ⏳ Reportes exportables

### Won't Have (No tendrá por ahora)
- ❌ Autenticación de usuarios
- ❌ Múltiples docentes
- ❌ App móvil nativa

## 2.8 Definición de MVP (Producto Mínimo Viable)

El **MVP** es la versión más simple que resuelve el problema principal.

### Alcance del MVP

```
1. Un docente puede:
   - Cargar sus cursos
   - Cargar sus alumnos
   - Inscribir alumnos a cursos
   - Crear clases
   - Registrar asistencia
   - Crear TPs
   - Registrar entregas de TPs

2. El sistema:
   - Guarda todo en base de datos
   - Funciona desde el navegador
   - Es accesible desde internet
```

### Fuera del MVP (versiones futuras)

```
- Login y autenticación
- Múltiples usuarios/docentes
- Permisos por rol
- Reportes en PDF
- Notificaciones automáticas
- Dashboard con gráficos
```

---

**Capítulo anterior**: [Introducción](./01_introduccion.md)

**Siguiente capítulo**: [Diseño y Arquitectura](./03_diseno_arquitectura.md)
