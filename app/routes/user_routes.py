from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# Nota: La importación del servicio sigue siendo la misma si solo usa Python puro
from app.services.user_service import get_users, create_user 

# 1. Define el objeto APIRouter
router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)

# 2. Define el esquema Pydantic para la data de entrada (POST)
class UserCreate(BaseModel):
    name: str
    email: str
    # Agrega aquí cualquier otro campo que tu servicio necesite

@router.get("/")
def list_users():
    """Obtiene y devuelve la lista de usuarios."""
    # FastAPI serializa automáticamente la respuesta
    users = get_users() 
    return users

@router.post("/")
def add_user(user_data: UserCreate): # FastAPI inyecta y valida el JSON
    """Crea un nuevo usuario."""
    try:
        # Convierte el modelo Pydantic a un diccionario para el servicio
        new_user = create_user(user_data.model_dump()) 
        return new_user
    except Exception as e:
        # Usa HTTPException para manejar errores de API
        raise HTTPException(status_code=400, detail=f"Error al crear usuario: {str(e)}")