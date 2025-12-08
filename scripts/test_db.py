
import os
import sys
from urllib.parse import urlparse
import pg8000
import ssl

def test_connection():
    print("--- Test de Conexión a Base de Datos ---")
    
    # Intentar cargar .env manualmente si no están cargadas
    if not os.environ.get("POSTGRES_URL"):
        print("Cargando variables desde .env...")
        try:
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'): continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        val = v.strip()
                        # Remove quotes if present
                        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                            val = val[1:-1]
                        os.environ[k.strip()] = val
        except FileNotFoundError:
            print("❌ Archivo .env no encontrado")
            return

    db_url = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
    
    if not db_url:
        print("❌ No se encontró POSTGRES_URL ni DATABASE_URL en variables de entorno")
        return

    print(f"URL encontrada (oculta): {db_url[:15]}...{db_url[-5:]}")
    
    try:
        parsed = urlparse(db_url)
        print(f"Host: {parsed.hostname}")
        print(f"Port: {parsed.port}")
        print(f"User: {parsed.username}")
        print(f"Database: {parsed.path.lstrip('/')}")
        
        # Crear contexto SSL explícito para debug
        ssl_context = ssl.create_default_context()
        
        print("\nIntentando conectar con pg8000...")
        conn = pg8000.connect(
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path.lstrip('/'),
            ssl_context=ssl_context 
        )
        print("✅ ¡CONEXIÓN EXITOSA!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"Versión de Servidor: {version}")
        conn.close()
        
    except Exception as e:
        print(f"\n❌ ERROR DE CONEXIÓN:")
        print(f"{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()
