# 🚀 Testing en Vercel - Guía Rápida

## ❓ ¿Dónde se Ejecutan los Tests?

**IMPORTANTE:** Los tests **NO se ejecutan en Vercel**. Vercel solo despliega la aplicación.

Los tests se ejecutan:
1. ✅ **Localmente** en tu computadora (antes de hacer push)
2. ✅ **En GitHub Actions** (automáticamente al hacer push)

---

## 💻 Opción 1: Ejecutar Tests Localmente

### Paso a Paso

#### 1. Instalar Dependencias (solo la primera vez)

```powershell
# Instalar pytest
pip install pytest pytest-cov pytest-mock
```

#### 2. Ejecutar Tests

```powershell
# Ejecutar todos los tests
pytest

# Con más detalle
pytest -v

# Con cobertura
pytest --cov=api
```

#### 3. Verificar Resultados

```
✅ Si todos pasan → Hacer push
❌ Si alguno falla → Arreglar y volver a probar
```

#### 4. Hacer Push a Vercel

```powershell
git add .
git commit -m "Update with tests passing"
git push
```

---

## 🤖 Opción 2: GitHub Actions (Automático)

### ¿Qué es?

GitHub Actions ejecuta los tests **automáticamente** cada vez que haces `git push`.

### Configuración (Ya está lista)

He creado el archivo `.github/workflows/tests.yml` que:
- ✅ Ejecuta tests de Python
- ✅ Ejecuta tests de JavaScript (si están configurados)
- ✅ Muestra resultados en GitHub
- ✅ Bloquea merge si los tests fallan

### Cómo Ver los Resultados

1. Haz push a GitHub:
   ```powershell
   git push
   ```

2. Ve a tu repositorio en GitHub

3. Click en la pestaña **"Actions"**

4. Verás el workflow ejecutándose:
   - 🟡 Amarillo = Ejecutando
   - ✅ Verde = Todos pasaron
   - ❌ Rojo = Alguno falló

### Ejemplo de Output

```
✅ Backend Tests (Python)
   ├─ test_health_endpoint ✓
   ├─ test_get_cursos ✓
   ├─ test_post_alumno_valido ✓
   └─ ... (20+ tests) ✓

✅ All tests passed! Ready to deploy to Vercel
```

---

## 🔄 Flujo de Trabajo Recomendado

### Antes de Cada Push

```powershell
# 1. Hacer cambios en el código
# 2. Ejecutar tests localmente
pytest -v

# 3. Si pasan, hacer commit y push
git add .
git commit -m "feat: Add new feature"
git push

# 4. GitHub Actions ejecuta tests automáticamente
# 5. Vercel despliega si todo está OK
```

---

## 📊 ¿Qué Pasa en Vercel?

### Build Process en Vercel

```
1. GitHub → Push
2. GitHub Actions → Ejecuta tests ✅
3. Vercel → Detecta push
4. Vercel → Build (instala dependencias)
5. Vercel → Deploy (publica la app)
```

### Lo que Vercel NO hace:
- ❌ No ejecuta pytest
- ❌ No ejecuta jest
- ❌ No corre tests

### Lo que Vercel SÍ hace:
- ✅ Instala `requirements.txt`
- ✅ Construye la aplicación
- ✅ Despliega a producción

---

## ⚙️ Configuración de Vercel

### Ignorar Archivos de Test

Ya está configurado en `.vercelignore`:
```
tests/
pytest.ini
*.test.js
__pycache__/
```

Esto evita que los archivos de test se suban a Vercel (no son necesarios en producción).

---

## 🎯 Resumen

| Herramienta | Propósito | Cuándo se ejecuta |
|-------------|-----------|-------------------|
| **pytest** | Tests de backend | Localmente o en GitHub Actions |
| **jest** | Tests de frontend | Localmente o en GitHub Actions |
| **GitHub Actions** | CI/CD automático | Al hacer push a GitHub |
| **Vercel** | Despliegue | Al hacer push (después de tests) |

---

## 📝 Comandos Rápidos

### Ejecutar Tests Localmente

```powershell
# Backend (Python)
pytest -v

# Con cobertura
pytest --cov=api --cov-report=html

# Ver reporte
start htmlcov/index.html
```

### Ver Tests en GitHub

1. Ve a: https://github.com/tu-usuario/tu-repo
2. Click en **"Actions"**
3. Ve los resultados

### Desplegar a Vercel

```powershell
# Simplemente hacer push
git push

# Vercel despliega automáticamente
```

---

## 🐛 Problemas Comunes

### "pytest: command not found"

```powershell
# Solución: Instalar pytest
pip install pytest
```

### "Tests fallan en GitHub pero pasan localmente"

```powershell
# Solución: Verificar dependencias
# Asegúrate que requirements.txt esté actualizado
pip freeze > requirements.txt
```

### "Vercel falla al desplegar"

```powershell
# Solución: Ver logs en Vercel Dashboard
# Deployments → Click en el deploy → Ver logs
```

---

## ✅ Checklist

Antes de cada push:

- [ ] Código funciona localmente
- [ ] Tests pasan localmente (`pytest -v`)
- [ ] Commit con mensaje descriptivo
- [ ] Push a GitHub
- [ ] Verificar GitHub Actions (opcional)
- [ ] Verificar deploy en Vercel

---

## 🎓 Aprende Más

- **Tests locales:** `docs/TESTING.md`
- **GitHub Actions:** `.github/workflows/tests.yml`
- **Vercel:** https://vercel.com/docs

---

**¡Los tests son para desarrollo local y CI/CD, no para Vercel!** 🧪✨
