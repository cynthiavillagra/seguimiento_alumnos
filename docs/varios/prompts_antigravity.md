
# 2️⃣ PROMPT 1 – Documentación completa + UML + trazabilidad + API

Este reemplaza y mejora el Prompt 1 anterior, incorporando:

* API mínima,
* user stories + criterios de aceptación,
* todos los UML que pediste (actividad, secuencia, clases, “componentes”, ER),
* matriz de trazabilidad.

> 📌 Lo podés copiar tal cual y tunear detalles de estilo/alcance.

---

### 🟦 PROMPT 1 – DISEÑO, REQUISITOS, UML Y TRAZABILIDAD

Rol: Actuá como Arquitecto/a de Software Senior y Desarrollador/a Python especializado en aplicaciones educativas y diseño orientado a dominio.

Contexto:
Quiero diseñar una aplicación de seguimiento de alumnos para una Tecnicatura Superior, con foco en **detección temprana de riesgo de deserción**.
La aplicación debe tener:

* Arquitectura limpia, con **capas separadas** (dominio, aplicación/servicios, infraestructura, API/presentación).
* **API HTTP mínima** (REST-like) para registrar y consultar datos.
* Uso de **Python POO** y **SQLite** como base de datos local (sin BBDD externa en el MVP), pero con diseño que permita migrar luego a Postgres u otra BBDD externa.
* Código pensado para vivir en **GitHub** y ser desplegado en **Vercel** (por ejemplo, como API serverless).

---

### Parte 1 – Definición del problema, necesidades y requisitos

Generá un documento en **Markdown** con las siguientes secciones:

1. **Contexto y problema**

   * Explicá el contexto de una Tecnicatura Superior.
   * Problema de deserción y necesidad de seguimiento clase a clase.
   * Rol de la app como herramienta de apoyo para docentes y coordinación.

2. **Objetivos del sistema**

   * Qué valor aporta a docentes, estudiantes y coordinación.
   * Cómo ayuda a la detección temprana de riesgo.

3. **Actores y stakeholders**

   * Docente
   * Estudiante
   * Coordinación de carrera
   * (Opcional) Tutor/a, preceptor/a, área de bienestar estudiantil.

4. **Requisitos funcionales (RF-xx)**

   * Listá los requisitos funcionales numerados (RF-01, RF-02, …).
   * Ejemplos: registrar asistencia, registrar participación, registrar entrega de TPs, consultar ficha de alumno, ver alertas de riesgo, etc.
   * Incluir RF relacionados con la API: por ejemplo, “RF-API-01: exponer endpoint para registrar asistencia”.

5. **Requisitos no funcionales (RNF-xx)**
   Incluir al menos:

   * Facilidad de uso para docentes.
   * Código mantenible y legible (uso didáctico).
   * Arquitectura modular y capas desacopladas.
   * Persistencia local con SQLite en el MVP.
   * Posibilidad de migrar a BBDD externa sin reescribir la lógica de negocio.
   * Preparado para despliegue en Vercel.
   * Seguridad básica pensada para una futura incorporación de login (aunque no se implemente en el MVP).

6. **Alcance del MVP vs futuras iteraciones**

   * Explicá qué incluye el MVP:

     * Registro y consulta de alumnos, cursos, clases, asistencia, participación, TPs y alertas simples.
     * API mínima sin login o con autenticación muy simple (por ejemplo, API key).
   * Explicá qué se deja para futuras iteraciones:

     * Sistema de login/roles completo (docente, coordinación).
     * Seguridad más avanzada.
     * Integraciones externas (Chamilo, SIU, etc.).

---

### Parte 2 – Casos de uso, escenarios, user stories y criterios

1. **Casos de uso (CU-xx)**

   * Listá los casos de uso principales (CU-01, CU-02, …) con breve descripción.
   * Ejemplos:

     * CU-01: Registrar asistencia de una clase.
     * CU-02: Registrar participación del alumno.
     * CU-03: Registrar entrega de trabajo práctico.
     * CU-04: Consultar ficha completa de un alumno.
     * CU-05: Consultar listado de alumnos en riesgo.
   * Para cada caso de uso, describí:

     * Actor(es) involucrados,
     * Precondiciones,
     * Flujo principal,
     * Flujos alternativos (por ejemplo: alumno no existe, clase no encontrada).

2. **User stories (historias de usuario)**

   * Escribí historias de usuario en formato:

     > Como [rol] quiero [acción] para [beneficio].
   * Cubrí a docentes, coordinación y (si tiene sentido) estudiantes.

3. **Criterios de aceptación (Given-When-Then)**

   * Para cada user story importante, agregá criterios de aceptación en estilo BDD:

     * Given (Dado que…)
     * When (Cuando…)
     * Then (Entonces…)

4. **Escenarios de uso relevantes**

   * Escenarios normales (camino feliz).
   * Escenarios con errores (datos faltantes, IDs inexistentes, etc.).
   * Escenarios de riesgo (por ejemplo, alumno con muchas inasistencias).

---

### Parte 3 – Modelo de dominio, API y UML

1. **Modelo de dominio (texto)**

   * Describí las entidades principales y sus responsabilidades:

     * Alumno
     * Curso / Materia
     * Clase (sesión)
     * RegistroAsistencia
     * RegistroParticipacion
     * TrabajoPractico / EntregaTP
     * IndicadorRiesgo o AlertaRiesgo
     * (Opcional) Usuario / Rol para futura autenticación

2. **Diseño de la API**

   * Listá los endpoints principales (ruta, método HTTP, breve descripción).
   * Ejemplo:

     * `POST /alumnos` – crear alumno
     * `GET /alumnos/{id}` – obtener alumno
     * `POST /clases` – crear clase
     * `POST /asistencias` – registrar asistencia
     * etc.
   * Para cada endpoint, indicá:

     * Datos de entrada (JSON esperados)
     * Datos de salida (JSON)
     * Validaciones básicas

