"""
Router de FastAPI para Entregas de TP
Sistema de Seguimiento de Alumnos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.application.services.entrega_service import EntregaTPService
from src.presentation.api.schemas.entrega_schema import (
    EntregaCreateSchema,
    EntregaResponseSchema
)
from src.domain.exceptions.domain_exceptions import (
    TrabajoPracticoNoEncontradoException,
    AlumnoNoInscriptoException
)

router = APIRouter(
    prefix="/entregas",
    tags=["Entregas"],
    responses={
        404: {"description": "Recurso no encontrado"}
    }
)

def get_entrega_service() -> EntregaTPService:
    from src.infrastructure.database.connection import get_db_connection
    from src.infrastructure.repositories.postgres.entrega_repository_postgres import EntregaTPRepositoryPostgres
    from src.infrastructure.repositories.postgres.tp_repository_postgres import TrabajoPracticoRepositoryPostgres
    from src.infrastructure.repositories.postgres.inscripcion_repository_postgres import InscripcionRepositoryPostgres
    
    conexion = get_db_connection()
    entrega_repo = EntregaTPRepositoryPostgres(conexion)
    tp_repo = TrabajoPracticoRepositoryPostgres(conexion)
    inscripcion_repo = InscripcionRepositoryPostgres(conexion)
    
    return EntregaTPService(entrega_repo, tp_repo, inscripcion_repo)

@router.post(
    "/",
    response_model=EntregaResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar entrega de TP"
)
def registrar_entrega(
    data: EntregaCreateSchema,
    service: EntregaTPService = Depends(get_entrega_service)
):
    try:
        entrega = service.registrar_entrega(
            tp_id=data.trabajo_practico_id,
            alumno_id=data.alumno_id,
            fecha_entrega_real=data.fecha_entrega_real,
            entregado=data.entregado
        )
        return EntregaResponseSchema.from_entity(entrega)
    except TrabajoPracticoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AlumnoNoInscriptoException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al registrar entrega: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/tp/{tp_id}",
    response_model=List[EntregaResponseSchema],
    summary="Listar entregas de un TP"
)
def listar_entregas_tp(
    tp_id: int,
    service: EntregaTPService = Depends(get_entrega_service)
):
    try:
        entregas = service.listar_entregas_tp(tp_id)
        return [EntregaResponseSchema.from_entity(e) for e in entregas]
    except TrabajoPracticoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al listar entregas: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete(
    "/{entrega_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar entrega"
)
def eliminar_entrega(
    entrega_id: int,
    service: EntregaTPService = Depends(get_entrega_service)
):
    try:
        eliminado = service.eliminar_entrega(entrega_id)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe entrega con ID {entrega_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado al eliminar entrega: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
