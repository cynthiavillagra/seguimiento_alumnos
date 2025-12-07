# Casos de Uso, User Stories y Criterios de Aceptación

## 1. Casos de Uso (CU)

### CU-01: Registrar Asistencia de una Clase

**Actor(es)**: Docente

**Precondiciones**:
- El docente está autenticado (en futuras versiones)
- Existe un curso creado
- Existe una clase (sesión) creada para ese curso
- Existen alumnos inscriptos en el curso

**Flujo Principal**:
1. El docente selecciona el curso y la clase
2. El sistema muestra el listado de alumnos inscriptos
3. El docente marca la asistencia de cada alumno (Presente/Ausente/Tardanza/Justificada)
4. El docente confirma el registro
5. El sistema guarda los registros de asistencia
6. El sistema actualiza los indicadores de riesgo de los alumnos afectados
7. El sistema confirma el registro exitoso

**Flujos Alternativos**:
- **FA-01**: Si la clase no existe, el sistema muestra error y sugiere crear la clase primero
- **FA-02**: Si no hay alumnos inscriptos, el sistema muestra mensaje informativo
- **FA-03**: Si ya existe registro de asistencia para esa clase, el sistema permite modificarlo

**Postcondiciones**:
- Los registros de asistencia quedan guardados
- Los indicadores de riesgo se actualizan

---

### CU-02: Registrar Participación del Alumno

**Actor(es)**: Docente

**Precondiciones**:
- Existe un curso y una clase
- Existe el alumno en el sistema

**Flujo Principal**:
1. Durante o después de la clase, el docente identifica al alumno
2. El docente registra el nivel de participación (Ninguna/Baja/Media/Alta)
3. Opcionalmente, el docente agrega un comentario sobre la participación
4. El sistema guarda el registro
5. El sistema actualiza los indicadores de riesgo

**Flujos Alternativos**:
- **FA-01**: Si el alumno no asistió a la clase, el sistema advierte pero permite registrar participación (caso: participación virtual)
- **FA-02**: Si ya existe un registro de participación para ese alumno en esa clase, el sistema permite agregar uno nuevo o modificar el existente

**Postcondiciones**:
- El registro de participación queda guardado
- Los indicadores se actualizan

---

### CU-03: Registrar Entrega de Trabajo Práctico

**Actor(es)**: Docente

**Precondiciones**:
- Existe un trabajo práctico definido para el curso
- Existe el alumno inscripto en el curso

**Flujo Principal**:
1. El docente selecciona el trabajo práctico
2. El docente selecciona al alumno (o lista de alumnos)
3. El docente marca como "Entregado" con la fecha de entrega
4. El sistema guarda el registro
5. El sistema actualiza los indicadores de riesgo

**Flujos Alternativos**:
- **FA-01**: Si la entrega es tardía (después de la fecha límite), el sistema lo marca automáticamente
- **FA-02**: Si el TP no existe, el sistema muestra error y sugiere crearlo primero
- **FA-03**: Si el alumno ya tiene una entrega registrada, el sistema permite actualizarla

**Postcondiciones**:
- La entrega queda registrada
- Los indicadores se actualizan

---

### CU-04: Consultar Ficha Completa de un Alumno

**Actor(es)**: Docente, Coordinación

**Precondiciones**:
- El alumno existe en el sistema
- El actor tiene permisos para ver la ficha (en futuras versiones)

**Flujo Principal**:
1. El actor busca al alumno por nombre, apellido o DNI
2. El sistema muestra la ficha completa con:
   - Datos personales
   - Cursos inscriptos
   - Historial de asistencias (por curso)
   - Historial de participación
   - Historial de entregas de TPs
   - Indicadores de riesgo calculados
   - Alertas activas
3. El actor puede exportar o imprimir la ficha (futuro)

**Flujos Alternativos**:
- **FA-01**: Si el alumno no existe, el sistema muestra mensaje de error
- **FA-02**: Si el alumno no tiene datos de seguimiento, el sistema muestra ficha con datos personales solamente

**Postcondiciones**:
- Ninguna (solo consulta)

---

### CU-05: Consultar Listado de Alumnos en Riesgo

**Actor(es)**: Coordinación, Docente

**Precondiciones**:
- Existen alumnos con datos de seguimiento en el sistema

