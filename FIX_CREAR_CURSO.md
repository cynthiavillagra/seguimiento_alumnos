# 🔧 Código Faltante para Crear Cursos

## ❌ Problema

Las funciones para **crear** alumnos, cursos y TPs no están en `app.js`.

---

## ✅ Solución

Agrega este código al **FINAL** del archivo `public/app.js` (antes de la última línea):

```javascript
// ========================================
// FUNCIONES DE CREACIÓN (CREATE)
// ========================================

function mostrarModalCrearAlumno() {
    showModal('modal-nuevo-alumno');
}

function mostrarModalCrearCurso() {
    showModal('modal-crear-curso');
}

async function mostrarModalCrearTP() {
    // Cargar cursos en el select
    try {
        const response = await fetch(`${API_URL}/cursos`);
        const data = await response.json();
        
        const select = document.getElementById('tp-curso');
        select.innerHTML = '<option value="">Selecciona un curso...</option>';
        
        data.clases.forEach(curso => {
            const option = document.createElement('option');
            option.value = curso.id;
            option.textContent = `${curso.materia} - ${curso.cohorte}`;
            select.appendChild(option);
        });
        
        showModal('modal-crear-tp');
    } catch (error) {
        console.error('Error al cargar cursos:', error);
        showToast('Error al cargar cursos', 'error');
    }
}

function cerrarModal(modalId) {
    closeModal(modalId);
}

async function crearCurso() {
    const materia = document.getElementById('curso-materia').value.trim();
    const anio = parseInt(document.getElementById('curso-anio').value);
    const cuatrimestre = parseInt(document.getElementById('curso-cuatrimestre').value);
    const docente = document.getElementById('curso-docente').value.trim();
    
    if (!materia || !anio || !cuatrimestre || !docente) {
        showToast('Por favor completa todos los campos', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/cursos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre_materia: materia,
                anio: anio,
                cuatrimestre: cuatrimestre,
                docente_responsable: docente
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showToast('Curso creado exitosamente', 'success');
            cerrarModal('modal-crear-curso');
            document.getElementById('form-crear-curso').reset();
            // Recargar dashboard
            if (state.currentPage === 'dashboard') {
                loadDashboardData();
            }
        } else {
            showToast(data.error || 'Error al crear curso', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al crear curso', 'error');
    }
}

async function crearTP() {
    const cursoId = parseInt(document.getElementById('tp-curso').value);
    const titulo = document.getElementById('tp-titulo').value.trim();
    const descripcion = document.getElementById('tp-descripcion').value.trim();
    const fecha = document.getElementById('tp-fecha').value;
    
    if (!cursoId || !titulo || !fecha) {
        showToast('Por favor completa todos los campos requeridos', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/trabajos-practicos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                curso_id: cursoId,
                titulo: titulo,
                descripcion: descripcion,
                fecha_entrega: fecha
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showToast('Trabajo Práctico creado exitosamente', 'success');
            cerrarModal('modal-crear-tp');
            document.getElementById('form-crear-tp').reset();
        } else {
            showToast(data.error || 'Error al crear TP', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al crear TP', 'error');
    }
}

// Exportar funciones de creación
window.mostrarModalCrearAlumno = mostrarModalCrearAlumno;
window.mostrarModalCrearCurso = mostrarModalCrearCurso;
window.mostrarModalCrearTP = mostrarModalCrearTP;
window.cerrarModal = cerrarModal;
window.crearCurso = crearCurso;
window.crearTP = crearTP;
```

---

## 📝 Cómo Agregarlo

### Opción 1: Manual (Recomendado)

1. Abre `public/app.js` en tu editor
2. Ve al **FINAL** del archivo
3. Pega el código de arriba
4. Guarda el archivo

### Opción 2: Con PowerShell

```powershell
# Copia el código de arriba y guárdalo en un archivo temporal
# Luego ejecuta:
Get-Content "temp-funciones.txt" | Add-Content "public/app.js"
```

---

## ✅ Verificar

Después de agregar el código, abre la consola del navegador (F12) y escribe:

```javascript
typeof crearCurso
```

Debería mostrar: `"function"`

---

## 🚀 Luego Desplegar

```powershell
git add .
git commit -m "fix: Add missing create functions for courses and TPs"
git push
```

---

**¡Esto debería solucionar el problema!** 🎉
