"""
Entidad: TrabajoPractico
Sistema de Seguimiento de Alumnos
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class TrabajoPractico:
    """
    Entidad de Dominio: TrabajoPractico
    Representa un trabajo práctico asignado a un curso.
    """
    curso_id: int
    titulo: str
    fecha_entrega: Optional[date] = None
    descripcion: Optional[str] = None
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None

    def __post_init__(self):
        if self.curso_id <= 0:
            raise ValueError("ID de curso inválido")
        if not self.titulo or not self.titulo.strip():
            raise ValueError("El título no puede estar vacío")
            
        if self.fecha_entrega and isinstance(self.fecha_entrega, str):
            self.fecha_entrega = date.fromisoformat(self.fecha_entrega)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'curso_id': self.curso_id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'fecha_entrega': self.fecha_entrega.isoformat(),
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TrabajoPractico':
        return cls(
            id=data.get('id'),
            curso_id=data['curso_id'],
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            fecha_entrega=date.fromisoformat(data['fecha_entrega']) if isinstance(data['fecha_entrega'], str) else data['fecha_entrega'],
            fecha_creacion=datetime.fromisoformat(data['fecha_creacion']) if data.get('fecha_creacion') else None
        )
