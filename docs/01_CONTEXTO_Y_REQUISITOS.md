# Contexto y Requisitos del Sistema

## 1. Contexto y Problema

### Contexto de la Tecnicatura Superior

Las Tecnicaturas Superiores son programas de educación terciaria no universitaria que preparan a los estudiantes para desempeñarse en áreas técnicas y profesionales específicas. Estos programas tienen características particulares:

- **Duración**: Típicamente entre 2 y 4 años
- **Perfil del estudiante**: Diverso, con estudiantes que trabajan, tienen responsabilidades familiares, o provienen de contextos socioeconómicos variados
- **Modalidad**: Presencial, con asistencia obligatoria y evaluación continua
- **Estructura**: Materias cuatrimestrales o anuales con trabajos prácticos, parciales y finales

### Problema de Deserción

La deserción estudiantil es un problema crítico en las Tecnicaturas Superiores:

- **Tasas de deserción**: Pueden alcanzar el 40-60% en los primeros años
- **Factores de riesgo**:
  - Inasistencias reiteradas
  - Bajo rendimiento académico
  - Falta de participación en clase
  - No entrega de trabajos prácticos
  - Problemas personales, laborales o económicos
  - Falta de integración al grupo

### Necesidad de Seguimiento Clase a Clase

El seguimiento tradicional (solo con notas de parciales) detecta el riesgo **demasiado tarde**. Se necesita:

- **Detección temprana**: Identificar señales de alerta desde las primeras semanas
- **Seguimiento continuo**: Registrar asistencia, participación y entregas clase por clase
- **Visión integral**: Combinar múltiples indicadores para evaluar el riesgo real
- **Intervención oportuna**: Permitir que coordinación y docentes actúen antes de que sea irreversible

### Rol de la Aplicación

La aplicación actúa como:

1. **Herramienta de registro** para docentes (rápida y simple de usar)
2. **Sistema de alertas** para coordinación (identificación automática de riesgo)
3. **Fuente de información** para tomar decisiones pedagógicas
4. **Base de datos histórica** para análisis y mejora continua

---

## 2. Objetivos del Sistema

### Valor para Docentes

- **Simplificar el registro**: Tomar asistencia y registrar participación de forma rápida
- **Visión del grupo**: Ver de un vistazo qué estudiantes necesitan atención
- **Seguimiento individual**: Consultar el historial completo de cada alumno
- **Fundamentar decisiones**: Tener datos objetivos para evaluaciones y tutorías

### Valor para Estudiantes

- **Transparencia**: Saber cómo están siendo evaluados más allá de las notas
- **Oportunidad de mejora**: Recibir alertas tempranas y apoyo antes de reprobar
- **Reconocimiento**: Que su participación y esfuerzo sean valorados y registrados

### Valor para Coordinación de Carrera

- **Detección temprana de riesgo**: Identificar estudiantes en peligro de deserción
- **Priorización de intervenciones**: Saber a quién contactar primero
- **Análisis de tendencias**: Ver patrones por materia, cohorte o docente
- **Toma de decisiones informada**: Basar políticas institucionales en datos reales

### Cómo Ayuda a la Detección Temprana

El sistema combina múltiples indicadores:

1. **Asistencia**: Porcentaje de clases asistidas
2. **Participación**: Frecuencia y calidad de intervenciones
3. **Entregas**: Cumplimiento con trabajos prácticos
4. **Tendencias**: Cambios bruscos en el comportamiento

Esto permite generar **alertas automáticas** cuando:
- Un alumno supera un umbral de inasistencias
- Hay caída abrupta en participación
- Se acumulan trabajos sin entregar
- La combinación de factores indica riesgo alto

---

## 3. Actores y Stakeholders

### Actores Principales

#### 1. Docente
- **Rol**: Registra información de cada clase (asistencia, participación, TPs)
- **Necesidades**: 
  - Interfaz rápida y simple
  - Acceso desde cualquier dispositivo
  - Ver estado de sus alumnos
- **Interacciones**: Crea clases, registra asistencias, consulta fichas

#### 2. Coordinación de Carrera
- **Rol**: Supervisa el estado general de los estudiantes y detecta riesgos
- **Necesidades**:
  - Dashboard con alertas
  - Reportes por materia y cohorte
  - Exportación de datos
