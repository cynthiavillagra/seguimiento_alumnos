# 🖥️ Guía de Desarrollo Local

## 🎯 Configuración Completada

Se ha configurado todo lo necesario para desarrollo local:

- ✅ Entorno virtual Python (`venv/`)
- ✅ Archivo `.env` para variables de entorno
- ✅ Archivo `.env.example` como plantilla
- ✅ `.gitignore` actualizado
- ✅ Servidor local (`local_server.py`)
- ✅ Dependencias actualizadas

---

## 📋 Pasos para Empezar

### 1. Activar el Entorno Virtual

```powershell
# En PowerShell
.\venv\Scripts\Activate.ps1

# Si da error de permisos, ejecuta primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Deberías ver `(venv)` al inicio de tu línea de comandos.

### 2. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

Esto instalará:
- `psycopg2-binary` - Para conectar a PostgreSQL
- `python-dotenv` - Para cargar variables de entorno
- `pytest` - Para testing

### 3. Configurar Variables de Entorno

Edita el archivo `.env` y agrega tu DATABASE_URL:

```env
DATABASE_URL=postgresql://usuario:password@host.neon.tech/database?sslmode=require
```

**¿Dónde obtener el DATABASE_URL?**

#### Opción A: Desde Neon
1. Ve a https://console.neon.tech
2. Selecciona tu proyecto
3. Ve a "Connection Details"
4. Copia la "Connection string"

#### Opción B: Desde Vercel
1. Ve a tu proyecto en Vercel
2. Settings > Environment Variables
3. Busca `DATABASE_URL` o `POSTGRES_URL`
4. Copia el valor

### 4. Iniciar el Servidor Local

```powershell
python local_server.py
```

Deberías ver:

```
╔═══════════════════════════════════════════════════════════╗
║  🎓 Sistema de Seguimiento de Alumnos - Servidor Local   ║
╚═══════════════════════════════════════════════════════════╝

✅ Servidor corriendo en: http://localhost:5000

📂 Sirviendo archivos desde: ./public
🔌 API disponible en: http://localhost:5000/api/*
```

### 5. Abrir en el Navegador

Ve a: **http://localhost:5000**

---

## 🧪 Probar la Aplicación

### Verificar que Funciona

1. **Abre la consola del navegador** (F12)
2. **Ve a la pestaña "Network"**
3. **Recarga la página** (Ctrl+R)
4. **Verifica que no haya errores** en rojo

### Probar CRUD de Cursos

1. Click en **"Cursos"** en el navbar
2. Deberías ver la tabla con cursos
3. Click en **"+ Nuevo Curso"**
4. Completa el formulario
5. Click en **"Crear Curso"**
6. Verifica que aparezca en la tabla

### Probar Editar/Eliminar

1. Click en **✏️ Editar** en un curso
2. Modifica algún campo
3. Click en **"Guardar Cambios"**
4. Verifica que se actualizó

---

## 🔧 Comandos Útiles

### Activar/Desactivar Entorno Virtual

```powershell
# Activar
.\venv\Scripts\Activate.ps1

# Desactivar
deactivate
```

### Instalar Nueva Dependencia

```powershell
# Activar venv primero
.\venv\Scripts\Activate.ps1

# Instalar paquete
pip install nombre-paquete

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### Ejecutar Tests

```powershell
# Tests de Python
pytest

# Con cobertura
pytest --cov=api

# Tests de JavaScript (requiere Node.js)
npm test
```

### Ver Logs de la BD

```powershell
# En la consola de Python
python
>>> from api.db import execute_query
>>> cursos = execute_query("SELECT * FROM curso")
>>> print(cursos)
```

---

## 🐛 Solución de Problemas

### Error: "DATABASE_URL no encontrada"

**Solución:** Verifica que el archivo `.env` existe y tiene la variable `DATABASE_URL`.

```powershell
# Verificar que existe
Test-Path .env

# Ver contenido
Get-Content .env
```

### Error: "ModuleNotFoundError: No module named 'psycopg2'"

**Solución:** Instala las dependencias.

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "Cannot connect to database"

**Solución:** Verifica que el `DATABASE_URL` es correcto.

1. Copia el URL desde Neon o Vercel
2. Asegúrate de incluir `?sslmode=require` al final
3. Verifica que no haya espacios extra

### Error: "Port 5000 already in use"

**Solución:** Cambia el puerto en `.env`.

```env
PORT=5001
```

### Error de CORS

**Solución:** Ya está configurado en el servidor local, pero si persiste:

```python
# En local_server.py, verifica que esté:
self.send_header('Access-Control-Allow-Origin', '*')
```

---

## 📁 Estructura de Archivos

```
proyecto/
├── venv/                  # Entorno virtual (NO subir a Git)
├── .env                   # Variables de entorno (NO subir a Git)
├── .env.example           # Plantilla de variables
├── .gitignore             # Archivos ignorados por Git
├── local_server.py        # Servidor de desarrollo
├── requirements.txt       # Dependencias Python
├── api/
│   ├── index.py          # Handler principal de la API
│   └── db.py             # Conexión a PostgreSQL
├── public/
│   ├── index.html        # Frontend
│   ├── css/              # Estilos modulares
│   └── js/               # JavaScript modular
└── tests/
    ├── test_api.py       # Tests de backend
    └── test_frontend.test.js  # Tests de frontend
```

---

## 🚀 Workflow de Desarrollo

### 1. Hacer Cambios

```powershell
# Activar venv
.\venv\Scripts\Activate.ps1

# Iniciar servidor
python local_server.py

# Hacer cambios en el código
# El servidor sirve los archivos directamente, no requiere rebuild
```

### 2. Probar Cambios

- Recarga el navegador (Ctrl+R)
- Verifica en la consola que no haya errores
- Prueba la funcionalidad modificada

### 3. Ejecutar Tests

```powershell
# Tests de Python
pytest

# Tests de JavaScript
npm test
```

### 4. Commit y Push

```powershell
git add .
git commit -m "feat: descripción del cambio"
git push
```

### 5. Verificar en Vercel

- Espera 1-2 minutos
- Ve a https://seguimiento-alumnos.vercel.app
- Verifica que funcione en producción

---

## 📝 Notas Importantes

### Variables de Entorno

- ✅ `.env` - **NO** subir a Git (contiene credenciales)
- ✅ `.env.example` - **SÍ** subir a Git (plantilla sin credenciales)

### Entorno Virtual

- ✅ `venv/` - **NO** subir a Git (muy pesado)
- ✅ `requirements.txt` - **SÍ** subir a Git (lista de dependencias)

### Base de Datos

- En local usas la **misma BD** que en producción (Neon)
- Ten cuidado al hacer cambios que afecten datos reales
- Considera crear una BD separada para desarrollo

---

## 🎯 Próximos Pasos

1. ✅ Configuración completada
2. ⏳ Activar venv e instalar dependencias
3. ⏳ Configurar DATABASE_URL en .env
4. ⏳ Iniciar servidor local
5. ⏳ Probar CRUD de cursos
6. 🔜 Desarrollar nuevas funcionalidades
7. 🔜 Ejecutar tests antes de cada commit

---

**¡Entorno local listo para desarrollo!** 🎉

**Siguiente paso:** Activa el venv e instala las dependencias.

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
