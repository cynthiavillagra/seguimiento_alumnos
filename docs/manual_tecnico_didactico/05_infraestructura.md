# Capítulo 5: Capa de Infraestructura

## 5.1 ¿Qué es la Capa de Infraestructura?

Es donde viven los **detalles técnicos**:

- Conexión a base de datos
- Repositorios (guardar/recuperar datos)
- Acceso a archivos, APIs externas, etc.

### Lo que SÍ sabe

- ✅ SQL
- ✅ PostgreSQL
- ✅ Cómo se guardan los datos

### Lo que NO sabe

- ❌ Lógica de negocio
- ❌ HTTP/REST
- ❌ Reglas de validación

---

## 5.2 Conexión a Base de Datos

Crear `src/infrastructure/database/connection.py`:

```python
"""
Conexión a PostgreSQL
---------------------
Maneja la conexión a la base de datos.
Usa el patrón Singleton para reutilizar conexión.
"""

import os
from urllib.parse import urlparse
import pg8000
import ssl

# Variable global para la conexión (Singleton)
_connection = None


def get_db_connection():
    """
    Obtiene la conexión a PostgreSQL.
    
    Usa Singleton: si ya hay conexión, la reutiliza.
    Si no hay, crea una nueva.
    
    Returns:
        Conexión pg8000 a PostgreSQL
    """
    global _connection
    
    # Si ya hay conexión, verificar que funcione
    if _connection is not None:
        try:
            cursor = _connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return _connection
        except:
            _connection = None  # Conexión rota, crear nueva
    
    # Obtener URL de las variables de entorno
    db_url = os.environ.get("POSTGRES_URL")
    
    if not db_url:
        raise Exception("POSTGRES_URL no está definida")
    
    # Parsear la URL
    # postgresql://usuario:password@host:puerto/database
    parsed = urlparse(db_url)
    
    # Crear contexto SSL (necesario para Neon)
    ssl_context = ssl.create_default_context()
    
    # Conectar
    _connection = pg8000.connect(
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path.lstrip('/'),
        ssl_context=ssl_context
    )
    
    print("✅ Conectado a PostgreSQL")
    
    return _connection


def close_db_connection():
    """Cierra la conexión a la base de datos."""
    global _connection
    if _connection:
        try:
            _connection.close()
            print("👋 Conexión cerrada")
        except:
            pass
        _connection = None


def inicializar_tablas():
    """
    Crea las tablas si no existen.
    Se ejecuta al iniciar la aplicación.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL para crear tablas
    tablas_sql = """
    -- Tabla de alumnos
    CREATE TABLE IF NOT EXISTS alumno (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        dni TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL
    );
    
    -- Tabla de cursos
    CREATE TABLE IF NOT EXISTS curso (
        id SERIAL PRIMARY KEY,
        nombre_materia TEXT NOT NULL,
        anio INTEGER NOT NULL,
        cuatrimestre INTEGER NOT NULL CHECK (cuatrimestre IN (1, 2))
    );
    
    -- Tabla de inscripciones
    CREATE TABLE IF NOT EXISTS inscripcion (
        id SERIAL PRIMARY KEY,
        alumno_id INTEGER REFERENCES alumno(id) ON DELETE CASCADE,
        curso_id INTEGER REFERENCES curso(id) ON DELETE CASCADE,
        fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(alumno_id, curso_id)
    );
    """
    
    try:
        # Ejecutar cada statement por separado
        for statement in tablas_sql.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        conn.commit()
        print("✅ Tablas inicializadas")
        
    except Exception as e:
        conn.rollback()
        print(f"⚠️ Error en tablas: {e}")
    
    finally:
        cursor.close()
```

### ¿Qué es el patrón Singleton?

```python
# Sin Singleton: cada vez crea una conexión nueva
conexion1 = crear_conexion()  # Conexión 1
conexion2 = crear_conexion()  # Conexión 2 (diferente)

# Con Singleton: reutiliza la misma conexión
conexion1 = get_db_connection()  # Conexión 1
conexion2 = get_db_connection()  # La misma conexión 1
```

