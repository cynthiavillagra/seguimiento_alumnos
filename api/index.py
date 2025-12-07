"""
API REST con PostgreSQL
Sistema de Seguimiento de Alumnos
"""

import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from api.db import execute_query, execute_insert

class APIHandler(BaseHTTPRequestHandler):
    """Handler HTTP para manejar requests REST con PostgreSQL"""
    
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
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode('utf-8'))
    
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
        """Maneja requests GET"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/' or path == '':
                self._handle_root()
            elif path == '/health':
                self._handle_health()
            elif path == '/clases' or path == '/cursos':
                self._handle_get_cursos()
            elif path == '/alumnos':
                self._handle_get_alumnos()
            elif path == '/alertas':
                self._handle_get_alertas()
            elif path.startswith('/cursos/') and '/alumnos' in path:
                # /cursos/{id}/alumnos
                curso_id = path.split('/')[2]
                self._handle_get_alumnos_curso(curso_id)
            elif path.startswith('/cursos/') and '/tps' in path:
                # /cursos/{id}/tps
                curso_id = path.split('/')[2]
                self._handle_get_tps_curso(curso_id)
            else:
                self._send_error_json('Ruta no encontrada', 404)
        
        except Exception as e:
            self._send_error_json(str(e), 500)
    
    def do_POST(self):
        """Maneja requests POST"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            # Leer body del request
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
            data = json.loads(body) if body else {}
            
            if path == '/alumnos':
                self._handle_create_alumno(data)
            elif path == '/clase/registrar':
                self._handle_registrar_clase(data)
            else:
                self._send_error_json('Ruta no encontrada', 404)
        
        except Exception as e:
            self._send_error_json(str(e), 500)
    
    # ========================================================================
    # Handlers
    # ========================================================================
    
    def _handle_root(self):
        """Info de la API"""
        self._send_json({
            'nombre': 'API de Seguimiento de Alumnos',
            'version': '2.0.0',
            'database': 'PostgreSQL (Vercel)',
            'endpoints': [
                'GET /',
                'GET /health',
                'GET /cursos',
                'GET /cursos/{id}/alumnos',
                'GET /cursos/{id}/tps',
                'GET /alumnos',
                'GET /alertas',
                'POST /alumnos',
                'POST /clase/registrar'
            ]
        })
    
    def _handle_health(self):
        """Health check con verificación de BD"""
        try:
            # Verificar conexión a BD
            result = execute_query("SELECT COUNT(*) as count FROM alumno", fetch_one=True)
            
            self._send_json({
                'status': 'healthy',
                'database': 'connected',
                'alumnos_count': result['count']
            })
        except Exception as e:
            self._send_json({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }, 500)
    
    def _handle_get_cursos(self):
        """Lista cursos con estadísticas"""
        query = """
            SELECT 
                c.id,
                c.nombre_materia as materia,
                c.anio as cohorte,
                c.cuatrimestre,
                c.docente_responsable as docente,
                COUNT(DISTINCT i.alumno_id) as "totalAlumnos",
                COALESCE(ROUND(AVG(vra.porcentaje_asistencia), 0), 0) as "asistenciaPromedio",
                COUNT(DISTINCT CASE 
                    WHEN vra.porcentaje_asistencia < 70 THEN vra.alumno_id 
                END) as "alumnosEnRiesgo",
                COUNT(DISTINCT cl.id) as "totalClases",
                MAX(cl.fecha) as "ultimaClase"
            FROM curso c
            LEFT JOIN inscripcion i ON c.id = i.curso_id
            LEFT JOIN vista_resumen_asistencias vra 
                ON i.alumno_id = vra.alumno_id 
                AND c.id = vra.curso_id
            LEFT JOIN clase cl ON c.id = cl.curso_id
            GROUP BY c.id, c.nombre_materia, c.anio, c.cuatrimestre, c.docente_responsable
            ORDER BY c.anio DESC, c.cuatrimestre DESC, c.nombre_materia
        """
        
        cursos = execute_query(query)
        
        self._send_json({
            'total': len(cursos),
            'clases': cursos
        })
    
    def _handle_get_alumnos(self):
        """Lista todos los alumnos"""
        query = """
            SELECT 
                id,
                nombre,
                apellido,
                dni,
                email,
                cohorte,
                CONCAT(apellido, ', ', nombre) as nombre_completo
            FROM alumno
            ORDER BY apellido, nombre
        """
        
        alumnos = execute_query(query)
        
        self._send_json({
            'total': len(alumnos),
            'alumnos': alumnos
        })
    
    def _handle_get_alumnos_curso(self, curso_id):
        """Lista alumnos de un curso específico"""
        query = """
            SELECT 
                a.id,
                a.nombre,
                a.apellido,
                a.dni,
                a.email,
                a.cohorte,
                CONCAT(a.apellido, ', ', a.nombre) as nombre_completo,
                COALESCE(vra.porcentaje_asistencia, 0) as porcentaje_asistencia,
                COALESCE(vrt.porcentaje_entregados, 0) as porcentaje_tps
            FROM alumno a
            JOIN inscripcion i ON a.id = i.alumno_id
            LEFT JOIN vista_resumen_asistencias vra 
                ON a.id = vra.alumno_id AND i.curso_id = vra.curso_id
            LEFT JOIN vista_resumen_tps vrt 
                ON a.id = vrt.alumno_id AND i.curso_id = vrt.curso_id
            WHERE i.curso_id = %s
            ORDER BY a.apellido, a.nombre
        """
        
        alumnos = execute_query(query, (curso_id,))
        
        self._send_json({
            'total': len(alumnos),
            'alumnos': alumnos
        })
    
    def _handle_get_tps_curso(self, curso_id):
        """Lista TPs de un curso"""
        query = """
            SELECT 
                tp.id,
                tp.titulo,
                tp.descripcion,
                tp.fecha_entrega as "fechaEntrega",
                COUNT(DISTINCT et.alumno_id) FILTER (WHERE et.entregado = TRUE) as entregados,
                COUNT(DISTINCT et.alumno_id) FILTER (WHERE et.entregado = FALSE) as "noEntregados",
                ROUND(AVG(et.nota), 2) as "promedioNotas"
            FROM trabajo_practico tp
            LEFT JOIN entrega_tp et ON tp.id = et.trabajo_practico_id
            WHERE tp.curso_id = %s
            GROUP BY tp.id, tp.titulo, tp.descripcion, tp.fecha_entrega
            ORDER BY tp.fecha_entrega DESC
        """
        
        tps = execute_query(query, (curso_id,))
        
        self._send_json({
            'total': len(tps),
            'tps': tps
        })
    
    def _handle_get_alertas(self):
        """Obtiene alertas de alumnos en riesgo"""
        # Detectar 2 faltas consecutivas
        query_faltas = """
            WITH clases_ordenadas AS (
                SELECT 
                    ra.alumno_id,
                    cl.curso_id,
                    cl.fecha,
                    ra.estado,
                    LAG(ra.estado, 1) OVER (
                        PARTITION BY ra.alumno_id, cl.curso_id 
                        ORDER BY cl.fecha
                    ) AS estado_anterior,
                    LAG(cl.fecha, 1) OVER (
                        PARTITION BY ra.alumno_id, cl.curso_id 
                        ORDER BY cl.fecha
                    ) AS fecha_anterior
                FROM registro_asistencia ra
                JOIN clase cl ON ra.clase_id = cl.id
            )
            SELECT DISTINCT
                a.id as alumno_id,
                CONCAT(a.apellido, ', ', a.nombre) as alumno_nombre,
                c.id as curso_id,
                c.nombre_materia as curso_nombre,
                co.fecha_anterior,
                co.fecha,
                'faltas_consecutivas' as tipo
            FROM clases_ordenadas co
            JOIN alumno a ON co.alumno_id = a.id
            JOIN curso c ON co.curso_id = c.id
            WHERE co.estado = 'Ausente' 
              AND co.estado_anterior = 'Ausente'
            ORDER BY co.fecha DESC
            LIMIT 50
        """
        
        # Alumnos con asistencia < 70%
        query_asistencia = """
            SELECT 
                a.id as alumno_id,
                CONCAT(a.apellido, ', ', a.nombre) as alumno_nombre,
                c.id as curso_id,
                c.nombre_materia as curso_nombre,
                vra.porcentaje_asistencia,
                'asistencia_baja' as tipo
            FROM vista_resumen_asistencias vra
            JOIN alumno a ON vra.alumno_id = a.id
            JOIN curso c ON vra.curso_id = c.id
            WHERE vra.porcentaje_asistencia < 70
            ORDER BY vra.porcentaje_asistencia ASC
            LIMIT 50
        """
        
        alertas_faltas = execute_query(query_faltas)
        alertas_asistencia = execute_query(query_asistencia)
        
        # Combinar alertas
        alertas = []
        
        for alerta in alertas_faltas:
            alertas.append({
                'tipo': 'faltas_consecutivas',
                'nivel': 'alto',
                'alumno': {
                    'id': alerta['alumno_id'],
                    'nombre': alerta['alumno_nombre']
                },
                'curso': {
                    'id': alerta['curso_id'],
                    'materia': alerta['curso_nombre']
                },
                'mensaje': f"2 faltas consecutivas ({alerta['fecha_anterior']} y {alerta['fecha']})"
            })
        
        for alerta in alertas_asistencia:
            alertas.append({
                'tipo': 'asistencia_baja',
                'nivel': 'medio' if alerta['porcentaje_asistencia'] >= 60 else 'alto',
                'alumno': {
                    'id': alerta['alumno_id'],
                    'nombre': alerta['alumno_nombre']
                },
                'curso': {
                    'id': alerta['curso_id'],
                    'materia': alerta['curso_nombre']
                },
                'mensaje': f"Asistencia: {alerta['porcentaje_asistencia']:.0f}%"
            })
        
        self._send_json({
            'total': len(alertas),
            'alertas': alertas
        })
    
    def _handle_create_alumno(self, data):
        """Crea un nuevo alumno"""
        query = """
            INSERT INTO alumno (nombre, apellido, dni, email, cohorte)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        
        try:
            alumno_id = execute_insert(query, (
                data['nombre'],
                data['apellido'],
                data['dni'],
                data['email'],
                data['cohorte']
            ))
            
            self._send_json({
                'success': True,
                'id': alumno_id,
                'message': 'Alumno creado exitosamente'
            }, 201)
        except Exception as e:
            self._send_error_json(f'Error al crear alumno: {str(e)}', 400)
    
    def _handle_registrar_clase(self, data):
        """Registra una clase completa con asistencia, participación, TPs, etc."""
        # TODO: Implementar guardado de clase
        # Por ahora solo devolvemos éxito
        self._send_json({
            'success': True,
            'message': 'Clase registrada (pendiente implementación completa)'
        })

# Handler para Vercel
def handler(request, response):
    """Entry point para Vercel"""
    return APIHandler(request, response)
