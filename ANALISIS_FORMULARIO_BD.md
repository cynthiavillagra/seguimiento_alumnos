# 🔍 Análisis: Formulario vs Base de Datos

## ❌ PROBLEMAS ENCONTRADOS

### Problema Principal
Los campos del formulario de registro **NO coinciden** exactamente con la estructura de la base de datos PostgreSQL.

---

## 📊 Comparación Detallada

### 1. ✅ ASISTENCIA - COINCIDE

#### Formulario
```javascript
asistencia: 'presente' | 'ausente' | 'tarde'
```

#### Base de Datos
```sql
estado VARCHAR(20) CHECK (estado IN ('Presente', 'Ausente', 'Tardanza', 'Justificada'))
```

#### ⚠️ PROBLEMA
- Formulario usa: `'tarde'`
- BD espera: `'Tardanza'`
- Falta en formulario: `'Justificada'`

#### ✅ SOLUCIÓN
```javascript
// Cambiar en app.js
asistencia: 'Presente' | 'Ausente' | 'Tardanza' | 'Justificada'
```

---

### 2. ✅ PARTICIPACIÓN - COINCIDE

#### Formulario
```javascript
participacion: 'alta' | 'media' | 'baja' | 'nula'
```

#### Base de Datos
```sql
nivel VARCHAR(20) CHECK (nivel IN ('Ninguna', 'Baja', 'Media', 'Alta'))
```

#### ⚠️ PROBLEMA
- Formulario usa minúsculas: `'alta'`, `'media'`, `'baja'`, `'nula'`
- BD espera mayúsculas: `'Alta'`, `'Media'`, `'Baja'`, `'Ninguna'`
- Formulario usa: `'nula'`
- BD espera: `'Ninguna'`

#### ✅ SOLUCIÓN
```javascript
// Cambiar en app.js
participacion: 'Alta' | 'Media' | 'Baja' | 'Ninguna'
```

---

### 3. ✅ ACTITUD - COINCIDE

#### Formulario
```javascript
actitud: 'excelente' | 'buena' | 'regular' | 'mala'
```

#### Base de Datos
```sql
actitud VARCHAR(20) CHECK (actitud IN ('Excelente', 'Buena', 'Regular', 'Mala'))
```

#### ⚠️ PROBLEMA
- Formulario usa minúsculas: `'excelente'`, `'buena'`, `'regular'`, `'mala'`
- BD espera mayúsculas: `'Excelente'`, `'Buena'`, `'Regular'`, `'Mala'`

#### ✅ SOLUCIÓN
```javascript
// Cambiar en app.js
actitud: 'Excelente' | 'Buena' | 'Regular' | 'Mala'
```

---

### 4. ⚠️ TRABAJO PRÁCTICO - ESTRUCTURA DIFERENTE

#### Formulario
```javascript
{
  tpEntregado: true | false,
  notaTP: 8.5  // número
}
```

#### Base de Datos
```sql
CREATE TABLE entrega_tp (
    trabajo_practico_id INTEGER NOT NULL,  -- ⚠️ FALTA EN FORMULARIO
    alumno_id INTEGER NOT NULL,
    fecha_entrega_real DATE,               -- ⚠️ FALTA EN FORMULARIO
    entregado BOOLEAN NOT NULL DEFAULT FALSE,
    nota DECIMAL(4,2),
    es_tardia BOOLEAN NOT NULL DEFAULT FALSE,  -- ⚠️ FALTA EN FORMULARIO
    ...
)
```

#### ⚠️ PROBLEMAS
1. **Falta `trabajo_practico_id`**: El formulario no pregunta QUÉ TP se entregó
2. **Falta `fecha_entrega_real`**: No se registra cuándo se entregó
3. **Falta `es_tardia`**: No se marca si es tardía

#### ✅ SOLUCIÓN
El formulario necesita:
1. Un select para elegir el TP
2. Fecha de entrega (opcional, usar fecha de la clase)
3. Checkbox para marcar si es tardía

---

### 5. ✅ CLASE - FALTA INFORMACIÓN

#### Formulario Actual
```javascript
{
  materia: '',
  cohorte: '',
  fecha: '',
  tema: ''
}
```

#### Base de Datos
```sql
CREATE TABLE clase (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL,  -- ⚠️ FALTA EN FORMULARIO
    fecha DATE NOT NULL,
    numero_clase INTEGER NOT NULL,  -- ⚠️ FALTA EN FORMULARIO
    tema TEXT,
    ...
)
```

#### ⚠️ PROBLEMAS
1. **Falta `curso_id`**: El formulario usa materia+cohorte pero debería usar el ID del curso
2. **Falta `numero_clase`**: No se auto-incrementa el número de clase

