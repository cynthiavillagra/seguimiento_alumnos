"""
Schemas de Pydantic para Clase
Sistema de Seguimiento de Alumnos
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ClaseCreateSchema(BaseModel):
    curso_id: int = Field(..., gt=0)
    numero_clase: int = Field(..., gt=0)
    fecha: date
    tema: Optional[str] = None

class ClaseUpdateSchema(BaseModel):
    numero_clase: Optional[int] = Field(None, gt=0)
    fecha: Optional[date] = None
    tema: Optional[str] = None

class ClaseResponseSchema(BaseModel):
    id: int
    curso_id: int
    numero_clase: int
    fecha: date
    tema: Optional[str]
    fecha_creacion: Optional[str]

    @classmethod
    def from_entity(cls, clase) -> 'ClaseResponseSchema':
        return cls(
            id=clase.id,
            curso_id=clase.curso_id,
            numero_clase=clase.numero_clase,
            fecha=clase.fecha,
            tema=clase.tema,
            fecha_creacion=clase.fecha_creacion.isoformat() if clase.fecha_creacion else None
        )
    
    class Config:
        from_attributes = True
