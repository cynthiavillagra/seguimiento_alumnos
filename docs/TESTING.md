# 🧪 Guía de Testing

Documentación completa para ejecutar tests en el Sistema de Seguimiento de Alumnos.

---

## 📁 Estructura de Tests

```
tests/
├── test_api.py              ← Tests de backend (Python)
├── test_frontend.test.js    ← Tests de frontend (JavaScript)
└── __init__.py              ← Archivo vacío para Python
```

---

## 🐍 Tests de Backend (Python)

### Instalación de Dependencias

```powershell
# Instalar pytest y dependencias
pip install pytest pytest-cov pytest-mock

# O agregar a requirements.txt
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
```

### Ejecutar Tests

```powershell
# Ejecutar todos los tests
pytest

# Ejecutar con verbose
pytest -v

# Ejecutar solo tests de API
pytest tests/test_api.py

# Ejecutar con cobertura
pytest --cov=api --cov-report=html

# Ejecutar tests específicos
pytest tests/test_api.py::test_health_endpoint
```

### Tests Disponibles

#### ✅ Tests de Endpoints GET
- `test_health_endpoint()` - Verifica /health
- `test_get_cursos()` - Verifica /cursos
- `test_get_alumnos()` - Verifica /alumnos
- `test_get_alertas()` - Verifica /alertas

#### ✅ Tests de Endpoints POST
- `test_post_alumno_valido()` - Crear alumno válido
- `test_post_alumno_sin_nombre()` - Validación de campos
- `test_post_curso_valido()` - Crear curso válido
- `test_post_tp_valido()` - Crear TP válido

#### ✅ Tests de Validación
- `test_validar_email()` - Validación de emails
- `test_validar_dni()` - Validación de DNI
- `test_validar_cohorte()` - Validación de cohorte

#### ✅ Tests de Integración
- `test_flujo_crear_curso_y_tp()` - Flujo completo
- `test_flujo_crear_alumno_e_inscribir()` - Flujo de inscripción

#### ✅ Tests de Seguridad
- `test_sql_injection_prevention()` - Prevención de SQL injection
- `test_cors_headers()` - Verificación de CORS

---

## 🌐 Tests de Frontend (JavaScript)

### Instalación de Dependencias

```powershell
# Instalar Jest y dependencias
npm install --save-dev jest @testing-library/dom @testing-library/jest-dom

# O con yarn
yarn add --dev jest @testing-library/dom @testing-library/jest-dom
```

### Configurar package.json

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "testEnvironment": "jsdom",
    "testMatch": ["**/tests/**/*.test.js"]
  }
}
```

### Ejecutar Tests

```powershell
# Ejecutar todos los tests
npm test

# Ejecutar en modo watch
npm run test:watch

# Ejecutar con cobertura
npm run test:coverage
```

### Tests Disponibles

#### ✅ Tests de Utilidad
- Validación de email
- Formateo de fechas
- Funciones helper

#### ✅ Tests de Estado
- Estructura del estado global
- Gestión de registros
- Navegación entre páginas

#### ✅ Tests de Formularios
- Validación de crear alumno
- Validación de crear curso
- Validación de crear TP

#### ✅ Tests de Registro
- Marcar asistencia
- Marcar participación
- Marcar actitud
- Validación de notas

#### ✅ Tests de API Calls
- Configuración de fetch
- Headers correctos
- Manejo de errores

---

## 📊 Cobertura de Código

### Generar Reporte de Cobertura

```powershell
# Python (pytest)
pytest --cov=api --cov-report=html
# Ver reporte en: htmlcov/index.html

# JavaScript (Jest)
npm run test:coverage
# Ver reporte en: coverage/lcov-report/index.html
```

### Objetivos de Cobertura

- **Mínimo aceptable:** 70%
- **Objetivo:** 80%
- **Ideal:** 90%+

---

## 🎯 Tests por Categoría

### Tests Unitarios
Prueban funciones individuales aisladas.

```python
# Ejemplo
def test_validar_email():
    assert validar_email("test@example.com") == True
```

### Tests de Integración
Prueban múltiples componentes juntos.

```python
# Ejemplo
def test_flujo_crear_curso_y_tp():
    curso_id = crear_curso(...)
    tp_id = crear_tp(curso_id, ...)
    assert tp_id > 0
```

### Tests End-to-End
Prueban flujos completos de usuario.

```javascript
// Ejemplo
test('flujo completo de registro de clase', () => {
    // 1. Seleccionar curso
    // 2. Iniciar registro
    // 3. Marcar asistencias
    // 4. Guardar clase
});
```

---

## 🔍 Debugging de Tests

### Ver Output Detallado

```powershell
# Python
pytest -vv --tb=long

# JavaScript
npm test -- --verbose
```

### Ejecutar Solo Tests que Fallan

```powershell
# Python
pytest --lf  # last failed

# JavaScript
npm test -- --onlyFailures
```

### Modo Debug

```powershell
# Python
pytest --pdb  # Abre debugger en fallo

# JavaScript
node --inspect-brk node_modules/.bin/jest --runInBand
```

---

## ✅ Checklist de Testing

Antes de hacer commit:

- [ ] Todos los tests pasan
- [ ] Cobertura > 70%
- [ ] No hay warnings
- [ ] Tests de nuevas funcionalidades agregados
- [ ] Tests de edge cases incluidos

---

## 📝 Escribir Buenos Tests

### Principios FIRST

- **F**ast - Rápidos de ejecutar
- **I**ndependent - Independientes entre sí
- **R**epeatable - Resultados consistentes
- **S**elf-validating - Pasan o fallan claramente
- **T**imely - Escritos junto con el código

### Patrón AAA

```python
def test_ejemplo():
    # Arrange (Preparar)
    alumno = crear_alumno_test()
    
    # Act (Actuar)
    resultado = validar_alumno(alumno)
    
    # Assert (Verificar)
    assert resultado == True
```

### Nombres Descriptivos

```python
# ❌ Mal
def test_1():
    ...

# ✅ Bien
def test_crear_alumno_con_email_invalido_debe_fallar():
    ...
```

---

## 🚀 CI/CD con Tests

### GitHub Actions (Ejemplo)

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov
```

---

## 📚 Recursos

### Documentación
- [Pytest](https://docs.pytest.org/)
- [Jest](https://jestjs.io/)
- [Testing Library](https://testing-library.com/)

### Tutoriales
- [Python Testing Tutorial](https://realpython.com/pytest-python-testing/)
- [JavaScript Testing Best Practices](https://testingjavascript.com/)

---

## 🐛 Problemas Comunes

### "Module not found"
```powershell
# Solución: Instalar dependencias
pip install -r requirements.txt
npm install
```

### "No tests collected"
```powershell
# Solución: Verificar nombres de archivos
# Deben empezar con test_
```

### "Import error"
```powershell
# Solución: Agregar __init__.py en carpeta tests
touch tests/__init__.py
```

---

## 📞 Ayuda

Si tienes problemas con los tests:

1. Verifica que las dependencias estén instaladas
2. Revisa los logs de error completos
3. Consulta la documentación de pytest/jest
4. Verifica que los paths sean correctos

---

**¡Happy Testing!** 🧪✨