3. **Diagramas UML y ER en Mermaid**

   Incluí los siguientes diagramas usando bloques de código en Mermaid:

   * **Diagrama ER (erDiagram)**

     ```mermaid
     erDiagram
       ...
     ```

   * **Diagrama de clases (classDiagram)**

     * Incluir clases de dominio y, si es posible, interfaces de repositorio y servicios.

   * **Diagrama de actividad (flow/activity)**

     * Podés usar `flowchart` en Mermaid para representar el flujo de actividad, por ejemplo:
       “Docente registra asistencia de una clase” de punta a punta.

   * **Diagrama de secuencia (sequenceDiagram)**

     * Al menos para:

       * Registrar asistencia vía API (Docente → API → Servicio → Repositorio → SQLite).
       * Consultar ficha de alumno.

   * **Diagrama de componentes (aproximado)**

     * Usá `flowchart` u otra notación en Mermaid para representar componentes lógicos:

       * Capa API,
       * Capa de servicios,
       * Capa de dominio,
       * Capa de infraestructura (SQLite),
       * Cliente (docente).

---

### Parte 4 – Estructura del proyecto y trazabilidad

1. **Estructura de carpetas propuesta**

   * Ejemplo (ajustalo según tu criterio):

     * `src/domain/...`
     * `src/application/...`
     * `src/infrastructure/...`
     * `src/presentation/api/...`
     * `tests/...`

2. **Descripción de cada capa**

   * Qué tipo de clases/módulos va en cada capa.
   * Cómo se comunican (por ejemplo: API → servicios → repositorios → SQLite).

3. **Matriz de trazabilidad**

   * Creá una tabla que vincule:

     * Requisitos funcionales (RF)
     * Casos de uso (CU)
     * Historias de usuario
     * Endpoints de API
     * (Opcional) posibles tests de aceptación
   * Esto tiene que mostrar claramente cómo cada necesidad se refleja en casos de uso y en endpoints.

4. **Plan de implementación por fases**

   * Fase 1: Modelo de dominio + repositorios + API básica sin login.
   * Fase 2: Cálculo de indicadores de riesgo.
   * Fase 3: Incorporación de login/autenticación y roles.
   * Fase 4: Integraciones externas.

> En esta etapa NO generes todavía código Python. Solo documentación en Markdown, tablas y diagramas Mermaid.

---

## 3️⃣ PROMPT 2 – Código Python POO + SQLite + API

Este actualiza el Prompt 2 para que ya piense en **API**, no CLI.

---

### 🟩 PROMPT 2 – IMPLEMENTACIÓN EN PYTHON + API BASADA EN LA DOCU

Rol: Ahora actuá como Desarrollador/a Senior en Python, respetando la documentación de diseño que te paso a continuación.

[PEGAR AQUÍ la documentación generada con el Prompt 1]

Objetivo:
Generar el código inicial de la aplicación en Python 3, con:

* Arquitectura por capas (`domain`, `application`, `infrastructure`, `presentation/api`).
* **POO** para el modelo de dominio.
* **SQLite** como base de datos local mediante `sqlite3`.
* **API HTTP mínima** para operar con el sistema (crear alumnos, cursos, clases, registrar asistencia, etc.).
* Diseño preparado para migrar a una BBDD externa y, más adelante, agregar login y roles.

Requisitos del código:

1. **Modelo de dominio (domain)**

   * Implementar las clases de dominio según el diagrama de clases (Alumno, Curso, Clase, RegistroAsistencia, etc.).
   * Usar type hints y docstrings aclarando el rol de cada clase en la arquitectura.

2. **Repositorios e infraestructura (infrastructure)**

   * Definir interfaces o clases base de repositorio (por ejemplo `AlumnoRepositoryBase`).
   * Implementar repositorios concretos basados en SQLite con `sqlite3`.
   * Centralizar la creación de la conexión y el esquema (creación de tablas).

3. **Servicios de aplicación (application)**

   * Implementar servicios que ejecuten los casos de uso (registrar asistencia, registrar TP, consultar estado del alumno, etc.).
   * Los servicios deben usar repositorios, no SQL directo.

4. **API (presentation/api)**

   * Implementar una API HTTP mínima.
   * Podés usar un microframework ligero como **FastAPI** para exponer los endpoints, pero manteniendo la lógica desacoplada.
   * Crear endpoints coherentes con el diseño:

     * `POST /alumnos`, `GET /alumnos/{id}`,
     * `POST /cursos`,
     * `POST /clases`,
     * `POST /asistencias`, etc.
   * Hacer que los endpoints llamen a los servicios de aplicación.

5. **Comentarios y justificación de decisiones**

   * En los puntos clave, usar comentarios en español del tipo:

     * `# Decisión de diseño: ...`
       explicando por qué se elige esa estructura, ese patrón o esa separación de responsabilidades.
   * No comentar lo obvio; enfocar los comentarios en decisiones de **arquitectura** y **POO**.

6. **Preparado para Vercel**

   * Estructurar el código para que la API pueda ser desplegada como función serverless (por ejemplo, con FastAPI + adaptador).
   * Aclarar en comentarios qué archivo sería el “entrypoint” en Vercel.

7. **Calidad y estilo**

   * Nombres claros de clases, métodos y variables.
   * Código organizado por módulos (no todo en un solo archivo).
   * Opcional: incluir un par de tests básicos de ejemplo si hay espacio.

Formato de salida:

* Mostrar la estructura de carpetas.
* Luego ir mostrando el contenido de los archivos clave (puede ser resumido si es muy largo, pero manteniendo coherencia).