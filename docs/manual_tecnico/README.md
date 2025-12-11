# 📚 Manual Técnico - Sistema de Seguimiento de Alumnos

## Índice de Capítulos

Este manual técnico está diseñado para guiar paso a paso en la construcción de un sistema web completo, desde el diseño hasta el deploy.

### Parte I: Fundamentos

| # | Capítulo | Descripción |
|---|----------|-------------|
| 1 | [Introducción](./01_introduccion.md) | Qué es el proyecto, stack tecnológico, objetivos |
| 2 | [Requisitos y Análisis](./02_requisitos.md) | Requisitos funcionales, casos de uso, modelo de datos |
| 3 | [Diseño y Arquitectura](./03_diseno_arquitectura.md) | Arquitectura por capas, patrones de diseño, diseño de API |

### Parte II: Proceso de Desarrollo

| # | Capítulo | Descripción |
|---|----------|-------------|
| 4 | [Pipeline de Desarrollo](./04_pipeline_desarrollo.md) | Fases de desarrollo, cronograma, control de versiones |
| 5 | [Estructura de Carpetas](./05_estructura_carpetas.md) | Organización del proyecto, justificación |
| 6 | [Diagramas UML](./06_uml.md) | Clases, secuencia, casos de uso, componentes |

### Parte III: Implementación

| # | Capítulo | Descripción |
|---|----------|-------------|
| 7 | [Instalación del Entorno](./07_instalacion_entorno.md) | Setup de Python, Git, VS Code, base de datos |
| 8 | [Construcción Paso a Paso](./08_construccion_paso_a_paso.md) | Tutorial de implementación por capas |
| 9 | [Código Base Completo](./09_codigo_base.md) | Código de referencia de entidades, servicios, routers |

### Parte IV: Calidad y Producción

| # | Capítulo | Descripción |
|---|----------|-------------|
| 10 | [Pruebas](./10_pruebas.md) | Tests unitarios, integración, E2E con pytest |
| 11 | [Deploy](./11_deploy.md) | Configuración de Vercel, Neon, CI/CD |
| 12 | [README Final](./12_readme_final.md) | Documentación del proyecto, badges, licencia |

---

## Cómo Usar Este Manual

### Para Aprender (camino recomendado)

1. Leé los capítulos **en orden**
2. No copies código sin entenderlo
3. Probá cada paso antes de continuar
4. Experimentá con modificaciones

### Para Consulta Rápida

- **¿Cómo crear una entidad?** → [Capítulo 8](./08_construccion_paso_a_paso.md)
- **¿Cómo configurar la BD?** → [Capítulo 7](./07_instalacion_entorno.md)
- **¿Cómo hacer deploy?** → [Capítulo 11](./11_deploy.md)
- **¿Cómo escribir tests?** → [Capítulo 10](./10_pruebas.md)

---

## Público Objetivo

Este manual está diseñado para personas que:

- ✅ Completaron un curso de Full Stack Python
- ✅ Conocen programación básica (POO, funciones, variables)
- ✅ Tienen nociones de HTML, CSS, JavaScript
- ✅ Saben SQL básico (SELECT, INSERT, UPDATE)
- ✅ Quieren aprender desarrollo profesional

---

## Convenciones del Manual

### Código

```python
# Esto es código Python
def ejemplo():
    return "Hola"
```

### Comandos de Terminal

```bash
# Esto es un comando de terminal
pip install fastapi
```

### Notas Importantes

> **Nota:** Información adicional relevante

### Advertencias

> ⚠️ **Advertencia:** Algo que puede causar problemas

### Tips

> 💡 **Tip:** Consejo útil

---

## Recursos Adicionales

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Documentación Pydantic](https://docs.pydantic.dev/)
- [Tutorial PostgreSQL](https://www.postgresqltutorial.com/)
- [Vercel Documentation](https://vercel.com/docs)
- [Neon Documentation](https://neon.tech/docs)

---

**Autor:** Sistema de Seguimiento de Alumnos  
**Versión:** 1.0.0  
**Última actualización:** Diciembre 2024
