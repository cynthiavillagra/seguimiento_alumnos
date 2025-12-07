"""
API REST con Python Puro + POO
Sistema de Seguimiento de Alumnos

Sin frameworks, solo Python estándar con Programación Orientada a Objetos.
"""

import json
import os
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Agregar src al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class APIHandler(BaseHTTPRequestHandler):
    """
    Handler HTTP con POO para manejar requests REST.
    
    Decisión de diseño: Clase que hereda de BaseHTTPRequestHandler
    - Maneja requests HTTP de forma orientada a objetos
    - Métodos para cada verbo HTTP (GET, POST, PUT, DELETE)
    - Compatible con Vercel sin dependencias externas
    """
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Configura headers de respuesta"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _send_json(self, data, status_code=200):
        """Envía respuesta JSON"""
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _send_error_json(self, message, status_code=500):
        """Envía error en formato JSON"""
        self._send_json({
            'error': message,
            'status': status_code
        }, status_code)
    
    def do_OPTIONS(self):
        """Maneja preflight requests de CORS"""
        self._set_headers(204)
    
    def do_GET(self):
        """
        Maneja requests GET.
        
        Rutas implementadas:
        - / : Info de la API
        - /health : Health check
        - /ping : Ping simple
        - /clases : Listar clases del profesor
        - /alumnos : Listar alumnos
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/' or path == '':
                self._handle_root()
            elif path == '/health':
                self._handle_health()
            elif path == '/ping':
                self._handle_ping()
            elif path == '/docs':
                self._handle_docs()
            elif path == '/clases':
                self._handle_get_clases()
            elif path == '/alumnos':
                self._handle_get_alumnos()
            else:
                self._send_error_json('Ruta no encontrada', 404)
        
        except Exception as e:
            self._send_error_json(str(e), 500)
    
    def do_POST(self):
        """
        Maneja requests POST.
        
        Rutas implementadas:
        - /alumnos : Crear alumno (futuro)
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            # Leer body del request
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
            data = json.loads(body) if body else {}
            
            if path == '/alumnos':
                self._handle_create_alumno(data)
            else:
                self._send_error_json('Ruta no encontrada', 404)
        
        except json.JSONDecodeError:
            self._send_error_json('JSON inválido', 400)
        except Exception as e:
            self._send_error_json(str(e), 500)
    
    # ========================================================================
    # Handlers de Rutas
    # ========================================================================
    
    def _handle_root(self):
        """Endpoint raíz - Info de la API"""
        self._send_json({
            'message': '🎓 API de Seguimiento de Alumnos',
            'version': '1.0.0',
            'status': 'running',
            'tecnologia': 'Python Puro + POO',
            'framework': 'Ninguno (Python estándar)',
            'endpoints': {
                'GET /': 'Info de la API',
                'GET /health': 'Health check',
                'GET /ping': 'Ping',
                'GET /docs': 'Documentación',
                'GET /alumnos': 'Listar alumnos',
                'POST /alumnos': 'Crear alumno'
            }
        })
    
    def _handle_health(self):
        """Health check"""
        self._send_json({
            'status': 'healthy',
            'api': 'running',
            'database': 'sqlite (efímero en Vercel)',
            'version': '1.0.0'
        })
    
    def _handle_ping(self):
        """Ping simple"""
        self._send_json({'ping': 'pong'})
    
    def _handle_docs(self):
        """Documentación de la API"""
        self._send_json({
            'title': 'API de Seguimiento de Alumnos',
            'description': 'API REST construida con Python puro y POO',
            'version': '1.0.0',
            'endpoints': [
                {
                    'method': 'GET',
                    'path': '/',
                    'description': 'Información general de la API'
                },
                {
                    'method': 'GET',
                    'path': '/health',
                    'description': 'Verifica el estado de la API'
                },
                {
                    'method': 'GET',
                    'path': '/ping',
                    'description': 'Ping simple para verificar conectividad'
                },
                {
                    'method': 'GET',
                    'path': '/alumnos',
                    'description': 'Lista todos los alumnos'
                },
                {
                    'method': 'POST',
                    'path': '/alumnos',
                    'description': 'Crea un nuevo alumno',
                    'body': {
                        'nombre': 'string',
                        'apellido': 'string',
                        'dni': 'string',
                        'email': 'string',
                        'cohorte': 'integer'
                    }
                }
            ]
        })
    
    def _handle_get_clases(self):
        """Lista clases del profesor (por ahora, datos de ejemplo)"""
        # TODO: Conectar con la base de datos
        clases_ejemplo = [
            {
                'id': 1,
                'materia': 'Programación I',
                'cohorte': 2024,
                'totalAlumnos': 30,
                'asistenciaPromedio': 85,
                'alumnosEnRiesgo': 3,
                'totalClases': 12,
                'ultimaClase': '2024-12-05'
            },
            {
                'id': 2,
                'materia': 'Matemática',
                'cohorte': 2024,
                'totalAlumnos': 28,
                'asistenciaPromedio': 90,
                'alumnosEnRiesgo': 1,
                'totalClases': 10,
                'ultimaClase': '2024-12-06'
            },
            {
                'id': 3,
                'materia': 'Física',
                'cohorte': 2023,
                'totalAlumnos': 25,
                'asistenciaPromedio': 78,
                'alumnosEnRiesgo': 5,
                'totalClases': 15,
                'ultimaClase': '2024-12-04'
            }
        ]
        
        self._send_json({
            'total': len(clases_ejemplo),
            'clases': clases_ejemplo
        })
    
    def _handle_get_alumnos(self):
        """Lista alumnos (por ahora, datos de ejemplo)"""
        # TODO: Conectar con la base de datos
        alumnos_ejemplo = [
            {
                'id': 1,
                'nombre': 'Juan',
                'apellido': 'Pérez',
                'dni': '12345678',
                'email': 'juan.perez@example.com',
                'cohorte': 2024,
                'nombre_completo': 'Pérez, Juan'
            },
            {
                'id': 2,
                'nombre': 'Ana',
                'apellido': 'García',
                'dni': '23456789',
                'email': 'ana.garcia@example.com',
                'cohorte': 2024,
                'nombre_completo': 'García, Ana'
            }
        ]
        
        self._send_json({
            'total': len(alumnos_ejemplo),
            'alumnos': alumnos_ejemplo
        })
    
    def _handle_create_alumno(self, data):
        """Crea un alumno (por ahora, solo valida y retorna)"""
        # Validar datos requeridos
        required_fields = ['nombre', 'apellido', 'dni', 'email', 'cohorte']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            self._send_error_json(
                f'Campos requeridos faltantes: {", ".join(missing_fields)}',
                400
            )
            return
        
        # TODO: Guardar en base de datos
        # Por ahora, solo retornamos el alumno creado
        alumno_creado = {
            'id': 999,  # ID temporal
            'nombre': data['nombre'],
            'apellido': data['apellido'],
            'dni': data['dni'],
            'email': data['email'],
            'cohorte': data['cohorte'],
            'nombre_completo': f"{data['apellido']}, {data['nombre']}",
            'mensaje': 'Alumno creado exitosamente (datos de ejemplo)'
        }
        
        self._send_json(alumno_creado, 201)


# Para Vercel, necesitamos exportar el handler
handler = APIHandler
