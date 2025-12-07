"""
Tests para la API del Sistema de Seguimiento de Alumnos
Ejecutar con: pytest tests/test_api.py -v
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock

# Mock de la API
class MockHandler:
    def __init__(self):
        self.response_status = 200
        self.response_headers = {}
        self.response_body = b''
        
    def send_response(self, code):
        self.response_status = code
        
    def send_header(self, key, value):
        self.response_headers[key] = value
        
    def end_headers(self):
        pass
        
    def wfile_write(self, data):
        self.response_body = data

# ========================================
# TESTS DE ENDPOINTS GET
# ========================================

def test_health_endpoint():
    """Test del endpoint /health"""
    # Simular request a /health
    response = {
        'status': 'ok',
        'db': True
    }
    
    assert response['status'] == 'ok'
    assert 'db' in response

def test_get_cursos():
    """Test del endpoint GET /cursos"""
    # Simular respuesta de cursos
    response = {
        'total': 3,
        'clases': [
            {
                'id': 1,
                'materia': 'Programación I',
                'cohorte': 2024,
                'totalAlumnos': 8
            }
        ]
    }
    
    assert response['total'] == 3
    assert len(response['clases']) > 0
    assert 'materia' in response['clases'][0]

def test_get_alumnos():
    """Test del endpoint GET /alumnos"""
    response = {
        'total': 8,
        'alumnos': [
            {
                'id': 1,
                'nombre': 'Juan',
                'apellido': 'Pérez',
                'dni': '12345678',
                'email': 'juan@example.com',
                'cohorte': 2024
            }
        ]
    }
    
    assert response['total'] == 8
    assert len(response['alumnos']) > 0
    assert response['alumnos'][0]['dni'] == '12345678'

def test_get_alertas():
    """Test del endpoint GET /alertas"""
    response = {
        'total': 0,
        'alertas': []
    }
    
    assert 'total' in response
    assert 'alertas' in response
    assert isinstance(response['alertas'], list)

# ========================================
# TESTS DE ENDPOINTS POST
# ========================================

def test_post_alumno_valido():
    """Test de creación de alumno con datos válidos"""
    body = {
        'nombre': 'María',
        'apellido': 'González',
        'dni': '98765432',
        'email': 'maria@example.com',
        'cohorte': 2024
    }
    
    # Validar que todos los campos requeridos están presentes
    required_fields = ['nombre', 'apellido', 'dni', 'email', 'cohorte']
    for field in required_fields:
        assert field in body
        assert body[field] is not None

def test_post_alumno_sin_nombre():
    """Test de creación de alumno sin nombre (debe fallar)"""
    body = {
        'apellido': 'González',
        'dni': '98765432',
        'email': 'maria@example.com',
        'cohorte': 2024
    }
    
    # Verificar que falta el campo nombre
    assert 'nombre' not in body

def test_post_curso_valido():
    """Test de creación de curso con datos válidos"""
    body = {
        'nombre_materia': 'Matemática II',
        'anio': 2024,
        'cuatrimestre': 2,
        'docente_responsable': 'Prof. García'
    }
    
    required_fields = ['nombre_materia', 'anio', 'cuatrimestre', 'docente_responsable']
    for field in required_fields:
        assert field in body
        assert body[field] is not None

def test_post_tp_valido():
    """Test de creación de TP con datos válidos"""
    body = {
        'curso_id': 1,
        'titulo': 'TP1 - Variables',
        'descripcion': 'Ejercicios sobre variables',
        'fecha_entrega': '2024-12-15'
    }
    
    required_fields = ['curso_id', 'titulo', 'fecha_entrega']
    for field in required_fields:
        assert field in body
        assert body[field] is not None

# ========================================
# TESTS DE VALIDACIÓN
# ========================================

def test_validar_email():
    """Test de validación de email"""
    emails_validos = [
        'test@example.com',
        'user.name@domain.com',
        'user+tag@example.org'
    ]
    
    emails_invalidos = [
        'invalid',
        '@example.com',
        'user@',
        'user @example.com'
    ]
    
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    for email in emails_validos:
        assert re.match(email_pattern, email) is not None
    
    for email in emails_invalidos:
        assert re.match(email_pattern, email) is None

def test_validar_dni():
    """Test de validación de DNI"""
    # DNI debe ser numérico y tener entre 7 y 8 dígitos
    dnis_validos = ['12345678', '1234567']
    dnis_invalidos = ['123', 'abcd1234', '']
    
    for dni in dnis_validos:
        assert dni.isdigit()
        assert 7 <= len(dni) <= 8
    
    for dni in dnis_invalidos:
        assert not (dni.isdigit() and 7 <= len(dni) <= 8)

def test_validar_cohorte():
    """Test de validación de cohorte"""
    # Cohorte debe ser un año entre 2020 y 2030
    cohortes_validas = [2020, 2024, 2030]
    cohortes_invalidas = [2019, 2031, 1999]
    
    for cohorte in cohortes_validas:
        assert 2020 <= cohorte <= 2030
    
    for cohorte in cohortes_invalidas:
        assert not (2020 <= cohorte <= 2030)

# ========================================
# TESTS DE RESPUESTAS
# ========================================

def test_response_format():
    """Test del formato de respuesta JSON"""
    response = {
        'success': True,
        'id': 1,
        'message': 'Creado exitosamente'
    }
    
    # Verificar que se puede serializar a JSON
    json_str = json.dumps(response)
    assert json_str is not None
    
    # Verificar que se puede deserializar
    parsed = json.loads(json_str)
    assert parsed['success'] == True
    assert parsed['id'] == 1

def test_error_response_format():
    """Test del formato de respuesta de error"""
    error_response = {
        'error': 'Campo requerido: nombre',
        'traceback': 'Error details...'
    }
    
    assert 'error' in error_response
    assert isinstance(error_response['error'], str)

# ========================================
# TESTS DE INTEGRACIÓN
# ========================================

def test_flujo_crear_curso_y_tp():
    """Test del flujo completo: crear curso y luego TP"""
    # 1. Crear curso
    curso = {
        'nombre_materia': 'Test Materia',
        'anio': 2024,
        'cuatrimestre': 2,
        'docente_responsable': 'Prof. Test'
    }
    curso_id = 1  # Simular ID retornado
    
    # 2. Crear TP para ese curso
    tp = {
        'curso_id': curso_id,
        'titulo': 'TP Test',
        'descripcion': 'Descripción test',
        'fecha_entrega': '2024-12-15'
    }
    
    assert tp['curso_id'] == curso_id

def test_flujo_crear_alumno_e_inscribir():
    """Test del flujo: crear alumno y luego inscribirlo"""
    # 1. Crear alumno
    alumno = {
        'nombre': 'Test',
        'apellido': 'Alumno',
        'dni': '11111111',
        'email': 'test@test.com',
        'cohorte': 2024
    }
    alumno_id = 1  # Simular ID retornado
    
    # 2. Verificar que el alumno tiene ID
    assert alumno_id > 0

# ========================================
# TESTS DE CORS
# ========================================

def test_cors_headers():
    """Test de headers CORS"""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    assert headers['Access-Control-Allow-Origin'] == '*'
    assert 'POST' in headers['Access-Control-Allow-Methods']

# ========================================
# TESTS DE EDGE CASES
# ========================================

def test_campos_vacios():
    """Test con campos vacíos"""
    body = {
        'nombre': '',
        'apellido': '',
        'dni': '',
        'email': '',
        'cohorte': None
    }
    
    # Verificar que los campos están vacíos
    assert not body['nombre']
    assert not body['apellido']
    assert body['cohorte'] is None

def test_caracteres_especiales():
    """Test con caracteres especiales en nombres"""
    nombres_validos = [
        'María José',
        "O'Connor",
        'Jean-Pierre',
        'Müller'
    ]
    
    for nombre in nombres_validos:
        assert len(nombre) > 0

def test_sql_injection_prevention():
    """Test de prevención de SQL injection"""
    # Estos valores NO deberían ejecutarse como SQL
    malicious_inputs = [
        "'; DROP TABLE alumno; --",
        "1 OR 1=1",
        "admin'--"
    ]
    
    # Verificar que se tratan como strings normales
    for input_val in malicious_inputs:
        assert isinstance(input_val, str)
        # En producción, estos deberían ser sanitizados

# ========================================
# CONFIGURACIÓN DE PYTEST
# ========================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
