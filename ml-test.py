import joblib
import numpy as np

# Load the best model
model = joblib.load('./model/model.pkl')

# Load the scalers
scaler_X = joblib.load('./model/scaler_X.pkl')
scaler_y = joblib.load('./model/scaler_y.pkl')

print("Model and scalers loaded successfully!")

new_company_features = [
    2.0,    # country codificado
    2025,   # year
    3.0,    # ai_adoption_level
    500000, # ai_investment_usd
    0.75,   # automation_rate
    100000, # cost_savings
    200000, # revenue_impact
    120,    # employee_ai_training_hours
    80,     # ai_maturity_score
    15      # deployment_count
]

# Convertir a numpy array y escalar
new_company_data = np.array(new_company_features).reshape(1, -1)
new_company_scaled = scaler_X.transform(new_company_data)

# Hacer predicción con el modelo cargado
predicted_productivity_scaled = model.predict(new_company_scaled)

# Invertir la transformación para volver a la escala original
predicted_productivity = scaler_y.inverse_transform(
    predicted_productivity_scaled.reshape(-1, 1)
)

print(f"Predicted productivity gain: {predicted_productivity[0][0]:.2f}%")