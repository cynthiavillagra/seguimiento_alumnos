"""
Entidad: Inscripcion
Sistema de Seguimiento de Alumnos
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Inscripcion:
    """
    Entidad de Dominio: Inscripcion
    Relaciona un alumno con un curso.
    """
    alumno_id: int
    curso_id: int
    id: Optional[int] = None
    fecha_inscripcion: Optional[datetime] = None

    def __post_init__(self):
        if self.alumno_id <= 0:
            raise ValueError("ID de alumno inválido")
        if self.curso_id <= 0:
            raise ValueError("ID de curso inválido")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'alumno_id': self.alumno_id,
            'curso_id': self.curso_id,
            'fecha_inscripcion': self.fecha_inscripcion.isoformat() if self.fecha_inscripcion else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Inscripcion':
        return cls(
            id=data.get('id'),
            alumno_id=data['alumno_id'],
            curso_id=data['curso_id'],
            fecha_inscripcion=datetime.fromisoformat(data['fecha_inscripcion']) if data.get('fecha_inscripcion') else None
        )
