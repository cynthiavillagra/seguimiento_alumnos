"""
Implementación PostgreSQL: ClaseRepository
Sistema de Seguimiento de Alumnos
"""

import psycopg2
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.clase_repository_base import ClaseRepositoryBase
from src.domain.entities.clase import Clase
from src.domain.exceptions.domain_exceptions import (
    BusinessRuleException,
    ClaseNoEncontradaException
)


class ClaseRepositoryPostgres(ClaseRepositoryBase):
    """
    Implementación PostgreSQL del repositorio de Clase.
    """
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, clase: Clase) -> Clase:
        """Crea una nueva clase"""
        query = """
            INSERT INTO clase (curso_id, fecha, numero_clase, tema, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, fecha_creacion;
        """
        params = (
            clase.curso_id,
            clase.fecha,
            clase.numero_clase,
            clase.tema,
            datetime.now()
        )
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                self.conexion.commit()
                
                clase.id = row['id']
                clase.fecha_creacion = row['fecha_creacion']
                return clase
                
        except psycopg2.errors.UniqueViolation:
            self.conexion.rollback()
            raise BusinessRuleException(f"Ya existe una clase con número {clase.numero_clase} para este curso.")
        except Exception as e:
            self.conexion.rollback()
            raise e

    def obtener_por_id(self, id: int) -> Optional[Clase]:
        """Obtiene una clase por ID"""
        query = "SELECT * FROM clase WHERE id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_clase(row) if row else None

    def obtener_por_curso(self, curso_id: int) -> List[Clase]:
        """Obtiene todas las clases de un curso"""
        query = "SELECT * FROM clase WHERE curso_id = %s ORDER BY numero_clase ASC"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (curso_id,))
            rows = cursor.fetchall()
            return [self._row_to_clase(row) for row in rows]

    def actualizar(self, clase: Clase) -> Clase:
        """Actualiza una clase existente"""
        if clase.id is None:
            raise ValueError("La clase debe tener un ID para actualizarla")
            
        check_query = "SELECT id FROM clase WHERE id = %s"
        update_query = """
            UPDATE clase 
            SET fecha = %s, numero_clase = %s, tema = %s
            WHERE id = %s
        """
        params = (
            clase.fecha,
            clase.numero_clase,
            clase.tema,
            clase.id
        )
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(check_query, (clase.id,))
                if not cursor.fetchone():
                    raise ClaseNoEncontradaException(f"No existe clase con ID {clase.id}")
                
                cursor.execute(update_query, params)
                self.conexion.commit()
                return clase
                
        except psycopg2.errors.UniqueViolation:
            self.conexion.rollback()
            raise BusinessRuleException(f"Ya existe una clase con número {clase.numero_clase} para este curso.")
        except Exception as e:
            self.conexion.rollback()
            raise e

    def eliminar(self, id: int) -> bool:
        """Elimina una clase por ID"""
        query = "DELETE FROM clase WHERE id = %s"
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, (id,))
                deleted = cursor.rowcount > 0
                self.conexion.commit()
                return deleted
        except Exception as e:
            self.conexion.rollback()
            raise e

    def _row_to_clase(self, row) -> Clase:
        """Convierte una fila de BD a una entidad Clase"""
        return Clase(
            id=row['id'],
            curso_id=row['curso_id'],
            fecha=row['fecha'],
            numero_clase=row['numero_clase'],
            tema=row['tema'],
            fecha_creacion=row['fecha_creacion'] if row.get('fecha_creacion') else None
        )
