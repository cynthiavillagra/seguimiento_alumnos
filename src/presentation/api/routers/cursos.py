"""
Router de FastAPI para Cursos
Sistema de Seguimiento de Alumnos
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from src.application.services.curso_service import CursoService
from src.presentation.api.schemas.curso_schema import (
    CursoCreateSchema,
    CursoUpdateSchema,
    CursoResponseSchema,
    CursoListResponseSchema
)
from src.domain.exceptions.domain_exceptions import (
    CursoNoEncontradoException,
    CuatrimestreInvalidoException
)

router = APIRouter(
    prefix="/cursos",
    tags=["Cursos"],
    responses={
        404: {"description": "Curso no encontrado"}
    }
)

def get_curso_service() -> CursoService:
    from src.infrastructure.database.connection import get_db_connection
    from src.infrastructure.repositories.postgres.curso_repository_postgres import CursoRepositoryPostgres
    
    conexion = get_db_connection()
    curso_repo = CursoRepositoryPostgres(conexion)
    return CursoService(curso_repo)

@router.post(
    "/",
    response_model=CursoResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo curso"
)
def crear_curso(
    curso_data: CursoCreateSchema,
    curso_service: CursoService = Depends(get_curso_service)
):
    try:
        curso = curso_service.crear_curso(
            nombre_materia=curso_data.nombre_materia,
            anio=curso_data.anio,
            cuatrimestre=curso_data.cuatrimestre,
            docente_responsable=curso_data.docente_responsable
        )
        return CursoResponseSchema.from_entity(curso)
    except CuatrimestreInvalidoException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al crear curso: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/{curso_id}",
    response_model=CursoResponseSchema,
    summary="Obtener un curso por ID"
)
def obtener_curso(
    curso_id: int,
    curso_service: CursoService = Depends(get_curso_service)
):
    try:
        curso = curso_service.obtener_curso(curso_id)
        return CursoResponseSchema.from_entity(curso)
    except CursoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al obtener curso: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get(
    "/",
    response_model=CursoListResponseSchema,
    summary="Listar cursos"
)
def listar_cursos(
    limite: Optional[int] = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    anio: Optional[int] = Query(None, ge=2000, le=2100),
    cuatrimestre: Optional[int] = Query(None, ge=1, le=2),
    curso_service: CursoService = Depends(get_curso_service)
):
    try:
        cursos = curso_service.listar_cursos(
            limite=limite,
            offset=offset,
            anio=anio,
            cuatrimestre=cuatrimestre
        )
        # Nota: El servicio no tiene contar_total, pero podemos implementarlo o usar len()
        # Para ser consistentes con el schema, necesitamos 'total'.
        # Usaremos algo simple por ahora, aunque ineficiente para muchos registros
        all_cursos = curso_service.listar_cursos(anio=anio, cuatrimestre=cuatrimestre) 
        total = len(all_cursos)
        
        return CursoListResponseSchema(
            total=total,
            limite=limite,
            offset=offset,
            cursos=[CursoResponseSchema.from_entity(c) for c in cursos]
        )
    except Exception as e:
        print(f"Error inesperado al listar cursos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.put(
    "/{curso_id}",
    response_model=CursoResponseSchema,
    summary="Actualizar un curso"
)
def actualizar_curso(
    curso_id: int,
    curso_data: CursoUpdateSchema,
    curso_service: CursoService = Depends(get_curso_service)
):
    try:
        curso = curso_service.actualizar_curso(
            curso_id=curso_id,
            nombre_materia=curso_data.nombre_materia,
            anio=curso_data.anio,
            cuatrimestre=curso_data.cuatrimestre,
            docente_responsable=curso_data.docente_responsable
        )
        return CursoResponseSchema.from_entity(curso)
    except CursoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CuatrimestreInvalidoException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado al actualizar curso: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete(
    "/{curso_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un curso"
)
def eliminar_curso(
    curso_id: int,
    curso_service: CursoService = Depends(get_curso_service)
):
    try:
        eliminado = curso_service.eliminar_curso(curso_id)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe curso con ID {curso_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error inesperado al eliminar curso: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
