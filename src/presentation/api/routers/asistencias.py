"""
Router de FastAPI para Asistencias
Sistema de Seguimiento de Alumnos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.application.services.asistencia_service import AsistenciaService
from src.presentation.api.schemas.asistencia_schema import (
    AsistenciaCreateSchema,
    AsistenciaUpdateSchema,
    AsistenciaResponseSchema
)
from src.domain.exceptions.domain_exceptions import (
    ClaseNoEncontradaException,
    AlumnoNoInscriptoException,
    AsistenciaYaRegistradaException
)

router = APIRouter(
    prefix="/asistencias",
    tags=["Asistencias"],
    responses={
        404: {"description": "Recurso no encontrado"},
        409: {"description": "Conflicto"}
    }
)

def get_asistencia_service() -> AsistenciaService:
    from src.infrastructure.database.connection import get_db_connection
    from src.infrastructure.repositories.postgres.asistencia_repository_postgres import RegistroAsistenciaRepositoryPostgres
    from src.infrastructure.repositories.postgres.clase_repository_postgres import ClaseRepositoryPostgres
    from src.infrastructure.repositories.postgres.inscripcion_repository_postgres import InscripcionRepositoryPostgres
    
    conexion = get_db_connection()
    asistencia_repo = RegistroAsistenciaRepositoryPostgres(conexion)
    clase_repo = ClaseRepositoryPostgres(conexion)
    inscripcion_repo = InscripcionRepositoryPostgres(conexion)
    
    return AsistenciaService(asistencia_repo, clase_repo, inscripcion_repo)

@router.post(
    "/",
    response_model=AsistenciaResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar asistencia"
)
def registrar_asistencia(
    data: AsistenciaCreateSchema,
    service: AsistenciaService = Depends(get_asistencia_service)
):
    try:
        registro = service.registrar_asistencia(
            alumno_id=data.alumno_id,
            clase_id=data.clase_id,
            estado=data.estado.value
        )
        return AsistenciaResponseSchema.from_entity(registro)
    except ClaseNoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AlumnoNoInscriptoException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except AsistenciaYaRegistradaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al registrar asistencia: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/clase/{clase_id}",
    response_model=List[AsistenciaResponseSchema],
    summary="Listar asistencias por clase"
)
def listar_por_clase(
    clase_id: int,
    service: AsistenciaService = Depends(get_asistencia_service)
):
    try:
        registros = service.listar_asistencias_clase(clase_id)
        return [AsistenciaResponseSchema.from_entity(r) for r in registros]
    except ClaseNoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al listar asistencias: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.put(
    "/{asistencia_id}",
    response_model=AsistenciaResponseSchema,
    summary="Actualizar estado de asistencia"
)
def actualizar_asistencia(
    asistencia_id: int,
    data: AsistenciaUpdateSchema,
    service: AsistenciaService = Depends(get_asistencia_service)
):
    try:
        registro = service.actualizar_asistencia(
            asistencia_id=asistencia_id,
            nuevo_estado=data.estado.value
        )
        return AsistenciaResponseSchema.from_entity(registro)
    except ValueError as e:
         # TODO: Handle not found specifically
         if "no encontrada" in str(e):
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al actualizar asistencia: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete(
    "/{asistencia_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar registro de asistencia"
)
def eliminar_asistencia(
    asistencia_id: int,
    service: AsistenciaService = Depends(get_asistencia_service)
):
    try:
        eliminado = service.eliminar_asistencia(asistencia_id)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe asistencia con ID {asistencia_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado al eliminar asistencia: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
