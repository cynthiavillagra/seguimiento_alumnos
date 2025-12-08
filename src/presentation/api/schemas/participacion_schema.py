"""
Schemas de Pydantic para RegistroParticipacion
Sistema de Seguimiento de Alumnos
"""

from pydantic import BaseModel, Field
from typing import Optional
from src.domain.value_objects.enums import NivelParticipacion

class ParticipacionCreateSchema(BaseModel):
    alumno_id: int = Field(..., gt=0)
    clase_id: int = Field(..., gt=0)
    nivel: NivelParticipacion
    comentario: Optional[str] = None

class ParticipacionUpdateSchema(BaseModel):
    nivel: Optional[NivelParticipacion] = None
    comentario: Optional[str] = None

class ParticipacionResponseSchema(BaseModel):
    id: int
    alumno_id: int
    clase_id: int
    nivel: str
    comentario: Optional[str]
    fecha_registro: Optional[str]

    @classmethod
    def from_entity(cls, registro) -> 'ParticipacionResponseSchema':
        return cls(
            id=registro.id,
            alumno_id=registro.alumno_id,
            clase_id=registro.clase_id,
            nivel=registro.nivel.value,
            comentario=registro.comentario,
            fecha_registro=registro.fecha_registro.isoformat() if registro.fecha_registro else None
        )
    
    class Config:
        from_attributes = True
        use_enum_values = True
