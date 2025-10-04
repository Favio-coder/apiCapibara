import google.generativeai as genai
import os
import re
import logging
from dotenv import load_dotenv

# Configuración y Carga
load_dotenv()
try:
    # Usamos os.environ.get en lugar de os.getenv en esta ubicación por si se
    # necesita manejar una excepción si no está definida en el entorno.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no está configurada en el entorno.")
    genai.configure(api_key=api_key)
except Exception as e:
    logging.error(f"Error al configurar la API de Gemini: {e}")


def clean_text(text: str) -> str:
    """Limpia el texto de entrada para el modelo, permitiendo caracteres en español."""
    text = text.strip().lower()
    text = re.sub(r"[^a-záéíóúüñ¿?¡! ]", "", text)
    return text

def get_assistant_response(user_message: str) -> str:
    """
    Gestiona la llamada al modelo Gemini con el prompt y los ejemplos definidos.
    """
    user_message_cleaned = clean_text(user_message)
    
    system_prompt = (
            "Eres un asistente virtual diseñado para ayudar a usuarios con actividades agrarias y temas sobre agricultura. "
            "Tu función es ser un guía profesional y preciso para analizar las peticiones de los usuarios y recomendar acciones ante las diversas consultas que tengan sobre la rancha de la papa y huertos de papa. "
            "Siempre usa un lenguaje profesional, directo y concreto, analiza en profundidad la situación que se toma con respecto a sus parcelas de papa. Las respuestas no deben ser demasiado extensas, pero además tienen que ser precisas con el tema a tratar, "
            "Evita expresiones vulgares o dialectos alejados de lo formal, limita solo a responder las consultas o temas relacionados a la agricultura y la rancha de papa (temperatura, humedad, etc), temas alejados de lo ya descrito omitelos o no continues respondiendo. "
            "Si es posible, ofrece un consejo práctico y fácil de seguir."
    )

    examples = [
            {"role": "user", "parts": ["¿Qué factores hacen que la rancha de la papa crezca?"]},
            {"role": "model", "parts": ["La rancha de la papa es causada por Phytophthora infestans y se desarrolla muy rápido en condiciones de alta humedad y temperaturas frescas; puede destruir un cultivo en pocos días si no se controla"]},
            {"role": "user", "parts": ["Quiero empezar mi propia parcela de papas, pero quiero evitar el riesgo de que crezca rancha en ellos."]},
            {"role": "model", "parts": ["Es increible saber que quieres rear tu parcela. Breve análisis: Empezar bien la parcela reduce mucho el riesgo de rancha si aplicas medidas como selección de sitio, preparación del suelo, semillas sanas y monitoreo constante.."]},
            {"role": "user", "parts": ["Mi parcela parece presentar indicios de crecimiento de rancha de papa, ¿Qué puedo hacer al respecto?."]},
            {"role": "model", "parts": ["Es alarmante saber que tu parcela está presentando indicios de la rancha en papa, sin embargo si se puede hacer algo al respecto como inspeccionar y marcar las plantas con síntomas severos y retíralas inmediatamente del lote, aislar la zona afectada y revisar con más frecuencia las parcelas en condiciones de riesgo."]}
    ]

    try:
        model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=system_prompt)
        chat = model.start_chat(history=examples)
        response = chat.send_message(user_message_cleaned)
        
        logging.info(f"Usuario: {user_message} | Respuesta: {response.text}")
        
        return response.text
    except Exception as e:
        # Relanzamos una excepción de más alto nivel para ser manejada en la capa de rutas
        logging.error(f"Error en el servicio de Gemini: {e}")
        raise RuntimeError(f"Fallo en la comunicación con el asistente: {str(e)}")