- **Interacciones**: Consulta alertas, ve reportes, exporta información

#### 3. Estudiante
- **Rol**: (En el MVP, rol pasivo; en futuras versiones, acceso a su propia ficha)
- **Necesidades futuras**:
  - Ver su propio estado
  - Conocer sus indicadores de riesgo
  - Recibir notificaciones
- **Interacciones futuras**: Consulta su ficha, ve recomendaciones

### Stakeholders Secundarios (Futuras Iteraciones)

#### 4. Tutor/a Académico
- **Rol**: Acompaña a estudiantes en riesgo
- **Necesidades**: Acceso a fichas de sus tutorados, seguimiento de intervenciones

#### 5. Preceptor/a
- **Rol**: Gestiona aspectos administrativos (inscripciones, regularidad)
- **Necesidades**: Datos de asistencia para determinar regularidad

#### 6. Área de Bienestar Estudiantil
- **Rol**: Brinda apoyo psicológico, social y económico
- **Necesidades**: Identificar estudiantes que necesitan apoyo integral

---

## 4. Requisitos Funcionales (RF)

### RF-01: Gestión de Alumnos
**Descripción**: El sistema debe permitir registrar, consultar, actualizar y eliminar alumnos.

**Criterios**:
- Datos mínimos: nombre, apellido, DNI/ID, email, cohorte
- DNI/ID único por alumno
- Validación de formato de email

---

### RF-02: Gestión de Cursos/Materias
**Descripción**: El sistema debe permitir crear y gestionar cursos (materias).

**Criterios**:
- Datos: nombre de materia, año, cuatrimestre, docente responsable
- Un curso puede tener múltiples alumnos inscriptos

---

### RF-03: Gestión de Clases (Sesiones)
**Descripción**: El sistema debe permitir crear clases (sesiones de cursada).

**Criterios**:
- Datos: curso, fecha, número de clase, tema
- Una clase pertenece a un único curso

---

### RF-04: Registro de Asistencia
**Descripción**: El docente debe poder registrar la asistencia de cada alumno a cada clase.

**Criterios**:
- Estados: Presente, Ausente, Tardanza, Justificada
- Un registro por alumno por clase
- Posibilidad de modificar asistencia ya registrada

---

### RF-05: Registro de Participación
**Descripción**: El docente debe poder registrar la participación de alumnos en clase.

**Criterios**:
- Niveles: Ninguna, Baja, Media, Alta
- Opcional: comentarios sobre la participación
- Múltiples registros por alumno por clase (si participa varias veces)

---

### RF-06: Registro de Trabajos Prácticos
**Descripción**: El sistema debe permitir definir TPs y registrar entregas.

**Criterios**:
- Datos del TP: título, descripción, fecha de entrega, curso
- Registro de entrega: alumno, TP, fecha de entrega real, estado (Entregado/No entregado)
- Posibilidad de marcar entregas tardías

---

### RF-07: Consulta de Ficha de Alumno
**Descripción**: El sistema debe mostrar una ficha completa del alumno con todos sus datos de seguimiento.

**Criterios**:
- Datos personales
- Cursos inscriptos
- Historial de asistencias (por curso)
- Historial de participación
- Historial de entregas de TPs
- Indicadores de riesgo calculados

---

### RF-08: Cálculo de Indicadores de Riesgo
**Descripción**: El sistema debe calcular automáticamente indicadores de riesgo para cada alumno.

**Criterios**:
- Porcentaje de asistencia
- Porcentaje de participación
- Porcentaje de TPs entregados
- Nivel de riesgo global: Bajo, Medio, Alto
- Actualización automática al registrar nuevos datos

---

### RF-09: Generación de Alertas
**Descripción**: El sistema debe generar alertas cuando un alumno supera umbrales de riesgo.

**Criterios**:
- Alerta por inasistencias (ej: >30%)
- Alerta por falta de participación
- Alerta por TPs no entregados
- Listado de alumnos en riesgo por curso

---

### RF-10: Consulta de Listados
**Descripción**: El sistema debe permitir consultar listados filtrados.

**Criterios**:
- Listado de alumnos por curso
- Listado de alumnos en riesgo
- Listado de asistencias de una clase
- Listado de entregas de un TP

---

### Requisitos Funcionales de la API

