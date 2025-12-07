# ✅ Problema Corregido - Crear Curso

## ❌ Problema Original

No se podía crear un curso porque faltaban las funciones JavaScript en `app.js`.

## ✅ Solución Aplicada

Se agregaron las siguientes funciones al final de `public/app.js`:

### Funciones Agregadas

1. ✅ `mostrarModalCrearAlumno()` - Abre modal de crear alumno
2. ✅ `mostrarModalCrearCurso()` - Abre modal de crear curso
3. ✅ `mostrarModalCrearTP()` - Abre modal de crear TP (carga cursos)
4. ✅ `cerrarModal(modalId)` - Cierra cualquier modal
5. ✅ `crearCurso()` - Crea un nuevo curso (POST)
6. ✅ `crearTP()` - Crea un nuevo TP (POST)

### Exportaciones

Todas las funciones fueron exportadas a `window` para que sean accesibles desde el HTML:

```javascript
window.mostrarModalCrearAlumno = mostrarModalCrearAlumno;
window.mostrarModalCrearCurso = mostrarModalCrearCurso;
window.mostrarModalCrearTP = mostrarModalCrearTP;
window.cerrarModal = cerrarModal;
window.crearCurso = crearCurso;
window.crearTP = crearTP;
```

---

## 🚀 Ahora Funciona

### Crear Curso

1. Click en el botón **📚+** en el navbar
2. Se abre el modal "Crear Nuevo Curso"
3. Completa los campos:
   - Nombre de la Materia
   - Año
   - Cuatrimestre
   - Docente Responsable
4. Click en "Crear Curso"
5. ✅ Toast de confirmación
6. ✅ Dashboard se recarga automáticamente

### Crear TP

1. Click en el botón **📝+** en el navbar
2. Se abre el modal "Crear Nuevo Trabajo Práctico"
3. El select de cursos se carga automáticamente
4. Completa los campos:
   - Curso (select)
   - Título del TP
   - Descripción (opcional)
   - Fecha de Entrega
5. Click en "Crear TP"
6. ✅ Toast de confirmación

---

## 📝 Para Desplegar

```powershell
git add .
git commit -m "fix: Add missing create functions for courses and TPs"
git push
```

Espera 1-2 minutos y todo estará funcionando en Vercel.

---

## ✅ Verificar Localmente

Abre la consola del navegador (F12) y verifica que las funciones existan:

```javascript
typeof crearCurso
// Debería mostrar: "function"

typeof mostrarModalCrearCurso
// Debería mostrar: "function"
```

---

**¡Problema resuelto!** 🎉

Ahora puedes crear cursos, TPs y alumnos sin problemas.
