"""
Schemas de Pydantic para EntregaTP
Sistema de Seguimiento de Alumnos
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class EntregaCreateSchema(BaseModel):
    trabajo_practico_id: int = Field(..., gt=0)
    alumno_id: int = Field(..., gt=0)
    fecha_entrega_real: Optional[date] = None
    entregado: bool = True

class EntregaResponseSchema(BaseModel):
    id: int
    trabajo_practico_id: int
    alumno_id: int
    fecha_entrega_real: Optional[date]
    entregado: bool
    es_tardia: bool
    fecha_registro: Optional[str]

    @classmethod
    def from_entity(cls, entrega) -> 'EntregaResponseSchema':
        return cls(
            id=entrega.id,
            trabajo_practico_id=entrega.trabajo_practico_id,
            alumno_id=entrega.alumno_id,
            fecha_entrega_real=entrega.fecha_entrega_real,
            entregado=entrega.entregado,
            es_tardia=entrega.es_tardia,
            fecha_registro=entrega.fecha_registro.isoformat() if entrega.fecha_registro else None
        )
    
    class Config:
        from_attributes = True
