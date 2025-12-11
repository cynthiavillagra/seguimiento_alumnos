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

# Router de alertas optimizado
from src.presentation.api.routers import alertas
app.include_router(alertas.router, prefix=api_prefix)

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
        from src.infrastructure.database.connection import inicializar_base_de_datos, get_db_connection
        
        # Inicializar schema
        result = inicializar_base_de_datos()
        
        # Verificar si hay cursos - en nueva transacción limpia
        conn = get_db_connection()
        try:
            conn.rollback()  # Asegurar estado limpio
        except:
            pass
            
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM curso")
            row = cursor.fetchone()
            conn.commit()
            curso_count = row[0] if row else 0
        except Exception as e:
            conn.rollback()
            curso_count = 0
        finally:
            cursor.close()
        
        return {
            "status": "success", 
            "message": f"Schema listo. {result.get('success', 0)} statements OK, {result.get('skipped', 0)} ya existían.",
            "cursos_existentes": curso_count
        }
                
    except Exception as e:
        import traceback
        return {
            "status": "error", 
            "message": str(e),
            "traceback": traceback.format_exc(),
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


@app.get(
    "/api/seed",
    tags=["Admin"],
    summary="Cargar datos de prueba"
)
def seed_database():
    """
    Carga datos de prueba en la base de datos.
    """
    from src.infrastructure.database.connection import get_db_connection
    from datetime import date, datetime
    
    conn = get_db_connection()
    results = {"cursos": 0, "alumnos": 0, "inscripciones": 0, "tps": 0}
    
    try:
        conn.rollback()  # Limpiar estado
        
        # Datos de cursos
        cursos_data = [
            ("Programación I", 2024, 1, "Prof. González"),
            ("Matemática Discreta", 2024, 1, "Prof. Martínez"),
            ("Base de Datos", 2024, 2, "Prof. López"),
            ("Programación II", 2024, 2, "Prof. González"),
        ]
        
        curso_ids = []
        for nombre, anio, cuatri, docente in cursos_data:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO curso (nombre_materia, anio, cuatrimestre, docente_responsable, fecha_creacion) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (nombre, anio, cuatri, docente, datetime.now())
                )
                row = cursor.fetchone()
                conn.commit()
                if row:
                    curso_ids.append(row[0])
                    results["cursos"] += 1
            except Exception as e:
                conn.rollback()
                if 'duplicate' not in str(e).lower():
                    print(f"Error curso: {e}")
            finally:
                cursor.close()
        
        # Datos de alumnos
        alumnos_data = [
            ("Juan", "Pérez", "12345678", "juan.perez@email.com", 2024),
            ("María", "García", "23456789", "maria.garcia@email.com", 2024),
            ("Carlos", "López", "34567890", "carlos.lopez@email.com", 2024),
            ("Ana", "Martínez", "45678901", "ana.martinez@email.com", 2024),
            ("Pedro", "Rodríguez", "56789012", "pedro.rodriguez@email.com", 2023),
            ("Laura", "Fernández", "67890123", "laura.fernandez@email.com", 2023),
            ("Diego", "Sánchez", "78901234", "diego.sanchez@email.com", 2024),
            ("Lucía", "Romero", "89012345", "lucia.romero@email.com", 2024),
        ]
        
        alumno_ids = []
        for nombre, apellido, dni, email, cohorte in alumnos_data:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO alumno (nombre, apellido, dni, email, cohorte, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (nombre, apellido, dni, email, cohorte, datetime.now())
                )
                row = cursor.fetchone()
                conn.commit()
                if row:
                    alumno_ids.append(row[0])
                    results["alumnos"] += 1
            except Exception as e:
                conn.rollback()
                if 'duplicate' not in str(e).lower():
                    print(f"Error alumno: {e}")
            finally:
                cursor.close()
        
        # Inscribir alumnos a cursos
        for alumno_id in alumno_ids:
            for curso_id in curso_ids[:2]:  # Inscribir en los primeros 2 cursos
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO inscripcion (alumno_id, curso_id, fecha_inscripcion) VALUES (%s, %s, %s)",
                        (alumno_id, curso_id, date.today())
                    )
                    conn.commit()
                    results["inscripciones"] += 1
                except Exception as e:
                    conn.rollback()
                finally:
                    cursor.close()
        
        # TPs
        if curso_ids:
            tps_data = [
                (curso_ids[0], "TP1 - Variables y Tipos", "Ejercicios de variables", "2024-04-15"),
                (curso_ids[0], "TP2 - Funciones", "Implementar funciones", "2024-05-01"),
                (curso_ids[1] if len(curso_ids) > 1 else curso_ids[0], "TP1 - Lógica Proposicional", "Ejercicios de lógica", "2024-04-20"),
            ]
            
            for curso_id, titulo, desc, fecha in tps_data:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO trabajo_practico (curso_id, titulo, descripcion, fecha_entrega, fecha_creacion) VALUES (%s, %s, %s, %s, %s)",
                        (curso_id, titulo, desc, fecha, datetime.now())
                    )
                    conn.commit()
                    results["tps"] += 1
                except Exception as e:
                    conn.rollback()
                finally:
                    cursor.close()
        
        return {
            "status": "success",
            "message": "Datos de prueba cargados",
            "results": results
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }


