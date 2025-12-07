"""
Entidad: RegistroAsistencia
Sistema de Seguimiento de Alumnos
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.domain.value_objects.enums import EstadoAsistencia


@dataclass
class RegistroAsistencia:
    """
    Entidad de Dominio: RegistroAsistencia
    
    Registra la asistencia de un alumno a una clase específica.
    
    Responsabilidades:
    - Almacenar el estado de asistencia de un alumno en una clase
    - Validar que el estado sea uno de los permitidos
    
    Reglas de Negocio:
    - Solo puede haber un registro de asistencia por alumno por clase
    - El estado debe ser uno de: Presente, Ausente, Tardanza, Justificada
    - El alumno debe estar inscripto en el curso de la clase (validado en servicio)
    
    Decisión de diseño:
    - Usamos el enum EstadoAsistencia en lugar de strings
    - Esto garantiza type-safety y evita errores de tipeo
    """
    
    alumno_id: int
    clase_id: int
    estado: EstadoAsistencia
    id: Optional[int] = None
    fecha_registro: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones al crear la instancia"""
        self._validar_datos()
    
    def _validar_datos(self) -> None:
        """Valida que los datos sean correctos"""
        if not isinstance(self.estado, EstadoAsistencia):
            # Si recibimos un string, intentamos convertirlo
            if isinstance(self.estado, str):
                try:
                    self.estado = EstadoAsistencia(self.estado)
                except ValueError:
                    raise ValueError(
                        f"Estado inválido: {self.estado}. "
                        f"Debe ser uno de: {EstadoAsistencia.valores_validos()}"
                    )
            else:
                raise ValueError("El estado debe ser un EstadoAsistencia o string válido")
        
        if self.alumno_id <= 0:
            raise ValueError("El alumno_id debe ser mayor a 0")
        
        if self.clase_id <= 0:
            raise ValueError("El clase_id debe ser mayor a 0")
    
    def cuenta_como_presente(self) -> bool:
        """
        Determina si este registro cuenta como "presente" para el cálculo de asistencia.
        
        Regla de negocio:
        - Presente, Tardanza y Justificada cuentan como presente
        - Solo Ausente no cuenta
        
        Returns:
            bool: True si cuenta como presente
        """
        return self.estado in [
            EstadoAsistencia.PRESENTE,
            EstadoAsistencia.TARDANZA,
            EstadoAsistencia.JUSTIFICADA
        ]
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'id': self.id,
            'alumno_id': self.alumno_id,
            'clase_id': self.clase_id,
            'estado': self.estado.value,
            'cuenta_como_presente': self.cuenta_como_presente(),
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RegistroAsistencia':
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get('id'),
            alumno_id=data['alumno_id'],
            clase_id=data['clase_id'],
            estado=EstadoAsistencia(data['estado']),
            fecha_registro=datetime.fromisoformat(data['fecha_registro']) if data.get('fecha_registro') else None
        )
    
    def __str__(self) -> str:
        return f"RegistroAsistencia(Alumno {self.alumno_id}, Clase {self.clase_id}, Estado: {self.estado.value})"
