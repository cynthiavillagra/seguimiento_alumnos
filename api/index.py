"""
API REST - Versión de Diagnóstico
Compatible con Vercel Serverless Functions
"""

import json
import os

def handler(event, context):
    """
    Handler principal para Vercel
    event: dict con información del request
    context: contexto de ejecución
    """
    
    # Obtener el path del request
    path = event.get('path', event.get('rawPath', '/'))
    method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method', 'GET'))
    
    # Headers CORS
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Manejar OPTIONS (CORS preflight)
    if method == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Routing
        if path == '/health' or path == '/api/health':
            response_data = {'status': 'ok', 'message': 'Function is working'}
            
        elif path == '/test-env' or path == '/api/test-env':
            env_vars = {
                'DATABASE_URL': 'SET' if os.getenv('DATABASE_URL') else 'NOT SET',
                'POSTGRES_URL': 'SET' if os.getenv('POSTGRES_URL') else 'NOT SET',
            }
            response_data = {'env_vars': env_vars}
            
        elif path == '/test-import' or path == '/api/test-import':
            try:
                import psycopg2
                response_data = {'psycopg2': 'OK', 'version': psycopg2.__version__}
            except Exception as e:
                response_data = {'psycopg2': 'ERROR', 'error': str(e)}
                
        elif path == '/test-db' or path == '/api/test-db':
            try:
                import psycopg2
                db_url = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
                
                if not db_url:
                    response_data = {'error': 'No DATABASE_URL or POSTGRES_URL found'}
                else:
                    conn = psycopg2.connect(db_url)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM alumno")
                    count = cursor.fetchone()[0]
                    cursor.close()
                    conn.close()
                    
                    response_data = {'database': 'OK', 'alumno_count': count}
            except Exception as e:
                import traceback
                response_data = {
                    'database': 'ERROR',
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
                
        elif path == '/cursos' or path == '/clases' or path == '/api/cursos' or path == '/api/clases':
            # Devolver datos de ejemplo por ahora
            response_data = {
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
            
        else:
            response_data = {'error': 'Not found', 'path': path}
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps(response_data, ensure_ascii=False)
            }
        
        # Respuesta exitosa
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data, ensure_ascii=False, default=str)
        }
        
    except Exception as e:
        import traceback
        error_data = {
            'error': str(e),
            'traceback': traceback.format_exc(),
            'path': path
        }
        
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(error_data, ensure_ascii=False)
        }
