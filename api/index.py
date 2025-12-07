from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(
    title="Sistema de Seguimiento de Alumnos",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "API de Seguimiento de Alumnos",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    return {"ping": "pong"}

# Para Vercel, el handler debe llamarse exactamente "handler"
handler = Mangum(app, lifespan="off")

# También exportar app por si Vercel lo necesita
__all__ = ["app", "handler"]
