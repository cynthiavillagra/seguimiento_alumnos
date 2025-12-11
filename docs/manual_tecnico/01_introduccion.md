# Capítulo 1: Introducción

## 1.1 ¿Qué es este manual?

Este manual técnico es una guía completa para construir el **Sistema de Seguimiento de Alumnos** desde cero. Está diseñado para que una persona con conocimientos básicos de programación (Python, HTML, CSS, JavaScript) pueda entender cada decisión técnica y reproducir el proyecto paso a paso.

## 1.2 ¿Qué problema resuelve este proyecto?

En las instituciones educativas de nivel superior (tecnicaturas, profesorados), los docentes necesitan:

- **Registrar asistencia** de manera eficiente
- **Hacer seguimiento de participación** en clase
- **Gestionar entregas de trabajos prácticos**
- **Identificar alumnos en riesgo de deserción** antes de que abandonen

Tradicionalmente, esto se hace con planillas Excel o papel, lo cual es propenso a errores y difícil de analizar.

## 1.3 La solución

Desarrollamos una **aplicación web** que permite:

| Funcionalidad | Descripción |
|---------------|-------------|
| Gestión de Cursos | Crear y administrar materias por cuatrimestre |
| Gestión de Alumnos | Base de datos de estudiantes con sus datos |
| Registro de Clases | Crear sesiones de clase con fecha y tema |
| Asistencia | Marcar presente/ausente/tarde por alumno |
| Participación | Registrar nivel de participación en clase |
| Trabajos Prácticos | Gestionar TPs y sus entregas |
| Inscripciones | Vincular alumnos a cursos específicos |

## 1.4 Stack Tecnológico

El proyecto utiliza tecnologías modernas pero accesibles:

### Frontend
- **HTML5** - Estructura de las páginas
- **CSS3** - Estilos visuales (sin frameworks)
- **JavaScript (Vanilla)** - Lógica del cliente, sin frameworks complejos

### Backend
- **Python 3.11+** - Lenguaje principal
- **FastAPI** - Framework web moderno y rápido
- **Pydantic** - Validación de datos
- **pg8000** - Driver de PostgreSQL (puro Python)

### Base de Datos
- **PostgreSQL** - Base de datos relacional robusta
- **Neon** - PostgreSQL serverless en la nube

### Infraestructura
- **Vercel** - Hosting serverless para frontend y backend
- **Git/GitHub** - Control de versiones

## 1.5 ¿Por qué estas tecnologías?

### ¿Por qué FastAPI y no Flask o Django?

| Aspecto | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Velocidad | Muy rápido (async) | Medio | Medio |
| Documentación automática | ✅ Swagger incluido | ❌ Requiere extensión | ❌ Requiere extensión |
| Validación de datos | ✅ Con Pydantic | ❌ Manual | Parcial |
| Curva de aprendizaje | Media | Baja | Alta |
| Ideal para APIs | ✅ Diseñado para esto | Adaptable | Overkill |

**Decisión**: FastAPI es perfecto para APIs modernas porque incluye documentación automática y validación de datos integrada.

### ¿Por qué JavaScript Vanilla y no React/Vue?

Para un proyecto de esta escala, usar un framework como React agregaría complejidad innecesaria:

- **Curva de aprendizaje** adicional
- **Build process** complicado
- **Dependencias** que mantener actualizadas

Con JavaScript vanilla logramos todo lo necesario de forma más simple y educativa.

### ¿Por qué PostgreSQL y no SQLite?

SQLite es excelente para proyectos locales, pero tiene limitaciones:

- No funciona bien en entornos serverless (Vercel)
- No escala para múltiples usuarios simultáneos
- No tiene las funciones avanzadas de PostgreSQL

**Neon** nos da PostgreSQL gratuito en la nube con un tier generoso.

## 1.6 Arquitectura General

El proyecto sigue una **arquitectura por capas** (Layered Architecture):

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (public/)                      │
│              HTML + CSS + JavaScript                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/JSON
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE PRESENTACIÓN                        │
│            FastAPI Routers + Schemas                        │
│                  (src/presentation/)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE APLICACIÓN                          │
│              Servicios de Negocio                           │
│                  (src/application/)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE DOMINIO                           │
│            Entidades + Excepciones                          │
│                    (src/domain/)                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               CAPA DE INFRAESTRUCTURA                       │
│         Repositorios + Conexión BD                          │
│                (src/infrastructure/)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS                            │
│                     PostgreSQL                              │
└─────────────────────────────────────────────────────────────┘
```

### ¿Por qué esta arquitectura?

1. **Separación de responsabilidades**: Cada capa tiene una función específica
2. **Testeable**: Podemos probar cada capa por separado
3. **Mantenible**: Cambios en una capa no afectan a las demás
4. **Escalable**: Fácil agregar nuevas funcionalidades

## 1.7 Objetivos de aprendizaje

Al completar este manual, habrás aprendido:

- ✅ Diseñar una aplicación web completa
- ✅ Implementar una API REST con FastAPI
- ✅ Estructurar un proyecto con arquitectura por capas
- ✅ Conectar con base de datos PostgreSQL
- ✅ Crear un frontend funcional sin frameworks
- ✅ Desplegar en la nube (Vercel + Neon)
- ✅ Documentar código profesionalmente

## 1.8 Requisitos previos

Antes de comenzar, asegurate de tener:

### Conocimientos
- Programación básica en Python
- Conceptos de POO (clases, objetos, herencia)
- HTML y CSS básico
- JavaScript básico (funciones, eventos, fetch)
- SQL básico (SELECT, INSERT, UPDATE, DELETE)

### Software
- Python 3.11 o superior
- Node.js (para algunas herramientas)
- Git
- Editor de código (VS Code recomendado)
- Cuenta de GitHub
- Cuenta de Vercel (gratuita)
- Cuenta de Neon (gratuita)

## 1.9 Cómo usar este manual

1. **Leé cada capítulo en orden** - Están diseñados para construir conocimiento gradualmente
2. **No copies sin entender** - Cada línea de código tiene una explicación
3. **Experimentá** - Modificá el código para ver qué pasa
4. **Preguntá** - Si algo no queda claro, investigá o preguntá

---

**Siguiente capítulo**: [Requisitos y Análisis](./02_requisitos.md)