**Flujo Principal**:
1. El actor solicita el listado de alumnos en riesgo
2. Opcionalmente, filtra por curso, nivel de riesgo, o tipo de alerta
3. El sistema calcula los indicadores de todos los alumnos
4. El sistema muestra listado ordenado por nivel de riesgo (de mayor a menor)
5. Para cada alumno muestra: nombre, curso(s), nivel de riesgo, alertas activas
6. El actor puede hacer clic en un alumno para ver su ficha completa

**Flujos Alternativos**:
- **FA-01**: Si no hay alumnos en riesgo, el sistema muestra mensaje positivo
- **FA-02**: Si no hay datos suficientes para calcular riesgo, el sistema lo indica

**Postcondiciones**:
- Ninguna (solo consulta)

---

### CU-06: Crear Curso

**Actor(es)**: Coordinación, Administrador

**Precondiciones**:
- El actor tiene permisos para crear cursos

**Flujo Principal**:
1. El actor ingresa datos del curso: nombre de materia, año, cuatrimestre, docente responsable
2. El sistema valida los datos
3. El sistema crea el curso
4. El sistema confirma la creación

**Flujos Alternativos**:
- **FA-01**: Si faltan datos obligatorios, el sistema muestra error de validación
- **FA-02**: Si ya existe un curso idéntico, el sistema advierte (pero permite crear)

**Postcondiciones**:
- El curso queda creado y disponible para inscribir alumnos

---

### CU-07: Crear Clase (Sesión)

**Actor(es)**: Docente

**Precondiciones**:
- Existe un curso creado

**Flujo Principal**:
1. El docente selecciona el curso
2. El docente ingresa: fecha, número de clase, tema
3. El sistema valida los datos
4. El sistema crea la clase
5. El sistema confirma la creación

**Flujos Alternativos**:
- **FA-01**: Si ya existe una clase con el mismo número para ese curso, el sistema advierte
- **FA-02**: Si la fecha es futura, el sistema permite crear pero advierte

**Postcondiciones**:
- La clase queda creada y disponible para registrar asistencia y participación

---

### CU-08: Definir Trabajo Práctico

**Actor(es)**: Docente

**Precondiciones**:
- Existe un curso creado

**Flujo Principal**:
1. El docente selecciona el curso
2. El docente ingresa: título del TP, descripción, fecha de entrega
3. El sistema valida los datos
4. El sistema crea el TP
5. El sistema confirma la creación

**Flujos Alternativos**:
- **FA-01**: Si la fecha de entrega es pasada, el sistema advierte pero permite crear

**Postcondiciones**:
- El TP queda creado y disponible para registrar entregas

---

### CU-09: Inscribir Alumno a Curso

**Actor(es)**: Coordinación, Administrador

**Precondiciones**:
- El alumno existe en el sistema
- El curso existe en el sistema

**Flujo Principal**:
1. El actor selecciona el curso
2. El actor selecciona al alumno (o lista de alumnos)
3. El sistema crea la inscripción
4. El sistema confirma

**Flujos Alternativos**:
- **FA-01**: Si el alumno ya está inscripto, el sistema muestra error
- **FA-02**: Si el alumno o curso no existen, el sistema muestra error

**Postcondiciones**:
- El alumno queda inscripto y aparece en los listados del curso

---

### CU-10: Crear Alumno

**Actor(es)**: Coordinación, Administrador

**Precondiciones**:
- El actor tiene permisos para crear alumnos

**Flujo Principal**:
1. El actor ingresa datos del alumno: nombre, apellido, DNI, email, cohorte
2. El sistema valida los datos (formato de email, DNI único)
3. El sistema crea el alumno
4. El sistema confirma la creación

**Flujos Alternativos**:
- **FA-01**: Si el DNI ya existe, el sistema muestra error
- **FA-02**: Si el email tiene formato inválido, el sistema muestra error de validación

**Postcondiciones**:
- El alumno queda creado y disponible para inscribir a cursos

---

## 2. User Stories (Historias de Usuario)

### Para Docentes

#### US-01: Tomar Asistencia Rápidamente
> **Como** docente  
> **Quiero** registrar la asistencia de mi clase en menos de 2 minutos  
> **Para** no perder tiempo de clase y tener datos actualizados

**Criterios de Aceptación**:
- **Given** que tengo una clase creada con 30 alumnos inscriptos
- **When** accedo al registro de asistencia
- **Then** veo la lista completa de alumnos con opciones claras (Presente/Ausente/Tardanza)
- **And** puedo marcar todos en menos de 2 minutos
- **And** el sistema guarda automáticamente

---

#### US-02: Ver Quién Está en Riesgo en Mi Materia
> **Como** docente  
> **Quiero** ver rápidamente qué alumnos de mi curso están en riesgo  
> **Para** poder darles atención especial o derivarlos a tutoría

