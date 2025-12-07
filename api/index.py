"""
Entrypoint para Vercel Serverless Functions
Sistema de Seguimiento de Alumnos

⚠️ ADVERTENCIA: SQLite en Vercel es EFÍMERO
Los datos se borran en cada despliegue.
Para producción: Usar PostgreSQL.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurar base de datos en /tmp (único directorio escribible en Vercel)
os.environ["DATABASE_PATH"] = "/tmp/database.db"

# Importar FastAPI y Mangum
try:
    from mangum import Mangum
    from src.presentation.api.main import app
    
    # Handler para Vercel
    handler = Mangum(app, lifespan="off")
    
except Exception as e:
    print(f"Error al importar la aplicación: {e}")
    import traceback
    traceback.print_exc()
    
    # Crear una app de fallback para debugging
    from fastapi import FastAPI
    
    fallback_app = FastAPI()
    
    @fallback_app.get("/")
    def root():
        return {
            "error": "Error al inicializar la aplicación",
            "details": str(e),
            "message": "Ver logs de Vercel para más detalles"
        }
    
    handler = Mangum(fallback_app, lifespan="off")
