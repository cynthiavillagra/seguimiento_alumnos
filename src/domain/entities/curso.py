"""
Entidad: Curso
Sistema de Seguimiento de Alumnos

Representa una materia dictada en un período específico (año + cuatrimestre).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Curso:
    """
    Entidad de Dominio: Curso
    
    Representa una materia dictada en un período académico específico.
    
    Responsabilidades:
    - Almacenar información del curso (materia, período, docente)
    - Validar que el cuatrimestre sea válido (1 o 2)
    - Validar que el año sea razonable
    
    Reglas de Negocio:
    - El cuatrimestre debe ser 1 o 2
    - El año debe estar en un rango válido (2000-2100)
    - El nombre de la materia no puede estar vacío
    - Debe tener un docente responsable asignado
    
    Ejemplo:
        curso = Curso(
            nombre_materia="Programación I",
            anio=2025,
            cuatrimestre=1,
            docente_responsable="Prof. García"
        )
    """
    
    nombre_materia: str
    anio: int
    cuatrimestre: int
    docente_responsable: str
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones al crear la instancia"""
        self._validar_datos()
    
    def _validar_datos(self) -> None:
        """Valida que los datos del curso sean correctos"""
        if not self.nombre_materia or not self.nombre_materia.strip():
            raise ValueError("El nombre de la materia no puede estar vacío")
        
        if not self.docente_responsable or not self.docente_responsable.strip():
            raise ValueError("El docente responsable no puede estar vacío")
        
        if self.anio < 2000 or self.anio > 2100:
            raise ValueError(f"Año inválido: {self.anio}. Debe estar entre 2000 y 2100")
        
        if self.cuatrimestre not in [1, 2]:
            raise ValueError(f"Cuatrimestre inválido: {self.cuatrimestre}. Debe ser 1 o 2")
    
    def nombre_completo(self) -> str:
        """
        Retorna el nombre completo del curso con período.
        
        Returns:
            str: Nombre en formato "Materia - Año/Cuatrimestre"
        """
        return f"{self.nombre_materia} - {self.anio}/{self.cuatrimestre}°C"
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'id': self.id,
            'nombre_materia': self.nombre_materia,
            'anio': self.anio,
            'cuatrimestre': self.cuatrimestre,
            'docente_responsable': self.docente_responsable,
            'nombre_completo': self.nombre_completo(),
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Curso':
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre_materia=data['nombre_materia'],
            anio=data['anio'],
            cuatrimestre=data['cuatrimestre'],
            docente_responsable=data['docente_responsable'],
            fecha_creacion=datetime.fromisoformat(data['fecha_creacion']) if data.get('fecha_creacion') else None
        )
    
    def __str__(self) -> str:
        return f"Curso({self.nombre_completo()}, Docente: {self.docente_responsable})"
