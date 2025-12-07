# 📚 Documentación Completa - Sistema de Seguimiento de Alumnos

## Índice de Documentos

### 1. [Contexto y Requisitos](./01_CONTEXTO_Y_REQUISITOS.md)
**Contenido**:
- Contexto del problema de deserción en Tecnicaturas Superiores
- Objetivos del sistema
- Actores y stakeholders
- Requisitos funcionales (RF-01 a RF-11 + RF-API-01 a RF-API-11)
- Requisitos no funcionales (RNF-01 a RNF-09)
- Alcance del MVP vs futuras iteraciones

**Para quién**: Todos los stakeholders, especialmente coordinación y dirección

---

### 2. [Casos de Uso, User Stories y Criterios de Aceptación](./02_CASOS_DE_USO_Y_STORIES.md)
**Contenido**:
- 10 casos de uso detallados (CU-01 a CU-10)
- 9 user stories (US-01 a US-09)
- Criterios de aceptación en formato BDD (Given-When-Then)
- Escenarios de uso relevantes (normales, errores, riesgo)

**Para quién**: Equipo de desarrollo, QA, product owners

---

### 3. [Modelo de Dominio, API y Diagramas UML](./03_MODELO_Y_API.md)
**Contenido**:
- Descripción textual del modelo de dominio (9 entidades principales)
- Diseño completo de la API REST:
  - 25+ endpoints documentados
  - Request/Response schemas
  - Validaciones y errores
- Diagramas UML en Mermaid:
  - Diagrama ER (Entidad-Relación)
  - Diagrama de Clases (Dominio)
  - Diagrama de Clases (Arquitectura Completa)
  - Diagramas de Secuencia (2)
  - Diagrama de Actividad
  - Diagrama de Componentes

**Para quién**: Arquitectos, desarrolladores, diseñadores de BD

---

### 4. [Estructura del Proyecto y Trazabilidad](./04_ESTRUCTURA_Y_TRAZABILIDAD.md)
**Contenido**:
- Estructura de carpetas completa del proyecto
- Descripción detallada de cada capa (Domain, Application, Infrastructure, Presentation)
- Ejemplos de código para cada capa
- Comunicación entre capas y flujo de requests
- **Matriz de trazabilidad completa**: RF → CU → US → Endpoints → Tests
- Plan de implementación por fases (7 fases)
- Resumen de decisiones de arquitectura

**Para quién**: Desarrolladores, arquitectos, tech leads

---

## Resumen Ejecutivo

### ¿Qué es este sistema?

Una aplicación de seguimiento de alumnos para Tecnicaturas Superiores que permite:
- Registrar asistencia, participación y entregas de trabajos prácticos clase por clase
- Calcular automáticamente indicadores de riesgo de deserción
- Generar alertas tempranas para intervención oportuna
- Consultar fichas completas de alumnos con todo su historial

### ¿Por qué es necesario?

- **Problema**: 40-60% de deserción en los primeros años de Tecnicaturas
- **Causa**: Detección tardía de estudiantes en riesgo
- **Solución**: Seguimiento continuo con indicadores objetivos y alertas automáticas

### Arquitectura

```
┌─────────────────────────────────────────────┐
│  🖥️  Cliente (Docente/Coordinación)         │
└───────────────────┬─────────────────────────┘
                    │ HTTP/JSON
┌───────────────────▼─────────────────────────┐
│  📡 API (FastAPI)                            │
│  - Endpoints REST                            │
│  - Validación con Pydantic                   │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│  ⚙️  Servicios de Aplicación                │
│  - Casos de uso                              │
│  - Orquestación                              │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│  🎯 Dominio                                  │
│  - Entidades (Alumno, Curso, etc.)           │
│  - Reglas de negocio                         │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│  🗄️  Repositorios (SQLite)                  │
│  - Persistencia                              │
│  - Acceso a datos                            │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│  💾 SQLite Database                          │
└─────────────────────────────────────────────┘
```

### Tecnologías

- **Backend**: Python 3.11+
- **Framework Web**: FastAPI
- **Base de Datos (MVP)**: SQLite
- **Validación**: Pydantic
- **Despliegue**: Vercel (serverless)
- **Versionado**: Git/GitHub

### Entidades Principales

1. **Alumno**: Estudiante de la institución
2. **Curso**: Materia en un período específico
3. **Clase**: Sesión de cursada
4. **RegistroAsistencia**: Asistencia de un alumno a una clase
5. **RegistroParticipacion**: Participación de un alumno en una clase
6. **TrabajoPractico**: TP asignado a un curso
7. **EntregaTP**: Entrega de un TP por un alumno
8. **IndicadorRiesgo**: Indicadores calculados de riesgo de deserción

### Indicadores de Riesgo

El sistema calcula automáticamente:

- **Porcentaje de Asistencia**: (Presentes + Tardanzas + Justificadas) / Total Clases
- **Porcentaje de Participación**: Nivel promedio de participación
- **Porcentaje de TPs Entregados**: TPs entregados / Total TPs
- **Nivel de Riesgo**: Bajo | Medio | Alto (basado en umbrales)

**Umbrales de Riesgo**:
- **Bajo**: Asistencia ≥ 80%, TPs ≥ 70%, Participación ≥ Media
- **Medio**: Asistencia 70-79%, TPs 50-69%, Participación Baja
- **Alto**: Asistencia < 70%, TPs < 50%, Participación Ninguna sostenida

### Endpoints Principales (MVP)

#### Alumnos
- `POST /alumnos` - Crear alumno
- `GET /alumnos/{id}` - Obtener alumno
- `GET /alumnos` - Listar alumnos
- `GET /alumnos/{id}/ficha` - Ficha completa con indicadores

#### Cursos
- `POST /cursos` - Crear curso
- `GET /cursos/{id}` - Obtener curso
- `GET /cursos/{curso_id}/alumnos` - Listar alumnos del curso
- `GET /cursos/{curso_id}/indicadores` - Estadísticas del curso

#### Clases
- `POST /clases` - Crear clase
- `GET /clases/{id}` - Obtener clase
- `GET /cursos/{curso_id}/clases` - Listar clases del curso

#### Asistencia
- `POST /asistencias` - Registrar asistencia (uno o varios alumnos)
- `GET /clases/{clase_id}/asistencias` - Listar asistencias de una clase
- `PUT /asistencias/{id}` - Modificar asistencia

#### Participación
- `POST /participaciones` - Registrar participación
- `GET /clases/{clase_id}/participaciones` - Listar participaciones de una clase

#### Trabajos Prácticos
- `POST /trabajos-practicos` - Crear TP
- `GET /trabajos-practicos/{id}` - Obtener TP
- `POST /entregas-tp` - Registrar entrega
- `GET /trabajos-practicos/{tp_id}/entregas` - Listar entregas de un TP

#### Alertas
- `GET /alertas/alumnos-en-riesgo` - Listar alumnos en riesgo (con filtros)

### Fases de Implementación

| Fase | Descripción | Duración | Estado |
|------|-------------|----------|--------|
| **1** | MVP Core (Dominio + API + SQLite) | 2-3 semanas | 🔄 En progreso |
| **2** | Indicadores y Alertas | 1-2 semanas | ⏳ Pendiente |
| **3** | Preparación para Vercel | 1 semana | ⏳ Pendiente |
| **4** | Autenticación y Roles | 2-3 semanas | 🔮 Futuro |
| **5** | Frontend Web | 4-6 semanas | 🔮 Futuro |
| **6** | Funcionalidades Avanzadas | Variable | 🔮 Futuro |
| **7** | Migración a PostgreSQL | 2-3 semanas | 🔮 Futuro |

### Próximos Pasos

1. ✅ **Documentación completa** (este documento)
2. 🔄 **Implementación del código Python** (Prompt 2)
3. ⏳ **Tests unitarios y de integración**
4. ⏳ **Despliegue en Vercel**
5. 🔮 **Iteraciones futuras**

---

## Cómo Navegar Esta Documentación

### Si eres Docente o Coordinador/a:
👉 Lee [01_CONTEXTO_Y_REQUISITOS.md](./01_CONTEXTO_Y_REQUISITOS.md) y [02_CASOS_DE_USO_Y_STORIES.md](./02_CASOS_DE_USO_Y_STORIES.md)

### Si eres Desarrollador/a:
👉 Lee todos los documentos en orden, especialmente [04_ESTRUCTURA_Y_TRAZABILIDAD.md](./04_ESTRUCTURA_Y_TRAZABILIDAD.md)

### Si eres Arquitecto/a:
👉 Enfócate en [03_MODELO_Y_API.md](./03_MODELO_Y_API.md) y [04_ESTRUCTURA_Y_TRAZABILIDAD.md](./04_ESTRUCTURA_Y_TRAZABILIDAD.md)

### Si eres QA/Tester:
👉 Lee [02_CASOS_DE_USO_Y_STORIES.md](./02_CASOS_DE_USO_Y_STORIES.md) (criterios de aceptación) y la matriz de trazabilidad en [04_ESTRUCTURA_Y_TRAZABILIDAD.md](./04_ESTRUCTURA_Y_TRAZABILIDAD.md)

---

## Contacto y Contribuciones

Este proyecto es de código abierto y está diseñado con fines educativos y de mejora continua de la educación superior.

**Repositorio**: [GitHub - App Seguimiento Alumnos](https://github.com/tu-usuario/app-seguimiento-alumnos) _(pendiente)_

**Licencia**: MIT _(pendiente definir)_

---

**Última actualización**: 2025-12-07  
**Versión de la documentación**: 1.0.0
