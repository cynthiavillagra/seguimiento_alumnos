# 📋 Casos de Uso Reales - Flujo del Docente

## 🎯 Escenario Principal

**Como docente**, durante la clase necesito:

### 1. Antes de la Clase
- Seleccionar la materia/curso
- Ver la lista completa de alumnos inscriptos
- Ver el historial de clases anteriores

### 2. Durante la Clase (Registro en Tiempo Real)
- **Tomar asistencia** - Marcar presente/ausente/tarde para cada alumno
- **Registrar participación** - Marcar nivel (alta/media/baja/nula) por alumno
- **Anotar observaciones** - Comentarios específicos por alumno
- **Ver quién falta** - Identificar rápidamente ausentes
- **Guardar todo** - Al finalizar la clase

### 3. Después de la Clase
- **Ver resumen** - Estadísticas de la clase
- **Revisar alertas** - Alumnos que necesitan atención
- **Ver histórico** - Evolución de cada alumno

### 4. Análisis Individual
- **Ficha del alumno** - Ver todo su historial
- **Filtrar por fechas** - Ver período específico
- **Ver indicadores** - Riesgo de deserción
- **Exportar datos** - Para informes

## 🎨 Interfaz Necesaria

### Vista 1: Selección de Clase
```
┌─────────────────────────────────────┐
│ Seleccionar Materia y Clase        │
├─────────────────────────────────────┤
│ Materia: [Programación I ▼]        │
│ Cohorte: [2024 ▼]                  │
│ Fecha:   [07/12/2024]              │
│                                     │
│ [Iniciar Registro de Clase]        │
└─────────────────────────────────────┘
```

### Vista 2: Registro Durante la Clase
```
┌──────────────────────────────────────────────────────┐
│ Programación I - Cohorte 2024 - 07/12/2024          │
├──────────────────────────────────────────────────────┤
│ Alumno              │ Asist. │ Partic. │ Obs.       │
├──────────────────────────────────────────────────────┤
│ García, Ana         │ [✓][✗] │ [A][M][B][N] │ [...]│
│ López, Carlos       │ [✓][✗] │ [A][M][B][N] │ [...]│
│ Martínez, Juan      │ [✓][✗] │ [A][M][B][N] │ [...]│
│ ...                 │        │              │       │
├──────────────────────────────────────────────────────┤
│ Presentes: 25/30    Ausentes: 5                     │
│                                                       │
│ [Guardar y Finalizar Clase]                         │
└──────────────────────────────────────────────────────┘
```

### Vista 3: Ficha Individual del Alumno
```
┌──────────────────────────────────────────────────────┐
│ García, Ana - DNI: 12345678                          │
├──────────────────────────────────────────────────────┤
│ 🚨 ALERTA: Riesgo Alto de Deserción                 │
├──────────────────────────────────────────────────────┤
│ Filtros: [Desde: 01/09/24] [Hasta: 07/12/24]       │
├──────────────────────────────────────────────────────┤
│ INDICADORES                                          │
│ • Asistencia:     55% (11/20 clases) 🔴             │
│ • Participación:  Baja                🔴             │
│ • TPs Entregados: 40% (4/10)         🔴             │
├──────────────────────────────────────────────────────┤
│ HISTORIAL DE CLASES                                  │
│ 07/12 - Presente - Participación: Media              │
│ 05/12 - Ausente                                      │
│ 30/11 - Presente - Participación: Baja               │
│ ...                                                   │
├──────────────────────────────────────────────────────┤
│ [Exportar PDF] [Enviar Alerta] [Registrar Contacto]│
└──────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Trabajo Completo

### Paso 1: Inicio de Clase
1. Docente abre la app
2. Selecciona materia y cohorte
3. Sistema muestra lista de alumnos inscriptos
4. Click en "Iniciar Registro"

### Paso 2: Durante la Clase
1. Por cada alumno:
   - ✓ Marcar presente/ausente
   - ✓ Marcar nivel de participación
   - ✓ Agregar observación (opcional)
2. Ver contador de presentes/ausentes en tiempo real
3. Click en "Guardar y Finalizar"

### Paso 3: Después de la Clase
1. Sistema calcula automáticamente:
   - % de asistencia de cada alumno
   - Tendencias de participación
   - Alertas de riesgo
2. Docente puede:
   - Ver resumen de la clase
   - Revisar alertas generadas
   - Acceder a fichas individuales

### Paso 4: Análisis Individual
1. Click en un alumno específico
2. Ver toda su información:
   - Datos personales
   - Indicadores de riesgo
   - Historial completo
3. Filtrar por fechas
4. Exportar o tomar acciones

## 🎯 Funcionalidades Clave

### Registro Rápido
- ✅ Interfaz tipo checklist
- ✅ Botones grandes para tocar en tablet
- ✅ Guardado automático
- ✅ Funciona offline (sync después)

### Alertas Automáticas
- 🚨 Riesgo Alto: < 60% asistencia o < 50% TPs
- ⚠️ Riesgo Medio: 60-75% asistencia o 50-70% TPs
- ℹ️ Seguimiento: Tendencia negativa

### Reportes
- 📊 Por alumno (individual)
- 📈 Por clase (grupal)
- 📉 Por período (histórico)
- 📋 Exportar a PDF/Excel

## 💡 Próximos Pasos de Implementación

Voy a crear:
1. ✅ Vista de "Registro de Clase" (la más importante)
2. ✅ Vista de "Ficha del Alumno" (detalle individual)
3. ✅ Sistema de alertas automáticas
4. ✅ Filtros por fecha
5. ✅ Exportación de datos

¿Te parece bien este flujo? ¿Hay algo que quieras agregar o cambiar?
