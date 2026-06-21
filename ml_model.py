import joblib
import numpy as np

# Cargar el modelo entrenado
model = joblib.load('./model/model.pkl')

# Cargar los scalers
scaler_X = joblib.load('./model/scaler_X.pkl')
scaler_y = joblib.load('./model/scaler_y.pkl')

def predict_productivity(features: list[float]) -> float:
    """
    Recibe una lista de 10 features en el mismo orden que X.columns
    Devuelve la productividad predicha (%)
    """
    # Convertir a numpy array y escalar
    new_data = np.array(features).reshape(1, -1)
    new_data_scaled = scaler_X.transform(new_data)
    predicted_scaled = model.predict(new_data_scaled)
    predicted = scaler_y.inverse_transform(predicted_scaled.reshape(-1, 1))
    productivity_gain = round(float(predicted[0][0]), 2)
    return productivity_gain