**Criterios de Aceptación**:
- **Given** que tengo alumnos con diferentes niveles de asistencia y participación
- **When** consulto el estado de mi curso
- **Then** veo un listado destacando alumnos en riesgo alto y medio
- **And** puedo ver el detalle de cada uno (% asistencia, participación, TPs)

---

#### US-03: Registrar Participación Destacada
> **Como** docente  
> **Quiero** registrar cuando un alumno participa activamente en clase  
> **Para** que su esfuerzo sea reconocido y considerado en la evaluación

**Criterios de Aceptación**:
- **Given** que estoy en una clase
- **When** un alumno participa con una intervención relevante
- **Then** puedo registrar su participación con nivel (Baja/Media/Alta)
- **And** opcionalmente agregar un comentario
- **And** esto se refleja en su ficha y en los indicadores

---

#### US-04: Consultar Historial de un Alumno
> **Como** docente  
> **Quiero** ver el historial completo de un alumno en mi materia  
> **Para** fundamentar decisiones pedagógicas y de evaluación

**Criterios de Aceptación**:
- **Given** que tengo un alumno inscripto en mi curso
- **When** consulto su ficha
- **Then** veo su asistencia clase por clase
- **And** veo su participación registrada
- **And** veo qué TPs entregó y cuáles no
- **And** veo indicadores calculados (% asistencia, % participación, % TPs)

---

### Para Coordinación de Carrera

#### US-05: Identificar Alumnos en Riesgo de Deserción
> **Como** coordinador/a  
> **Quiero** ver un listado de todos los alumnos en riesgo alto  
> **Para** contactarlos y ofrecerles apoyo antes de que abandonen

**Criterios de Aceptación**:
- **Given** que hay alumnos con diferentes niveles de riesgo en el sistema
- **When** accedo al dashboard de alertas
- **Then** veo un listado ordenado por nivel de riesgo
- **And** puedo filtrar por carrera, cohorte o materia
- **And** para cada alumno veo: nombre, materias cursando, nivel de riesgo, alertas activas

---

#### US-06: Analizar Tendencias por Materia
> **Como** coordinador/a  
> **Quiero** ver estadísticas de deserción y riesgo por materia  
> **Para** identificar materias problemáticas y tomar acciones institucionales

**Criterios de Aceptación**:
- **Given** que hay múltiples cursos con datos de seguimiento
- **When** consulto el reporte por materia
- **Then** veo para cada materia: % promedio de asistencia, % de alumnos en riesgo, % de TPs entregados
- **And** puedo comparar entre materias
- **And** puedo exportar los datos

---

#### US-07: Exportar Datos para Análisis
> **Como** coordinador/a  
> **Quiero** exportar datos de seguimiento a Excel o CSV  
> **Para** hacer análisis más profundos o presentar informes a dirección

**Criterios de Aceptación**:
- **Given** que hay datos de seguimiento en el sistema
- **When** solicito exportar datos
- **Then** puedo elegir qué datos exportar (alumnos, asistencias, participaciones, TPs)
- **And** puedo filtrar por fecha, curso o cohorte
- **And** el sistema genera un archivo descargable en formato estándar

---

### Para Estudiantes (Futuras Versiones)

#### US-08: Ver Mi Propio Estado
> **Como** estudiante  
> **Quiero** ver mi propia ficha de seguimiento  
> **Para** saber cómo estoy y qué necesito mejorar

**Criterios de Aceptación**:
- **Given** que estoy autenticado como estudiante
- **When** accedo a mi perfil
- **Then** veo mis indicadores de asistencia, participación y TPs por materia
- **And** veo si tengo alertas de riesgo
- **And** veo recomendaciones de mejora

---

#### US-09: Recibir Notificaciones de Alerta
> **Como** estudiante  
> **Quiero** recibir una notificación cuando entre en riesgo  
> **Para** poder reaccionar a tiempo y no perder la regularidad

**Criterios de Aceptación**:
- **Given** que mi nivel de riesgo pasa de bajo a medio o alto
- **When** el sistema recalcula mis indicadores
- **Then** recibo una notificación por email
- **And** la notificación explica qué indicador me pone en riesgo
- **And** incluye recomendaciones o contacto de tutoría

---

## 3. Criterios de Aceptación Detallados (BDD)

### Para US-01: Tomar Asistencia Rápidamente

