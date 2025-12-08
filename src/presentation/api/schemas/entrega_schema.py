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
    estado: str = 'entregado'
    nota: Optional[float] = Field(None, ge=1, le=10)
    observaciones: Optional[str] = None

class EntregaResponseSchema(BaseModel):
    id: int
    trabajo_practico_id: int
    alumno_id: int
    fecha_entrega_real: Optional[date]
    entregado: bool
    es_tardia: bool
    estado: str
    nota: Optional[float]
    observaciones: Optional[str]
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
            estado=entrega.estado,
            nota=entrega.nota,
            observaciones=entrega.observaciones,
            fecha_registro=entrega.fecha_registro.isoformat() if entrega.fecha_registro else None
        )
    
    class Config:
        from_attributes = True
