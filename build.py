"""
Script de Construcción: build.py
Sistema de Seguimiento de Alumnos

Este script lee el template principal (index.template.html) y reemplaza
todas las instrucciones {{ include "archivo.html" }} por el contenido
real de los archivos, generando un index.html final listo para deploy.

Uso:
    python build.py
    
Esto genera/actualiza public/index.html

Arquitectura:
- Separa diseño (componentes) de estructura (template) de construcción (este script)
- Permite escalar a cientos de componentes
- El HTML final se genera automáticamente antes del deploy
"""

import re
from pathlib import Path
import sys

# Ruta base del proyecto (donde está este script)
BASE_DIR = Path(__file__).parent
PUBLIC_DIR = BASE_DIR / "public"

# Archivo template y archivo de salida
TEMPLATE_FILE = PUBLIC_DIR / "index.template.html"
OUTPUT_FILE = PUBLIC_DIR / "index.html"

# Expresión regular para detectar patrones: {{ include "archivo.html" }}
INCLUDE_PATTERN = r'\{\{\s*include\s*"(.+?)"\s*\}\}'


def replace_include(match: re.Match, template_dir: Path) -> str:
    """
    Reemplaza una instrucción {{ include "archivo.html" }} por el contenido real.
    
    Args:
        match: El match de la expresión regular
        template_dir: Directorio base para resolver rutas relativas
        
    Returns:
        El contenido del archivo incluido
        
    Raises:
        FileNotFoundError: Si el componente no existe
    """
    filename = match.group(1)
    component_path = template_dir / filename
    
    if not component_path.exists():
        raise FileNotFoundError(f"❌ Componente no encontrado: {filename}")
    
    content = component_path.read_text(encoding="utf-8")
    
    # Procesar includes anidados (recursivo)
    content = re.sub(
        INCLUDE_PATTERN, 
        lambda m: replace_include(m, component_path.parent), 
        content
    )
    
    return content


def build():
    """
    Función principal de construcción.
    Lee el template, procesa todos los includes y genera el HTML final.
    """
    print("🔧 Iniciando construcción de index.html...")
    
    # Verificar que existe el template
    if not TEMPLATE_FILE.exists():
        print(f"❌ No se encontró el template: {TEMPLATE_FILE}")
        sys.exit(1)
    
    # Leer el template
    print(f"📖 Leyendo template: {TEMPLATE_FILE.name}")
    template_content = TEMPLATE_FILE.read_text(encoding="utf-8")
    
    # Contar includes
    includes = re.findall(INCLUDE_PATTERN, template_content)
    print(f"🧩 Componentes encontrados: {len(includes)}")
    for inc in includes:
        print(f"   ├─ {inc}")
    
    # Reemplazar todos los includes
    try:
        output_html = re.sub(
            INCLUDE_PATTERN, 
            lambda m: replace_include(m, PUBLIC_DIR), 
            template_content
        )
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)
    
    # Guardar el HTML final
    OUTPUT_FILE.write_text(output_html, encoding="utf-8")
    
    # Estadísticas
    lines_count = output_html.count('\n') + 1
    size_kb = len(output_html.encode('utf-8')) / 1024
    
    print(f"\n✅ index.html generado correctamente!")
    print(f"   📄 Líneas: {lines_count}")
    print(f"   📦 Tamaño: {size_kb:.1f} KB")
    print(f"   💾 Guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
