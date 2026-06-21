from fastapi import FastAPI
from database import engine
from models import Base
from routers import companies_ai

app = FastAPI(
    title="Productivity AI API",
    description="API para predicción de ganancia de productividad en manufactura",
    version="1.0.0"
)

app.include_router(companies_ai.router)

@app.get("/")
def index():
    return {
        "title": "PRODUCTIVITY AI API VERSION 1.0",
        "message": "Bienvenido a la API de productividad"
    }
    
#Base.metadata.create_all(engine)