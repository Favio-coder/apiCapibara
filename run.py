# run.py (Ejemplo de cómo debería verse la integración)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importar el router del asistente
from app.routes.chatbot_routes import router as assistant_router 
# Importar el router de usuarios (asumimos que existe)
from app.routes.user_routes import router as user_router 
from app.routes.prediction_routes import router as prediction_router

app = FastAPI(
    title="WAOS API",
    description="Backend para la aplicación de agricultura."
)

# --- Configuración de CORS (copiado de tu código original) ---
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
# -----------------------------------------------------------


# --- Incluir todos los routers de la aplicación ---

# 1. Router de Usuarios
app.include_router(user_router, prefix="/users") 

# 2. Router del Asistente (nuevo)
# La ruta final será: /assistant/text
app.include_router(assistant_router)

# --- Ruta Root (si la tenías) ---
@app.get("/")
def root():
    return {"message": "WAOS API funcionando piola."}


app.include_router(prediction_router, prefix="/weather")  # /weather/predict
