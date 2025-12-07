"""
Entrypoint para Vercel Serverless Functions
Sistema de Seguimiento de Alumnos

Este archivo es el punto de entrada para el despliegue en Vercel.
Vercel ejecuta este archivo como una función serverless.

⚠️ ADVERTENCIA CRÍTICA - BASE DE DATOS EFÍMERA ⚠️

IMPORTANTE: SQLite en Vercel es EFÍMERO. Esto significa:
- ❌ Los datos se BORRAN en cada despliegue
- ❌ Los datos pueden NO persistir entre requests
- ❌ NO usar para datos de producción reales

Razón: Vercel usa contenedores efímeros. SQLite se guarda en /tmp
que se borra constantemente.

Para producción REAL: Migrar a PostgreSQL (Vercel Postgres, Supabase, etc.)
Ver DESPLIEGUE_VERCEL.md para instrucciones completas.

Decisión de diseño: Adaptación para Serverless
- Vercel ejecuta cada request en un contenedor efímero
- No podemos mantener conexiones persistentes a BD
- Debemos inicializar la BD en cada request (con caché)
- SQLite debe estar en /tmp (único directorio escribible en Vercel)
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Importar la aplicación FastAPI
from src.presentation.api.main import app

# ============================================================================
# Adaptación para Vercel Serverless
# ============================================================================

# Decisión de diseño: Base de datos en /tmp
# - Vercel solo permite escritura en /tmp
# - Cada instancia serverless tiene su propio /tmp
# - Para producción real, usar PostgreSQL o base de datos externa
os.environ["DATABASE_PATH"] = "/tmp/database.db"

# Inicializar base de datos si no existe
def inicializar_bd_vercel():
    """
    Inicializa la base de datos en /tmp si no existe.
    
    ⚠️ ADVERTENCIA: Los datos en /tmp son EFÍMEROS
    - Se borran en cada despliegue
    - Pueden no persistir entre requests
    - NO usar para datos de producción
    
    Para producción: Usar PostgreSQL (Vercel Postgres, Supabase, etc.)
    """
    db_path = os.environ.get("DATABASE_PATH", "/tmp/database.db")
    
    # Si la BD ya existe, no hacer nada
    if os.path.exists(db_path):
        return
    
    print("=" * 70)
    print("⚠️  ADVERTENCIA: Inicializando SQLite en /tmp (EFÍMERO)")
    print("=" * 70)
    print(f"🔧 Ruta: {db_path}")
    print("❌ Los datos se BORRARÁN en cada despliegue")
    print("❌ NO usar para datos de producción reales")
    print("✅ Para producción: Migrar a PostgreSQL")
    print("=" * 70)
    
    try:
        from src.infrastructure.database.connection import DatabaseConnection
        
        # Crear conexión con la ruta de /tmp
        db = DatabaseConnection()
        db._conectar(db_path)
        db.inicializar_schema()
        
        print("✅ Base de datos inicializada en Vercel (EFÍMERA)")
        print("=" * 70)
    except Exception as e:
        print(f"❌ Error al inicializar BD en Vercel: {e}")
        print("=" * 70)
        # No lanzar excepción, permitir que la app arranque

# Inicializar BD al cargar el módulo
inicializar_bd_vercel()

# ============================================================================
# Handler para Vercel
# ============================================================================

# Mangum es un adaptador ASGI para AWS Lambda y Vercel
# Convierte requests de Vercel a formato ASGI que FastAPI entiende
handler = Mangum(app, lifespan="off")

# ============================================================================
# Notas de Despliegue
# ============================================================================
"""
Para desplegar en Vercel:

1. Instalar Vercel CLI:
   npm install -g vercel

2. Iniciar sesión:
   vercel login

3. Desplegar:
   vercel

4. Para producción:
   vercel --prod

Limitaciones de SQLite en Vercel:
- La base de datos se reinicia en cada despliegue
- No hay persistencia entre requests (cada función tiene su /tmp)
- Solo sirve para desarrollo/demo

Para producción real:
- Usar PostgreSQL (Vercel Postgres, Supabase, etc.)
- Actualizar los repositorios para usar PostgreSQL
- Agregar variables de entorno para la conexión
"""
