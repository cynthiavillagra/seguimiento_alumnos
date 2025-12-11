# 📚 Manual Técnico Didáctico
## Sistema de Gestión de Alumnos y Cursos - MVP

---

## Índice

| # | Capítulo | Qué aprenderás |
|---|----------|----------------|
| 1 | [Introducción](./01_introduccion.md) | Qué vamos a construir y por qué |
| 2 | [Diseño](./02_diseno.md) | Arquitectura y patrones de diseño |
| 3 | [Setup](./03_setup.md) | Instalar todo lo necesario |
| 4 | [Dominio](./04_dominio.md) | Crear entidades y excepciones |
| 5 | [Infraestructura](./05_infraestructura.md) | Repositorios y base de datos |
| 6 | [Aplicación](./06_aplicacion.md) | Servicios de negocio |
| 7 | [Presentación](./07_presentacion.md) | API REST con FastAPI |
| 8 | [Frontend](./08_frontend.md) | Interfaz web simple |
| 9 | [Testing](./09_testing.md) | Pruebas automatizadas |
| 10 | [Deploy](./10_deploy.md) | Publicar en la nube |

---

## ¿Qué es este manual?

Este es un **manual simplificado** diseñado para aprender desarrollo web profesional construyendo un proyecto real mínimo pero completo.

### El MVP que construiremos

```
┌─────────────────────────────────────────────────────┐
│        Sistema de Gestión de Alumnos y Cursos       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ✅ Gestión de ALUMNOS (nombre, dni, email)         │
│  ✅ Gestión de CURSOS (materia, año, cuatrimestre)  │
│  ✅ INSCRIPCIONES (vincular alumnos a cursos)       │
│                                                     │
│  Solo 3 entidades, pero arquitectura profesional   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### ¿Por qué solo 2+1 entidades?

| Cantidad | Problema |
|----------|----------|
| 1 entidad | No muestra relaciones |
| 2 entidades | Muestra CRUD pero no relaciones N:M |
| **2 + 1 relación** | **Perfecto: CRUD + relaciones + patrones** |
| 5+ entidades | Demasiado para un tutorial |

Con **Alumno + Curso + Inscripción** aprendés:
1. CRUD completo
2. Relaciones muchos-a-muchos
3. Arquitectura por capas
4. Todos los patrones de diseño
5. Testing
6. Deploy

---

## Qué aprenderás

### Conceptos de Diseño
- ✅ Arquitectura por capas
- ✅ Patrón Repository
- ✅ Inyección de dependencias
- ✅ DTOs (Data Transfer Objects)
- ✅ Separación de responsabilidades

### Tecnologías
- ✅ Python 3.11+
- ✅ FastAPI
- ✅ PostgreSQL
- ✅ HTML/CSS/JavaScript
- ✅ Pytest

### Prácticas Profesionales
- ✅ Control de versiones (Git)
- ✅ Testing automatizado
- ✅ Deploy a producción
- ✅ Documentación

---

## Tiempo estimado

| Capítulo | Tiempo |
|----------|--------|
| Setup | 30 min |
| Dominio | 1 hora |
| Infraestructura | 1.5 horas |
| Aplicación | 1 hora |
| Presentación | 1.5 horas |
| Frontend | 2 horas |
| Testing | 1 hora |
| Deploy | 30 min |
| **Total** | **~9 horas** |

---

## Prerrequisitos

Necesitás saber:
- Programación básica en Python (variables, funciones, clases)
- HTML y CSS básico
- JavaScript básico (variables, funciones, eventos)
- SQL básico (SELECT, INSERT, UPDATE, DELETE)

No necesitás saber:
- FastAPI (lo aprendés acá)
- Arquitectura de software (lo aprendés acá)
- Testing (lo aprendés acá)
- Deploy (lo aprendés acá)

---

**Empezar:** [Capítulo 1 - Introducción](./01_introduccion.md)
