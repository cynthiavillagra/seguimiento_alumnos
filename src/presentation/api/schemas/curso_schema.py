"""
Schemas de Pydantic para Curso
Sistema de Seguimiento de Alumnos
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CursoCreateSchema(BaseModel):
    """Schema para crear un curso."""
    
    nombre_materia: str = Field(..., min_length=1, description="Nombre de la materia")
    anio: int = Field(..., ge=2000, le=2100, description="Año del curso")
    cuatrimestre: int = Field(..., ge=1, le=2, description="Cuatrimestre (1 o 2)")
    docente_responsable: str = Field(..., min_length=1, description="Docente responsable")

    @field_validator('nombre_materia', 'docente_responsable')
    @classmethod
    def validar_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('No puede estar vacío o contener solo espacios')
        return v.strip()

class CursoUpdateSchema(BaseModel):
    """Schema para actualizar un curso."""
    
    nombre_materia: Optional[str] = Field(None, min_length=1, description="Nombre de la materia")
    anio: Optional[int] = Field(None, ge=2000, le=2100, description="Año del curso")
    cuatrimestre: Optional[int] = Field(None, ge=1, le=2, description="Cuatrimestre (1 o 2)")
    docente_responsable: Optional[str] = Field(None, min_length=1, description="Docente responsable")

class CursoResponseSchema(BaseModel):
    """Schema para respuestas de curso."""
    
    id: int
    nombre_materia: str
    anio: int
    cuatrimestre: int
    docente_responsable: str
    nombre_completo: str
    fecha_creacion: Optional[str]

    @classmethod
    def from_entity(cls, curso) -> 'CursoResponseSchema':
        return cls(
            id=curso.id,
            nombre_materia=curso.nombre_materia,
            anio=curso.anio,
            cuatrimestre=curso.cuatrimestre,
            docente_responsable=curso.docente_responsable,
            nombre_completo=curso.nombre_completo(),
            fecha_creacion=curso.fecha_creacion.isoformat() if curso.fecha_creacion else None
        )
    
    class Config:
        from_attributes = True

class CursoListResponseSchema(BaseModel):
    """Schema para listado de cursos."""
    
    total: int
    limite: Optional[int]
    offset: int
    cursos: list[CursoResponseSchema]
