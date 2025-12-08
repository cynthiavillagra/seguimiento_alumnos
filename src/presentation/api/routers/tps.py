"""
Router de FastAPI para Trabajos Prácticos
Sistema de Seguimiento de Alumnos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.application.services.tp_service import TrabajoPracticoService
from src.presentation.api.schemas.tp_schema import (
    TPCreateSchema,
    TPUpdateSchema,
    TPResponseSchema
)
from src.domain.exceptions.domain_exceptions import (
    CursoNoEncontradoException,
    TrabajoPracticoNoEncontradoException
)

router = APIRouter(
    prefix="/tps",
    tags=["Trabajos Prácticos"],
    responses={
        404: {"description": "Recurso no encontrado"}
    }
)

def get_tp_service() -> TrabajoPracticoService:
    from src.infrastructure.database.connection import get_db_connection
    from src.infrastructure.repositories.postgres.tp_repository_postgres import TrabajoPracticoRepositoryPostgres
    from src.infrastructure.repositories.postgres.curso_repository_postgres import CursoRepositoryPostgres
    
    conexion = get_db_connection()
    tp_repo = TrabajoPracticoRepositoryPostgres(conexion)
    curso_repo = CursoRepositoryPostgres(conexion)
    
    return TrabajoPracticoService(tp_repo, curso_repo)

@router.post(
    "/",
    response_model=TPResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear Trabajo Práctico"
)
def crear_tp(
    data: TPCreateSchema,
    service: TrabajoPracticoService = Depends(get_tp_service)
):
    try:
        tp = service.crear_tp(
            curso_id=data.curso_id,
            titulo=data.titulo,
            fecha_entrega=data.fecha_entrega,
            descripcion=data.descripcion
        )
        return TPResponseSchema.from_entity(tp)
    except CursoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al crear TP: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/{tp_id}",
    response_model=TPResponseSchema,
    summary="Obtener TP por ID"
)
def obtener_tp(
    tp_id: int,
    service: TrabajoPracticoService = Depends(get_tp_service)
):
    try:
        tp = service.obtener_tp(tp_id)
        return TPResponseSchema.from_entity(tp)
    except TrabajoPracticoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al obtener TP: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/curso/{curso_id}",
    response_model=List[TPResponseSchema],
    summary="Listar TPs de un curso"
)
def listar_tps_curso(
    curso_id: int,
    service: TrabajoPracticoService = Depends(get_tp_service)
):
    try:
        tps = service.listar_tps_curso(curso_id)
        return [TPResponseSchema.from_entity(tp) for tp in tps]
    except CursoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al listar TPs: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.put(
    "/{tp_id}",
    response_model=TPResponseSchema,
    summary="Actualizar TP"
)
def actualizar_tp(
    tp_id: int,
    data: TPUpdateSchema,
    service: TrabajoPracticoService = Depends(get_tp_service)
):
    try:
        tp = service.actualizar_tp(
            tp_id=tp_id,
            titulo=data.titulo,
            descripcion=data.descripcion,
            fecha_entrega=data.fecha_entrega
        )
        return TPResponseSchema.from_entity(tp)
    except TrabajoPracticoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al actualizar TP: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete(
    "/{tp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar TP"
)
def eliminar_tp(
    tp_id: int,
    service: TrabajoPracticoService = Depends(get_tp_service)
):
    try:
        eliminado = service.eliminar_tp(tp_id)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe TP con ID {tp_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado al eliminar TP: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
