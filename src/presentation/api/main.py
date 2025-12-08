"""
Aplicación Principal de FastAPI
Sistema de Seguimiento de Alumnos

Este es el punto de entrada de la API.
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.presentation.api.routers import alumnos, cursos, inscripciones, clases, asistencias, participaciones, tps, entregas
from fastapi.staticfiles import StaticFiles


# ============================================================================
# Lifecycle Events
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    
    Nota para Vercel: En Vercel con Mangum (lifespan="off"),
    este código NO se ejecuta. La inicialización se hace bajo demanda.
    """
    # Startup: Inicializar base de datos
    print("🚀 Iniciando aplicación...")
    
    # Solo inicializar BD si NO estamos en Vercel
    if not os.environ.get("VERCEL"):
        try:
            from src.infrastructure.database.connection import inicializar_base_de_datos
            inicializar_base_de_datos()
            print("✅ Base de datos inicializada")
        except Exception as e:
            print(f"⚠️ Advertencia al inicializar BD: {e}")
    else:
        print("ℹ️ Entorno Vercel detectado - BD se inicializa bajo demanda")
    
    yield  # La aplicación está corriendo
    
    # Shutdown
    print("👋 Cerrando aplicación...")


# ============================================================================
# Crear aplicación FastAPI
# ============================================================================

app = FastAPI(
    title="Sistema de Seguimiento de Alumnos",
    description="""
    API para el seguimiento de alumnos en Tecnicaturas Superiores.
    
    Permite:
    - Gestionar alumnos, cursos y clases
    - Registrar asistencia, participación y entregas de TPs
    - Calcular indicadores de riesgo de deserción
    - Generar alertas tempranas
    
    ## Arquitectura
    
    Esta API está construida con:
    - **FastAPI** para el framework web
    - **SQLite** para persistencia (MVP)
    - **Arquitectura por capas** (Domain, Application, Infrastructure, Presentation)
    - **Patrón Repository** para abstracción de datos
    
    ## Documentación
    
    - **Swagger UI**: `/docs` (esta página)
    - **ReDoc**: `/redoc`
    - **OpenAPI JSON**: `/openapi.json`
    """,
    version="1.0.0",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "dev@seguimiento-alumnos.edu"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    lifespan=lifespan
)


# ============================================================================
# Configurar CORS
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Incluir Routers
# ============================================================================



# ============================================================================
# Incluir Routers (Prefijo /api)
# ============================================================================

api_prefix = "/api"

app.include_router(alumnos.router, prefix=api_prefix)
app.include_router(cursos.router, prefix=api_prefix)
app.include_router(inscripciones.router, prefix=api_prefix)
app.include_router(clases.router, prefix=api_prefix)
app.include_router(asistencias.router, prefix=api_prefix)
app.include_router(participaciones.router, prefix=api_prefix)
app.include_router(tps.router, prefix=api_prefix)
app.include_router(entregas.router, prefix=api_prefix)

# ============================================================================
# Servir Archivos Estáticos (Frontend)
# ============================================================================

# En Vercel, el frontend se sirve por separado o desde la raíz
# Si estamos en local, servimos public desde aquí para facilitar pruebas
if not os.environ.get("VERCEL"):
    try:
        app.mount("/", StaticFiles(directory="public", html=True), name="public")
    except Exception as e:
        print(f"⚠️ No se pudo montar directorio public: {e}")


# ============================================================================
# Endpoints de Health Check
# ============================================================================

@app.get(
    "/api",
    tags=["Health"],
    summary="Health check",
    description="Verifica que la API esté funcionando"
)
def root():
    """Endpoint raíz de la API"""
    return {
        "message": "API de Seguimiento de Alumnos",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "environment": "vercel" if os.environ.get("VERCEL") else "local"
    }


@app.get(
    "/api/health",
    tags=["Health"],
    summary="Health check detallado"
)
def health_check():
    """Health check detallado"""
    try:
        from src.infrastructure.database.connection import get_db_connection
        conexion = get_db_connection()
        # Verificar conexión simple
        with conexion.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "api": "healthy",
        "database": db_status,
        "version": "1.0.0",
        "environment": "vercel" if os.environ.get("VERCEL") else "local"
    }


@app.get(
    "/api/setup",
    tags=["Admin"],
    summary="Inicializar Base de Datos (First Run)"
)
def setup_database():
    """
    Endpoint temporal para inicializar la base de datos en Vercel.
    Crea las tablas si no existen.
    """
    try:
        from src.infrastructure.database.connection import inicializar_base_de_datos
        inicializar_base_de_datos()
        
        # Opcional: Correr seed básico si no hay datos
        from src.infrastructure.database.connection import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM curso")
            row = cursor.fetchone()
            if row[0] == 0:
                return {"status": "success", "message": "Schema inicializado. Tablas creadas."}
            else:
                return {"status": "success", "message": "Schema ya existe. No se realizaron cambios."}
        finally:
            cursor.close()
                
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e),
            "hint": "Verifica POSTGRES_URL en variables de entorno"
        }

@app.get(
    "/api/debug",
    tags=["Admin"],
    summary="Debug Connection"
)
def debug_connection():
    import os
    import sys
    results = {}
    try:
        import pg8000
        results["pg8000_version"] = pg8000.__version__
        
        db_url = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
        results["has_db_url"] = bool(db_url)
        if db_url:
            from urllib.parse import urlparse
            parsed = urlparse(db_url)
            results["db_host"] = parsed.hostname
            results["db_port"] = parsed.port
            results["db_name"] = parsed.path.lstrip('/')
            
        from src.infrastructure.database.connection import get_db_connection
        conn = get_db_connection()
        if conn:
             results["connection_status"] = "OK"
             # Test query
             cursor = conn.cursor()
             cursor.execute("SELECT 1")
             cursor.close()
             results["query_test"] = "OK"
        else:
             results["connection_status"] = "Failed"
             
    except Exception as e:
        results["error"] = str(e)
        import traceback
        results["traceback"] = traceback.format_exc()
        
    return results


# ============================================================================
# Manejo de Errores Global
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones"""
    print(f"❌ Error no manejado: {exc}")
    print(f"   Request: {request.method} {request.url}")
    
    import traceback
    traceback.print_exc()
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "type": "internal_server_error",
            "error": str(exc) if os.environ.get("VERCEL") else "Ver logs"
        }
    )


# ============================================================================
# Ejecutar aplicación (solo para desarrollo local)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
