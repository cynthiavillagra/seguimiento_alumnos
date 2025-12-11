# Capítulo 7: Instalación del Entorno

## 7.1 Requisitos de Software

Antes de comenzar, asegurate de tener instalado:

### Python 3.11+

**Windows:**
1. Ir a https://www.python.org/downloads/
2. Descargar Python 3.11 o superior
3. Durante instalación, marcar "Add Python to PATH"
4. Verificar: `python --version`

**Linux/Mac:**
```bash
# Con pyenv (recomendado)
curl https://pyenv.run | bash
pyenv install 3.11.0
pyenv global 3.11.0
```

### Git

**Windows:**
1. Descargar de https://git-scm.com/download/windows
2. Instalar con opciones por defecto
3. Verificar: `git --version`

**Linux:**
```bash
sudo apt update
sudo apt install git
```

### VS Code (Recomendado)

1. Descargar de https://code.visualstudio.com/
2. Instalar extensiones recomendadas:
   - **Python** (Microsoft)
   - **Pylance** (Microsoft)
   - **GitLens**
   - **REST Client** (para probar API)

## 7.2 Crear el Proyecto desde Cero

### Paso 1: Crear Carpeta del Proyecto

```bash
# Windows (PowerShell)
mkdir "seguimiento_alumnos"
cd seguimiento_alumnos

# Linux/Mac
mkdir seguimiento_alumnos
cd seguimiento_alumnos
```

### Paso 2: Inicializar Git

```bash
git init
```

Crear archivo `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
.env
.env.local

# IDE
.vscode/
.idea/

# Build
dist/
build/
*.egg-info/

# Vercel
.vercel/

# Local database
*.db
*.sqlite
```

### Paso 3: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
.\venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Deberías ver (venv) al inicio del prompt
```

**¿Por qué usar entorno virtual?**

- Aísla las dependencias de este proyecto
- Evita conflictos con otros proyectos
- Permite tener versiones específicas de librerías

### Paso 4: Instalar Dependencias

Crear archivo `requirements.txt`:

```
fastapi>=0.109.0
uvicorn>=0.27.0
pydantic>=2.6.0
python-multipart>=0.0.9
pg8000>=1.30.0
email-validator>=2.0.0
```

Instalar:

```bash
pip install -r requirements.txt
```

Verificar instalación:

```bash
pip list
# Deberías ver fastapi, uvicorn, etc.
```

### Paso 5: Crear Estructura de Carpetas

```bash
# Windows (PowerShell)
mkdir src
mkdir src\domain
mkdir src\domain\entities
mkdir src\domain\exceptions
mkdir src\application
mkdir src\application\services
mkdir src\infrastructure
mkdir src\infrastructure\database
mkdir src\infrastructure\repositories
mkdir src\infrastructure\repositories\base
mkdir src\infrastructure\repositories\postgres
mkdir src\presentation
mkdir src\presentation\api
mkdir src\presentation\api\routers
mkdir src\presentation\api\schemas
mkdir public
mkdir public\components
mkdir public\components\modals
mkdir docs
mkdir tests
mkdir scripts
mkdir api

# Crear archivos __init__.py necesarios (PowerShell)
New-Item -ItemType File -Path src\__init__.py
New-Item -ItemType File -Path src\domain\__init__.py
New-Item -ItemType File -Path src\domain\entities\__init__.py
New-Item -ItemType File -Path src\domain\exceptions\__init__.py
New-Item -ItemType File -Path src\application\__init__.py
New-Item -ItemType File -Path src\application\services\__init__.py
New-Item -ItemType File -Path src\infrastructure\__init__.py
New-Item -ItemType File -Path src\infrastructure\database\__init__.py
New-Item -ItemType File -Path src\infrastructure\repositories\__init__.py
New-Item -ItemType File -Path src\infrastructure\repositories\base\__init__.py
New-Item -ItemType File -Path src\infrastructure\repositories\postgres\__init__.py
New-Item -ItemType File -Path src\presentation\__init__.py
New-Item -ItemType File -Path src\presentation\api\__init__.py
New-Item -ItemType File -Path src\presentation\api\routers\__init__.py
New-Item -ItemType File -Path src\presentation\api\schemas\__init__.py
```

**Linux/Mac:**
```bash
mkdir -p src/{domain/{entities,exceptions},application/services,infrastructure/{database,repositories/{base,postgres}},presentation/api/{routers,schemas}}
mkdir -p public/components/modals
mkdir -p {docs,tests,scripts,api}

# Crear __init__.py
find src -type d -exec touch {}/__init__.py \;
```

## 7.3 Configurar Base de Datos (Neon)

### Paso 1: Crear Cuenta en Neon

1. Ir a https://neon.tech/
2. Registrarse con GitHub o email
3. Crear nuevo proyecto
4. Elegir región más cercana (ej: South America)

### Paso 2: Obtener Connection String

1. En el dashboard de Neon, ir a "Connection Details"
2. Copiar la URL de conexión:
   ```
   postgresql://usuario:password@host/base?sslmode=require
   ```

### Paso 3: Crear Archivo .env

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de datos PostgreSQL (Neon)
POSTGRES_URL=postgresql://neondb_owner:xxxxx@ep-xxx.sa-east-1.aws.neon.tech/neondb?sslmode=require

# Entorno
ENVIRONMENT=development
```