#### Escenario 1: Registro exitoso de asistencia completa
```gherkin
Given que soy un docente autenticado
And existe un curso "Programación I" con 25 alumnos inscriptos
And existe una clase del 2025-12-07 para ese curso
When accedo al registro de asistencia de esa clase
Then veo la lista de 25 alumnos ordenados alfabéticamente
And cada alumno tiene opciones: Presente, Ausente, Tardanza, Justificada
And puedo marcar todos los alumnos
And hago clic en "Guardar"
Then el sistema confirma "Asistencia registrada exitosamente"
And los 25 registros quedan guardados en la base de datos
And los indicadores de riesgo de los alumnos se actualizan
```

#### Escenario 2: Modificación de asistencia ya registrada
```gherkin
Given que ya registré la asistencia de la clase del 2025-12-07
And marqué a "Juan Pérez" como Ausente
When vuelvo a acceder al registro de esa clase
Then veo que "Juan Pérez" está marcado como Ausente
When cambio su estado a Presente
And guardo
Then el sistema actualiza el registro
And recalcula los indicadores de "Juan Pérez"
```

#### Escenario 3: Error al registrar sin clase creada
```gherkin
Given que no he creado una clase para hoy
When intento registrar asistencia
Then el sistema muestra error "Debe crear la clase primero"
And me ofrece un botón para crear la clase
```

---

### Para US-05: Identificar Alumnos en Riesgo de Deserción

#### Escenario 1: Listado de alumnos en riesgo alto
```gherkin
Given que existen los siguientes alumnos:
  | Nombre       | Asistencia | Participación | TPs Entregados | Riesgo |
  | Ana García   | 95%        | Alta          | 100%           | Bajo   |
  | Juan Pérez   | 60%        | Baja          | 50%            | Alto   |
  | María López  | 70%        | Media         | 80%            | Medio  |
  | Pedro Gómez  | 40%        | Ninguna       | 20%            | Alto   |
When accedo al listado de alumnos en riesgo
And filtro por "Riesgo Alto"
Then veo 2 alumnos: Juan Pérez y Pedro Gómez
And están ordenados por nivel de riesgo descendente
And para cada uno veo: nombre, cursos, % asistencia, % participación, % TPs
```

#### Escenario 2: Filtro por curso específico
```gherkin
Given que hay alumnos en riesgo en múltiples cursos
When filtro por curso "Programación I"
Then veo solo alumnos en riesgo de ese curso
And puedo ver cuántos alumnos en riesgo hay en total en ese curso
```

#### Escenario 3: Sin alumnos en riesgo
```gherkin
Given que todos los alumnos tienen indicadores saludables
When accedo al listado de alumnos en riesgo
Then veo el mensaje "¡Excelente! No hay alumnos en riesgo alto en este momento"
And veo estadísticas positivas generales
```

---

### Para US-04: Consultar Historial de un Alumno

#### Escenario 1: Ficha completa con todos los datos
```gherkin
Given que existe el alumno "Juan Pérez" con DNI 12345678
And está inscripto en "Programación I"
And tiene registradas 8 asistencias de 10 clases
And tiene 3 participaciones registradas
And tiene 4 TPs entregados de 5
When consulto su ficha
Then veo sus datos personales: nombre, DNI, email, cohorte
And veo "Programación I" en sus cursos inscriptos
And veo el detalle de asistencias: 8/10 (80%)
And veo el detalle de participaciones: 3 registros con niveles y fechas
And veo el detalle de TPs: 4/5 entregados (80%)
And veo indicadores calculados:
  | Indicador          | Valor |
  | Asistencia         | 80%   |
  | Participación      | Media |
  | TPs Entregados     | 80%   |
  | Nivel de Riesgo    | Medio |
And veo alertas activas si las hay
```

#### Escenario 2: Alumno sin datos de seguimiento
```gherkin
Given que existe el alumno "María Nueva" recién creada
And no está inscripta en ningún curso
When consulto su ficha
Then veo sus datos personales
And veo el mensaje "Este alumno aún no tiene datos de seguimiento"
And no veo indicadores ni alertas
```

---

## 4. Escenarios de Uso Relevantes

### Escenario Normal 1: Flujo Completo de una Clase

**Contexto**: Es lunes 7 de diciembre de 2025, clase de Programación I

1. **Antes de la clase**:
   - El docente crea la clase en el sistema: "Clase 10 - Recursividad"
   
2. **Al inicio de la clase**:
   - El docente toma asistencia usando el sistema
   - Marca 22 presentes, 3 ausentes, 2 tardanzas
   - El sistema guarda y actualiza indicadores
   