**Beneficio:** No abrimos múltiples conexiones innecesarias.

---

## 5.3 Repositorio de Alumnos

Crear `src/infrastructure/repositories/alumno_repo.py`:

```python
"""
Repositorio de Alumnos
----------------------
Maneja el acceso a la tabla 'alumno' en PostgreSQL.

Responsabilidades:
- Guardar alumnos
- Buscar alumnos
- Actualizar alumnos
- Eliminar alumnos
"""

from typing import List, Optional

from src.domain.entities import Alumno
from src.infrastructure.database.connection import get_db_connection


class AlumnoRepository:
    """
    Repositorio para operaciones CRUD de alumnos.
    
    Cada método hace UNA cosa y retorna entidades de dominio,
    no tuplas ni diccionarios.
    """
    
    def __init__(self):
        """Obtiene la conexión a la BD"""
        self.conn = get_db_connection()
    
    def _row_to_alumno(self, row: tuple) -> Alumno:
        """
        Convierte una fila de la BD a entidad Alumno.
        
        row = (1, 'Juan', 'Pérez', '12345678', 'juan@mail.com')
        return = Alumno(id=1, nombre='Juan', ...)
        """
        return Alumno(
            id=row[0],
            nombre=row[1],
            apellido=row[2],
            dni=row[3],
            email=row[4]
        )
    
    def guardar(self, alumno: Alumno) -> Alumno:
        """
        Guarda un alumno nuevo en la BD.
        
        Args:
            alumno: Entidad Alumno (sin id)
        
        Returns:
            Alumno con id asignado
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO alumno (nombre, apellido, dni, email)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                alumno.nombre,
                alumno.apellido,
                alumno.dni,
                alumno.email
            ))
            
            # Obtener el ID generado
            row = cursor.fetchone()
            self.conn.commit()
            
            alumno.id = row[0]
            return alumno
            
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def obtener_por_id(self, id: int) -> Optional[Alumno]:
        """
        Busca un alumno por su ID.
        
        Returns:
            Alumno si existe, None si no
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, nombre, apellido, dni, email
                FROM alumno
                WHERE id = %s
            """, (id,))
            
            row = cursor.fetchone()
            self.conn.commit()
            
            if row:
                return self._row_to_alumno(row)
            return None
            
        finally:
            cursor.close()
    
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """Busca alumno por DNI"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, nombre, apellido, dni, email
                FROM alumno
                WHERE dni = %s
            """, (dni,))
            
            row = cursor.fetchone()
            self.conn.commit()
            
            if row:
                return self._row_to_alumno(row)
            return None
            
        finally:
            cursor.close()
    
    def listar(self, limite: int = 100) -> List[Alumno]:
        """Lista todos los alumnos"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, nombre, apellido, dni, email
                FROM alumno
                ORDER BY apellido, nombre
                LIMIT %s
            """, (limite,))
            
            rows = cursor.fetchall()
            self.conn.commit()
            
            return [self._row_to_alumno(row) for row in rows]
            
        finally:
            cursor.close()
    
    def actualizar(self, alumno: Alumno) -> Alumno:
        """Actualiza un alumno existente"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE alumno
                SET nombre = %s, apellido = %s, dni = %s, email = %s
                WHERE id = %s
            """, (
                alumno.nombre,
                alumno.apellido,
                alumno.dni,
                alumno.email,
                alumno.id
            ))
            
            self.conn.commit()
            return alumno
            
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def eliminar(self, id: int) -> bool:
        """
        Elimina un alumno por ID.
        
        Returns:
            True si se eliminó, False si no existía
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("DELETE FROM alumno WHERE id = %s", (id,))
            eliminados = cursor.rowcount
            self.conn.commit()
            
            return eliminados > 0
            
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def contar(self) -> int:
        """Cuenta el total de alumnos"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM alumno")
            row = cursor.fetchone()
            self.conn.commit()
            
            return row[0] if row else 0
            
        finally:
            cursor.close()
```

