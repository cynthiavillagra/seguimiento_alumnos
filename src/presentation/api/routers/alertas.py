"""
Router de FastAPI para Alertas
Sistema de Seguimiento de Alumnos

Endpoint optimizado que calcula alertas en el servidor
para evitar múltiples llamadas desde el frontend.
"""

from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from src.infrastructure.database.connection import get_db_connection

router = APIRouter(
    prefix="/alertas",
    tags=["Alertas"],
)

@router.get(
    "/",
    summary="Obtener alertas de riesgo",
    description="Calcula y devuelve alertas basadas en ausencias consecutivas y TPs no entregados"
)
def obtener_alertas():
    """
    Calcula alertas de riesgo para todos los alumnos.
    
    Criterios:
    - 2 ausencias consecutivas
    - 2 TPs consecutivos no entregados o desaprobados (nota < 6)
    """
    conn = get_db_connection()
    alertas = []
    
    try:
        cursor = conn.cursor()
        
        # Obtener todos los cursos
        cursor.execute("SELECT id, nombre_materia, anio, cuatrimestre FROM curso")
        cursos = cursor.fetchall()
        
        for curso in cursos:
            curso_id, nombre_materia, anio, cuatrimestre = curso
            curso_info = {
                "id": curso_id,
                "nombre_materia": nombre_materia,
                "anio": anio,
                "cuatrimestre": cuatrimestre
            }
            
            # Obtener alumnos inscriptos en el curso
            cursor.execute("""
                SELECT a.id, a.nombre, a.apellido 
                FROM alumno a
                JOIN inscripcion i ON a.id = i.alumno_id
                WHERE i.curso_id = %s
            """, (curso_id,))
            alumnos = cursor.fetchall()
            
            # Obtener clases del curso ordenadas por fecha
            cursor.execute("""
                SELECT id, fecha FROM clase 
                WHERE curso_id = %s 
                ORDER BY fecha ASC
            """, (curso_id,))
            clases = cursor.fetchall()
            
            # Obtener TPs del curso ordenados por fecha
            cursor.execute("""
                SELECT id, titulo, fecha_entrega FROM trabajo_practico 
                WHERE curso_id = %s 
                ORDER BY fecha_entrega ASC
            """, (curso_id,))
            tps = cursor.fetchall()
            
            # Analizar cada alumno
            for alumno in alumnos:
                alumno_id, nombre, apellido = alumno
                alumno_info = {
                    "id": alumno_id,
                    "nombre_completo": f"{apellido}, {nombre}"
                }
                motivos = []
                
                # Verificar ausencias consecutivas
                if len(clases) >= 2:
                    ausencias_consecutivas = verificar_ausencias_consecutivas(
                        cursor, alumno_id, clases
                    )
                    if ausencias_consecutivas:
                        motivos.append(ausencias_consecutivas)
                
                # Verificar TPs problemáticos consecutivos
                if len(tps) >= 2:
                    tps_problematicos = verificar_tps_consecutivos(
                        cursor, alumno_id, tps
                    )
                    if tps_problematicos:
                        motivos.append(tps_problematicos)
                
                # Si hay motivos, crear alerta
                if motivos:
                    alertas.append({
                        "alumno": alumno_info,
                        "curso": curso_info,
                        "motivos": motivos,
                        "nivel": "high" if len(motivos) >= 2 else "medium"
                    })
        
        conn.commit()
        cursor.close()
        
        # Ordenar alertas: high primero
        alertas.sort(key=lambda a: (0 if a["nivel"] == "high" else 1))
        
        return {
            "alertas": alertas,
            "resumen": {
                "total": len(alertas),
                "high": len([a for a in alertas if a["nivel"] == "high"]),
                "medium": len([a for a in alertas if a["nivel"] == "medium"])
            }
        }
        
    except Exception as e:
        print(f"Error calculando alertas: {e}")
        import traceback
        traceback.print_exc()
        return {
            "alertas": [],
            "resumen": {"total": 0, "high": 0, "medium": 0},
            "error": str(e)
        }


def verificar_ausencias_consecutivas(cursor, alumno_id: int, clases: list) -> dict:
    """Verifica si el alumno tiene 2 ausencias consecutivas"""
    asistencias = []
    
    for clase in clases:
        clase_id, fecha = clase
        cursor.execute("""
            SELECT estado FROM registro_asistencia 
            WHERE alumno_id = %s AND clase_id = %s
        """, (alumno_id, clase_id))
        row = cursor.fetchone()
        estado = row[0] if row else "Sin registro"
        asistencias.append({"clase_id": clase_id, "fecha": fecha, "estado": estado})
    
    # Buscar 2 ausencias consecutivas (desde las más recientes)
    for i in range(len(asistencias) - 1, 0, -1):
        estado_actual = (asistencias[i]["estado"] or "").lower()
        estado_anterior = (asistencias[i-1]["estado"] or "").lower()
        if estado_actual == "ausente" and estado_anterior == "ausente":
            fecha1 = asistencias[i-1]["fecha"].strftime("%d/%m/%Y") if hasattr(asistencias[i-1]["fecha"], 'strftime') else str(asistencias[i-1]["fecha"])
            fecha2 = asistencias[i]["fecha"].strftime("%d/%m/%Y") if hasattr(asistencias[i]["fecha"], 'strftime') else str(asistencias[i]["fecha"])
            return {
                "tipo": "asistencia",
                "mensaje": f"2 ausencias consecutivas ({fecha1} y {fecha2})",
                "icono": "❌"
            }
    
    return None


def verificar_tps_consecutivos(cursor, alumno_id: int, tps: list) -> dict:
    """Verifica si el alumno tiene 2 TPs problemáticos consecutivos"""
    entregas = []
    
    for tp in tps:
        tp_id, titulo, fecha_entrega = tp
        cursor.execute("""
            SELECT entregado, nota, estado FROM entrega_tp 
            WHERE alumno_id = %s AND trabajo_practico_id = %s
        """, (alumno_id, tp_id))
        row = cursor.fetchone()
        
        es_problematico = False
        motivo = ""
        
        if not row:
            es_problematico = True
            motivo = "No entregado"
        else:
            entregado, nota, estado = row
            if not entregado:
                es_problematico = True
                motivo = "No entregado"
            elif nota is not None and nota < 6:
                es_problematico = True
                motivo = f"Desaprobado ({nota})"
        
        entregas.append({
            "tp_id": tp_id,
            "titulo": titulo,
            "es_problematico": es_problematico,
            "motivo": motivo
        })
    
    # Buscar 2 TPs problemáticos consecutivos (desde los más recientes)
    for i in range(len(entregas) - 1, 0, -1):
        if entregas[i]["es_problematico"] and entregas[i-1]["es_problematico"]:
            return {
                "tipo": "tp",
                "mensaje": f"2 TPs con problemas: {entregas[i-1]['titulo']} ({entregas[i-1]['motivo']}) y {entregas[i]['titulo']} ({entregas[i]['motivo']})",
                "icono": "📝"
            }
    
    return None