3. **Durante la clase**:
   - Un alumno hace una pregunta muy buena
   - El docente registra participación "Alta" con comentario
   - Otro alumno participa con nivel "Medio"
   
4. **Al final de la clase**:
   - El docente recuerda que había un TP con fecha de entrega hoy
   - Registra quiénes entregaron (18 alumnos)
   - El sistema marca automáticamente como "No entregado" a los 7 restantes
   
5. **Después de la clase**:
   - El sistema recalcula indicadores de todos los alumnos
   - Genera alertas para 2 alumnos que pasaron a riesgo alto
   - Coordinación recibe notificación (en futuras versiones)

---

### Escenario Normal 2: Coordinación Detecta Riesgo y Actúa

**Contexto**: Coordinadora revisa alertas semanalmente

1. **Lunes por la mañana**:
   - Coordinadora accede al dashboard de alertas
   - Ve que hay 5 alumnos en riesgo alto
   
2. **Análisis individual**:
   - Hace clic en "Pedro Gómez"
   - Ve su ficha: 40% asistencia, 20% TPs entregados, sin participación
   - Nota que la caída fue abrupta en las últimas 3 semanas
   
3. **Acción**:
   - Contacta a Pedro por email y teléfono
   - Descubre que tiene problemas laborales
   - Lo deriva a tutoría y área de bienestar
   - Registra la intervención en el sistema (futuro)
   
4. **Seguimiento**:
   - En las semanas siguientes, monitorea si Pedro mejora
   - Ve en el sistema que Pedro volvió a asistir y entregar TPs
   - Su nivel de riesgo baja a "Medio"

---

### Escenario de Error 1: Intento de Registrar Asistencia sin Clase

**Contexto**: Docente olvidó crear la clase

1. Docente intenta registrar asistencia
2. Sistema detecta que no hay clase creada para hoy
3. Sistema muestra error claro: "No existe una clase para hoy. ¿Desea crearla?"
4. Docente hace clic en "Crear clase"
5. Completa datos rápidos (número, tema)
6. Sistema crea la clase y lo redirige al registro de asistencia
7. Docente completa el registro normalmente

---

### Escenario de Error 2: Datos Inválidos al Crear Alumno

**Contexto**: Coordinación carga alumnos nuevos

1. Coordinadora ingresa datos de un alumno
2. Pone email inválido: "juan.perez@" (sin dominio)
3. Pone DNI que ya existe en el sistema
4. Hace clic en "Guardar"
5. Sistema valida y muestra errores:
   - "El email no tiene formato válido"
   - "Ya existe un alumno con DNI 12345678"
6. Coordinadora corrige los datos
7. Sistema acepta y crea el alumno

---

### Escenario de Riesgo 1: Alumno con Muchas Inasistencias

**Contexto**: Alumno falta 4 clases seguidas

1. **Clase 1**: Alumno ausente → Asistencia baja a 85%
2. **Clase 2**: Alumno ausente → Asistencia baja a 78%
3. **Clase 3**: Alumno ausente → Asistencia baja a 70% → Sistema genera alerta "Riesgo Medio"
4. **Clase 4**: Alumno ausente → Asistencia baja a 62% → Sistema eleva a "Riesgo Alto"
5. Sistema notifica a coordinación (futuro)
6. Coordinación contacta al alumno
7. Alumno explica situación y se compromete a volver
8. **Clase 5**: Alumno presente → Asistencia sube a 65%
9. **Clases siguientes**: Alumno asiste regularmente → Riesgo baja a "Medio" y luego a "Bajo"

---

### Escenario de Riesgo 2: Alumno con Bajo Rendimiento Integral

**Contexto**: Alumno con múltiples indicadores negativos

**Datos del alumno "Ana Rodríguez"**:
- Asistencia: 65% (límite es 70%)
- Participación: Ninguna en las últimas 5 clases
- TPs: 2 de 5 entregados (40%)

**Cálculo de riesgo**:
- Sistema detecta que 2 de 3 indicadores están en rojo
- Nivel de riesgo: **Alto**
- Alertas generadas:
  - "Asistencia por debajo del 70%"
  - "Falta de participación sostenida"
  - "Menos del 50% de TPs entregados"

**Acción recomendada**:
- Contacto urgente con la alumna
- Derivación a tutoría académica
- Evaluación de situación personal/laboral
- Plan de recuperación

---

**Siguiente documento**: [Modelo de Dominio, API y Diagramas UML](./03_MODELO_Y_API.md)
