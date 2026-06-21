from pydantic import BaseModel, Field

# Entrada: lo que envías para crear/predicción
class CompanyCreate(BaseModel):
    country: float = Field(..., example=2.0)
    year: int = Field(..., example=2025)
    ai_adoption_level: float = Field(..., example=3.0)
    ai_investment_usd: int = Field(..., example=500000)
    automation_rate: float = Field(..., example=0.75)
    cost_savings: int = Field(..., example=100000)
    revenue_impact: int = Field(..., example=200000)
    employee_ai_training_hours: float = Field(..., example=120)
    ai_maturity_score: float = Field(..., example=80)
    deployment_count: int = Field(..., example=15)

# Respuesta de predicción
class CompanyPredictionResponse(BaseModel):
    message: str
    productivity_gain: float

# Respuesta al guardar/consultar en DB
class CompanyResponse(CompanyCreate):
    id: int = Field(..., example=1)
    productivity_gain: float | None = Field(None, example=1.20)

    class Config:
        orm_mode = True
