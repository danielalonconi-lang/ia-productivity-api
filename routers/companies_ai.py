from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import CompanyAI
from ml_model import predict_productivity

from schemas import (
    CompanyCreate,
    CompanyPredictionResponse,
    CompanyResponse
)

router = APIRouter(
    prefix="/company",
    tags=["company"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función auxiliar para clasificar productividad
def classify_productivity(value: float) -> str:
    if value < 0.30:
        return "Baja productividad"
    elif value < 0.70:
        return "Productividad media"
    else:
        return "Alta productividad"

# Endpoint de predicción
@router.post("/predict", response_model=CompanyPredictionResponse)
def predict(data: CompanyCreate):
    # Construir el vector de features en el mismo orden que X.columns
    features = [
        data.country,
        data.year,
        data.ai_adoption_level,
        data.ai_investment_usd,
        data.automation_rate,
        data.cost_savings,
        data.revenue_impact,
        data.employee_ai_training_hours,
        data.ai_maturity_score,
        data.deployment_count
    ]

    productivity_gain = predict_productivity(features)
    nivel = classify_productivity(productivity_gain)

    return {
        "message": f"Productividad predicha: {nivel}",
        "productivity_gain": productivity_gain
    }

# Endpoint para crear registro en DB
@router.post("/", response_model=CompanyResponse)
def create(data: CompanyCreate, db: Session = Depends(get_db)):
    features = [
        data.country,
        data.year,
        data.ai_adoption_level,
        data.ai_investment_usd,
        data.automation_rate,
        data.cost_savings,
        data.revenue_impact,
        data.employee_ai_training_hours,
        data.ai_maturity_score,
        data.deployment_count
    ]

    productivity_gain = predict_productivity(features)

    new_company = CompanyAI(
        country=data.country,
        year=data.year,
        ai_adoption_level=data.ai_adoption_level,
        ai_investment_usd=data.ai_investment_usd,
        automation_rate=data.automation_rate,
        cost_savings=data.cost_savings,
        revenue_impact=data.revenue_impact,
        employee_ai_training_hours=data.employee_ai_training_hours,
        ai_maturity_score=data.ai_maturity_score,
        deployment_count=data.deployment_count,
        productivity_gain=productivity_gain
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company

# GET todos
@router.get("/", response_model=list[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    return db.query(CompanyAI).all()

# GET por id
@router.get("/{id}", response_model=CompanyResponse)
def get_company_by_id(id: int, db: Session = Depends(get_db)):
    company = db.query(CompanyAI).filter(CompanyAI.id == id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return company

# PUT actualizar
@router.put("/{id}", response_model=CompanyResponse)
def update_company(id: int, data: CompanyCreate, db: Session = Depends(get_db)):
    company = db.query(CompanyAI).filter(CompanyAI.id == id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    features = [
        data.country,
        data.year,
        data.ai_adoption_level,
        data.ai_investment_usd,
        data.automation_rate,
        data.cost_savings,
        data.revenue_impact,
        data.employee_ai_training_hours,
        data.ai_maturity_score,
        data.deployment_count
    ]

    productivity_gain = predict_productivity(features)

    company.country = data.country
    company.year = data.year
    company.ai_adoption_level = data.ai_adoption_level
    company.ai_investment_usd = data.ai_investment_usd
    company.automation_rate = data.automation_rate
    company.cost_savings = data.cost_savings
    company.revenue_impact = data.revenue_impact
    company.employee_ai_training_hours = data.employee_ai_training_hours
    company.ai_maturity_score = data.ai_maturity_score
    company.deployment_count = data.deployment_count
    company.productivity_gain = productivity_gain

    db.commit()
    db.refresh(company)

    return company

# DELETE
@router.delete("/{id}")
def delete_company(id: int, db: Session = Depends(get_db)):
    company = db.query(CompanyAI).filter(CompanyAI.id == id).first