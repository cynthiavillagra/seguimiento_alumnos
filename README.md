# 🎓 Sistema de Seguimiento de Alumnos

Sistema web para el seguimiento académico de estudiantes, diseñado para facilitar el registro de clases, asistencia, participación, trabajos prácticos y análisis de rendimiento individual.

## 🚀 Características Principales

- ✅ **Dashboard Multi-Clase**: Vista general de todos los cursos con estadísticas en tiempo real (alumnos, clases, asistencia)
- ✅ **Registro Completo de Clase**: Asistencia, participación, TPs, notas y actitud
- ✅ **Ficha Individual de Alumno**: Historial completo con indicadores de rendimiento
- ✅ **Alertas Dinámicas**: Detección automática de alumnos en riesgo (2 ausencias consecutivas, TPs no entregados)
- ✅ **API Optimizada**: Endpoints eficientes que calculan estadísticas en el servidor
- ✅ **Búsqueda y Filtros**: Encuentra rápidamente alumnos y clases
- ✅ **Diseño Responsive**: Funciona en desktop, tablet y móvil


## 🛠️ Tecnologías

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Diseño moderno con gradientes y animaciones
- SPA (Single Page Application)

### Backend
- Python 3.12
- PostgreSQL (Neon Database)
- Vercel Serverless Functions

## 📦 Instalación y Despliegue

### Requisitos Previos
- Cuenta en [Vercel](https://vercel.com)
- Cuenta en [GitHub](https://github.com)
- Node.js instalado (para Vercel CLI)

### Despliegue en Vercel

1. **Fork o Clone el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/seguimiento-alumnos.git
   cd seguimiento-alumnos
   ```

2. **Conectar con Vercel**
   - Ve a [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click en "Import Project"
   - Selecciona tu repositorio
   - Click en "Deploy"

3. **Configurar Base de Datos**
   - En Vercel Dashboard → Storage → Create Database
   - Selecciona "Neon (Postgres)"
   - Conecta la BD a tu proyecto
   - Ejecuta el SQL de inicialización (ver `docs/CREAR_BD_WEB.md`)

4. **Verificar**
   - Abre tu URL de Vercel
   - Deberías ver el dashboard con las clases

## 📚 Documentación

### Documentos Esenciales (Raíz)
- **[README.md](README.md)** - Este archivo
- **[REGISTRO_COMPLETO.md](REGISTRO_COMPLETO.md)** - Guía de uso del registro de clase

### Documentación Completa (docs/)
- **[GUIA_USO_COMPLETA.md](docs/GUIA_USO_COMPLETA.md)** - Manual de usuario completo
- **[CREAR_BD_WEB.md](docs/CREAR_BD_WEB.md)** - Cómo crear la base de datos
- **[IMPLEMENTACION_POSTGRES.md](docs/IMPLEMENTACION_POSTGRES.md)** - Detalles técnicos de PostgreSQL
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Solución de problemas comunes

## 🎯 Uso Rápido

### 1. Registrar una Clase

1. Click en **"Registrar Clase"**
2. Selecciona materia y cohorte
3. Ingresa fecha y tema
4. Click en **"Iniciar Registro"**
5. Para cada alumno, marca:
   - ✅ Asistencia (Presente/Ausente/Tarde)
   - 📊 Participación (Alta/Media/Baja/Nula)
   - 📝 TP Entregado (Sí/No) + Nota
   - 😊 Actitud (Excelente/Buena/Regular/Mala)
   - 💬 Observaciones (opcional)
6. Click en **"Guardar y Finalizar"**

### 2. Ver Ficha de Alumno

1. Click en **"Alumnos"**
2. Busca el alumno
3. Click en su nombre
4. Verás:
   - Historial de clases
   - Indicadores de rendimiento
   - Alertas activas

### 3. Ver Alertas

1. Click en **"Alertas"** (🔔)
2. Verás alumnos con:
   - 2 faltas consecutivas
   - Asistencia < 70%
   - Bajo rendimiento en TPs

## 📊 Estructura del Proyecto

```
seguimiento-alumnos/
├── api/                    # Entry points Vercel
│   └── index.py           # Adaptador Vercel -> FastAPI
├── public/                # Frontend SPA
│   ├── index.html         # HTML principal
│   ├── app.js             # Lógica JavaScript
│   └── styles.css         # Estilos CSS
├── docs/                  # Documentación
│   ├── ARQUITECTURA.md    # Arquitectura detallada
│   └── ...
├── src/                   # Código Fuente Modular
│   ├── domain/            # Entidades y Reglas de Negocio
│   ├── application/       # casos de Uso y Servicios
│   ├── infrastructure/    # Implementación (DB, Repositorios)
│   └── presentation/      # API Routers y Schemas
├── vercel.json            # Configuración de Vercel
├── requirements.txt       # Dependencias Python
└── README.md              # Este archivo
```

## 🔧 Desarrollo Local

### Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar Localmente
```bash
# Opción 1: Servidor Python simple
python -m http.server 8000

# Opción 2: Vercel Dev
vercel dev
```

Abre: http://localhost:8000

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Variables Registradas por Alumno

Por cada clase, se registra:

| Variable | Tipo | Valores |
|----------|------|---------|
| Asistencia | Obligatorio | Presente / Ausente / Tarde |
| Participación | Opcional | Alta / Media / Baja / Nula |
| TP Entregado | Opcional | Sí / No |
| Nota TP | Opcional | 1-10 (con decimales) |
| Actitud | Opcional | Excelente / Buena / Regular / Mala |
| Observaciones | Opcional | Texto libre |

## 🎨 Capturas de Pantalla

### Dashboard
Vista general de todas las clases con estadísticas.

### Registro de Clase
Interfaz para registrar asistencia y variables por alumno.

### Ficha de Alumno
Historial completo con gráficos e indicadores.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Autores

- **Cynthia Villagra** - Desarrollo inicial

## 🙏 Agradecimientos

- Diseño inspirado en plataformas educativas modernas
- Iconos y emojis para mejorar la UX
- Comunidad de Vercel por la documentación

---

**¿Necesitas ayuda?** Lee la [Guía de Uso Completa](docs/GUIA_USO_COMPLETA.md) o consulta [Troubleshooting](docs/TROUBLESHOOTING.md).
