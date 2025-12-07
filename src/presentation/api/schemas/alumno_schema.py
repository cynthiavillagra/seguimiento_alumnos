"""
Schemas de Pydantic para Alumno
Sistema de Seguimiento de Alumnos

Decisión de diseño: Pydantic para validación
- Pydantic valida automáticamente datos de entrada
- Genera documentación automática (Swagger/OpenAPI)
- Convierte tipos automáticamente
- Separa modelos de API de entidades de dominio

Separación de Schemas:
- CreateSchema: Para crear (POST) - sin ID
- UpdateSchema: Para actualizar (PUT/PATCH) - campos opcionales
- ResponseSchema: Para respuestas (GET) - con ID y datos calculados
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class AlumnoCreateSchema(BaseModel):
    """
    Schema para crear un alumno (POST /alumnos).
    
    Decisión de diseño: Validaciones en Pydantic
    - EmailStr valida formato de email automáticamente
    - Field() permite agregar validaciones y documentación
    - Los mensajes de error son automáticos y claros
    """
    
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del alumno",
        examples=["Juan"]
    )
    
    apellido: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Apellido del alumno",
        examples=["Pérez"]
    )
    
    dni: str = Field(
        ...,
        min_length=7,
        max_length=20,
        description="DNI o documento de identidad (debe ser único)",
        examples=["12345678"]
    )
    
    email: EmailStr = Field(
        ...,
        description="Email del alumno",
        examples=["juan.perez@example.com"]
    )
    
    cohorte: int = Field(
        ...,
        ge=2000,
        le=2100,
        description="Año de ingreso del alumno",
        examples=[2024]
    )
    
    @field_validator('nombre', 'apellido')
    @classmethod
    def validar_no_vacio(cls, v: str) -> str:
        """Valida que nombre y apellido no sean solo espacios"""
        if not v.strip():
            raise ValueError('No puede estar vacío o contener solo espacios')
        return v.strip()
    
    @field_validator('dni')
    @classmethod
    def validar_dni(cls, v: str) -> str:
        """Valida formato básico de DNI"""
        # Remover espacios
        v = v.strip()
        
        # Validar que no esté vacío
        if not v:
            raise ValueError('El DNI no puede estar vacío')
        
        return v
    
    class Config:
        """Configuración del schema"""
        json_schema_extra = {
            "example": {
                "nombre": "Juan",
                "apellido": "Pérez",
                "dni": "12345678",
                "email": "juan.perez@example.com",
                "cohorte": 2024
            }
        }


class AlumnoUpdateSchema(BaseModel):
    """
    Schema para actualizar un alumno (PUT/PATCH /alumnos/{id}).
    
    Decisión de diseño: Todos los campos opcionales
    - Permite actualización parcial (PATCH)
    - Solo se actualizan los campos proporcionados
    """
    
    nombre: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Nuevo nombre del alumno"
    )
    
    apellido: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Nuevo apellido del alumno"
    )
    
    dni: Optional[str] = Field(
        None,
        min_length=7,
        max_length=20,
        description="Nuevo DNI del alumno"
    )
    
    email: Optional[EmailStr] = Field(
        None,
        description="Nuevo email del alumno"
    )
    
    cohorte: Optional[int] = Field(
        None,
        ge=2000,
        le=2100,
        description="Nueva cohorte del alumno"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "nuevo.email@example.com",
                "cohorte": 2025
            }
        }


class AlumnoResponseSchema(BaseModel):
    """
    Schema para respuestas de alumno (GET /alumnos, GET /alumnos/{id}).
    
    Incluye todos los datos del alumno, incluyendo ID y fecha de creación.
    """
    
    id: int = Field(..., description="ID único del alumno")
    nombre: str = Field(..., description="Nombre del alumno")
    apellido: str = Field(..., description="Apellido del alumno")
    dni: str = Field(..., description="DNI del alumno")
    email: str = Field(..., description="Email del alumno")
    cohorte: int = Field(..., description="Año de ingreso")
    nombre_completo: str = Field(..., description="Nombre completo (Apellido, Nombre)")
    fecha_creacion: Optional[str] = Field(None, description="Fecha de creación del registro")
    
    @classmethod
    def from_entity(cls, alumno) -> 'AlumnoResponseSchema':
        """
        Crea un schema desde una entidad Alumno.
        
        Decisión de diseño: Método de conversión
        - Centraliza la lógica de conversión Entidad → Schema
        - Facilita cambios en el mapeo
        
        Args:
            alumno: Entidad Alumno de dominio
        
        Returns:
            AlumnoResponseSchema: Schema para respuesta de API
        """
        return cls(
            id=alumno.id,
            nombre=alumno.nombre,
            apellido=alumno.apellido,
            dni=alumno.dni,
            email=alumno.email,
            cohorte=alumno.cohorte,
            nombre_completo=alumno.nombre_completo(),
            fecha_creacion=alumno.fecha_creacion.isoformat() if alumno.fecha_creacion else None
        )
    
    class Config:
        """Configuración del schema"""
        from_attributes = True  # Permite crear desde objetos con atributos (no solo dicts)
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Juan",
                "apellido": "Pérez",
                "dni": "12345678",
                "email": "juan.perez@example.com",
                "cohorte": 2024,
                "nombre_completo": "Pérez, Juan",
                "fecha_creacion": "2025-12-07T12:00:00"
            }
        }


class AlumnoListResponseSchema(BaseModel):
    """
    Schema para respuesta de listado de alumnos (GET /alumnos).
    
    Incluye metadatos de paginación.
    """
    
    total: int = Field(..., description="Total de alumnos (sin paginación)")
    limite: Optional[int] = Field(None, description="Límite de resultados por página")
    offset: int = Field(0, description="Número de resultados saltados")
    alumnos: list[AlumnoResponseSchema] = Field(..., description="Lista de alumnos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 50,
                "limite": 10,
                "offset": 0,
                "alumnos": [
                    {
                        "id": 1,
                        "nombre": "Juan",
                        "apellido": "Pérez",
                        "dni": "12345678",
                        "email": "juan.perez@example.com",
                        "cohorte": 2024,
                        "nombre_completo": "Pérez, Juan",
                        "fecha_creacion": "2025-12-07T12:00:00"
                    }
                ]
            }
        }
