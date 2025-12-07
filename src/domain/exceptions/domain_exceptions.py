"""
Excepciones de Dominio
Sistema de Seguimiento de Alumnos

Decisión de diseño: Excepciones personalizadas
- Permiten manejar errores de negocio de forma específica
- Facilitan el debugging (stack traces más claros)
- Permiten convertir a códigos HTTP apropiados en la API
- Separan errores de negocio de errores técnicos
"""


class DomainException(Exception):
    """
    Excepción base para todas las excepciones de dominio.
    
    Todas las excepciones de negocio heredan de esta clase.
    Esto permite capturarlas todas con un solo except si es necesario.
    """
    pass


# ============================================================================
# Excepciones de Validación
# ============================================================================

class ValidationException(DomainException):
    """Excepción base para errores de validación"""
    pass


class EmailInvalidoException(ValidationException):
    """El email no tiene un formato válido"""
    pass


class DNIInvalidoException(ValidationException):
    """El DNI no tiene un formato válido"""
    pass


class CuatrimestreInvalidoException(ValidationException):
    """El cuatrimestre debe ser 1 o 2"""
    pass


class EstadoAsistenciaInvalidoException(ValidationException):
    """El estado de asistencia no es válido"""
    pass


class NivelParticipacionInvalidoException(ValidationException):
    """El nivel de participación no es válido"""
    pass


# ============================================================================
# Excepciones de Reglas de Negocio
# ============================================================================

class BusinessRuleException(DomainException):
    """Excepción base para violaciones de reglas de negocio"""
    pass


class DNIDuplicadoException(BusinessRuleException):
    """Ya existe un alumno con ese DNI"""
    pass


class AlumnoYaInscriptoException(BusinessRuleException):
    """El alumno ya está inscripto en ese curso"""
    pass


class AlumnoNoInscriptoException(BusinessRuleException):
    """El alumno no está inscripto en el curso de la clase"""
    pass


class AsistenciaYaRegistradaException(BusinessRuleException):
    """Ya existe un registro de asistencia para ese alumno en esa clase"""
    pass


class EntregaYaRegistradaException(BusinessRuleException):
    """Ya existe un registro de entrega para ese alumno en ese TP"""
    pass


# ============================================================================
# Excepciones de No Encontrado
# ============================================================================

class NotFoundException(DomainException):
    """Excepción base para recursos no encontrados"""
    pass


class AlumnoNoEncontradoException(NotFoundException):
    """El alumno no existe en el sistema"""
    pass


class CursoNoEncontradoException(NotFoundException):
    """El curso no existe en el sistema"""
    pass


class ClaseNoEncontradaException(NotFoundException):
    """La clase no existe en el sistema"""
    pass


class TrabajoPracticoNoEncontradoException(NotFoundException):
    """El trabajo práctico no existe en el sistema"""
    pass


class InscripcionNoEncontradaException(NotFoundException):
    """La inscripción no existe en el sistema"""
    pass


# ============================================================================
# Excepciones de Datos Insuficientes
# ============================================================================

class DatosInsuficientesException(DomainException):
    """
    No hay datos suficientes para realizar la operación.
    
    Ejemplo: Calcular indicadores de riesgo con menos de 3 clases registradas.
    """
    pass
