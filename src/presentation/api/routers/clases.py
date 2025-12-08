"""
Router de FastAPI para Clases
Sistema de Seguimiento de Alumnos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.application.services.clase_service import ClaseService
from src.presentation.api.schemas.clase_schema import (
    ClaseCreateSchema,
    ClaseUpdateSchema,
    ClaseResponseSchema
)
from src.domain.exceptions.domain_exceptions import (
    ClaseNoEncontradaException,
    CursoNoEncontradoException,
    BusinessRuleException
)

router = APIRouter(
    prefix="/clases",
    tags=["Clases"],
    responses={
        404: {"description": "Recurso no encontrado"},
        409: {"description": "Conflicto"}
    }
)

def get_clase_service() -> ClaseService:
    from src.infrastructure.database.connection import get_db_connection
    from src.infrastructure.repositories.postgres.clase_repository_postgres import ClaseRepositoryPostgres
    from src.infrastructure.repositories.postgres.curso_repository_postgres import CursoRepositoryPostgres
    
    conexion = get_db_connection()
    clase_repo = ClaseRepositoryPostgres(conexion)
    curso_repo = CursoRepositoryPostgres(conexion)
    
    return ClaseService(clase_repo, curso_repo)

@router.post(
    "/",
    response_model=ClaseResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva clase"
)
def registrar_clase(
    data: ClaseCreateSchema,
    service: ClaseService = Depends(get_clase_service)
):
    try:
        print(f"Intentando crear clase: curso_id={data.curso_id}, fecha={data.fecha}, numero={data.numero_clase}")
        clase = service.registrar_clase(
            curso_id=data.curso_id,
            numero_clase=data.numero_clase,
            fecha=data.fecha,
            tema=data.tema
        )
        print(f"Clase creada exitosamente: id={clase.id}")
        return ClaseResponseSchema.from_entity(clase)
    except CursoNoEncontradoException as e:
        print(f"Curso no encontrado: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        print(f"Error de regla de negocio: {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al registrar clase: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/curso/{curso_id}",
    response_model=List[ClaseResponseSchema],
    summary="Listar clases de un curso"
)
def listar_clases_curso(
    curso_id: int,
    service: ClaseService = Depends(get_clase_service)
):
    try:
        clases = service.listar_clases_curso(curso_id)
        return [ClaseResponseSchema.from_entity(c) for c in clases]
    except CursoNoEncontradoException:
        # Retornar lista vacía si el curso no existe (más amigable para el frontend)
        return []
    except Exception as e:
        print(f"Error inesperado al listar clases: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/{clase_id}",
    response_model=ClaseResponseSchema,
    summary="Obtener una clase"
)
def obtener_clase(
    clase_id: int,
    service: ClaseService = Depends(get_clase_service)
):
    try:
        clase = service.obtener_clase(clase_id)
        return ClaseResponseSchema.from_entity(clase)
    except ClaseNoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al obtener clase: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.put(
    "/{clase_id}",
    response_model=ClaseResponseSchema,
    summary="Actualizar una clase"
)
def actualizar_clase(
    clase_id: int,
    data: ClaseUpdateSchema,
    service: ClaseService = Depends(get_clase_service)
):
    try:
        clase = service.actualizar_clase(
            clase_id=clase_id,
            numero_clase=data.numero_clase,
            fecha=data.fecha,
            tema=data.tema
        )
        return ClaseResponseSchema.from_entity(clase)
    except ClaseNoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al actualizar clase: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete(
    "/{clase_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una clase"
)
def eliminar_clase(
    clase_id: int,
    service: ClaseService = Depends(get_clase_service)
):
    try:
        eliminado = service.eliminar_clase(clase_id)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe clase con ID {clase_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado al eliminar clase: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
