# ✅ Scripts Preparados - Próximos Pasos

## 📦 Lo que he preparado

1. ✅ **Script de migración** (`scripts/migrate_to_postgres.py`)
   - Convierte schema SQLite → PostgreSQL
   - Crea todas las tablas
   - Inserta datos iniciales (8 alumnos, 3 cursos, 2 TPs)

2. ✅ **Requirements actualizados** (`requirements.txt`)
   - psycopg2-binary (driver PostgreSQL)
   - python-dotenv (variables de entorno)

## 🎯 Pasos que DEBES ejecutar ahora

### Paso 1: Instalar Vercel CLI

Abre PowerShell y ejecuta:

```powershell
npm install -g vercel
```

### Paso 2: Login en Vercel

```powershell
vercel login
```

Sigue las instrucciones en el navegador.

### Paso 3: Navegar al Proyecto

```powershell
cd "C:\Users\Cynthia\OneDrive\Escritorio\EDUCACION\00 Pedagogia\app seguimiento de alumnos"
```

### Paso 4: Crear Base de Datos PostgreSQL

```powershell
vercel postgres create
```

Cuando te pregunte:
- **Database name**: `seguimiento-alumnos-db`
- **Region**: Elegir la más cercana (ej: `iad1`)

### Paso 5: Conectar BD al Proyecto

```powershell
# Link el proyecto a Vercel
vercel link

# Descargar variables de entorno
vercel env pull .env.local
```

Esto creará `.env.local` con las credenciales de PostgreSQL.

### Paso 6: Instalar Dependencias Python

```powershell
pip install -r requirements.txt
```

### Paso 7: Ejecutar Migración

```powershell
python scripts/migrate_to_postgres.py
```

Deberías ver:
```
🔄 Conectando a PostgreSQL...
✅ Conexión exitosa
📝 Creando tablas...
✅ Tablas creadas
🌱 Insertando datos iniciales...
✅ Datos insertados

📊 Resumen:
   - Alumnos: 8
   - Cursos: 3

🎉 ¡Migración completada exitosamente!
```

---

## ⏸️ DETENTE AQUÍ

Una vez que hayas ejecutado los pasos 1-7, **avísame** y continuaré con:

- ✅ Actualizar `api/index.py` para usar PostgreSQL
- ✅ Crear endpoints para alertas
- ✅ Implementar detección de 2 faltas consecutivas
- ✅ Redesplegar en Vercel

---

## 🐛 Troubleshooting

### Error: "vercel: command not found"
**Solución**: Reinicia PowerShell después de instalar Vercel CLI

### Error: "No se encontró POSTGRES_URL"
**Solución**: Asegúrate de ejecutar `vercel env pull .env.local`

### Error: "psycopg2 not found"
**Solución**: Ejecuta `pip install -r requirements.txt`

---

## 📋 Checklist

- [ ] Paso 1: Instalar Vercel CLI
- [ ] Paso 2: Login en Vercel
- [ ] Paso 3: Navegar al proyecto
- [ ] Paso 4: Crear BD PostgreSQL
- [ ] Paso 5: Descargar credenciales
- [ ] Paso 6: Instalar dependencias
- [ ] Paso 7: Ejecutar migración

**¿Listo para empezar? Ejecuta el Paso 1 y avísame si tienes algún problema!** 🚀
