from sqlalchemy import Column, Integer, Float, String
from database import Base

class CompanyAI(Base):
    __tablename__ = "companies_ai"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(Float, nullable=False)  # codificado con OrdinalEncoder
    year = Column(Integer, nullable=False)
    ai_adoption_level = Column(Float, nullable=False)
    ai_investment_usd = Column(Integer, nullable=False)
    automation_rate = Column(Float, nullable=False)
    cost_savings = Column(Integer, nullable=False)
    revenue_impact = Column(Integer, nullable=False)
    employee_ai_training_hours = Column(Float, nullable=False)
    ai_maturity_score = Column(Float, nullable=False)
    deployment_count = Column(Integer, nullable=False)

    # Este campo es opcional: se llena después de la predicción
    productivity_gain = Column(Float, nullable=True)
    