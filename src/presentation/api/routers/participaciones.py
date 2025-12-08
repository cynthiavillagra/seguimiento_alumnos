"""
Router de FastAPI para Participaciones
Sistema de Seguimiento de Alumnos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.application.services.participacion_service import ParticipacionService
from src.presentation.api.schemas.participacion_schema import (
    ParticipacionCreateSchema,
    ParticipacionUpdateSchema,
    ParticipacionResponseSchema
)
from src.domain.exceptions.domain_exceptions import (
    ClaseNoEncontradaException,
    AlumnoNoInscriptoException
)

router = APIRouter(
    prefix="/participaciones",
    tags=["Participaciones"],
    responses={
        404: {"description": "Recurso no encontrado"},
        409: {"description": "Conflicto"}
    }
)

def get_participacion_service() -> ParticipacionService:
    from src.infrastructure.database.connection import get_db_connection
    from src.infrastructure.repositories.postgres.participacion_repository_postgres import RegistroParticipacionRepositoryPostgres
    from src.infrastructure.repositories.postgres.clase_repository_postgres import ClaseRepositoryPostgres
    from src.infrastructure.repositories.postgres.inscripcion_repository_postgres import InscripcionRepositoryPostgres
    
    conexion = get_db_connection()
    participacion_repo = RegistroParticipacionRepositoryPostgres(conexion)
    clase_repo = ClaseRepositoryPostgres(conexion)
    inscripcion_repo = InscripcionRepositoryPostgres(conexion)
    
    return ParticipacionService(participacion_repo, clase_repo, inscripcion_repo)

@router.post(
    "/",
    response_model=ParticipacionResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar participación"
)
def registrar_participacion(
    data: ParticipacionCreateSchema,
    service: ParticipacionService = Depends(get_participacion_service)
):
    try:
        registro = service.registrar_participacion(
            alumno_id=data.alumno_id,
            clase_id=data.clase_id,
            nivel=data.nivel.value,
            comentario=data.comentario
        )
        return ParticipacionResponseSchema.from_entity(registro)
    except ClaseNoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AlumnoNoInscriptoException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al registrar participacion: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/clase/{clase_id}",
    response_model=List[ParticipacionResponseSchema],
    summary="Listar participaciones por clase"
)
def listar_por_clase(
    clase_id: int,
    service: ParticipacionService = Depends(get_participacion_service)
):
    try:
        registros = service.listar_participaciones_clase(clase_id)
        return [ParticipacionResponseSchema.from_entity(r) for r in registros]
    except ClaseNoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al listar participaciones: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.put(
    "/{participacion_id}",
    response_model=ParticipacionResponseSchema,
    summary="Actualizar participación"
)
def actualizar_participacion(
    participacion_id: int,
    data: ParticipacionUpdateSchema,
    service: ParticipacionService = Depends(get_participacion_service)
):
    try:
        nivel_value = data.nivel.value if data.nivel else None
        registro = service.actualizar_participacion(
            participacion_id=participacion_id,
            nivel=nivel_value,
            comentario=data.comentario
        )
        return ParticipacionResponseSchema.from_entity(registro)
    except ValueError as e:
         if "no encontrada" in str(e):
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al actualizar participacion: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete(
    "/{participacion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar registro de participación"
)
def eliminar_participacion(
    participacion_id: int,
    service: ParticipacionService = Depends(get_participacion_service)
):
    try:
        eliminado = service.eliminar_participacion(participacion_id)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe participacion con ID {participacion_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado al eliminar participacion: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
