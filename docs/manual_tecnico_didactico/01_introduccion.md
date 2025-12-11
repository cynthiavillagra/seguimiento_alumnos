# Capítulo 1: Introducción

## ¿Qué vamos a construir?

Un sistema web simple pero profesional para gestionar **alumnos** y **cursos**.

```
┌──────────────────────────────────────────────────────────────┐
│                    NUESTRO MVP                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ALUMNO ◄─────────────────────────────────► CURSO           │
│   • id                   INSCRIPCIÓN          • id           │
│   • nombre               (les conecta)        • materia      │
│   • dni                                       • año          │
│   • email                                     • cuatrimestre │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Funcionalidades

| Recurso | Operaciones |
|---------|-------------|
| **Alumnos** | Crear, Listar, Ver, Editar, Eliminar |
| **Cursos** | Crear, Listar, Ver, Editar, Eliminar |
| **Inscripciones** | Inscribir alumno a curso, Listar |

---

## ¿Por qué este proyecto?

### Es lo suficientemente simple para aprender

- Solo 2 entidades principales + 1 relación
- No abruma con complejidad
- Se puede hacer en un fin de semana

### Es lo suficientemente completo para ser útil

- Tiene CRUD completo
- Tiene relaciones entre entidades
- Usa arquitectura real
- Se despliega en producción

---

## Stack Tecnológico

### Backend

| Tecnología | Para qué |
|------------|----------|
| **Python 3.11+** | Lenguaje de programación |
| **FastAPI** | Framework web (crear API) |
| **Pydantic** | Validar datos |
| **pg8000** | Conectar con PostgreSQL |

### Frontend

| Tecnología | Para qué |
|------------|----------|
| **HTML5** | Estructura de la página |
| **CSS3** | Estilos visuales |
| **JavaScript** | Lógica e interactividad |

### Base de Datos

| Tecnología | Para qué |
|------------|----------|
| **PostgreSQL** | Base de datos relacional |
| **Neon** | PostgreSQL gratis en la nube |

### Deploy

| Tecnología | Para qué |
|------------|----------|
| **Vercel** | Hosting gratuito |
| **Git/GitHub** | Control de versiones |

---

## ¿Por qué FastAPI?

```python
# Con Flask (tradicional)
@app.route("/alumnos", methods=["POST"])
def crear_alumno():
    data = request.json
    # Validar manualmente cada campo...
    if not data.get("nombre"):
        return {"error": "Falta nombre"}, 400
    # ... más código

# Con FastAPI (moderno)
@app.post("/alumnos")
def crear_alumno(alumno: AlumnoSchema):  # ¡Valida automáticamente!
    return crear(alumno)
```

**Ventajas de FastAPI:**
- ✅ Validación automática de datos
- ✅ Documentación automática (Swagger)
- ✅ Muy rápido
- ✅ Fácil de aprender

---

## ¿Por qué arquitectura por capas?

### Sin arquitectura (todo mezclado)

```python
# ❌ MAL: Todo en un archivo, todo mezclado
@app.post("/alumnos")
def crear_alumno(data: dict):
    # Validar
    if not data["nombre"]:
        raise Error("Falta nombre")
    
    # Conectar BD
    conn = psycopg2.connect(...)
    
    # SQL
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alumno VALUES (%s)", ...)
    
    # Devolver
    return {"ok": True}
```

**Problemas:**
- Difícil de testear
- Difícil de mantener
- Si cambiás la BD, tenés que tocar todo
- Código repetido

### Con arquitectura por capas (separado)

```python
# ✅ BIEN: Cada cosa en su lugar

# Capa de Presentación (solo recibe/devuelve HTTP)
@router.post("/alumnos")
def crear_alumno(data: AlumnoSchema):
    return service.crear(data)

# Capa de Aplicación (lógica de negocio)
class AlumnoService:
    def crear(self, datos):
        alumno = Alumno(**datos)
        return self.repo.guardar(alumno)

# Capa de Dominio (reglas de negocio)
class Alumno:
    def __init__(self, nombre, dni):
        if not nombre:
            raise ValueError("Falta nombre")

# Capa de Infraestructura (acceso a BD)
class AlumnoRepository:
    def guardar(self, alumno):
        cursor.execute("INSERT INTO alumno...")
```

**Beneficios:**
- ✅ Fácil de testear cada parte
- ✅ Fácil de mantener
- ✅ Si cambiás la BD, solo tocás el repositorio
- ✅ Código reutilizable

---

## El diagrama completo

```
┌─────────────────────────────────────────────────────────────┐
│                        NAVEGADOR                            │
│                     (HTML + JS + CSS)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/JSON
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE PRESENTACIÓN                        │
│                   (FastAPI Routers)                         │
│                                                             │
│  • Recibe requests HTTP                                     │
│  • Valida formato de datos (Pydantic)                       │
│  • Devuelve responses HTTP                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE APLICACIÓN                          │
│                     (Servicios)                             │
│                                                             │
│  • Contiene la lógica de negocio                            │
│  • Orquesta operaciones                                     │
│  • Lanza excepciones de negocio                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE DOMINIO                           │
│              (Entidades + Excepciones)                      │
│                                                             │
│  • Define qué es un Alumno, un Curso                        │
│  • Reglas de validación                                     │
│  • No sabe de BD ni HTTP                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               CAPA DE INFRAESTRUCTURA                       │
│                   (Repositorios)                            │
│                                                             │
│  • Guarda y recupera datos                                  │
│  • Sabe de SQL y PostgreSQL                                 │
│  • Implementa interfaces                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      BASE DE DATOS                          │
│                       PostgreSQL                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Resultado Final

Al terminar tendrás:

1. **Una API REST** que funciona
   - `GET /api/alumnos/` - Listar alumnos
   - `POST /api/alumnos/` - Crear alumno
   - `GET /api/cursos/` - Listar cursos
   - `POST /api/inscripciones/` - Inscribir alumno

2. **Un frontend web** simple pero funcional

3. **Tests automatizados** que verifican que todo ande

4. **Deploy en producción** accesible desde internet

---

## Estructura del proyecto que crearemos

```
mi_proyecto/
│
├── src/                          # Backend
│   ├── domain/                   # Capa de Dominio
│   │   ├── entities/
│   │   │   ├── alumno.py        # Entidad Alumno
│   │   │   └── curso.py         # Entidad Curso
│   │   └── exceptions/
│   │       └── exceptions.py    # Excepciones de negocio
│   │
│   ├── application/              # Capa de Aplicación
│   │   └── services/
│   │       ├── alumno_service.py
│   │       └── curso_service.py
│   │
│   ├── infrastructure/           # Capa de Infraestructura
│   │   ├── database/
│   │   │   └── connection.py
│   │   └── repositories/
│   │       ├── alumno_repo.py
│   │       └── curso_repo.py
│   │
│   └── presentation/             # Capa de Presentación
│       └── api/
│           ├── main.py          # App FastAPI
│           ├── routers/
│           │   ├── alumnos.py
│           │   └── cursos.py
│           └── schemas/
│               ├── alumno.py
│               └── curso.py
│
├── public/                       # Frontend
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── tests/                        # Tests
│   ├── test_alumno.py
│   └── test_curso.py
│
├── requirements.txt              # Dependencias
├── .env                          # Variables (no commitear)
└── README.md
```

---

**Siguiente:** [Capítulo 2 - Diseño](./02_diseno.md)
