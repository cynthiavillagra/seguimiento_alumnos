"""
Schemas de Pydantic para TrabajoPractico
Sistema de Seguimiento de Alumnos
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TPCreateSchema(BaseModel):
    curso_id: int = Field(..., gt=0)
    titulo: str = Field(..., min_length=1)
    fecha_entrega: date
    descripcion: Optional[str] = None

class TPUpdateSchema(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1)
    fecha_entrega: Optional[date] = None
    descripcion: Optional[str] = None

class TPResponseSchema(BaseModel):
    id: int
    curso_id: int
    titulo: str
    fecha_entrega: date
    descripcion: Optional[str]
    fecha_creacion: Optional[str]

    @classmethod
    def from_entity(cls, tp) -> 'TPResponseSchema':
        return cls(
            id=tp.id,
            curso_id=tp.curso_id,
            titulo=tp.titulo,
            fecha_entrega=tp.fecha_entrega,
            descripcion=tp.descripcion,
            fecha_creacion=tp.fecha_creacion.isoformat() if tp.fecha_creacion else None
        )
    
    class Config:
        from_attributes = True