### RF-API-01: Endpoint para Crear Alumno
**Descripción**: `POST /alumnos` - Crear un nuevo alumno en el sistema.

---

### RF-API-02: Endpoint para Obtener Alumno
**Descripción**: `GET /alumnos/{id}` - Obtener datos de un alumno específico.

---

### RF-API-03: Endpoint para Listar Alumnos
**Descripción**: `GET /alumnos` - Listar todos los alumnos (con filtros opcionales).

---

### RF-API-04: Endpoint para Crear Curso
**Descripción**: `POST /cursos` - Crear un nuevo curso.

---

### RF-API-05: Endpoint para Crear Clase
**Descripción**: `POST /clases` - Crear una nueva sesión de clase.

---

### RF-API-06: Endpoint para Registrar Asistencia
**Descripción**: `POST /asistencias` - Registrar asistencia de uno o varios alumnos a una clase.

---

### RF-API-07: Endpoint para Registrar Participación
**Descripción**: `POST /participaciones` - Registrar participación de un alumno en una clase.

---

### RF-API-08: Endpoint para Crear Trabajo Práctico
**Descripción**: `POST /trabajos-practicos` - Definir un nuevo TP para un curso.

---

### RF-API-09: Endpoint para Registrar Entrega de TP
**Descripción**: `POST /entregas-tp` - Registrar que un alumno entregó un TP.

---

### RF-API-10: Endpoint para Consultar Ficha de Alumno
**Descripción**: `GET /alumnos/{id}/ficha` - Obtener ficha completa con indicadores.

---

### RF-API-11: Endpoint para Listar Alumnos en Riesgo
**Descripción**: `GET /alertas/alumnos-en-riesgo` - Listar alumnos con indicadores de riesgo alto.

---

## 5. Requisitos No Funcionales (RNF)

### RNF-01: Facilidad de Uso
**Descripción**: La interfaz (API y futura UI) debe ser intuitiva y rápida de usar para docentes con diferentes niveles de habilidad tecnológica.

**Criterios**:
- Endpoints con nombres claros y predecibles
- Mensajes de error descriptivos
- Documentación clara de la API

---

### RNF-02: Código Mantenible y Legible
**Descripción**: El código debe ser didáctico, bien documentado y seguir principios de clean code.

**Criterios**:
- Arquitectura por capas claramente separadas
- Uso de POO con responsabilidades bien definidas
- Comentarios explicando decisiones de diseño
- Type hints en Python
- Nombres descriptivos de clases, métodos y variables

---

### RNF-03: Arquitectura Modular y Desacoplada
**Descripción**: El sistema debe estar organizado en capas con bajo acoplamiento.

**Criterios**:
- Capa de dominio independiente de infraestructura
- Uso de interfaces/abstracciones para repositorios
- Servicios de aplicación que orquestan casos de uso
- API que solo delega a servicios

---

### RNF-04: Persistencia Local con SQLite (MVP)
**Descripción**: El MVP debe usar SQLite como base de datos local.

**Criterios**:
- Uso de `sqlite3` nativo de Python
- Esquema de base de datos bien diseñado
- Transacciones para operaciones críticas

---

### RNF-05: Preparado para Migración a BBDD Externa
**Descripción**: El diseño debe permitir cambiar de SQLite a PostgreSQL u otra BBDD sin reescribir lógica de negocio.

**Criterios**:
- Repositorios implementan interfaces abstractas
- Lógica de negocio no depende de detalles de SQLite
- Configuración de conexión centralizada y fácil de cambiar

---

### RNF-06: Preparado para Despliegue en Vercel
**Descripción**: La API debe poder desplegarse como función serverless en Vercel.

**Criterios**:
- Estructura compatible con Vercel (ej: carpeta `api/`)
- Uso de FastAPI u otro framework compatible
- Documentación de cómo desplegar

---

### RNF-07: Seguridad Básica
**Descripción**: Aunque el MVP no incluye login completo, debe estar preparado para incorporarlo.

**Criterios**:
- Validación de datos de entrada
- Prevención de SQL injection (uso de parámetros)
- Estructura para agregar autenticación JWT en el futuro
- Opcional: API key simple para proteger endpoints en el MVP

---

### RNF-08: Rendimiento Aceptable
**Descripción**: Las operaciones comunes deben ser rápidas.

