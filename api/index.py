"""
Entrypoint Ultra-Simple para Vercel
"""

from fastapi import FastAPI
from mangum import Mangum

# Crear app directamente aquí
app = FastAPI(
    title="Sistema de Seguimiento de Alumnos",
    version="1.0.0"
)

@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "status": "✅ API funcionando",
        "message": "Sistema de Seguimiento de Alumnos",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    """Health check"""
    return {
        "status": "healthy",
        "api": "running"
    }

@app.get("/ping")
def ping():
    """Ping simple"""
    return {"ping": "pong"}

# Handler para Vercel
handler = Mangum(app, lifespan="off")