### ¿Por qué el método `_row_to_alumno`?

```python
# Sin helper: repetición de código
def obtener_por_id(self, id):
    row = cursor.fetchone()
    return Alumno(id=row[0], nombre=row[1], apellido=row[2], ...)

def listar(self):
    rows = cursor.fetchall()
    return [Alumno(id=r[0], nombre=r[1], ...) for r in rows]  # Repetido!

# Con helper: código limpio
def _row_to_alumno(self, row):
    return Alumno(id=row[0], nombre=row[1], apellido=row[2], ...)

def obtener_por_id(self, id):
    row = cursor.fetchone()
    return self._row_to_alumno(row)

def listar(self):
    rows = cursor.fetchall()
    return [self._row_to_alumno(r) for r in rows]  # Reutiliza!
```

---

## 5.4 Repositorio de Cursos

Crear `src/infrastructure/repositories/curso_repo.py`:

```python
"""
Repositorio de Cursos
---------------------
Maneja el acceso a la tabla 'curso' en PostgreSQL.
"""

from typing import List, Optional

from src.domain.entities import Curso
from src.infrastructure.database.connection import get_db_connection


class CursoRepository:
    """Repositorio para operaciones CRUD de cursos."""
    
    def __init__(self):
        self.conn = get_db_connection()
    
    def _row_to_curso(self, row: tuple) -> Curso:
        """Convierte fila a entidad Curso"""
        return Curso(
            id=row[0],
            nombre_materia=row[1],
            anio=row[2],
            cuatrimestre=row[3]
        )
    
    def guardar(self, curso: Curso) -> Curso:
        """Guarda un curso nuevo"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO curso (nombre_materia, anio, cuatrimestre)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (
                curso.nombre_materia,
                curso.anio,
                curso.cuatrimestre
            ))
            
            row = cursor.fetchone()
            self.conn.commit()
            
            curso.id = row[0]
            return curso
            
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def obtener_por_id(self, id: int) -> Optional[Curso]:
        """Busca curso por ID"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, nombre_materia, anio, cuatrimestre
                FROM curso
                WHERE id = %s
            """, (id,))
            
            row = cursor.fetchone()
            self.conn.commit()
            
            if row:
                return self._row_to_curso(row)
            return None
            
        finally:
            cursor.close()
    
    def listar(self, limite: int = 100) -> List[Curso]:
        """Lista todos los cursos"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, nombre_materia, anio, cuatrimestre
                FROM curso
                ORDER BY anio DESC, cuatrimestre DESC, nombre_materia
                LIMIT %s
            """, (limite,))
            
            rows = cursor.fetchall()
            self.conn.commit()
            
            return [self._row_to_curso(row) for row in rows]
            
        finally:
            cursor.close()
    
    def actualizar(self, curso: Curso) -> Curso:
        """Actualiza un curso existente"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE curso
                SET nombre_materia = %s, anio = %s, cuatrimestre = %s
                WHERE id = %s
            """, (
                curso.nombre_materia,
                curso.anio,
                curso.cuatrimestre,
                curso.id
            ))
            
            self.conn.commit()
            return curso
            
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def eliminar(self, id: int) -> bool:
        """Elimina un curso por ID"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("DELETE FROM curso WHERE id = %s", (id,))
            eliminados = cursor.rowcount
            self.conn.commit()
            
            return eliminados > 0
            
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def contar(self) -> int:
        """Cuenta el total de cursos"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM curso")
            row = cursor.fetchone()
            self.conn.commit()
            
            return row[0] if row else 0
            
        finally:
            cursor.close()
```

---

## 5.5 Repositorio de Inscripciones

Crear `src/infrastructure/repositories/inscripcion_repo.py`:

