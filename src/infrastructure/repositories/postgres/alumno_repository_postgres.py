"""
Implementación PostgreSQL: AlumnoRepository
Sistema de Seguimiento de Alumnos
"""

import psycopg2
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.alumno_repository_base import AlumnoRepositoryBase
from src.domain.entities.alumno import Alumno
from src.domain.exceptions.domain_exceptions import (
    DNIDuplicadoException,
    AlumnoNoEncontradoException
)


class AlumnoRepositoryPostgres(AlumnoRepositoryBase):
    """
    Implementación PostgreSQL del repositorio de Alumno.
    """
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, alumno: Alumno) -> Alumno:
        """Crea un nuevo alumno en la base de datos"""
        query = """
            INSERT INTO alumno (nombre, apellido, dni, email, cohorte, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, fecha_creacion;
        """
        params = (
            alumno.nombre,
            alumno.apellido,
            alumno.dni,
            alumno.email,
            alumno.cohorte,
            datetime.now()
        )
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                self.conexion.commit()
                
                alumno.id = row['id']
                alumno.fecha_creacion = row['fecha_creacion']
                return alumno
                
        except psycopg2.errors.UniqueViolation:
            self.conexion.rollback()
            raise DNIDuplicadoException(f"Ya existe un alumno con DNI {alumno.dni}")
        except Exception as e:
            self.conexion.rollback()
            raise e

    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        """Obtiene un alumno por ID"""
        query = "SELECT * FROM alumno WHERE id = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_alumno(row)
            return None

    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """Obtiene un alumno por DNI"""
        query = "SELECT * FROM alumno WHERE dni = %s"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (dni,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_alumno(row)
            return None

    def obtener_todos(self, limite: Optional[int] = None, offset: int = 0) -> List[Alumno]:
        """Obtiene todos los alumnos con paginación opcional"""
        query = "SELECT * FROM alumno ORDER BY apellido, nombre"
        
        if limite is not None:
            query += f" LIMIT {limite} OFFSET {offset}"
            
        with self.conexion.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._row_to_alumno(row) for row in rows]

    def buscar_por_nombre(self, nombre: str) -> List[Alumno]:
        """Busca alumnos por nombre o apellido (búsqueda parcial)"""
        query = """
            SELECT * FROM alumno 
            WHERE LOWER(nombre) LIKE LOWER(%s) OR LOWER(apellido) LIKE LOWER(%s)
            ORDER BY apellido, nombre
        """
        search_term = f"%{nombre}%"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (search_term, search_term))
            rows = cursor.fetchall()
            return [self._row_to_alumno(row) for row in rows]

    def obtener_por_cohorte(self, cohorte: int) -> List[Alumno]:
        """Obtiene todos los alumnos de una cohorte específica"""
        query = "SELECT * FROM alumno WHERE cohorte = %s ORDER BY apellido, nombre"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (cohorte,))
            rows = cursor.fetchall()
            return [self._row_to_alumno(row) for row in rows]

    def actualizar(self, alumno: Alumno) -> Alumno:
        """Actualiza un alumno existente"""
        if alumno.id is None:
            raise ValueError("El alumno debe tener un ID para actualizarlo")
            
        check_query = "SELECT id FROM alumno WHERE id = %s"
        update_query = """
            UPDATE alumno 
            SET nombre = %s, apellido = %s, dni = %s, email = %s, cohorte = %s
            WHERE id = %s
        """
        params = (
            alumno.nombre,
            alumno.apellido,
            alumno.dni,
            alumno.email,
            alumno.cohorte,
            alumno.id
        )
        
        try:
            with self.conexion.cursor() as cursor:
                # Verificar existencia
                cursor.execute(check_query, (alumno.id,))
                if not cursor.fetchone():
                    raise AlumnoNoEncontradoException(f"No existe alumno con ID {alumno.id}")
                
                # Actualizar
                cursor.execute(update_query, params)
                self.conexion.commit()
                return alumno
                
        except psycopg2.errors.UniqueViolation:
            self.conexion.rollback()
            raise DNIDuplicadoException(f"Ya existe otro alumno con DNI {alumno.dni}")
        except Exception as e:
            self.conexion.rollback()
            raise e

    def eliminar(self, id: int) -> bool:
        """Elimina un alumno por ID"""
        query = "DELETE FROM alumno WHERE id = %s"
        
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(query, (id,))
                deleted = cursor.rowcount > 0
                self.conexion.commit()
                return deleted
        except Exception as e:
            self.conexion.rollback()
            raise e

    def contar_total(self) -> int:
        """Cuenta el total de alumnos"""
        query = "SELECT COUNT(*) as total FROM alumno"
        
        with self.conexion.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            return row['total'] if row else 0

    def _row_to_alumno(self, row) -> Alumno:
        """Convierte una fila de BD a una entidad Alumno"""
        return Alumno(
            id=row['id'],
            nombre=row['nombre'],
            apellido=row['apellido'],
            dni=row['dni'],
            email=row['email'],
            cohorte=row['cohorte'],
            fecha_creacion=row['fecha_creacion'] if row.get('fecha_creacion') else None
        )
