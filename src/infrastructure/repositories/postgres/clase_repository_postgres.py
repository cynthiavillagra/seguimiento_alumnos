"""
Implementación PostgreSQL: ClaseRepository
Compatible con pg8000.
"""

from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.clase_repository_base import ClaseRepositoryBase
from src.domain.entities.clase import Clase
from src.domain.exceptions.domain_exceptions import ClaseNoEncontradaException, BusinessRuleException


class ClaseRepositoryPostgres(ClaseRepositoryBase):
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, clase: Clase) -> Clase:
        query = """
            INSERT INTO clase (curso_id, fecha, numero_clase, tema, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, fecha_creacion
        """
        params = (
            clase.curso_id,
            clase.fecha,
            clase.numero_clase,
            clase.tema,
            datetime.now()
        )
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            self.conexion.commit()
            
            clase.id = row[0]
            clase.fecha_creacion = row[1]
            return clase
        except Exception as e:
            self.conexion.rollback()
            if 'unique' in str(e).lower():
                raise BusinessRuleException(f"Ya existe una clase con número {clase.numero_clase}")
            raise e
        finally:
            cursor.close()

    def obtener_por_id(self, id: int) -> Optional[Clase]:
        query = "SELECT id, curso_id, fecha, numero_clase, tema, fecha_creacion FROM clase WHERE id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_clase(row) if row else None
        finally:
            cursor.close()

    def obtener_por_curso(self, curso_id: int) -> List[Clase]:
        query = "SELECT id, curso_id, fecha, numero_clase, tema, fecha_creacion FROM clase WHERE curso_id = %s ORDER BY numero_clase"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (curso_id,))
            rows = cursor.fetchall()
            return [self._row_to_clase(row) for row in rows]
        finally:
            cursor.close()

    def actualizar(self, clase: Clase) -> Clase:
        if clase.id is None:
            raise ValueError("La clase debe tener un ID")
        
        query = """
            UPDATE clase 
            SET fecha = %s, numero_clase = %s, tema = %s
            WHERE id = %s
        """
        params = (clase.fecha, clase.numero_clase, clase.tema, clase.id)
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, params)
            self.conexion.commit()
            return clase
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def eliminar(self, id: int) -> bool:
        query = "DELETE FROM clase WHERE id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (id,))
            deleted = cursor.rowcount > 0
            self.conexion.commit()
            return deleted
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def _row_to_clase(self, row) -> Clase:
        return Clase(
            id=row[0],
            curso_id=row[1],
            fecha=row[2],
            numero_clase=row[3],
            tema=row[4],
            fecha_creacion=row[5] if len(row) > 5 else None
        )