```python
"""
Repositorio de Inscripciones
----------------------------
Maneja la relación N:M entre Alumno y Curso.
"""

from typing import List, Optional
from datetime import datetime

from src.domain.entities import Inscripcion, Alumno
from src.infrastructure.database.connection import get_db_connection


class InscripcionRepository:
    """Repositorio para operaciones de inscripción."""
    
    def __init__(self):
        self.conn = get_db_connection()
    
    def inscribir(self, alumno_id: int, curso_id: int) -> Inscripcion:
        """
        Inscribe un alumno en un curso.
        
        Raises:
            Exception si ya está inscripto (UNIQUE constraint)
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO inscripcion (alumno_id, curso_id)
                VALUES (%s, %s)
                RETURNING id, fecha_inscripcion
            """, (alumno_id, curso_id))
            
            row = cursor.fetchone()
            self.conn.commit()
            
            return Inscripcion(
                id=row[0],
                alumno_id=alumno_id,
                curso_id=curso_id,
                fecha_inscripcion=row[1]
            )
            
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def ya_inscripto(self, alumno_id: int, curso_id: int) -> bool:
        """Verifica si un alumno ya está inscripto en un curso"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 1 FROM inscripcion
                WHERE alumno_id = %s AND curso_id = %s
            """, (alumno_id, curso_id))
            
            row = cursor.fetchone()
            self.conn.commit()
            
            return row is not None
            
        finally:
            cursor.close()
    
    def alumnos_de_curso(self, curso_id: int) -> List[Alumno]:
        """Obtiene los alumnos inscriptos en un curso"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                SELECT a.id, a.nombre, a.apellido, a.dni, a.email
                FROM alumno a
                INNER JOIN inscripcion i ON a.id = i.alumno_id
                WHERE i.curso_id = %s
                ORDER BY a.apellido, a.nombre
            """, (curso_id,))
            
            rows = cursor.fetchall()
            self.conn.commit()
            
            return [
                Alumno(id=r[0], nombre=r[1], apellido=r[2], dni=r[3], email=r[4])
                for r in rows
            ]
            
        finally:
            cursor.close()
    
    def desinscribir(self, alumno_id: int, curso_id: int) -> bool:
        """Elimina la inscripción de un alumno en un curso"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                DELETE FROM inscripcion
                WHERE alumno_id = %s AND curso_id = %s
            """, (alumno_id, curso_id))
            
            eliminados = cursor.rowcount
            self.conn.commit()
            
            return eliminados > 0
            
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
```

---

## 5.6 Actualizar __init__.py

`src/infrastructure/repositories/__init__.py`:

```python
"""Exportar repositorios"""
from .alumno_repo import AlumnoRepository
from .curso_repo import CursoRepository
from .inscripcion_repo import InscripcionRepository
```

`src/infrastructure/database/__init__.py`:

```python
"""Exportar funciones de conexión"""
from .connection import get_db_connection, close_db_connection, inicializar_tablas
```

---

## 5.7 Resumen

### Archivos creados

```
src/infrastructure/
├── database/
│   ├── __init__.py
│   └── connection.py     ✅
└── repositories/
    ├── __init__.py
    ├── alumno_repo.py    ✅
    ├── curso_repo.py     ✅
    └── inscripcion_repo.py ✅
```

### Qué aprendiste

| Concepto | Explicación |
|----------|-------------|
| Singleton | Reutilizar la misma conexión |
| Repository | Clase que maneja acceso a datos |
| CRUD | Create, Read, Update, Delete |
| `_metodo` | Método privado (convención) |
| `RETURNING` | Obtener datos después de INSERT |

### Patrón observado

Todos los repositorios siguen el mismo patrón:

1. Constructor obtiene conexión
2. Método helper `_row_to_entidad`
3. Métodos CRUD: `guardar`, `obtener_por_id`, `listar`, `actualizar`, `eliminar`
4. Manejo de errores con try/except/finally
5. `commit()` si todo OK, `rollback()` si error

---

**Anterior:** [Capítulo 4 - Dominio](./04_dominio.md)

**Siguiente:** [Capítulo 6 - Aplicación](./06_aplicacion.md)
