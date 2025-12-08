import sys
import os

# Agregar el directorio raíz del proyecto al path para que Python pueda encontrar 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.presentation.api.main import app
