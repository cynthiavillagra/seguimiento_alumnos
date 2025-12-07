"""
Value Object: IndicadorRiesgo
Sistema de Seguimiento de Alumnos

Decisión de diseño: Value Object vs Entidad
- IndicadorRiesgo es un Value Object porque:
  1. Se CALCULA a partir de otros datos (asistencias, participaciones, TPs)
  2. No tiene identidad propia (se identifica por alumno_id + curso_id)
  3. Es inmutable una vez calculado
  4. Puede recrearse en cualquier momento con los mismos datos
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.domain.value_objects.enums import NivelRiesgo, NivelParticipacion


@dataclass(frozen=True)
class IndicadorRiesgo:
    """
    Value Object: IndicadorRiesgo
    
    Representa los indicadores de riesgo de deserción de un alumno en un curso.
    
    Responsabilidades:
    - Almacenar indicadores calculados (%, niveles)
    - Determinar el nivel de riesgo global
    - Generar alertas basadas en umbrales
    
    Reglas de Negocio (Umbrales):
    - Riesgo BAJO: Asistencia >= 80%, TPs >= 70%, Participación >= Media
    - Riesgo MEDIO: Asistencia 70-79%, TPs 50-69%, Participación Baja
    - Riesgo ALTO: Asistencia < 70%, TPs < 50%, Participación Ninguna sostenida
    
    Decisión de diseño: frozen=True
    - Los indicadores son inmutables una vez calculados
    - Para actualizar, se crea una nueva instancia
    - Esto garantiza consistencia de datos
    """
    
    alumno_id: int
    curso_id: int
    porcentaje_asistencia: float
    nivel_participacion_promedio: NivelParticipacion
    porcentaje_tps_entregados: float
    total_clases: int
    total_participaciones: int
    total_tps: int
    fecha_calculo: datetime
    
    # Umbrales de riesgo (constantes de clase)
    UMBRAL_ASISTENCIA_BAJO = 80.0
    UMBRAL_ASISTENCIA_MEDIO = 70.0
    UMBRAL_TPS_BAJO = 70.0
    UMBRAL_TPS_MEDIO = 50.0
    
    @property
    def nivel_riesgo(self) -> NivelRiesgo:
        """
        Calcula el nivel de riesgo global basado en los indicadores.
        
        Decisión de diseño: Property en lugar de atributo
        - Se calcula dinámicamente cada vez que se accede
        - Garantiza que siempre esté sincronizado con los indicadores
        - No se almacena, se deriva de otros datos
        
        Lógica:
        - Si 2 o más indicadores están en rojo → ALTO
        - Si 1 indicador está en rojo o 2 en amarillo → MEDIO
        - En otro caso → BAJO
        """
        indicadores_en_rojo = 0
        indicadores_en_amarillo = 0
        
        # Evaluar asistencia
        if self.porcentaje_asistencia < self.UMBRAL_ASISTENCIA_MEDIO:
            indicadores_en_rojo += 1
        elif self.porcentaje_asistencia < self.UMBRAL_ASISTENCIA_BAJO:
            indicadores_en_amarillo += 1
        
        # Evaluar TPs
        if self.porcentaje_tps_entregados < self.UMBRAL_TPS_MEDIO:
            indicadores_en_rojo += 1
        elif self.porcentaje_tps_entregados < self.UMBRAL_TPS_BAJO:
            indicadores_en_amarillo += 1
        
        # Evaluar participación
        if self.nivel_participacion_promedio == NivelParticipacion.NINGUNA:
            indicadores_en_rojo += 1
        elif self.nivel_participacion_promedio == NivelParticipacion.BAJA:
            indicadores_en_amarillo += 1
        
        # Determinar nivel de riesgo
        if indicadores_en_rojo >= 2:
            return NivelRiesgo.ALTO
        elif indicadores_en_rojo >= 1 or indicadores_en_amarillo >= 2:
            return NivelRiesgo.MEDIO
        else:
            return NivelRiesgo.BAJO
    
    @property
    def alertas_activas(self) -> list[str]:
        """
        Genera lista de alertas basadas en los indicadores.
        
        Returns:
            list[str]: Lista de mensajes de alerta
        """
        alertas = []
        
        if self.porcentaje_asistencia < self.UMBRAL_ASISTENCIA_MEDIO:
            alertas.append(f"⚠️ Asistencia crítica: {self.porcentaje_asistencia:.1f}% (< 70%)")
        elif self.porcentaje_asistencia < self.UMBRAL_ASISTENCIA_BAJO:
            alertas.append(f"⚡ Asistencia baja: {self.porcentaje_asistencia:.1f}% (< 80%)")
        
        if self.porcentaje_tps_entregados < self.UMBRAL_TPS_MEDIO:
            alertas.append(f"⚠️ Entregas críticas: {self.porcentaje_tps_entregados:.1f}% (< 50%)")
        elif self.porcentaje_tps_entregados < self.UMBRAL_TPS_BAJO:
            alertas.append(f"⚡ Entregas bajas: {self.porcentaje_tps_entregados:.1f}% (< 70%)")
        
        if self.nivel_participacion_promedio == NivelParticipacion.NINGUNA:
            alertas.append("⚠️ Sin participación registrada")
        elif self.nivel_participacion_promedio == NivelParticipacion.BAJA:
            alertas.append("⚡ Participación baja")
        
        # Alerta especial si no hay datos suficientes
        if self.total_clases < 3:
            alertas.append("ℹ️ Datos insuficientes (menos de 3 clases)")
        
        return alertas
    
    def tiene_datos_suficientes(self) -> bool:
        """
        Determina si hay datos suficientes para un cálculo confiable.
        
        Returns:
            bool: True si hay al menos 3 clases registradas
        """
        return self.total_clases >= 3
    
    def to_dict(self) -> dict:
        """Convierte el value object a diccionario"""
        return {
            'alumno_id': self.alumno_id,
            'curso_id': self.curso_id,
            'porcentaje_asistencia': round(self.porcentaje_asistencia, 2),
            'nivel_participacion_promedio': self.nivel_participacion_promedio.value,
            'porcentaje_tps_entregados': round(self.porcentaje_tps_entregados, 2),
            'nivel_riesgo': self.nivel_riesgo.value,
            'alertas_activas': self.alertas_activas,
            'total_clases': self.total_clases,
            'total_participaciones': self.total_participaciones,
            'total_tps': self.total_tps,
            'tiene_datos_suficientes': self.tiene_datos_suficientes(),
            'fecha_calculo': self.fecha_calculo.isoformat()
        }
    
    def __str__(self) -> str:
        return (f"IndicadorRiesgo(Alumno {self.alumno_id}, Curso {self.curso_id}, "
                f"Riesgo: {self.nivel_riesgo.value}, Asistencia: {self.porcentaje_asistencia:.1f}%)")
