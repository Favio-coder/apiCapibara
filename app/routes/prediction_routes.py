from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.prediction_service import predecir_color

router = APIRouter()

class PrediccionRequest(BaseModel):
    ubicacion: str
    temp_7d: float
    hr_7d: float
    ppt_7d: float

class PrediccionResponse(BaseModel):
    ubicacion: str
    prediccion: str

@router.post("/predict", response_model=List[PrediccionResponse])
def predict_colores(datos: List[PrediccionRequest]):
    resultados = []
    for d in datos:
        color = predecir_color(d.temp_7d, d.hr_7d, d.ppt_7d)
        resultados.append(PrediccionResponse(ubicacion=d.ubicacion, prediccion=color))
    return resultados
