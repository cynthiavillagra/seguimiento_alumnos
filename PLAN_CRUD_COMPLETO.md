# 🚀 CRUD Completo - Plan de Implementación

## 🎯 Objetivo

Implementar funcionalidad completa de **Crear, Leer, Actualizar y Eliminar** (CRUD) para:
- ✅ Alumnos
- ✅ Cursos/Materias
- ✅ Trabajos Prácticos
- ✅ Clases

**PLUS:** Corregir valores del formulario de registro para que coincidan con la BD.

---

## 📋 Funcionalidades a Implementar

### 1. CRUD de Alumnos

#### CREATE ✅ (Ya existe)
- Modal para crear alumno
- POST /alumnos

#### READ ✅ (Ya existe)
- GET /alumnos
- Lista de alumnos

#### UPDATE ⭐ NUEVO
- Modal para editar alumno
- PUT /alumnos/{id}
- Botón "Editar" en cada alumno

#### DELETE ⭐ NUEVO
- Confirmación antes de borrar
- DELETE /alumnos/{id}
- Botón "Eliminar" en cada alumno

---

### 2. CRUD de Cursos

#### CREATE ✅ (Ya existe)
- Modal para crear curso
- POST /cursos

#### READ ✅ (Ya existe)
- GET /cursos
- Dashboard de cursos

#### UPDATE ⭐ NUEVO
- Modal para editar curso
- PUT /cursos/{id}
- Botón "Editar" en tarjeta de curso

#### DELETE ⭐ NUEVO
- Confirmación antes de borrar
- DELETE /cursos/{id}
- Botón "Eliminar" en tarjeta de curso

---

### 3. CRUD de Trabajos Prácticos

#### CREATE ✅ (Ya existe)
- Modal para crear TP
- POST /trabajos-practicos

#### READ ⭐ NUEVO
- GET /trabajos-practicos?curso_id={id}
- Lista de TPs por curso

#### UPDATE ⭐ NUEVO
- Modal para editar TP
- PUT /trabajos-practicos/{id}
- Botón "Editar" en cada TP

#### DELETE ⭐ NUEVO
- Confirmación antes de borrar
- DELETE /trabajos-practicos/{id}
- Botón "Eliminar" en cada TP

---

### 4. CRUD de Clases

#### CREATE ⭐ NUEVO
- Formulario para crear clase
- POST /clases
- Campos: curso_id, fecha, numero_clase, tema

#### READ ⭐ NUEVO
- GET /clases?curso_id={id}
- Lista de clases por curso

#### UPDATE ⭐ NUEVO
- Modal para editar clase
- PUT /clases/{id}

#### DELETE ⭐ NUEVO
- Confirmación antes de borrar
- DELETE /clases/{id}

---

## 🔧 Correcciones de Registro

### Valores a Corregir

#### Asistencia
```javascript
// ❌ ANTES
'presente', 'ausente', 'tarde'

// ✅ DESPUÉS
'Presente', 'Ausente', 'Tardanza', 'Justificada'
```

#### Participación
```javascript
// ❌ ANTES
'alta', 'media', 'baja', 'nula'

// ✅ DESPUÉS
'Alta', 'Media', 'Baja', 'Ninguna'
```

#### Actitud
```javascript
// ❌ ANTES
'excelente', 'buena', 'regular', 'mala'

// ✅ DESPUÉS
'Excelente', 'Buena', 'Regular', 'Mala'
```

---

## 📝 API Endpoints a Implementar

### Backend (api/index.py)

```python
# ALUMNOS
GET    /alumnos           # ✅ Ya existe
POST   /alumnos           # ✅ Ya existe
PUT    /alumnos/{id}      # ⭐ NUEVO
DELETE /alumnos/{id}      # ⭐ NUEVO

# CURSOS
GET    /cursos            # ✅ Ya existe
POST   /cursos            # ✅ Ya existe
PUT    /cursos/{id}       # ⭐ NUEVO
DELETE /cursos/{id}       # ⭐ NUEVO

# TRABAJOS PRÁCTICOS
GET    /trabajos-practicos              # ⭐ NUEVO
GET    /trabajos-practicos?curso_id=1   # ⭐ NUEVO
POST   /trabajos-practicos              # ✅ Ya existe
PUT    /trabajos-practicos/{id}         # ⭐ NUEVO
DELETE /trabajos-practicos/{id}         # ⭐ NUEVO

# CLASES
GET    /clases?curso_id=1   # ⭐ NUEVO
POST   /clases              # ⭐ NUEVO
PUT    /clases/{id}         # ⭐ NUEVO
DELETE /clases/{id}         # ⭐ NUEVO
```

