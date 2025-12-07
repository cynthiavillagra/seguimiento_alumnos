# 📐 Diseño y Requisitos del Sistema

Resumen del diseño inicial y requisitos del Sistema de Seguimiento de Alumnos.

## 🎯 Contexto y Problema

### Problema de Deserción
- **Tasas de deserción:** 40-60% en primeros años de Tecnicaturas Superiores
- **Factores de riesgo:** Inasistencias, bajo rendimiento, falta de participación, problemas personales

### Solución
Seguimiento **clase a clase** para detección temprana de riesgo, permitiendo intervención oportuna antes de que sea irreversible.

---

## 👥 Actores del Sistema

### 1. Docente
- Registra asistencia, participación y TPs
- Consulta estado de alumnos
- Necesita interfaz rápida y simple

### 2. Coordinación de Carrera
- Supervisa estado general
- Detecta alumnos en riesgo
- Genera reportes

### 3. Estudiante (Futuro)
- Consulta su propia ficha
- Recibe notificaciones

---

## ✅ Requisitos Funcionales Principales

### RF-01: Gestión de Alumnos
Registrar, consultar, actualizar y eliminar alumnos.
- Datos: nombre, apellido, DNI, email, cohorte

### RF-02: Gestión de Cursos
Crear y gestionar materias.
- Datos: nombre, año, cuatrimestre, docente

### RF-03: Gestión de Clases
Crear sesiones de cursada.
- Datos: curso, fecha, número, tema

### RF-04: Registro de Asistencia
Registrar asistencia por clase.
- Estados: Presente, Ausente, Tardanza, Justificada

### RF-05: Registro de Participación
Registrar participación en clase.
- Niveles: Ninguna, Baja, Media, Alta

### RF-06: Trabajos Prácticos
Definir TPs y registrar entregas.
- Datos: título, descripción, fecha entrega
- Registro: entregado/no entregado, nota, tardía

### RF-07: Ficha de Alumno
Mostrar ficha completa con historial.
- Datos personales, cursos, asistencias, participación, TPs, indicadores

### RF-08: Indicadores de Riesgo
Calcular automáticamente indicadores.
- % asistencia, % participación, % TPs entregados
- Nivel de riesgo: Bajo, Medio, Alto

### RF-09: Alertas
Generar alertas automáticas.
- Inasistencias > umbral
- Falta de participación
- TPs no entregados
- 2 faltas consecutivas

### RF-10: Listados
Consultar listados filtrados.
- Por curso, en riesgo, asistencias, entregas

---

## 🔧 Requisitos No Funcionales

### RNF-01: Facilidad de Uso
Interfaz intuitiva para docentes con diferentes niveles tecnológicos.

### RNF-02: Código Mantenible
- Arquitectura por capas
- POO con responsabilidades claras
- Comentarios didácticos
- Type hints

### RNF-03: Arquitectura Modular
- Dominio independiente de infraestructura
- Bajo acoplamiento
- Servicios de aplicación

### RNF-04: Persistencia
- MVP: SQLite local
- Migrado a: PostgreSQL (Neon)

### RNF-05: Despliegue
- Compatible con Vercel Serverless
- Estructura en carpeta `api/`

### RNF-06: Seguridad
- Validación de datos
- Prevención de SQL injection
- Preparado para autenticación JWT

### RNF-07: Rendimiento
- Consultas < 500ms
- Registro de clase < 2s
- Índices en campos clave

---

## 📊 Alcance del MVP (Implementado)

### ✅ Funcionalidades Core
- [x] Registro de alumnos, cursos, clases
- [x] Asistencia (presente/ausente/tarde)
- [x] Participación (alta/media/baja/nula)
- [x] Trabajos prácticos y entregas
- [x] Notas de TPs (1-10)
- [x] Actitud (excelente/buena/regular/mala)
- [x] Indicadores de riesgo automáticos
- [x] Alertas (2 faltas consecutivas, asistencia < 70%)
- [x] Ficha completa de alumno
- [x] Dashboard multi-clase

