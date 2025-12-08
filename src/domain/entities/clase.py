"""
Entidad: Clase
Sistema de Seguimiento de Alumnos
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Clase:
    """
    Entidad de Dominio: Clase
    Representa una sesión de cursada específica en una fecha determinada.
    """
    curso_id: int
    fecha: date
    numero_clase: int
    tema: Optional[str] = None
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None

    def __post_init__(self):
        if self.curso_id <= 0:
            raise ValueError("El ID del curso debe ser mayor a 0")
        if self.numero_clase <= 0:
            raise ValueError("El número de clase debe ser mayor a 0")
        
        # Validar que fecha sea un date o parsearlo si es string (ISO)
        if isinstance(self.fecha, str):
            self.fecha = date.fromisoformat(self.fecha)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'curso_id': self.curso_id,
            'fecha': self.fecha.isoformat(),
            'numero_clase': self.numero_clase,
            'tema': self.tema,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Clase':
        return cls(
            id=data.get('id'),
            curso_id=data['curso_id'],
            fecha=date.fromisoformat(data['fecha']) if isinstance(data['fecha'], str) else data['fecha'],
            numero_clase=data['numero_clase'],
            tema=data.get('tema'),
            fecha_creacion=datetime.fromisoformat(data['fecha_creacion']) if data.get('fecha_creacion') else None
        )
