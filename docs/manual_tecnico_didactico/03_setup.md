# Capítulo 3: Setup del Entorno

## 3.1 Instalar Python

### Windows

1. Ir a https://www.python.org/downloads/
2. Descargar Python 3.11 o superior
3. **IMPORTANTE:** Marcar "Add Python to PATH" durante la instalación
4. Verificar en terminal:
   ```powershell
   python --version
   # Debe mostrar: Python 3.11.x
   ```

### Verificar pip

```powershell
pip --version
# pip 23.x from ...
```

---

## 3.2 Crear el Proyecto

### Paso 1: Crear carpeta

```powershell
mkdir mi_proyecto_mvp
cd mi_proyecto_mvp
```

### Paso 2: Crear entorno virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
.\venv\Scripts\activate

# Deberías ver (venv) al inicio del prompt
```

> 💡 **Tip:** Para desactivar después: `deactivate`

### Paso 3: Instalar dependencias

Crear archivo `requirements.txt`:

```
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.6.0
pg8000==1.30.0
email-validator==2.1.0
```

Instalar:

```powershell
pip install -r requirements.txt
```

Verificar:

```powershell
pip list
# Debe mostrar fastapi, uvicorn, etc.
```

---

## 3.3 Crear Estructura de Carpetas

```powershell
# Crear carpetas principales
mkdir src
mkdir src\domain
mkdir src\domain\entities
mkdir src\domain\exceptions
mkdir src\application
mkdir src\application\services
mkdir src\infrastructure
mkdir src\infrastructure\database
mkdir src\infrastructure\repositories
mkdir src\presentation
mkdir src\presentation\api
mkdir src\presentation\api\routers
mkdir src\presentation\api\schemas
mkdir public
mkdir tests

# Crear archivos __init__.py (necesarios para Python)
New-Item -ItemType File -Path src\__init__.py -Force
New-Item -ItemType File -Path src\domain\__init__.py -Force
New-Item -ItemType File -Path src\domain\entities\__init__.py -Force
New-Item -ItemType File -Path src\domain\exceptions\__init__.py -Force
New-Item -ItemType File -Path src\application\__init__.py -Force
New-Item -ItemType File -Path src\application\services\__init__.py -Force
New-Item -ItemType File -Path src\infrastructure\__init__.py -Force
New-Item -ItemType File -Path src\infrastructure\database\__init__.py -Force
New-Item -ItemType File -Path src\infrastructure\repositories\__init__.py -Force
New-Item -ItemType File -Path src\presentation\__init__.py -Force
New-Item -ItemType File -Path src\presentation\api\__init__.py -Force
New-Item -ItemType File -Path src\presentation\api\routers\__init__.py -Force
New-Item -ItemType File -Path src\presentation\api\schemas\__init__.py -Force
```

### Estructura resultante

```
mi_proyecto_mvp/
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── __init__.py
│   │   └── exceptions/
│   │       └── __init__.py
│   ├── application/
│   │   └── services/
│   │       └── __init__.py
│   ├── infrastructure/
│   │   ├── database/
│   │   │   └── __init__.py
│   │   └── repositories/
│   │       └── __init__.py
│   └── presentation/
│       └── api/
│           ├── routers/
│           │   └── __init__.py
│           └── schemas/
│               └── __init__.py
├── public/
├── tests/
├── venv/
└── requirements.txt
```

---

## 3.4 Configurar Base de Datos (Neon)

### Paso 1: Crear cuenta en Neon

1. Ir a https://neon.tech
2. Registrarse con GitHub
3. Click "Create a project"
4. Nombre: `mi-proyecto-mvp`
5. Región: La más cercana

### Paso 2: Obtener URL de conexión

1. En el dashboard, click en "Connection Details"
2. Copiar la URL (tipo `postgresql://...`)

### Paso 3: Crear archivo .env

Crear archivo `.env` en la raíz:

```env
POSTGRES_URL=postgresql://tu_usuario:tu_password@tu_host/tu_database?sslmode=require
```

> ⚠️ **IMPORTANTE:** Este archivo NUNCA debe subirse a Git

### Paso 4: Crear .gitignore

