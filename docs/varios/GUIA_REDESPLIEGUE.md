# 🚀 Guía Rápida - Redesplegar en Vercel

## ✅ Cambios Realizados

Se han corregido los siguientes archivos para que funcionen en Vercel:

1. **`api/index.py`** - Simplificado con mejor manejo de errores
2. **`src/presentation/api/main.py`** - Detecta Vercel y no lanza excepciones
3. **`vercel.json`** - Configuración correcta
4. **`runtime.txt`** - Especifica Python 3.11

## 🎯 Cómo Redesplegar

### Opción 1: Desde Vercel Dashboard (Más Fácil)

1. Ve a https://vercel.com/dashboard
2. Click en tu proyecto
3. Click en "Deployments"
4. Click en los 3 puntos (...) del último despliegue
5. Click en "Redeploy"
6. ✅ ¡Listo!

### Opción 2: Con Git (Si usas GitHub)

```bash
# Asegurarte de que todos los cambios estén guardados
git add .
git commit -m "Fix Vercel deployment - handle errors gracefully"
git push
```

Vercel redesplegar automáticamente.

### Opción 3: Con Vercel CLI

```bash
vercel --prod --force
```

## 🔍 Qué se Arregló

### Problema Anterior:
- La aplicación intentaba inicializar la BD en el startup
- Lanzaba una excepción si fallaba
- Vercel con Mangum (lifespan="off") no maneja bien esto

### Solución Aplicada:
- ✅ El entrypoint (`api/index.py`) ahora tiene manejo de errores
- ✅ El `main.py` detecta si está en Vercel y no lanza excepciones
- ✅ La BD se inicializa bajo demanda (en el primer request)
- ✅ Los errores se muestran en lugar de crashear

## 📊 Qué Esperar Después del Redespliegue

### Si Todo Sale Bien:
- ✅ La página raíz (`/`) mostrará un JSON con info de la API
- ✅ `/docs` mostrará la documentación de Swagger
- ✅ `/health` mostrará el estado de la API

### Si Sigue Fallando:
1. Ve a Vercel Dashboard → Tu Proyecto → Deployments
2. Click en el deployment activo
3. Ve a la pestaña "Logs"
4. Busca mensajes de error
5. Copia el error y podemos solucionarlo

## 🆘 Troubleshooting

### Error: "Module not found"
**Solución**: Verifica que `requirements.txt` esté en la raíz

### Error: "Database locked"
**Solución**: Normal en SQLite serverless, ignorar por ahora

### Error: "Import error"
**Solución**: Verifica que todos los archivos estén commiteados en Git

## ✅ Checklist Pre-Redespliegue

- [x] `api/index.py` corregido
- [x] `src/presentation/api/main.py` corregido
- [x] `vercel.json` configurado
- [x] `requirements.txt` incluye mangum
- [x] `runtime.txt` especifica Python 3.11

## 🎉 Después del Redespliegue Exitoso

Una vez que funcione, podrás:

1. **Acceder a la documentación**:
   - `https://tu-app.vercel.app/docs`

2. **Probar los endpoints**:
   - `GET /` - Info de la API
   - `GET /health` - Estado de salud
   - `POST /alumnos` - Crear alumno
   - `GET /alumnos` - Listar alumnos

3. **Ver los logs**:
   - Vercel Dashboard → Deployments → Logs

## 📝 Nota Importante

Recuerda que **SQLite en Vercel es EFÍMERO**:
- Los datos se borran en cada despliegue
- Ideal para demos y testing
- Para producción: Migrar a PostgreSQL

---

**¡Ahora redespliegua y debería funcionar!** 🚀
