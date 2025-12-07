# 📊 Dashboard Mejorado - Múltiples Clases

## 🎯 Nuevo Diseño del Dashboard

### Concepto
Un dashboard que permite al docente:
1. **Ver todas sus clases** en tarjetas separadas
2. **Seleccionar una clase** para ver detalles
3. **Acciones rápidas** por clase
4. **Resumen general** de todas las clases

## 🎨 Propuesta de Interfaz

### Vista Principal del Dashboard

```
┌─────────────────────────────────────────────────────────┐
│ Dashboard - Mis Clases                                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│ │ Programación I│  │ Matemática   │  │ Física       │  │
│ │ Cohorte 2024  │  │ Cohorte 2024 │  │ Cohorte 2023 │  │
│ ├──────────────┤  ├──────────────┤  ├──────────────┤  │
│ │ 👥 30 alumnos│  │ 👥 28 alumnos│  │ 👥 25 alumnos│  │
│ │ 📊 85% asist.│  │ 📊 90% asist.│  │ 📊 78% asist.│  │
│ │ 🚨 3 en riesgo│  │ 🚨 1 en riesgo│  │ 🚨 5 en riesgo│  │
│ │              │  │              │  │              │  │
│ │ [Ver Clase]  │  │ [Ver Clase]  │  │ [Ver Clase]  │  │
│ │ [Registrar]  │  │ [Registrar]  │  │ [Registrar]  │  │
│ └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│ [+ Nueva Clase]                                         │
└─────────────────────────────────────────────────────────┘
```

### Vista de Clase Individual

```
┌─────────────────────────────────────────────────────────┐
│ ← Volver al Dashboard                                   │
│                                                          │
│ Programación I - Cohorte 2024                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ESTADÍSTICAS                                            │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│ │ 30       │ │ 85%      │ │ 3        │ │ 12       │   │
│ │ Alumnos  │ │ Asist.   │ │ En Riesgo│ │ Clases   │   │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│                                                          │
│ ALUMNOS EN RIESGO                                       │
│ • García, Ana - Asist: 55% 🔴                          │
│ • López, Carlos - Asist: 72% 🟠                        │
│ • Martínez, Juan - Asist: 68% 🟠                       │
│                                                          │
│ ACCIONES RÁPIDAS                                        │
│ [Registrar Clase] [Ver Alumnos] [Ver Alertas]          │
└─────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Trabajo Actualizado

### Opción 1: Desde Dashboard
```
1. Abrir app → Dashboard con todas las clases
2. Click en tarjeta de "Programación I - 2024"
3. Ver detalles de esa clase específica
4. Click en "Registrar Clase"
5. Ya tiene materia y cohorte seleccionadas
6. Registrar asistencia
```

### Opción 2: Registro Directo
```
1. Abrir app → Dashboard
2. Click en "Registrar" en la tarjeta de la clase
3. Ir directo al registro (sin seleccionar materia/cohorte)
4. Registrar asistencia
```

## 📊 Datos que Necesita el Dashboard

### Por Clase
```javascript
{
  id: 1,
  materia: "Programación I",
  cohorte: 2024,
  totalAlumnos: 30,
  asistenciaPromedio: 85,
  alumnosEnRiesgo: 3,
  totalClases: 12,
  ultimaClase: "2024-12-05"
}
```

### Resumen General
```javascript
{
  totalClases: 3,
  totalAlumnos: 83,
  asistenciaPromedioGeneral: 84,
  totalAlumnosEnRiesgo: 9
}
```

## 🎯 Ventajas de Este Diseño

1. ✅ **Organizado por clase** - Cada materia/cohorte es independiente
2. ✅ **Vista rápida** - Ver estado de todas las clases de un vistazo
3. ✅ **Acceso directo** - Registrar clase sin navegar mucho
4. ✅ **Foco en lo importante** - Alumnos en riesgo por clase
5. ✅ **Escalable** - Funciona con 1 o 20 clases

## 🚀 Implementación

### Paso 1: Crear Modelo de Clase
```python
class Clase:
    id: int
    materia: str
    cohorte: int
    profesor_id: int  # Para futuro multi-usuario
```

### Paso 2: Endpoint de Clases
```
GET /clases → Lista todas las clases del profesor
GET /clases/{id} → Detalle de una clase
GET /clases/{id}/alumnos → Alumnos de esa clase
GET /clases/{id}/estadisticas → Stats de la clase
```

### Paso 3: Actualizar Dashboard
- Mostrar tarjetas de clases
- Click en tarjeta → Vista de clase individual
- Botón "Registrar" → Pre-selecciona materia/cohorte

## 💡 Características Adicionales

### Filtros en el Dashboard
- Ver solo clases activas
- Ver solo clases con alertas
- Ordenar por % asistencia

### Vista de Calendario
```
┌─────────────────────────────────────┐
│ Diciembre 2024                      │
├─────────────────────────────────────┤
│ Lun  Mar  Mie  Jue  Vie  Sab  Dom  │
│  2    3    4    5    6    7    8   │
│      Prog  Mat       Fis            │
│  9   10   11   12   13   14   15   │
│      Prog  Mat       Fis            │
└─────────────────────────────────────┘
```

### Notificaciones
- "Tienes 3 clases sin registrar esta semana"
- "5 alumnos nuevos en riesgo"
- "Recordatorio: Clase de Programación I hoy"

## 🎨 Mockup Visual

Voy a crear un dashboard actualizado con:
1. Tarjetas de clases (grid responsive)
2. Vista de clase individual
3. Acceso rápido a registro
4. Resumen de alertas por clase

¿Te parece bien este diseño? ¿Quieres que lo implemente ahora?