```gitignore
# Entorno virtual
venv/

# Variables de entorno
.env

# Python
__pycache__/
*.pyc

# IDE
.vscode/
.idea/
```

---

## 3.5 Probar la Conexión

Crear archivo `scripts/test_db.py`:

```python
"""Script para probar conexión a la base de datos"""
import os
from urllib.parse import urlparse
import pg8000
import ssl

def test_connection():
    print("=== Test de Conexión ===\n")
    
    # Cargar .env manualmente
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Quitar comillas si las hay
                    value = value.strip().strip('"').strip("'")
                    os.environ[key.strip()] = value
    except FileNotFoundError:
        print("❌ No se encontró archivo .env")
        return
    
    # Obtener URL
    db_url = os.environ.get("POSTGRES_URL")
    if not db_url:
        print("❌ POSTGRES_URL no está definida en .env")
        return
    
    print(f"URL: ...{db_url[-30:]}")
    
    # Parsear URL
    parsed = urlparse(db_url)
    
    try:
        # Conectar con SSL
        ssl_context = ssl.create_default_context()
        conn = pg8000.connect(
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path.lstrip('/'),
            ssl_context=ssl_context
        )
        
        print("✅ ¡CONEXIÓN EXITOSA!")
        
        # Probar query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"PostgreSQL: {version[:50]}...")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()
```

Ejecutar:

```powershell
python scripts/test_db.py
```

Resultado esperado:

```
=== Test de Conexión ===

URL: ...neondb?sslmode=require
✅ ¡CONEXIÓN EXITOSA!
PostgreSQL: PostgreSQL 16.x ...
```

---

## 3.6 Crear App Mínima FastAPI

Crear `src/presentation/api/main.py`:

```python
"""Aplicación FastAPI mínima para verificar que todo funciona"""
from fastapi import FastAPI

# Crear la aplicación
app = FastAPI(
    title="Mi Proyecto MVP",
    description="Sistema de gestión de alumnos y cursos",
    version="0.1.0"
)

# Endpoint de prueba
@app.get("/")
def raiz():
    return {"mensaje": "¡Hola! La API funciona 🎉"}

@app.get("/api")
def api_root():
    return {
        "status": "ok",
        "version": "0.1.0",
        "endpoints": {
            "alumnos": "/api/alumnos/",
            "cursos": "/api/cursos/"
        }
    }
```

---

## 3.7 Ejecutar el Servidor

Crear archivo `run.bat` (Windows):

```batch
@echo off
echo Iniciando servidor...
call venv\Scripts\activate
uvicorn src.presentation.api.main:app --reload
```

Ejecutar:

```powershell
.\run.bat
```

O directamente:

```powershell
uvicorn src.presentation.api.main:app --reload
```

### Navegar

1. Abrir http://localhost:8000 → Ver mensaje "¡Hola!"
2. Abrir http://localhost:8000/docs → Ver Swagger UI
3. Abrir http://localhost:8000/api → Ver info de la API

---

## 3.8 Verificación Final

### Checklist

```
✅ Python 3.11+ instalado
✅ Entorno virtual creado y activado
✅ Dependencias instaladas (pip list)
✅ Estructura de carpetas creada
✅ Archivo .env con POSTGRES_URL
✅ Conexión a BD funcionando (test_db.py)
✅ FastAPI corriendo (localhost:8000)
✅ Swagger UI accesible (/docs)
```

Si todo está ✅, estás listo para empezar a codear.

---

## 3.9 Comandos Útiles

| Comando | Qué hace |
|---------|----------|
| `.\venv\Scripts\activate` | Activar entorno virtual |
| `deactivate` | Desactivar entorno virtual |
| `pip install -r requirements.txt` | Instalar dependencias |
| `pip freeze > requirements.txt` | Guardar dependencias |
| `uvicorn src.presentation.api.main:app --reload` | Correr servidor |
| `python scripts/test_db.py` | Probar conexión BD |

---

**Anterior:** [Capítulo 2 - Diseño](./02_diseno.md)

**Siguiente:** [Capítulo 4 - Dominio](./04_dominio.md)
