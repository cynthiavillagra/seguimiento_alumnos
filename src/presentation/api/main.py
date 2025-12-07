"""
Aplicación Principal de FastAPI
Sistema de Seguimiento de Alumnos

Este es el punto de entrada de la API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.infrastructure.database.connection import inicializar_base_de_datos
from src.presentation.api.routers import alumnos


# ============================================================================
# Lifecycle Events
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    
    Decisión de diseño: Lifespan context manager
    - Se ejecuta al iniciar la aplicación (startup)
    - Se ejecuta al cerrar la aplicación (shutdown)
    - Reemplaza los decoradores @app.on_event("startup") (deprecated)
    """
    # Startup: Inicializar base de datos
    print("🚀 Iniciando aplicación...")
    try:
        inicializar_base_de_datos()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        raise
    
    yield  # La aplicación está corriendo
    
    # Shutdown: Limpiar recursos
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

# Decisión de diseño: CORS permisivo en MVP
# En producción, restringir origins a dominios específicos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: ["https://mi-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Incluir Routers
# ============================================================================

# Decisión de diseño: Routers separados por recurso
# Facilita organización y permite versionar la API
app.include_router(alumnos.router)

# Aquí se incluirían los demás routers:
# app.include_router(cursos.router)
# app.include_router(asistencias.router)
# app.include_router(alertas.router)
# etc.


# ============================================================================
# Endpoints de Health Check
# ============================================================================

@app.get(
    "/",
    tags=["Health"],
    summary="Health check",
    description="Verifica que la API esté funcionando"
)
def root():
    """
    Endpoint raíz de la API.
    
    Útil para:
    - Health checks de Vercel/Docker
    - Verificar que la API está corriendo
    """
    return {
        "message": "API de Seguimiento de Alumnos",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check detallado",
    description="Verifica el estado de la API y sus dependencias"
)
def health_check():
    """
    Health check detallado.
    
    Verifica:
    - API corriendo
    - Conexión a base de datos
    """
    from src.infrastructure.database.connection import get_db_connection
    
    try:
        # Intentar conectar a la BD
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "api": "healthy",
        "database": db_status,
        "version": "1.0.0"
    }


# ============================================================================
# Manejo de Errores Global
# ============================================================================

from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Manejador global de excepciones no capturadas.
    
    Decisión de diseño: Logging centralizado
    - En producción, esto debería loggear a un servicio (Sentry, CloudWatch, etc.)
    - No exponer detalles internos al cliente
    """
    print(f"❌ Error no manejado: {exc}")
    print(f"   Request: {request.method} {request.url}")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "type": "internal_server_error"
        }
    )


# ============================================================================
# Ejecutar aplicación (solo para desarrollo local)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Decisión de diseño: Configuración de desarrollo
    # En producción, usar gunicorn + uvicorn workers
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )
