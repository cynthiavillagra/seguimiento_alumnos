"""
Router de FastAPI para Alumnos
Sistema de Seguimiento de Alumnos

Decisión de diseño: Separación de routers
- Cada recurso (alumnos, cursos, etc.) tiene su propio router
- Facilita organización y mantenimiento
- Permite versionar la API fácilmente
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from src.application.services.alumno_service import AlumnoService
from src.presentation.api.schemas.alumno_schema import (
    AlumnoCreateSchema,
    AlumnoUpdateSchema,
    AlumnoResponseSchema,
    AlumnoListResponseSchema
)
from src.domain.exceptions.domain_exceptions import (
    AlumnoNoEncontradoException,
    DNIDuplicadoException,
    EmailInvalidoException
)


# Crear router
router = APIRouter(
    prefix="/alumnos",
    tags=["Alumnos"],
    responses={
        404: {"description": "Alumno no encontrado"},
        409: {"description": "Conflicto (DNI duplicado)"}
    }
)


# ============================================================================
# Dependency Injection
# ============================================================================

def get_alumno_service() -> AlumnoService:
    """
    Inyección de dependencias para AlumnoService.
    
    Decisión de diseño: Función de dependencia
    - FastAPI llama a esta función automáticamente
    - Crea una nueva instancia del servicio para cada request
    - Permite cambiar la implementación fácilmente
    
    En producción, esto debería:
    - Usar un pool de conexiones
    - Manejar transacciones
    - Implementar retry logic
    """
    from src.infrastructure.database.connection import get_db_connection
    from src.infrastructure.repositories.sqlite.alumno_repository_sqlite import AlumnoRepositorySQLite
    
    conexion = get_db_connection()
    alumno_repo = AlumnoRepositorySQLite(conexion)
    return AlumnoService(alumno_repo)


# ============================================================================
# Endpoints
# ============================================================================

@router.post(
    "/",
    response_model=AlumnoResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo alumno",
    description="Crea un nuevo alumno en el sistema. El DNI debe ser único."
)
def crear_alumno(
    alumno_data: AlumnoCreateSchema,
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """
    Endpoint: POST /alumnos
    
    Caso de Uso: CU-10 - Crear Alumno
    
    Decisión de diseño: Este endpoint SOLO se encarga de:
    1. Recibir y validar datos HTTP (Pydantic lo hace automáticamente)
    2. Delegar al servicio de aplicación
    3. Convertir el resultado a formato HTTP (JSON)
    4. Manejar errores y convertirlos a códigos HTTP apropiados
    
    NO contiene lógica de negocio, NO accede a la BD directamente.
    """
    try:
        alumno = alumno_service.crear_alumno(
            nombre=alumno_data.nombre,
            apellido=alumno_data.apellido,
            dni=alumno_data.dni,
            email=alumno_data.email,
            cohorte=alumno_data.cohorte
        )
        
        return AlumnoResponseSchema.from_entity(alumno)
    
    except EmailInvalidoException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except DNIDuplicadoException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        # Log del error (en producción)
        print(f"Error inesperado al crear alumno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get(
    "/{alumno_id}",
    response_model=AlumnoResponseSchema,
    summary="Obtener un alumno por ID",
    description="Retorna los datos de un alumno específico."
)
def obtener_alumno(
    alumno_id: int,
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """
    Endpoint: GET /alumnos/{id}
    
    Caso de Uso: CU-04 - Consultar Ficha de Alumno (parcial)
    """
    try:
        alumno = alumno_service.obtener_alumno(alumno_id)
        return AlumnoResponseSchema.from_entity(alumno)
    
    except AlumnoNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except Exception as e:
        print(f"Error inesperado al obtener alumno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get(
    "/",
    response_model=AlumnoListResponseSchema,
    summary="Listar alumnos",
    description="Retorna una lista de alumnos con filtros opcionales y paginación."
)
def listar_alumnos(
    limite: Optional[int] = Query(None, ge=1, le=100, description="Límite de resultados por página"),
    offset: int = Query(0, ge=0, description="Número de resultados a saltar"),
    cohorte: Optional[int] = Query(None, ge=2000, le=2100, description="Filtrar por cohorte"),
    buscar: Optional[str] = Query(None, min_length=1, description="Buscar por nombre o apellido"),
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """
    Endpoint: GET /alumnos
    
    Caso de Uso: CU-04 - Consultar Listado de Alumnos
    
    Soporta:
    - Paginación (limite, offset)
    - Filtro por cohorte
    - Búsqueda por nombre/apellido
    """
    try:
        alumnos = alumno_service.listar_alumnos(
            limite=limite,
            offset=offset,
            cohorte=cohorte,
            buscar=buscar
        )
        
        total = alumno_service.contar_alumnos(cohorte=cohorte)
        
        return AlumnoListResponseSchema(
            total=total,
            limite=limite,
            offset=offset,
            alumnos=[AlumnoResponseSchema.from_entity(a) for a in alumnos]
        )
    
    except Exception as e:
        print(f"Error inesperado al listar alumnos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put(
    "/{alumno_id}",
    response_model=AlumnoResponseSchema,
    summary="Actualizar un alumno",
    description="Actualiza los datos de un alumno existente."
)
def actualizar_alumno(
    alumno_id: int,
    alumno_data: AlumnoUpdateSchema,
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """
    Endpoint: PUT /alumnos/{id}
    
    Permite actualización parcial (solo los campos proporcionados).
    """
    try:
        alumno = alumno_service.actualizar_alumno(
            alumno_id=alumno_id,
            nombre=alumno_data.nombre,
            apellido=alumno_data.apellido,
            dni=alumno_data.dni,
            email=alumno_data.email,
            cohorte=alumno_data.cohorte
        )
        
        return AlumnoResponseSchema.from_entity(alumno)
    
    except AlumnoNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except DNIDuplicadoException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    
    except EmailInvalidoException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        print(f"Error inesperado al actualizar alumno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete(
    "/{alumno_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un alumno",
    description="Elimina un alumno del sistema."
)
def eliminar_alumno(
    alumno_id: int,
    alumno_service: AlumnoService = Depends(get_alumno_service)
):
    """
    Endpoint: DELETE /alumnos/{id}
    
    Retorna 204 No Content si se eliminó exitosamente.
    Retorna 404 Not Found si el alumno no existe.
    """
    try:
        eliminado = alumno_service.eliminar_alumno(alumno_id)
        
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe alumno con ID {alumno_id}"
            )
        
        # 204 No Content no retorna body
        return None
    
    except HTTPException:
        raise  # Re-lanzar HTTPException
    
    except Exception as e:
        print(f"Error inesperado al eliminar alumno: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
