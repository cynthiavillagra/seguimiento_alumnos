"""
API REST - Versión de Diagnóstico
"""

import json
import os
from http.server import BaseHTTPRequestHandler

class APIHandler(BaseHTTPRequestHandler):
    """Handler HTTP simplificado para diagnóstico"""
    
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _send_json(self, data, status_code=200):
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self._set_headers(204)
    
    def do_GET(self):
        path = self.path
        
        try:
            if path == '/health':
                # Test 1: Verificar que la función funciona
                self._send_json({'status': 'ok', 'message': 'Function is working'})
                
            elif path == '/test-env':
                # Test 2: Verificar variables de entorno
                env_vars = {
                    'DATABASE_URL': 'SET' if os.getenv('DATABASE_URL') else 'NOT SET',
                    'POSTGRES_URL': 'SET' if os.getenv('POSTGRES_URL') else 'NOT SET',
                }
                self._send_json({'env_vars': env_vars})
                
            elif path == '/test-import':
                # Test 3: Verificar que psycopg2 se puede importar
                try:
                    import psycopg2
                    self._send_json({'psycopg2': 'OK', 'version': psycopg2.__version__})
                except Exception as e:
                    self._send_json({'psycopg2': 'ERROR', 'error': str(e)}, 500)
                    
            elif path == '/test-db':
                # Test 4: Verificar conexión a BD
                try:
                    import psycopg2
                    db_url = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
                    
                    if not db_url:
                        self._send_json({'error': 'No DATABASE_URL or POSTGRES_URL found'}, 500)
                        return
                    
                    conn = psycopg2.connect(db_url)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM alumno")
                    count = cursor.fetchone()[0]
                    cursor.close()
                    conn.close()
                    
                    self._send_json({'database': 'OK', 'alumno_count': count})
                except Exception as e:
                    import traceback
                    self._send_json({
                        'database': 'ERROR',
                        'error': str(e),
                        'traceback': traceback.format_exc()
                    }, 500)
                    
            else:
                self._send_json({'error': 'Not found', 'path': path}, 404)
                
        except Exception as e:
            import traceback
            self._send_json({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, 500)

# Handler para Vercel
def handler(request, response):
    return APIHandler(request, response)
