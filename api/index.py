"""
API REST Simple para Vercel
"""

from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Headers CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        path = self.path
        
        try:
            if '/health' in path:
                response = {'status': 'ok', 'message': 'Working!'}
                
            elif '/cursos' in path or '/clases' in path:
                response = {
                    'total': 3,
                    'clases': [
                        {
                            'id': 1,
                            'materia': 'Programación I',
                            'cohorte': 2024,
                            'totalAlumnos': 8,
                            'asistenciaPromedio': 0,
                            'alumnosEnRiesgo': 0,
                            'totalClases': 0,
                            'ultimaClase': None
                        },
                        {
                            'id': 2,
                            'materia': 'Matemática',
                            'cohorte': 2024,
                            'totalAlumnos': 8,
                            'asistenciaPromedio': 0,
                            'alumnosEnRiesgo': 0,
                            'totalClases': 0,
                            'ultimaClase': None
                        },
                        {
                            'id': 3,
                            'materia': 'Física',
                            'cohorte': 2023,
                            'totalAlumnos': 0,
                            'asistenciaPromedio': 0,
                            'alumnosEnRiesgo': 0,
                            'totalClases': 0,
                            'ultimaClase': None
                        }
                    ]
                }
                
            elif '/alumnos' in path:
                response = {
                    'total': 8,
                    'alumnos': [
                        {'id': 1, 'nombre': 'Juan', 'apellido': 'Pérez', 'nombre_completo': 'Pérez, Juan', 'dni': '12345678', 'email': 'juan@example.com', 'cohorte': 2024},
                        {'id': 2, 'nombre': 'Ana', 'apellido': 'García', 'nombre_completo': 'García, Ana', 'dni': '23456789', 'email': 'ana@example.com', 'cohorte': 2024},
                        {'id': 3, 'nombre': 'Carlos', 'apellido': 'López', 'nombre_completo': 'López, Carlos', 'dni': '34567890', 'email': 'carlos@example.com', 'cohorte': 2024},
                        {'id': 4, 'nombre': 'María', 'apellido': 'Rodríguez', 'nombre_completo': 'Rodríguez, María', 'dni': '45678901', 'email': 'maria@example.com', 'cohorte': 2024},
                        {'id': 5, 'nombre': 'Pedro', 'apellido': 'Fernández', 'nombre_completo': 'Fernández, Pedro', 'dni': '56789012', 'email': 'pedro@example.com', 'cohorte': 2024},
                        {'id': 6, 'nombre': 'Laura', 'apellido': 'González', 'nombre_completo': 'González, Laura', 'dni': '67890123', 'email': 'laura@example.com', 'cohorte': 2024},
                        {'id': 7, 'nombre': 'Diego', 'apellido': 'Sánchez', 'nombre_completo': 'Sánchez, Diego', 'dni': '78901234', 'email': 'diego@example.com', 'cohorte': 2024},
                        {'id': 8, 'nombre': 'Sofía', 'apellido': 'Pérez', 'nombre_completo': 'Pérez, Sofía', 'dni': '89012345', 'email': 'sofia@example.com', 'cohorte': 2024}
                    ]
                }
                
            elif '/alertas' in path:
                response = {
                    'total': 0,
                    'alertas': []
                }
                
            else:
                response = {'error': 'Not found', 'path': path}
            
            self.wfile.write(json.dumps(response, ensure_ascii=False, default=str).encode('utf-8'))
            
        except Exception as e:
            import traceback
            error = {
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            self.wfile.write(json.dumps(error).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