@app.delete(
    "/api/seed",
    tags=["Admin"],
    summary="Borrar datos de prueba"
)
def clear_seed_database():
    """
    Borra los datos de prueba cargados previamente.
    Identifica los datos por DNIs y nombres conocidos.
    """
    from src.infrastructure.database.connection import get_db_connection
    
    conn = get_db_connection()
    results = {"alumnos": 0, "cursos": 0}
    
    # DNIs de prueba conocidos
    test_dnis = ['12345678', '23456789', '34567890', '45678901', '56789012', '67890123', '78901234', '89012345']
    # Nombres de cursos de prueba
    test_cursos = ['Programación I', 'Matemática Discreta', 'Base de Datos', 'Programación II']
    
    try:
        conn.rollback()
        
        # Borrar alumnos de prueba (por DNI)
        for dni in test_dnis:
            cursor = conn.cursor()
            try:
                # Primero obtener el ID del alumno
                cursor.execute("SELECT id FROM alumno WHERE dni = %s", (dni,))
                row = cursor.fetchone()
                if row:
                    alumno_id = row[0]
                    # Borrar registros relacionados
                    cursor.execute("DELETE FROM registro_asistencia WHERE alumno_id = %s", (alumno_id,))
                    cursor.execute("DELETE FROM registro_participacion WHERE alumno_id = %s", (alumno_id,))
                    cursor.execute("DELETE FROM entrega_tp WHERE alumno_id = %s", (alumno_id,))
                    cursor.execute("DELETE FROM inscripcion WHERE alumno_id = %s", (alumno_id,))
                    cursor.execute("DELETE FROM alumno WHERE id = %s", (alumno_id,))
                    conn.commit()
                    results["alumnos"] += 1
            except Exception as e:
                conn.rollback()
                print(f"Error borrando alumno {dni}: {e}")
            finally:
                cursor.close()
        
        # Borrar cursos de prueba (por nombre)
        for nombre in test_cursos:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id FROM curso WHERE nombre_materia = %s", (nombre,))
                row = cursor.fetchone()
                if row:
                    curso_id = row[0]
                    # Borrar registros relacionados
                    cursor.execute("DELETE FROM trabajo_practico WHERE curso_id = %s", (curso_id,))
                    cursor.execute("DELETE FROM clase WHERE curso_id = %s", (curso_id,))
                    cursor.execute("DELETE FROM inscripcion WHERE curso_id = %s", (curso_id,))
                    cursor.execute("DELETE FROM curso WHERE id = %s", (curso_id,))
                    conn.commit()
                    results["cursos"] += 1
            except Exception as e:
                conn.rollback()
                print(f"Error borrando curso {nombre}: {e}")
            finally:
                cursor.close()
        
        return {
            "status": "success",
            "message": "Datos de prueba eliminados",
            "results": results
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }


@app.delete(
    "/api/clear-all",
    tags=["Admin"],
    summary="Borrar TODOS los datos"
)
def clear_all_data():
    """
    Borra TODOS los datos de todas las tablas.
    ¡Cuidado! Esta operación no se puede deshacer.
    """
    from src.infrastructure.database.connection import get_db_connection
    
    conn = get_db_connection()
    results = {}
    
    # Orden específico para respetar constraints de FK
    tables = [
        'entrega_tp',
        'registro_participacion', 
        'registro_asistencia',
        'inscripcion',
        'trabajo_practico',
        'clase',
        'alumno',
        'curso'
    ]
    
    try:
        conn.rollback()
        
        for table in tables:
            cursor = conn.cursor()
            try:
                cursor.execute(f"DELETE FROM {table}")
                results[table] = cursor.rowcount
                conn.commit()
            except Exception as e:
                conn.rollback()
                results[table] = f"error: {str(e)}"
            finally:
                cursor.close()
        
        return {
            "status": "success",
            "message": "Todos los datos eliminados",
            "results": results
        }
        
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }


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
