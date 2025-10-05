import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import os

# Cargar modelo
model_path = os.path.join("app", "models", "modelo_clasificacion.keras")
model = load_model(model_path)

# Etiquetas conocidas
le = LabelEncoder()
le.classes_ = np.array(["verde", "amarillo", "naranja", "rojo"])  # ajustar según tu entrenamiento

def predecir_color(temp_7d, hr_7d, ppt_7d):
    """
    temp_7d, hr_7d, ppt_7d: valores numéricos de los últimos 7 días
    """
    X = np.array([[temp_7d, hr_7d, ppt_7d]])
    pred_num = np.argmax(model.predict(X), axis=1)[0]
    pred_label = le.inverse_transform([pred_num])[0]
    return pred_label
