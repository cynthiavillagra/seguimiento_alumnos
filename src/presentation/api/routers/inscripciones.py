"""
Router de FastAPI para Inscripciones
Sistema de Seguimiento de Alumnos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.application.services.inscripcion_service import InscripcionService
from src.presentation.api.schemas.inscripcion_schema import (
    InscripcionCreateSchema,
    InscripcionResponseSchema
)
from src.domain.exceptions.domain_exceptions import (
    AlumnoNoEncontradoException,
    CursoNoEncontradoException,
    AlumnoYaInscriptoException,
    InscripcionNoEncontradaException
)

router = APIRouter(
    prefix="/inscripciones",
    tags=["Inscripciones"],
    responses={
        404: {"description": "Recurso no encontrado"},
        409: {"description": "Conflicto (Ya inscripto)"}
    }
)

def get_inscripcion_service() -> InscripcionService:
    from src.infrastructure.database.connection import get_db_connection
    from src.infrastructure.repositories.sqlite.inscripcion_repository_sqlite import InscripcionRepositorySQLite
    from src.infrastructure.repositories.sqlite.alumno_repository_sqlite import AlumnoRepositorySQLite
    from src.infrastructure.repositories.sqlite.curso_repository_sqlite import CursoRepositorySQLite
    
    conexion = get_db_connection()
    inscripcion_repo = InscripcionRepositorySQLite(conexion)
    alumno_repo = AlumnoRepositorySQLite(conexion)
    curso_repo = CursoRepositorySQLite(conexion)
    
    return InscripcionService(inscripcion_repo, alumno_repo, curso_repo)

@router.post(
    "/",
    response_model=InscripcionResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Inscribir alumno a curso"
)
def inscribir_alumno(
    data: InscripcionCreateSchema,
    service: InscripcionService = Depends(get_inscripcion_service)
):
    try:
        inscripcion = service.matricular_alumno(data.alumno_id, data.curso_id)
        return InscripcionResponseSchema.from_entity(inscripcion)
    except AlumnoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CursoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AlumnoYaInscriptoException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al inscribir: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/alumno/{alumno_id}",
    response_model=List[InscripcionResponseSchema],
    summary="Listar inscripciones de un alumno"
)
def listar_por_alumno(
    alumno_id: int,
    service: InscripcionService = Depends(get_inscripcion_service)
):
    try:
        inscripciones = service.listar_inscripciones_alumno(alumno_id)
        return [InscripcionResponseSchema.from_entity(i) for i in inscripciones]
    except AlumnoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al listar inscripciones de alumno: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete(
    "/{inscripcion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancelar inscripción"
)
def cancelar_inscripcion(
    inscripcion_id: int,
    service: InscripcionService = Depends(get_inscripcion_service)
):
    try:
        eliminado = service.cancelar_inscripcion(inscripcion_id)
        if not eliminado:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe inscripcion con ID {inscripcion_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado al cancelar inscripcion: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
