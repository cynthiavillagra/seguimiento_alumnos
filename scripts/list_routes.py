
import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.presentation.api.main import app

print("--- Rutas Registradas en FastAPI ---")
for route in app.routes:
    methods = ", ".join(route.methods) if hasattr(route, "methods") else "None"
    print(f"{methods:20} {route.path}")