---

## 🎨 UI a Implementar

### 1. Página de Gestión de Curso

```
┌─────────────────────────────────────────┐
│ Programación I - 2024                   │
│ [Editar Curso] [Eliminar Curso]         │
├─────────────────────────────────────────┤
│ 📚 Trabajos Prácticos                   │
│ ┌─────────────────────────────────────┐ │
│ │ TP1 - Variables  [Editar] [Borrar] │ │
│ │ TP2 - Funciones  [Editar] [Borrar] │ │
│ └─────────────────────────────────────┘ │
│ [+ Nuevo TP]                            │
├─────────────────────────────────────────┤
│ 📅 Clases Dictadas                      │
│ ┌─────────────────────────────────────┐ │
│ │ Clase 1 - 01/12  [Editar] [Borrar] │ │
│ │ Clase 2 - 05/12  [Editar] [Borrar] │ │
│ └─────────────────────────────────────┘ │
│ [+ Nueva Clase]                         │
├─────────────────────────────────────────┤
│ 👥 Alumnos Inscriptos                   │
│ ┌─────────────────────────────────────┐ │
│ │ Pérez, Juan      [Ver] [Desinscribir]│
│ │ García, Ana      [Ver] [Desinscribir]│
│ └─────────────────────────────────────┘ │
│ [+ Inscribir Alumno]                    │
└─────────────────────────────────────────┘
```

### 2. Lista de Alumnos con Acciones

```
┌─────────────────────────────────────────┐
│ Alumnos                                  │
├─────────────────────────────────────────┤
│ Pérez, Juan - DNI: 12345678             │
│ juan@example.com                         │
│ [Ver Ficha] [Editar] [Eliminar]         │
├─────────────────────────────────────────┤
│ García, Ana - DNI: 23456789             │
│ ana@example.com                          │
│ [Ver Ficha] [Editar] [Eliminar]         │
└─────────────────────────────────────────┘
```

---

## 🔄 Flujo de Trabajo

### Editar Alumno
1. Click en "Editar" → Abre modal
2. Modal pre-cargado con datos actuales
3. Usuario modifica campos
4. Click en "Guardar" → PUT /alumnos/{id}
5. Toast de confirmación
6. Recarga lista

### Eliminar Alumno
1. Click en "Eliminar" → Modal de confirmación
2. "¿Estás seguro? Esta acción no se puede deshacer"
3. Click en "Sí, eliminar" → DELETE /alumnos/{id}
4. Toast de confirmación
5. Recarga lista

---

## 📦 Archivos a Modificar/Crear

### Backend
- ✅ `api/index.py` - Agregar endpoints PUT y DELETE
- ✅ `api/db.py` - Agregar función execute_update y execute_delete

### Frontend
- ✅ `public/index.html` - Agregar modales de edición
- ✅ `public/app.js` - Agregar funciones CRUD
- ✅ `public/styles.css` - Estilos para botones de acción

### Configuración
- ✅ `vercel.json` - Ya está configurado

---

## ⏱️ Estimación de Tiempo

- Backend (API endpoints): 30 min
- Frontend (UI + funciones): 45 min
- Correcciones de registro: 15 min
- Testing: 15 min
- **Total: ~2 horas**

---

## 🚀 Orden de Implementación

### Fase 1: Backend (30 min)
1. Agregar execute_update y execute_delete en db.py
2. Implementar PUT y DELETE para alumnos
3. Implementar PUT y DELETE para cursos
4. Implementar PUT y DELETE para TPs
5. Implementar CRUD de clases

### Fase 2: Correcciones de Registro (15 min)
1. Corregir valores de asistencia
2. Corregir valores de participación
3. Corregir valores de actitud

### Fase 3: Frontend CRUD (45 min)
1. Modales de edición
2. Funciones de actualización
3. Confirmaciones de eliminación
4. Botones de acción en listas

### Fase 4: Testing y Deploy (15 min)
1. Probar cada operación
2. Verificar en BD
3. Deploy a Vercel

---

**¿Empezamos con la Fase 1 (Backend)?** 🚀
