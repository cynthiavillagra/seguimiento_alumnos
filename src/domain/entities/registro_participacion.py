"""
Entidad: RegistroParticipacion
Sistema de Seguimiento de Alumnos
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.domain.value_objects.enums import NivelParticipacion

@dataclass
class RegistroParticipacion:
    """
    Entidad de Dominio: RegistroParticipacion
    Registra el nivel de participación de un alumno en una clase.
    """
    alumno_id: int
    clase_id: int
    nivel: NivelParticipacion
    comentario: Optional[str] = None
    id: Optional[int] = None
    fecha_registro: Optional[datetime] = None

    def __post_init__(self):
        if self.alumno_id <= 0:
            raise ValueError("ID de alumno inválido")
        if self.clase_id <= 0:
            raise ValueError("ID de clase inválido")
        
        if not isinstance(self.nivel, NivelParticipacion):
             if isinstance(self.nivel, str):
                 self.nivel = NivelParticipacion(self.nivel)
             else:
                 raise ValueError("Nivel de participación inválido")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'alumno_id': self.alumno_id,
            'clase_id': self.clase_id,
            'nivel': self.nivel.value,
            'comentario': self.comentario,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RegistroParticipacion':
        return cls(
            id=data.get('id'),
            alumno_id=data['alumno_id'],
            clase_id=data['clase_id'],
            nivel=NivelParticipacion(data['nivel']),
            comentario=data.get('comentario'),
            fecha_registro=datetime.fromisoformat(data['fecha_registro']) if data.get('fecha_registro') else None
        )
