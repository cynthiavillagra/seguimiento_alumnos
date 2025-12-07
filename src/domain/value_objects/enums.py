"""
Enumeraciones del Dominio
Sistema de Seguimiento de Alumnos

Decisión de diseño: Uso de Enums
- Los enums evitan "strings mágicos" en el código
- Facilitan la validación y el autocompletado en IDEs
- Hacen explícitos los valores permitidos
- Son type-safe (con type hints)
"""

from enum import Enum


class EstadoAsistencia(str, Enum):
    """
    Estados posibles de asistencia de un alumno a una clase.
    
    Decisión de diseño: Heredar de str y Enum
    - Permite usar los valores como strings en JSON/DB
    - Mantiene las ventajas de type checking de Enum
    - Compatible con Pydantic para validación en API
    """
    PRESENTE = "Presente"
    AUSENTE = "Ausente"
    TARDANZA = "Tardanza"
    JUSTIFICADA = "Justificada"
    
    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def valores_validos(cls) -> list[str]:
        """Retorna lista de valores válidos como strings"""
        return [estado.value for estado in cls]


class NivelParticipacion(str, Enum):
    """
    Niveles de participación de un alumno en una clase.
    
    Regla de negocio:
    - Ninguna: El alumno no participó en absoluto
    - Baja: Participación mínima o poco relevante
    - Media: Participación adecuada
    - Alta: Participación destacada, aportes significativos
    """
    NINGUNA = "Ninguna"
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    
    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def valores_validos(cls) -> list[str]:
        """Retorna lista de valores válidos como strings"""
        return [nivel.value for nivel in cls]
    
    def valor_numerico(self) -> int:
        """
        Convierte el nivel a un valor numérico para cálculos.
        
        Decisión de diseño: Escala 0-3
        - Facilita el cálculo de promedios
        - Permite comparaciones numéricas
        """
        mapping = {
            NivelParticipacion.NINGUNA: 0,
            NivelParticipacion.BAJA: 1,
            NivelParticipacion.MEDIA: 2,
            NivelParticipacion.ALTA: 3
        }
        return mapping[self]
    
    @classmethod
    def desde_valor_numerico(cls, valor: float) -> 'NivelParticipacion':
        """
        Convierte un valor numérico (0-3) a NivelParticipacion.
        Útil para calcular nivel promedio.
        """
        if valor < 0.5:
            return cls.NINGUNA
        elif valor < 1.5:
            return cls.BAJA
        elif valor < 2.5:
            return cls.MEDIA
        else:
            return cls.ALTA


class NivelRiesgo(str, Enum):
    """
    Niveles de riesgo de deserción de un alumno.
    
    Regla de negocio (umbrales):
    - Bajo: Asistencia >= 80%, TPs >= 70%, Participación >= Media
    - Medio: Asistencia 70-79%, TPs 50-69%, Participación Baja
    - Alto: Asistencia < 70%, TPs < 50%, Participación Ninguna sostenida
    
    Decisión de diseño:
    - El nivel de riesgo se calcula automáticamente en base a indicadores
    - No se almacena directamente, se calcula on-the-fly (en MVP)
    - En futuras versiones, se puede cachear en tabla indicador_riesgo
    """
    BAJO = "Bajo"
    MEDIO = "Medio"
    ALTO = "Alto"
    
    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def valores_validos(cls) -> list[str]:
        """Retorna lista de valores válidos como strings"""
        return [nivel.value for nivel in cls]
    
    def prioridad(self) -> int:
        """
        Retorna un valor numérico de prioridad para ordenamiento.
        Mayor número = mayor prioridad de atención.
        """
        mapping = {
            NivelRiesgo.BAJO: 1,
            NivelRiesgo.MEDIO: 2,
            NivelRiesgo.ALTO: 3
        }
        return mapping[self]
    
    def color_ui(self) -> str:
        """
        Retorna un código de color sugerido para UI.
        Útil para frontend.
        """
        mapping = {
            NivelRiesgo.BAJO: "#4CAF50",  # Verde
            NivelRiesgo.MEDIO: "#FF9800",  # Naranja
            NivelRiesgo.ALTO: "#F44336"    # Rojo
        }
        return mapping[self]