### ✅ Arquitectura
- [x] Python 3.12 puro (POO)
- [x] PostgreSQL (Neon)
- [x] API REST con BaseHTTPRequestHandler
- [x] Frontend SPA (Vanilla JS)
- [x] Desplegado en Vercel
- [x] Código en GitHub

---

## 🔮 Futuras Iteraciones

### Iteración 2: Autenticación
- Login completo (JWT)
- Roles: Docente, Coordinación, Estudiante
- Permisos por rol (RBAC)

### Iteración 3: Funcionalidades Avanzadas
- Notificaciones automáticas (email/SMS)
- Reportes y gráficos avanzados
- Exportación a PDF/Excel
- Predicción de riesgo con ML

### Iteración 4: Integraciones
- Integración con Moodle/Chamilo
- Integración con SIU Guaraní
- API pública

### Iteración 5: Analítica
- Dashboard de analítica institucional
- Comparación entre cohortes
- Identificación de patrones
- Recomendaciones automáticas

---

## 🏗️ Arquitectura Implementada

### Stack Tecnológico
```
Frontend (SPA)
  ↓ HTTP/JSON
Vercel (Hosting + Routing)
  ↓
Backend (Python 3.12)
  ↓ SQL
PostgreSQL (Neon)
```

### Capas
1. **Presentation:** `api/index.py` (API REST)
2. **Application:** Lógica de negocio
3. **Domain:** Modelos de datos
4. **Infrastructure:** `api/db.py` (PostgreSQL)

---

## 📋 Casos de Uso Principales

### CU-01: Registrar Clase
**Actor:** Docente  
**Flujo:**
1. Selecciona materia y cohorte
2. Ingresa fecha y tema
3. Para cada alumno marca:
   - Asistencia
   - Participación
   - TP entregado + nota
   - Actitud
   - Observaciones
4. Guarda registro

### CU-02: Consultar Ficha de Alumno
**Actor:** Docente/Coordinación  
**Flujo:**
1. Busca alumno
2. Ve historial completo
3. Analiza indicadores
4. Identifica alertas

### CU-03: Ver Alertas
**Actor:** Coordinación  
**Flujo:**
1. Accede a dashboard de alertas
2. Ve alumnos en riesgo
3. Filtra por tipo de alerta
4. Toma acción (contacto, tutoría)

---

## 🎯 Indicadores de Riesgo

### Cálculo Automático
```
Riesgo = f(asistencia, participación, TPs, actitud)

Nivel Alto si:
- Asistencia < 70%
- 2 faltas consecutivas
- TPs entregados < 50%
- Participación = Nula en > 50% clases
```

### Alertas Generadas
1. **2 Faltas Consecutivas** (nivel: alto)
2. **Asistencia < 70%** (nivel: medio)
3. **TPs no entregados** (nivel: medio)
4. **Baja participación** (nivel: bajo)

---

## 📚 Modelo de Datos

### Entidades Principales
- **Alumno:** id, nombre, apellido, dni, email, cohorte
- **Curso:** id, materia, año, cuatrimestre, docente
- **Clase:** id, curso_id, fecha, número, tema
- **Registro_Asistencia:** id, alumno_id, clase_id, estado
- **Registro_Participacion:** id, alumno_id, clase_id, nivel
- **Trabajo_Practico:** id, curso_id, título, descripción, fecha_entrega
- **Entrega_TP:** id, tp_id, alumno_id, entregado, nota, tardía
- **Registro_Actitud:** id, alumno_id, clase_id, actitud

### Vistas
- **vista_resumen_asistencias:** Estadísticas por alumno/curso
- **vista_resumen_tps:** Estadísticas de TPs por alumno/curso

---

## 🔗 Referencias

Para más detalles técnicos:
- **Arquitectura actual:** Ver `ARQUITECTURA.md`
- **Guía de uso:** Ver `GUIA_USO_COMPLETA.md`
- **Implementación PostgreSQL:** Ver `IMPLEMENTACION_POSTGRES.md`

---

**Nota:** Este documento resume el diseño inicial. El sistema ha evolucionado desde entonces. Para estado actual, consulta la documentación principal.
