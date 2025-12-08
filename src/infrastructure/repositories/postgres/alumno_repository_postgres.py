"""
Implementación PostgreSQL: AlumnoRepository
Sistema de Seguimiento de Alumnos

Compatible con pg8000 (pure Python driver).
"""

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
    Usa pg8000 como driver.
    """
    
    # Columnas de la tabla alumno en orden
    COLUMNS = ['id', 'nombre', 'apellido', 'dni', 'email', 'cohorte', 'fecha_creacion']
    
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, alumno: Alumno) -> Alumno:
        """Crea un nuevo alumno en la base de datos"""
        query = """
            INSERT INTO alumno (nombre, apellido, dni, email, cohorte, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, fecha_creacion
        """
        params = (
            alumno.nombre,
            alumno.apellido,
            alumno.dni,
            alumno.email,
            alumno.cohorte,
            datetime.now()
        )
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            self.conexion.commit()
            
            alumno.id = row[0]
            alumno.fecha_creacion = row[1]
            return alumno
            
        except Exception as e:
            self.conexion.rollback()
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                raise DNIDuplicadoException(f"Ya existe un alumno con DNI {alumno.dni}")
            raise e
        finally:
            cursor.close()

    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        """Obtiene un alumno por ID"""
        query = "SELECT id, nombre, apellido, dni, email, cohorte, fecha_creacion FROM alumno WHERE id = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            self.conexion.commit()
            return self._row_to_alumno(row) if row else None
        finally:
            cursor.close()

    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """Obtiene un alumno por DNI"""
        query = "SELECT id, nombre, apellido, dni, email, cohorte, fecha_creacion FROM alumno WHERE dni = %s"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (dni,))
            row = cursor.fetchone()
            self.conexion.commit()
            return self._row_to_alumno(row) if row else None
        finally:
            cursor.close()

    def obtener_todos(self, limite: Optional[int] = None, offset: int = 0) -> List[Alumno]:
        """Obtiene todos los alumnos con paginación opcional"""
        query = "SELECT id, nombre, apellido, dni, email, cohorte, fecha_creacion FROM alumno ORDER BY apellido, nombre"
        
        if limite is not None:
            query += f" LIMIT {limite} OFFSET {offset}"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            self.conexion.commit()
            return [self._row_to_alumno(row) for row in rows]
        finally:
            cursor.close()

    def buscar_por_nombre(self, nombre: str) -> List[Alumno]:
        """Busca alumnos por nombre o apellido (búsqueda parcial)"""
        query = """
            SELECT id, nombre, apellido, dni, email, cohorte, fecha_creacion FROM alumno 
            WHERE LOWER(nombre) LIKE LOWER(%s) OR LOWER(apellido) LIKE LOWER(%s)
            ORDER BY apellido, nombre
        """
        search_term = f"%{nombre}%"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (search_term, search_term))
            rows = cursor.fetchall()
            self.conexion.commit()
            return [self._row_to_alumno(row) for row in rows]
        finally:
            cursor.close()

    def obtener_por_cohorte(self, cohorte: int) -> List[Alumno]:
        """Obtiene todos los alumnos de una cohorte específica"""
        query = "SELECT id, nombre, apellido, dni, email, cohorte, fecha_creacion FROM alumno WHERE cohorte = %s ORDER BY apellido, nombre"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (cohorte,))
            rows = cursor.fetchall()
            self.conexion.commit()
            return [self._row_to_alumno(row) for row in rows]
        finally:
            cursor.close()

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
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(check_query, (alumno.id,))
            if not cursor.fetchone():
                raise AlumnoNoEncontradoException(f"No existe alumno con ID {alumno.id}")
            
            cursor.execute(update_query, params)
            self.conexion.commit()
            return alumno
            
        except Exception as e:
            self.conexion.rollback()
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                raise DNIDuplicadoException(f"Ya existe otro alumno con DNI {alumno.dni}")
            raise e
        finally:
            cursor.close()

    def eliminar(self, id: int) -> bool:
        """Elimina un alumno por ID"""
        query = "DELETE FROM alumno WHERE id = %s"
        
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

    def contar_total(self) -> int:
        """Cuenta el total de alumnos"""
        query = "SELECT COUNT(*) FROM alumno"
        
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query)
            row = cursor.fetchone()
            return row[0] if row else 0
        finally:
            cursor.close()

    def _row_to_alumno(self, row) -> Alumno:
        """Convierte una tupla de BD a una entidad Alumno"""
        # row es una tupla: (id, nombre, apellido, dni, email, cohorte, fecha_creacion)
        return Alumno(
            id=row[0],
            nombre=row[1],
            apellido=row[2],
            dni=row[3],
            email=row[4],
            cohorte=row[5],
            fecha_creacion=row[6] if len(row) > 6 else None
        )
