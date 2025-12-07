"""
API REST con PostgreSQL - CRUD Completo
Sistema de Seguimiento de Alumnos
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs, urlparse

# Importar funciones de BD
try:
    from api.db import execute_query, execute_insert, execute_update
    DB_AVAILABLE = True
except:
    DB_AVAILABLE = False

class handler(BaseHTTPRequestHandler):
    
    def _send_response(self, data, status_code=200):
        """Envía respuesta JSON con CORS"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
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
    
    def _get_id_from_path(self):
        """Extrae el ID de la ruta (ej: /alumnos/5 → 5)"""
        parts = self.path.strip('/').split('/')
        if len(parts) >= 2 and parts[-1].isdigit():
            return int(parts[-1])
        return None
    
    def _get_query_params(self):
        """Extrae parámetros de query string"""
        parsed = urlparse(self.path)
        return parse_qs(parsed.query)
    
    def do_OPTIONS(self):
        """Maneja preflight CORS"""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Maneja requests GET"""
        path = self.path.split('?')[0]  # Remover query params
        
        try:
            if '/health' in path:
                self._send_response({'status': 'ok', 'db': DB_AVAILABLE})
                
            elif '/cursos' in path or '/clases' in path and '/clases/' not in path:
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
                    self._send_response({'total': 0, 'clases': []})
                
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
            
            elif '/trabajos-practicos' in path or '/tps' in path:
                if DB_AVAILABLE:
                    params = self._get_query_params()
                    curso_id = params.get('curso_id', [None])[0]
                    
                    if curso_id:
                        tps = execute_query("""
                            SELECT id, curso_id, titulo, descripcion, fecha_entrega
                            FROM trabajo_practico
                            WHERE curso_id = %s
                            ORDER BY fecha_entrega
                        """, (curso_id,))
                    else:
                        tps = execute_query("""
                            SELECT id, curso_id, titulo, descripcion, fecha_entrega
                            FROM trabajo_practico
                            ORDER BY fecha_entrega
                        """)
                    
                    self._send_response({'total': len(tps), 'tps': tps})
                else:
                    self._send_response({'total': 0, 'tps': []})
                
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
        """Maneja requests POST (CREATE)"""
        path = self.path
        
        try:
            body = self._get_body()
            
            if '/alumnos' in path:
                if not DB_AVAILABLE:
                    self._send_response({'error': 'Database not available'}, 500)
                    return
                
                required = ['nombre', 'apellido', 'dni', 'email', 'cohorte']
                for field in required:
                    if field not in body or not body[field]:
                        self._send_response({'error': f'Campo requerido: {field}'}, 400)
                        return
                
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
                if not DB_AVAILABLE:
                    self._send_response({'error': 'Database not available'}, 500)
                    return
                
                required = ['nombre_materia', 'anio', 'cuatrimestre', 'docente_responsable']
                for field in required:
                    if field not in body or not body[field]:
                        self._send_response({'error': f'Campo requerido: {field}'}, 400)
                        return
                
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
                if not DB_AVAILABLE:
                    self._send_response({'error': 'Database not available'}, 500)
                    return
                
                required = ['curso_id', 'titulo', 'fecha_entrega']
                for field in required:
                    if field not in body or not body[field]:
                        self._send_response({'error': f'Campo requerido: {field}'}, 400)
                        return
                
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
    
    def do_PUT(self):
        """Maneja requests PUT (UPDATE)"""
        path = self.path
        entity_id = self._get_id_from_path()
        
        try:
            body = self._get_body()
            
            if not DB_AVAILABLE:
                self._send_response({'error': 'Database not available'}, 500)
                return
            
            if not entity_id:
                self._send_response({'error': 'ID no proporcionado'}, 400)
                return
            
            if '/alumnos' in path:
                # Actualizar alumno
                fields = []
                values = []
                
                if 'nombre' in body:
                    fields.append('nombre = %s')
                    values.append(body['nombre'])
                if 'apellido' in body:
                    fields.append('apellido = %s')
                    values.append(body['apellido'])
                if 'dni' in body:
                    fields.append('dni = %s')
                    values.append(body['dni'])
                if 'email' in body:
                    fields.append('email = %s')
                    values.append(body['email'])
                if 'cohorte' in body:
                    fields.append('cohorte = %s')
                    values.append(body['cohorte'])
                
                if not fields:
                    self._send_response({'error': 'No hay campos para actualizar'}, 400)
                    return
                
                values.append(entity_id)
                query = f"UPDATE alumno SET {', '.join(fields)} WHERE id = %s"
                
                rows = execute_update(query, tuple(values))
                
                self._send_response({
                    'success': True,
                    'rows_affected': rows,
                    'message': 'Alumno actualizado exitosamente'
                })
                
            elif '/cursos' in path:
                # Actualizar curso
                fields = []
                values = []
                
                if 'nombre_materia' in body:
                    fields.append('nombre_materia = %s')
                    values.append(body['nombre_materia'])
                if 'anio' in body:
                    fields.append('anio = %s')
                    values.append(body['anio'])
                if 'cuatrimestre' in body:
                    fields.append('cuatrimestre = %s')
                    values.append(body['cuatrimestre'])
                if 'docente_responsable' in body:
                    fields.append('docente_responsable = %s')
                    values.append(body['docente_responsable'])
                
                if not fields:
                    self._send_response({'error': 'No hay campos para actualizar'}, 400)
                    return
                
                values.append(entity_id)
                query = f"UPDATE curso SET {', '.join(fields)} WHERE id = %s"
                
                rows = execute_update(query, tuple(values))
                
                self._send_response({
                    'success': True,
                    'rows_affected': rows,
                    'message': 'Curso actualizado exitosamente'
                })
                
            elif '/trabajos-practicos' in path or '/tps' in path:
                # Actualizar TP
                fields = []
                values = []
                
                if 'titulo' in body:
                    fields.append('titulo = %s')
                    values.append(body['titulo'])
                if 'descripcion' in body:
                    fields.append('descripcion = %s')
                    values.append(body['descripcion'])
                if 'fecha_entrega' in body:
                    fields.append('fecha_entrega = %s')
                    values.append(body['fecha_entrega'])
                
                if not fields:
                    self._send_response({'error': 'No hay campos para actualizar'}, 400)
                    return
                
                values.append(entity_id)
                query = f"UPDATE trabajo_practico SET {', '.join(fields)} WHERE id = %s"
                
                rows = execute_update(query, tuple(values))
                
                self._send_response({
                    'success': True,
                    'rows_affected': rows,
                    'message': 'Trabajo Práctico actualizado exitosamente'
                })
                
            else:
                self._send_response({'error': 'Endpoint not found'}, 404)
                
        except Exception as e:
            import traceback
            self._send_response({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, 500)
    
    def do_DELETE(self):
        """Maneja requests DELETE"""
        path = self.path
        entity_id = self._get_id_from_path()
        
        try:
            if not DB_AVAILABLE:
                self._send_response({'error': 'Database not available'}, 500)
                return
            
            if not entity_id:
                self._send_response({'error': 'ID no proporcionado'}, 400)
                return
            
            if '/alumnos' in path:
                rows = execute_update("DELETE FROM alumno WHERE id = %s", (entity_id,))
                self._send_response({
                    'success': True,
                    'rows_affected': rows,
                    'message': 'Alumno eliminado exitosamente'
                })
                
            elif '/cursos' in path:
                rows = execute_update("DELETE FROM curso WHERE id = %s", (entity_id,))
                self._send_response({
                    'success': True,
                    'rows_affected': rows,
                    'message': 'Curso eliminado exitosamente'
                })
                
            elif '/trabajos-practicos' in path or '/tps' in path:
                rows = execute_update("DELETE FROM trabajo_practico WHERE id = %s", (entity_id,))
                self._send_response({
                    'success': True,
                    'rows_affected': rows,
                    'message': 'Trabajo Práctico eliminado exitosamente'
                })
                
            else:
                self._send_response({'error': 'Endpoint not found'}, 404)
                
        except Exception as e:
            import traceback
            self._send_response({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, 500)
