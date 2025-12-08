"""
Schemas de Pydantic para Inscripcion
Sistema de Seguimiento de Alumnos
"""

from pydantic import BaseModel, Field
from typing import Optional

class InscripcionCreateSchema(BaseModel):
    """Schema para inscribir un alumno a un curso."""
    alumno_id: int = Field(..., gt=0, description="ID del alumno")
    curso_id: int = Field(..., gt=0, description="ID del curso")

class InscripcionResponseSchema(BaseModel):
    """Schema para respuesta de inscripción."""
    id: int
    alumno_id: int
    curso_id: int
    fecha_inscripcion: Optional[str]

    @classmethod
    def from_entity(cls, inscripcion) -> 'InscripcionResponseSchema':
        return cls(
            id=inscripcion.id,
            alumno_id=inscripcion.alumno_id,
            curso_id=inscripcion.curso_id,
            fecha_inscripcion=inscripcion.fecha_inscripcion.isoformat() if inscripcion.fecha_inscripcion else None
        )
    
    class Config:
        from_attributes = True