**⚠️ IMPORTANTE:** Este archivo NO debe subirse a Git. Ya está en `.gitignore`.

### Paso 4: Crear Archivo .env.example

Para que otros desarrolladores sepan qué variables necesitan:

```env
# Base de datos PostgreSQL (Neon)
POSTGRES_URL=postgresql://user:password@host/database?sslmode=require

# Entorno
ENVIRONMENT=development
```

## 7.4 Configurar Vercel (Deploy)

### Paso 1: Crear Cuenta

1. Ir a https://vercel.com/
2. Registrarse con GitHub

### Paso 2: Crear vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "public/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "public/$1"
    }
  ]
}
```

### Paso 3: Crear Archivo de Entrada para Vercel

Crear `api/index.py`:

```python
"""
Punto de entrada para Vercel Serverless Functions.
Importa la app de FastAPI y la expone como handler.
"""

from mangum import Mangum
from src.presentation.api.main import app

# Mangum adapta FastAPI para funcionar con AWS Lambda / Vercel
handler = Mangum(app, lifespan="off")
```

Agregar `mangum` a `requirements.txt`:

```
fastapi>=0.109.0
uvicorn>=0.27.0
pydantic>=2.6.0
python-multipart>=0.0.9
pg8000>=1.30.0
email-validator>=2.0.0
mangum>=0.17.0
```

## 7.5 Script para Correr Localmente

Crear `run_local.bat` (Windows):

```batch
@echo off
echo Starting Local Development Server...
call venv\Scripts\activate
uvicorn src.presentation.api.main:app --reload --env-file .env
pause
```

Crear `run_local.sh` (Linux/Mac):

```bash
#!/bin/bash
echo "Starting Local Development Server..."
source venv/bin/activate
uvicorn src.presentation.api.main:app --reload --env-file .env
```

Hacer ejecutable (Linux/Mac):
```bash
chmod +x run_local.sh
```

## 7.6 Verificar Instalación

### Test 1: Python y Dependencias

```bash
# Activar entorno virtual
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Verificar Python
python --version
# Python 3.11.x

# Verificar FastAPI
python -c "import fastapi; print(fastapi.__version__)"
# 0.109.x

# Verificar pg8000
python -c "import pg8000; print(pg8000.__version__)"
# 1.30.x
```

### Test 2: Conexión a Base de Datos

Crear `scripts/test_db.py`:

```python
import os
from urllib.parse import urlparse
import pg8000
import ssl

def test_connection():
    print("--- Test de Conexión a Base de Datos ---")
    
    # Cargar .env manualmente
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): 
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    val = v.strip()
                    if (val.startswith('"') and val.endswith('"')):
                        val = val[1:-1]
                    os.environ[k.strip()] = val
    except FileNotFoundError:
        print("❌ Archivo .env no encontrado")
        return

    db_url = os.environ.get("POSTGRES_URL")
    
    if not db_url:
        print("❌ No se encontró POSTGRES_URL en .env")
        return

    print(f"URL encontrada: ...{db_url[-20:]}")
    
    try:
        parsed = urlparse(db_url)
        print(f"Host: {parsed.hostname}")
        print(f"Database: {parsed.path.lstrip('/')}")
        
        ssl_context = ssl.create_default_context()
        
        print("\nConectando...")
        conn = pg8000.connect(
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path.lstrip('/'),
            ssl_context=ssl_context 
        )
        print("✅ ¡CONEXIÓN EXITOSA!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"PostgreSQL: {version[:60]}...")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    test_connection()
```

Ejecutar:
```bash
python scripts/test_db.py
```

Resultado esperado:
```
--- Test de Conexión a Base de Datos ---
URL encontrada: ...neondb?sslmode=require
Host: ep-xxx.sa-east-1.aws.neon.tech
Database: neondb

Conectando...
✅ ¡CONEXIÓN EXITOSA!
PostgreSQL: PostgreSQL 16.x on ...
```

## 7.7 Primer Commit

Una vez que todo funciona:

```bash
git add .
git commit -m "feat: setup inicial del proyecto"
```

Crear repositorio en GitHub y subir:

```bash
git remote add origin https://github.com/tu-usuario/seguimiento-alumnos.git
git branch -M main
git push -u origin main
```

## 7.8 Conectar con Vercel

1. Ir a https://vercel.com/new
2. Importar repositorio de GitHub
3. Configurar:
   - Framework Preset: `Other`
   - Build Command: (dejar vacío o `python build.py` si tenés script)
   - Output Directory: `public`
   - Install Command: `pip install -r requirements.txt`
4. Agregar variables de entorno:
   - `POSTGRES_URL` = (tu URL de Neon)
   - `VERCEL` = `1`
5. Deploy

## 7.9 Resumen de Comandos

| Acción | Comando |
|--------|---------|
| Activar venv (Windows) | `.\venv\Scripts\activate` |
| Activar venv (Linux/Mac) | `source venv/bin/activate` |
| Instalar dependencias | `pip install -r requirements.txt` |
| Correr servidor local | `.\run_local.bat` o `./run_local.sh` |
| Ver API docs | http://localhost:8000/docs |
| Test conexión BD | `python scripts/test_db.py` |

---

**Capítulo anterior**: [Diagramas UML](./06_uml.md)

**Siguiente capítulo**: [Construcción Paso a Paso](./08_construccion_paso_a_paso.md)
