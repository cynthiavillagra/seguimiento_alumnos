# 🐛 Troubleshooting: Function Crashed

## Problema Actual

La función de Python en Vercel está crasheando con:
```
FUNCTION_INVOCATION_FAILED
This Serverless Function has crashed
```

## Causas Más Comunes

### 1. Falta `psycopg2-binary` en requirements.txt
**Solución**: Ya lo agregamos, pero Vercel puede no haberlo instalado.

### 2. Variables de entorno no configuradas
**Solución**: Neon debería haber configurado `DATABASE_URL` automáticamente.

### 3. Error de sintaxis en el código Python
**Solución**: Simplificamos la API para diagnóstico.

### 4. Problema con el handler de Vercel
**Solución**: El formato del handler puede estar incorrecto.

## 🔍 Necesito Ver los Logs

Para diagnosticar correctamente, necesito que me envíes:

1. **Build Logs** (cuando Vercel construye el proyecto)
2. **Runtime Logs** (cuando intentas acceder a `/health`)

### Cómo obtener los logs:

1. Ve a: https://vercel.com/dashboard
2. Click en **seguimiento-alumnos**
3. Click en **Deployments**
4. Click en el deployment más reciente
5. **Captura de pantalla de "Build Logs"**
6. Scroll a **Functions** → **`/api/index.py`**
7. **Captura de pantalla de los logs de runtime**

## 🚨 Solución Temporal: Volver a Datos Estáticos

Si necesitas que el sistema funcione YA mientras diagnosticamos, puedo:

1. Revertir la API a usar datos estáticos (sin PostgreSQL)
2. El frontend funcionará normalmente
3. Luego arreglamos PostgreSQL con calma

¿Quieres que haga esto?

## 🔧 Posibles Soluciones (Sin Ver Logs)

### Solución 1: Verificar que psycopg2 se instaló

En el dashboard de Vercel:
1. Deployments → Último deploy
2. Build Logs
3. Buscar: "Installing required dependencies"
4. ¿Dice "psycopg2-binary"?

### Solución 2: Verificar variables de entorno

1. Settings → Environment Variables
2. ¿Ves `DATABASE_URL`?
3. Si NO está, necesitamos reconectar Neon

### Solución 3: Reconectar Neon

1. Storage → seguimiento-alumnos-db
2. Settings → Connected Projects
3. ¿Está conectado a tu proyecto?
4. Si NO, click "Connect Project"

## 📊 Información que Necesito

Por favor envíame:

1. ✅ Captura de Build Logs
2. ✅ Captura de Runtime Logs (al acceder a /health)
3. ✅ Captura de Environment Variables (Settings)
4. ✅ Captura de Storage → Connected Projects

Con esta información podré identificar exactamente el problema.

## ⏰ Tiempo Estimado de Solución

- Con logs: 5-10 minutos
- Sin logs: Imposible diagnosticar correctamente

---

**Por favor, envíame las capturas de los logs para poder ayudarte.** 🙏
