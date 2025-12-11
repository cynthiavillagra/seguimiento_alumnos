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

@router.get(
    "/con-stats",
    summary="Listar cursos con estadísticas",
    description="Devuelve cursos con total de alumnos, clases y asistencia promedio"
)
def listar_cursos_con_stats():
    """
    Endpoint optimizado que devuelve cursos con estadísticas calculadas.
    Usado por el dashboard.
    """
    from src.infrastructure.database.connection import get_db_connection
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Obtener cursos con estadísticas en queries eficientes
        cursor.execute("""
            SELECT 
                c.id,
                c.nombre_materia,
                c.anio,
                c.cuatrimestre,
                c.docente_responsable,
                (SELECT COUNT(*) FROM inscripcion i WHERE i.curso_id = c.id) as total_alumnos,
                (SELECT COUNT(*) FROM clase cl WHERE cl.curso_id = c.id) as total_clases
            FROM curso c
            ORDER BY c.anio DESC, c.cuatrimestre DESC, c.nombre_materia
        """)
        
        cursos = []
        for row in cursor.fetchall():
            curso_id, nombre, anio, cuatri, docente, total_alumnos, total_clases = row
            
            # Calcular asistencia promedio
            asistencia_promedio = 0
            if total_clases > 0 and total_alumnos > 0:
                cursor.execute("""
                    SELECT 
                        COUNT(CASE WHEN ra.estado IN ('Presente', 'Tarde') THEN 1 END) as presentes,
                        COUNT(*) as total
                    FROM registro_asistencia ra
                    JOIN clase cl ON ra.clase_id = cl.id
                    WHERE cl.curso_id = %s
                """, (curso_id,))
                stats_row = cursor.fetchone()
                if stats_row and stats_row[1] > 0:
                    asistencia_promedio = round((stats_row[0] / stats_row[1]) * 100)
            
            # Obtener última clase
            ultima_clase = None
            cursor.execute("""
                SELECT fecha FROM clase 
                WHERE curso_id = %s 
                ORDER BY fecha DESC LIMIT 1
            """, (curso_id,))
            fecha_row = cursor.fetchone()
            if fecha_row:
                ultima_clase = fecha_row[0].strftime("%d/%m/%Y") if hasattr(fecha_row[0], 'strftime') else str(fecha_row[0])
            
            # Calcular alumnos en riesgo (simplificado)
            alumnos_en_riesgo = 0
            try:
                # Obtener alumnos inscriptos
                cursor.execute("""
                    SELECT alumno_id FROM inscripcion WHERE curso_id = %s
                """, (curso_id,))
                alumnos_inscritos = [r[0] for r in cursor.fetchall()]
                
                # Obtener clases ordenadas
                cursor.execute("""
                    SELECT id FROM clase WHERE curso_id = %s ORDER BY fecha ASC
                """, (curso_id,))
                clases_ids = [r[0] for r in cursor.fetchall()]
                
                for alumno_id in alumnos_inscritos:
                    es_riesgo = False
                    
                    # Verificar 2 ausencias consecutivas
                    if len(clases_ids) >= 2:
                        asistencias = []
                        for clase_id in clases_ids:
                            cursor.execute("""
                                SELECT estado FROM registro_asistencia 
                                WHERE alumno_id = %s AND clase_id = %s
                            """, (alumno_id, clase_id))
                            r = cursor.fetchone()
                            asistencias.append(r[0] if r else None)
                        
                        # Buscar 2 ausencias consecutivas
                        for i in range(len(asistencias) - 1, 0, -1):
                            if asistencias[i] == 'Ausente' and asistencias[i-1] == 'Ausente':
                                es_riesgo = True
                                break
                    
                    if es_riesgo:
                        alumnos_en_riesgo += 1
            except:
                pass  # En caso de error, dejamos en 0
            
            cursos.append({
                "id": curso_id,
                "nombre_materia": nombre,
                "anio": anio,
                "cuatrimestre": cuatri,
                "docente_responsable": docente,
                "totalAlumnos": total_alumnos,
                "totalClases": total_clases,
                "asistenciaPromedio": asistencia_promedio,
                "alumnosEnRiesgo": alumnos_en_riesgo,
                "ultimaClase": ultima_clase
            })
        
        conn.commit()
        cursor.close()
        
        return {"cursos": cursos, "total": len(cursos)}
        
    except Exception as e:
        print(f"Error obteniendo cursos con stats: {e}")
        import traceback
        traceback.print_exc()
        return {"cursos": [], "total": 0, "error": str(e)}


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