---

## 🔧 CORRECCIONES NECESARIAS

### Archivo: `public/app.js`

#### 1. Corregir Valores de Asistencia
```javascript
// ❌ ANTES
function marcarAsistencia(alumnoId, estado) {
    // estado: 'presente', 'ausente', 'tarde'
}

// ✅ DESPUÉS
function marcarAsistencia(alumnoId, estado) {
    // estado: 'Presente', 'Ausente', 'Tardanza', 'Justificada'
    const estadosValidos = ['Presente', 'Ausente', 'Tardanza', 'Justificada'];
    if (!estadosValidos.includes(estado)) {
        console.error('Estado inválido:', estado);
        return;
    }
    // ...
}
```

#### 2. Corregir Valores de Participación
```javascript
// ❌ ANTES
function marcarParticipacion(alumnoId, nivel) {
    // nivel: 'alta', 'media', 'baja', 'nula'
}

// ✅ DESPUÉS
function marcarParticipacion(alumnoId, nivel) {
    // nivel: 'Alta', 'Media', 'Baja', 'Ninguna'
    const nivelesValidos = ['Alta', 'Media', 'Baja', 'Ninguna'];
    if (!nivelesValidos.includes(nivel)) {
        console.error('Nivel inválido:', nivel);
        return;
    }
    // ...
}
```

#### 3. Corregir Valores de Actitud
```javascript
// ❌ ANTES
function marcarActitud(alumnoId, actitud) {
    // actitud: 'excelente', 'buena', 'regular', 'mala'
}

// ✅ DESPUÉS
function marcarActitud(alumnoId, actitud) {
    // actitud: 'Excelente', 'Buena', 'Regular', 'Mala'
    const actitudesValidas = ['Excelente', 'Buena', 'Regular', 'Mala'];
    if (!actitudesValidas.includes(actitud)) {
        console.error('Actitud inválida:', actitud);
        return;
    }
    // ...
}
```

#### 4. Agregar Campos de TP
```javascript
// ❌ ANTES
state.claseActual.registros[alumnoId] = {
    tpEntregado: null,
    notaTP: null
};

// ✅ DESPUÉS
state.claseActual.registros[alumnoId] = {
    trabajoPracticoId: null,  // ⭐ NUEVO: ID del TP
    tpEntregado: false,
    notaTP: null,
    fechaEntregaReal: null,   // ⭐ NUEVO: Fecha de entrega
    esTardia: false           // ⭐ NUEVO: Si es tardía
};
```

---

## 📝 RESUMEN DE CAMBIOS NECESARIOS

### Prioridad ALTA (Crítico)

1. ✅ **Cambiar valores de asistencia**
   - `'tarde'` → `'Tardanza'`
   - Agregar `'Justificada'`

2. ✅ **Cambiar valores de participación**
   - Usar mayúsculas: `'Alta'`, `'Media'`, `'Baja'`
   - `'nula'` → `'Ninguna'`

3. ✅ **Cambiar valores de actitud**
   - Usar mayúsculas: `'Excelente'`, `'Buena'`, `'Regular'`, `'Mala'`

### Prioridad MEDIA (Importante)

4. ✅ **Agregar campos de TP**
   - `trabajoPracticoId` - Select para elegir TP
   - `fechaEntregaReal` - Fecha de entrega
   - `esTardia` - Checkbox si es tardía

5. ✅ **Agregar campos de clase**
   - `cursoId` - ID del curso (en lugar de materia+cohorte)
   - `numeroClase` - Auto-incrementar

---

## 🚀 PLAN DE ACCIÓN

### Paso 1: Corregir Valores (15 min)
- Actualizar `app.js` con valores en mayúsculas
- Actualizar HTML con valores correctos

### Paso 2: Agregar Campos de TP (30 min)
- Agregar select de TPs en el formulario
- Agregar checkbox "Entrega tardía"
- Actualizar lógica de guardado

### Paso 3: Probar (10 min)
- Crear clase de prueba
- Registrar asistencia
- Verificar que se guarda en BD

### Paso 4: Desplegar (5 min)
- `git add .`
- `git commit -m "fix: Match form values with database schema"`
- `git push`

---

## ⚠️ IMPACTO

### Si NO se corrige:
- ❌ Los datos NO se guardarán en la BD
- ❌ Errores de validación de CHECK constraints
- ❌ Inconsistencia entre frontend y backend

### Si se corrige:
- ✅ Datos se guardan correctamente
- ✅ Validaciones funcionan
- ✅ Sistema completo funcional

---

**¿Quieres que corrija estos problemas ahora?** 🔧
