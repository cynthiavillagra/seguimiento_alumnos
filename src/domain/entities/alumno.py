"""
Entidad: Alumno
Sistema de Seguimiento de Alumnos

Decisión de diseño: Uso de dataclass
- Reduce boilerplate (no necesitamos escribir __init__, __repr__, etc.)
- Inmutable por defecto si usamos frozen=True (no lo usamos para permitir updates)
- Type hints nativos
- Método __eq__ automático basado en atributos
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import re


@dataclass
class Alumno:
    """
    Entidad de Dominio: Alumno
    
    Representa a un estudiante de la institución.
    
    Responsabilidades:
    - Almacenar datos personales del alumno
    - Validar formato de email
    - Validar datos básicos (nombre, DNI, etc.)
    
    Reglas de Negocio:
    - El DNI debe ser único en el sistema (validado en repositorio)
    - El email debe tener formato válido
    - El nombre y apellido no pueden estar vacíos
    - La cohorte debe ser un año válido (>= 2000)
    
    Decisión de diseño:
    - Esta clase NO conoce nada sobre base de datos, HTTP, JSON, etc.
    - Es una entidad de dominio pura
    - La validación de unicidad de DNI se hace en el repositorio o servicio,
      no aquí (porque requiere acceso a BD)
    """
    
    # Atributos obligatorios
    nombre: str
    apellido: str
    dni: str
    email: str
    cohorte: int
    
    # Atributos opcionales (asignados por el sistema)
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    
    def __post_init__(self):
        """
        Validaciones básicas al crear la instancia.
        
        Decisión de diseño: Validar en __post_init__
        - Se ejecuta automáticamente después de __init__ (generado por dataclass)
        - Permite validar datos inmediatamente al crear el objeto
        - Lanza excepciones si los datos son inválidos
        """
        self._validar_datos_basicos()
    
    def _validar_datos_basicos(self) -> None:
        """Valida que los datos básicos sean correctos"""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        if not self.apellido or not self.apellido.strip():
            raise ValueError("El apellido no puede estar vacío")
        
        if not self.dni or not self.dni.strip():
            raise ValueError("El DNI no puede estar vacío")
        
        if not self.email or not self.email.strip():
            raise ValueError("El email no puede estar vacío")
        
        if self.cohorte < 2000 or self.cohorte > 2100:
            raise ValueError(f"Cohorte inválida: {self.cohorte}. Debe estar entre 2000 y 2100")
        
        # Validar formato de email
        if not self.validar_email():
            raise ValueError(f"Email inválido: {self.email}")
    
    def validar_email(self) -> bool:
        """
        Valida que el email tenga un formato válido.
        
        Decisión de diseño: Regex simple
        - No validamos si el email existe realmente
        - Solo validamos formato básico: algo@algo.algo
        - Para validación más estricta, se puede usar una librería como email-validator
        
        Returns:
            bool: True si el email es válido, False en caso contrario
        """
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, self.email) is not None
    
    def nombre_completo(self) -> str:
        """
        Retorna el nombre completo del alumno.
        
        Returns:
            str: Nombre completo en formato "Apellido, Nombre"
        """
        return f"{self.apellido}, {self.nombre}"
    
    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario.
        
        Decisión de diseño: Método to_dict
        - Facilita la serialización a JSON
        - Útil para respuestas de API
        - Separa la representación interna de la externa
        
        Returns:
            dict: Diccionario con los datos del alumno
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'email': self.email,
            'cohorte': self.cohorte,
            'nombre_completo': self.nombre_completo(),
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Alumno':
        """
        Crea una instancia de Alumno desde un diccionario.
        
        Útil para deserialización desde JSON o desde filas de BD.
        
        Args:
            data: Diccionario con los datos del alumno
        
        Returns:
            Alumno: Nueva instancia de Alumno
        """
        return cls(
            id=data.get('id'),
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            email=data['email'],
            cohorte=data['cohorte'],
            fecha_creacion=datetime.fromisoformat(data['fecha_creacion']) if data.get('fecha_creacion') else None
        )
    
    def __str__(self) -> str:
        """Representación en string del alumno"""
        return f"Alumno({self.nombre_completo()}, DNI: {self.dni}, Cohorte: {self.cohorte})"
    
    def __repr__(self) -> str:
        """Representación técnica del alumno (para debugging)"""
        return (f"Alumno(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', "
                f"dni='{self.dni}', email='{self.email}', cohorte={self.cohorte})")
