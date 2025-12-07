"""
Implementación SQLite: AlumnoRepository
Sistema de Seguimiento de Alumnos

Decisión de diseño: Implementación concreta con SQLite
- Esta clase SÍ conoce detalles de SQLite: SQL, conexiones, cursores
- Implementa la interfaz AlumnoRepositoryBase
- Puede ser reemplazada por AlumnoRepositoryPostgreSQL sin afectar servicios
- Maneja errores de BD y los convierte a excepciones de dominio
"""

import sqlite3
from typing import List, Optional
from datetime import datetime

from src.infrastructure.repositories.base.alumno_repository_base import AlumnoRepositoryBase
from src.domain.entities.alumno import Alumno
from src.domain.exceptions.domain_exceptions import (
    DNIDuplicadoException,
    AlumnoNoEncontradoException
)


class AlumnoRepositorySQLite(AlumnoRepositoryBase):
    """
    Implementación SQLite del repositorio de Alumno.
    
    Responsabilidades:
    - Ejecutar queries SQL para operaciones CRUD
    - Convertir filas de SQLite a entidades Alumno
    - Manejar errores de BD (constraints, conexión, etc.)
    - Convertir errores de BD a excepciones de dominio
    
    Decisión de diseño: Inyección de conexión
    - Recibimos la conexión por constructor (no la creamos aquí)
    - Esto permite:
      * Reutilizar conexiones
      * Usar transacciones desde fuera del repositorio
      * Facilitar testing con conexiones in-memory
    """
    
    def __init__(self, conexion: sqlite3.Connection):
        """
        Inicializa el repositorio con una conexión SQLite.
        
        Args:
            conexion: Conexión activa a la base de datos SQLite
        """
        self.conexion = conexion
        # Configurar row_factory para acceder a columnas por nombre
        self.conexion.row_factory = sqlite3.Row
    
    def crear(self, alumno: Alumno) -> Alumno:
        """Crea un nuevo alumno en la base de datos"""
        try:
            cursor = self.conexion.cursor()
            
            # Decisión de diseño: Usar parámetros (?) en lugar de f-strings
            # - Previene SQL injection
            # - SQLite maneja el escaping automáticamente
            cursor.execute("""
                INSERT INTO alumno (nombre, apellido, dni, email, cohorte, fecha_creacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                alumno.nombre,
                alumno.apellido,
                alumno.dni,
                alumno.email,
                alumno.cohorte,
                datetime.now()
            ))
            
            self.conexion.commit()
            
            # Asignar el ID generado al alumno
            alumno.id = cursor.lastrowid
            alumno.fecha_creacion = datetime.now()
            
            return alumno
        
        except sqlite3.IntegrityError as e:
            # El constraint UNIQUE del DNI fue violado
            if 'dni' in str(e).lower():
                raise DNIDuplicadoException(f"Ya existe un alumno con DNI {alumno.dni}")
            raise  # Re-lanzar si es otro tipo de error de integridad
    
    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        """Obtiene un alumno por ID"""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM alumno WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_alumno(row)
        return None
    
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """Obtiene un alumno por DNI"""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM alumno WHERE dni = ?", (dni,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_alumno(row)
        return None
    
    def obtener_todos(self, limite: Optional[int] = None, offset: int = 0) -> List[Alumno]:
        """Obtiene todos los alumnos con paginación opcional"""
        cursor = self.conexion.cursor()
        
        query = "SELECT * FROM alumno ORDER BY apellido, nombre"
        
        if limite is not None:
            query += f" LIMIT {limite} OFFSET {offset}"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        return [self._row_to_alumno(row) for row in rows]
    
    def buscar_por_nombre(self, nombre: str) -> List[Alumno]:
        """Busca alumnos por nombre o apellido (búsqueda parcial)"""
        cursor = self.conexion.cursor()
        
        # Decisión de diseño: Búsqueda case-insensitive con LIKE
        # - Permite búsquedas parciales: "juan" encuentra "Juan Pérez"
        # - El % es wildcard de SQL
        patron = f"%{nombre}%"
        
        cursor.execute("""
            SELECT * FROM alumno 
            WHERE nombre LIKE ? OR apellido LIKE ?
            ORDER BY apellido, nombre
        """, (patron, patron))
        
        rows = cursor.fetchall()
        return [self._row_to_alumno(row) for row in rows]
    
    def obtener_por_cohorte(self, cohorte: int) -> List[Alumno]:
        """Obtiene alumnos de una cohorte específica"""
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT * FROM alumno 
            WHERE cohorte = ?
            ORDER BY apellido, nombre
        """, (cohorte,))
        
        rows = cursor.fetchall()
        return [self._row_to_alumno(row) for row in rows]
    
    def actualizar(self, alumno: Alumno) -> Alumno:
        """Actualiza un alumno existente"""
        if alumno.id is None:
            raise ValueError("El alumno debe tener un ID para actualizarlo")
        
        # Verificar que el alumno existe
        existente = self.obtener_por_id(alumno.id)
        if not existente:
            raise AlumnoNoEncontradoException(f"No existe alumno con ID {alumno.id}")
        
        # Verificar que el DNI no esté duplicado (si cambió)
        if alumno.dni != existente.dni:
            duplicado = self.obtener_por_dni(alumno.dni)
            if duplicado and duplicado.id != alumno.id:
                raise DNIDuplicadoException(f"Ya existe otro alumno con DNI {alumno.dni}")
        
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                UPDATE alumno 
                SET nombre = ?, apellido = ?, dni = ?, email = ?, cohorte = ?
                WHERE id = ?
            """, (
                alumno.nombre,
                alumno.apellido,
                alumno.dni,
                alumno.email,
                alumno.cohorte,
                alumno.id
            ))
            
            self.conexion.commit()
            return alumno
        
        except sqlite3.IntegrityError as e:
            if 'dni' in str(e).lower():
                raise DNIDuplicadoException(f"Ya existe un alumno con DNI {alumno.dni}")
            raise
    
    def eliminar(self, id: int) -> bool:
        """Elimina un alumno por ID"""
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM alumno WHERE id = ?", (id,))
        self.conexion.commit()
        
        # rowcount indica cuántas filas fueron afectadas
        return cursor.rowcount > 0
    
    def contar_total(self) -> int:
        """Cuenta el total de alumnos"""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM alumno")
        row = cursor.fetchone()
        return row['total'] if row else 0
    
    def _row_to_alumno(self, row: sqlite3.Row) -> Alumno:
        """
        Convierte una fila de SQLite a una entidad Alumno.
        
        Decisión de diseño: Método privado de conversión
        - Centraliza la lógica de mapeo BD → Entidad
        - Facilita cambios en el schema de BD
        - Maneja conversión de tipos (datetime, etc.)
        
        Args:
            row: Fila de SQLite (con row_factory = sqlite3.Row)
        
        Returns:
            Alumno: Entidad de dominio
        """
        return Alumno(
            id=row['id'],
            nombre=row['nombre'],
            apellido=row['apellido'],
            dni=row['dni'],
            email=row['email'],
            cohorte=row['cohorte'],
            fecha_creacion=datetime.fromisoformat(row['fecha_creacion']) if row['fecha_creacion'] else None
        )
