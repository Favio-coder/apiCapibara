# app/routes/chatbot_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.chatbot_service import get_assistant_response # Importar el servicio

# Definición del esquema Pydantic
class ChatRequest(BaseModel):
    message: str

# Inicialización del router de FastAPI
router = APIRouter(
    prefix="/assistant", # Un prefijo para todas las rutas del asistente
    tags=["Asistente AI"]
)

@router.get("/")
def check_assistant():
    """Ruta para verificar que el módulo del asistente está vivo."""
    return {"message": "Asistente de Agricultura listo para consultas."}


@router.post("/text")
async def assistant_text_route(req: ChatRequest):
    """
    Ruta para enviar un mensaje de texto al asistente y obtener la respuesta de Gemini.
    """
    # 1. Validación de entrada (además de Pydantic)
    if not req.message or len(req.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="El mensaje de entrada no puede estar vacío.")

    try:
        assistant_text = get_assistant_response(req.message)
        return {"assistant_response": assistant_text}
    except RuntimeError as e:
        # Capturar el error del servicio para devolver un 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=str(e))