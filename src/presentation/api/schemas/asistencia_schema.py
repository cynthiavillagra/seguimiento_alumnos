"""
Schemas de Pydantic para RegistroAsistencia
Sistema de Seguimiento de Alumnos
"""

from pydantic import BaseModel, Field
from typing import Optional
from src.domain.value_objects.enums import EstadoAsistencia

class AsistenciaCreateSchema(BaseModel):
    alumno_id: int = Field(..., gt=0)
    clase_id: int = Field(..., gt=0)
    estado: EstadoAsistencia

class AsistenciaUpdateSchema(BaseModel):
    estado: EstadoAsistencia

class AsistenciaResponseSchema(BaseModel):
    id: int
    alumno_id: int
    clase_id: int
    estado: str
    cuenta_como_presente: bool
    fecha_registro: Optional[str]

    @classmethod
    def from_entity(cls, registro) -> 'AsistenciaResponseSchema':
        return cls(
            id=registro.id,
            alumno_id=registro.alumno_id,
            clase_id=registro.clase_id,
            estado=registro.estado.value,
            cuenta_como_presente=registro.cuenta_como_presente(),
            fecha_registro=registro.fecha_registro.isoformat() if registro.fecha_registro else None
        )
    
    class Config:
        from_attributes = True
        use_enum_values = True
