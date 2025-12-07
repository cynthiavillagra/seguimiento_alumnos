"""
API REST con PostgreSQL
Sistema de Seguimiento de Alumnos
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs

# Importar funciones de BD
try:
    from api.db import execute_query, execute_insert
    DB_AVAILABLE = True
except:
    DB_AVAILABLE = False

class handler(BaseHTTPRequestHandler):
    
    def _send_response(self, data, status_code=200):
        """Envía respuesta JSON con CORS"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode('utf-8'))
    
    def _get_body(self):
        """Lee el body del request"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        return {}
    
    def do_OPTIONS(self):
        """Maneja preflight CORS"""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Maneja requests GET"""
        path = self.path
        
        try:
            if '/health' in path:
                self._send_response({'status': 'ok', 'db': DB_AVAILABLE})
                
            elif '/cursos' in path or '/clases' in path:
                if DB_AVAILABLE:
                    cursos = execute_query("""
                        SELECT 
                            c.id,
                            c.nombre_materia as materia,
                            c.anio as cohorte,
                            c.cuatrimestre,
                            c.docente_responsable as docente,
                            COUNT(DISTINCT i.alumno_id) as "totalAlumnos"
                        FROM curso c
                        LEFT JOIN inscripcion i ON c.id = i.curso_id
                        GROUP BY c.id, c.nombre_materia, c.anio, c.cuatrimestre, c.docente_responsable
                        ORDER BY c.anio DESC, c.cuatrimestre DESC
                    """)
                    self._send_response({'total': len(cursos), 'clases': cursos})
                else:
                    # Datos de ejemplo si no hay BD
                    self._send_response({
                        'total': 3,
                        'clases': [
                            {'id': 1, 'materia': 'Programación I', 'cohorte': 2024, 'totalAlumnos': 8},
                            {'id': 2, 'materia': 'Matemática', 'cohorte': 2024, 'totalAlumnos': 8},
                            {'id': 3, 'materia': 'Física', 'cohorte': 2023, 'totalAlumnos': 0}
                        ]
                    })
                
            elif '/alumnos' in path:
                if DB_AVAILABLE:
                    alumnos = execute_query("""
                        SELECT 
                            id,
                            nombre,
                            apellido,
                            apellido || ', ' || nombre as nombre_completo,
                            dni,
                            email,
                            cohorte
                        FROM alumno
                        ORDER BY apellido, nombre
                    """)
                    self._send_response({'total': len(alumnos), 'alumnos': alumnos})
                else:
                    self._send_response({'total': 0, 'alumnos': []})
                
            elif '/alertas' in path:
                self._send_response({'total': 0, 'alertas': []})
                
            else:
                self._send_response({'error': 'Not found'}, 404)
                
        except Exception as e:
            import traceback
            self._send_response({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, 500)
    
    def do_POST(self):
        """Maneja requests POST"""
        path = self.path
        
        try:
            body = self._get_body()
            
            if '/alumnos' in path:
                # Crear alumno
                if not DB_AVAILABLE:
                    self._send_response({'error': 'Database not available'}, 500)
                    return
                
                # Validar datos requeridos
                required = ['nombre', 'apellido', 'dni', 'email', 'cohorte']
                for field in required:
                    if field not in body or not body[field]:
                        self._send_response({'error': f'Campo requerido: {field}'}, 400)
                        return
                
                # Insertar alumno
                alumno_id = execute_insert("""
                    INSERT INTO alumno (nombre, apellido, dni, email, cohorte)
                    VALUES (%s, %s, %s, %s, %s)
                """, (body['nombre'], body['apellido'], body['dni'], body['email'], body['cohorte']))
                
                self._send_response({
                    'success': True,
                    'id': alumno_id,
                    'message': 'Alumno creado exitosamente'
                }, 201)
                
            elif '/cursos' in path or '/clases' in path:
                # Crear curso
                if not DB_AVAILABLE:
                    self._send_response({'error': 'Database not available'}, 500)
                    return
                
                # Validar datos requeridos
                required = ['nombre_materia', 'anio', 'cuatrimestre', 'docente_responsable']
                for field in required:
                    if field not in body or not body[field]:
                        self._send_response({'error': f'Campo requerido: {field}'}, 400)
                        return
                
                # Insertar curso
                curso_id = execute_insert("""
                    INSERT INTO curso (nombre_materia, anio, cuatrimestre, docente_responsable)
                    VALUES (%s, %s, %s, %s)
                """, (body['nombre_materia'], body['anio'], body['cuatrimestre'], body['docente_responsable']))
                
                self._send_response({
                    'success': True,
                    'id': curso_id,
                    'message': 'Curso creado exitosamente'
                }, 201)
                
            elif '/trabajos-practicos' in path or '/tps' in path:
                # Crear TP
                if not DB_AVAILABLE:
                    self._send_response({'error': 'Database not available'}, 500)
                    return
                
                # Validar datos requeridos
                required = ['curso_id', 'titulo', 'fecha_entrega']
                for field in required:
                    if field not in body or not body[field]:
                        self._send_response({'error': f'Campo requerido: {field}'}, 400)
                        return
                
                # Insertar TP
                tp_id = execute_insert("""
                    INSERT INTO trabajo_practico (curso_id, titulo, descripcion, fecha_entrega)
                    VALUES (%s, %s, %s, %s)
                """, (body['curso_id'], body['titulo'], body.get('descripcion', ''), body['fecha_entrega']))
                
                self._send_response({
                    'success': True,
                    'id': tp_id,
                    'message': 'Trabajo Práctico creado exitosamente'
                }, 201)
                
            else:
                self._send_response({'error': 'Endpoint not found'}, 404)
                
        except Exception as e:
            import traceback
            self._send_response({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, 500)