**Criterios**:
- Consultas de ficha de alumno en <500ms
- Registro de asistencia de una clase completa en <2s
- Índices en campos clave de la base de datos

---

### RNF-09: Escalabilidad Futura
**Descripción**: El diseño debe permitir crecer en funcionalidad y usuarios.

**Criterios**:
- Arquitectura que soporte agregar nuevos módulos
- Código preparado para migrar a microservicios si es necesario
- Base de datos normalizada

---

## 6. Alcance del MVP vs Futuras Iteraciones

### ✅ Incluido en el MVP

#### Funcionalidades Core
- ✅ Registro y consulta de **alumnos**
- ✅ Registro y consulta de **cursos**
- ✅ Creación de **clases** (sesiones)
- ✅ Registro de **asistencia** (presente/ausente/tardanza/justificada)
- ✅ Registro de **participación** (niveles: ninguna/baja/media/alta)
- ✅ Definición de **trabajos prácticos**
- ✅ Registro de **entregas de TPs**
- ✅ Cálculo automático de **indicadores de riesgo**:
  - Porcentaje de asistencia
  - Porcentaje de participación
  - Porcentaje de TPs entregados
  - Nivel de riesgo global (bajo/medio/alto)
- ✅ Generación de **alertas simples** (listado de alumnos en riesgo)
- ✅ Consulta de **ficha completa de alumno**

#### Arquitectura y Tecnología
- ✅ Arquitectura por capas (domain, application, infrastructure, presentation)
- ✅ POO en Python 3
- ✅ SQLite como base de datos local
- ✅ API HTTP REST-like con FastAPI
- ✅ Autenticación muy simple (API key opcional) o sin autenticación
- ✅ Preparado para despliegue en Vercel
- ✅ Código en GitHub

#### Documentación
- ✅ Documentación completa de diseño
- ✅ Diagramas UML (ER, clases, secuencia, actividad, componentes)
- ✅ Matriz de trazabilidad
- ✅ Comentarios didácticos en el código

---

### 🔮 Futuras Iteraciones

#### Iteración 2: Autenticación y Roles
- 🔮 Sistema de login completo (JWT)
- 🔮 Roles: Docente, Coordinación, Estudiante, Tutor
- 🔮 Permisos por rol (RBAC)
- 🔮 Estudiantes pueden ver su propia ficha

#### Iteración 3: Interfaz de Usuario
- 🔮 Frontend web (React/Vue/Svelte)
- 🔮 Dashboard para coordinación
- 🔮 Interfaz de registro para docentes
- 🔮 Portal de estudiantes

#### Iteración 4: Funcionalidades Avanzadas
- 🔮 Notificaciones automáticas (email/SMS)
- 🔮 Reportes y gráficos avanzados
- 🔮 Exportación a PDF/Excel
- 🔮 Predicción de riesgo con ML
- 🔮 Registro de intervenciones (tutorías, seguimientos)
- 🔮 Comentarios y notas de docentes sobre alumnos

#### Iteración 5: Integraciones Externas
- 🔮 Integración con Chamilo/Moodle
- 🔮 Integración con SIU Guaraní
- 🔮 Sincronización con sistemas de gestión institucional
- 🔮 API pública para terceros

#### Iteración 6: Migración a BBDD Externa
- 🔮 Migración de SQLite a PostgreSQL
- 🔮 Despliegue en servidor dedicado o cloud
- 🔮 Backups automáticos
- 🔮 Alta disponibilidad

#### Iteración 7: Analítica y BI
- 🔮 Dashboard de analítica institucional
- 🔮 Comparación entre cohortes
- 🔮 Identificación de patrones de deserción
- 🔮 Recomendaciones automáticas de intervención

---

## Resumen de Prioridades

| Prioridad | Alcance | Descripción |
|-----------|---------|-------------|
| **P0 (MVP)** | Core funcional | Registro de datos + cálculo de riesgo + API básica |
| **P1** | Seguridad | Login, roles, permisos |
| **P2** | UX | Frontend completo |
| **P3** | Avanzado | Notificaciones, ML, reportes |
| **P4** | Integración | Conexión con sistemas externos |
| **P5** | Escalabilidad | BBDD externa, alta disponibilidad |

---

**Siguiente documento**: [Casos de Uso, User Stories y Criterios de Aceptación](./02_CASOS_DE_USO_Y_STORIES.md)
