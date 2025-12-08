"""
Entidad: EntregaTP
Sistema de Seguimiento de Alumnos
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class EntregaTP:
    """
    Entidad de Dominio: EntregaTP
    Registra la entrega de un TP por parte de un alumno.
    """
    trabajo_practico_id: int
    alumno_id: int
    fecha_entrega_real: Optional[date] = None
    entregado: bool = False
    es_tardia: bool = False
    id: Optional[int] = None
    fecha_registro: Optional[datetime] = None

    def __post_init__(self):
        if self.trabajo_practico_id <= 0:
            raise ValueError("ID de TP inválido")
        if self.alumno_id <= 0:
            raise ValueError("ID de alumno inválido")
            
        if isinstance(self.fecha_entrega_real, str):
            self.fecha_entrega_real = date.fromisoformat(self.fecha_entrega_real)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'trabajo_practico_id': self.trabajo_practico_id,
            'alumno_id': self.alumno_id,
            'fecha_entrega_real': self.fecha_entrega_real.isoformat() if self.fecha_entrega_real else None,
            'entregado': self.entregado,
            'es_tardia': self.es_tardia,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'EntregaTP':
        return cls(
            id=data.get('id'),
            trabajo_practico_id=data['trabajo_practico_id'],
            alumno_id=data['alumno_id'],
            fecha_entrega_real=date.fromisoformat(data['fecha_entrega_real']) if data.get('fecha_entrega_real') else None,
            entregado=data.get('entregado', False),
            es_tardia=data.get('es_tardia', False),
            fecha_registro=datetime.fromisoformat(data['fecha_registro']) if data.get('fecha_registro') else None
        )
