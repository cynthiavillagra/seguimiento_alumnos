"""
Servidor Local de Desarrollo
Ejecuta la API localmente para pruebas
"""

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

# Agregar el directorio api al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

# Importar el handler de la API
from api.index import handler as api_handler

class LocalRequestHandler(SimpleHTTPRequestHandler):
    """Handler que sirve archivos estáticos y maneja rutas de API"""
    
    def __init__(self, *args, **kwargs):
        # Servir desde la carpeta public
        super().__init__(*args, directory='public', **kwargs)
    
    def do_GET(self):
        """Maneja requests GET"""
        # Si es una ruta de API, usar el handler de la API
        if self.path.startswith('/api/') or self.path in ['/cursos', '/alumnos', '/trabajos-practicos', '/alertas', '/health']:
            self.handle_api_request()
        else:
            # Si no, servir archivo estático
            super().do_GET()
    
    def do_POST(self):
        """Maneja requests POST"""
        self.handle_api_request()
    
    def do_PUT(self):
        """Maneja requests PUT"""
        self.handle_api_request()
    
    def do_DELETE(self):
        """Maneja requests DELETE"""
        self.handle_api_request()
    
    def do_OPTIONS(self):
        """Maneja requests OPTIONS (CORS)"""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def handle_api_request(self):
        """Delega el request al handler de la API"""
        try:
            # Crear un objeto request simulado para Vercel
            class FakeRequest:
                def __init__(self, handler):
                    self.method = handler.command
                    self.path = handler.path
                    self.headers = handler.headers
                    
                    # Leer el body si existe
                    content_length = int(handler.headers.get('Content-Length', 0))
                    if content_length > 0:
                        self.body = handler.rfile.read(content_length)
                    else:
                        self.body = b''
            
            fake_request = FakeRequest(self)
            
            # Llamar al handler de la API
            # Nota: Esto es una simulación, el handler real de Vercel funciona diferente
            # pero para desarrollo local es suficiente
            api_handler(fake_request, None)
            
        except Exception as e:
            self.send_error(500, f"Error en API: {str(e)}")

def run_server(port=5000):
    """Inicia el servidor local"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LocalRequestHandler)
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🎓 Sistema de Seguimiento de Alumnos - Servidor Local   ║
    ╚═══════════════════════════════════════════════════════════╝
    
    ✅ Servidor corriendo en: http://localhost:{port}
    
    📂 Sirviendo archivos desde: ./public
    🔌 API disponible en: http://localhost:{port}/api/*
    
    ⚠️  IMPORTANTE:
    - Asegúrate de tener configurado el archivo .env
    - La variable DATABASE_URL debe apuntar a tu BD
    
    Presiona Ctrl+C para detener el servidor
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Servidor detenido")
        httpd.shutdown()

if __name__ == '__main__':
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    # Obtener puerto de .env o usar 5000 por defecto
    port = int(os.getenv('PORT', 5000))
    
    run_server(port)
