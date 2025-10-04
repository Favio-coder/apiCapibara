# Simula la lógica de negocio
def get_users():
    return [
        {"id": 1, "name": "Ana"},
        {"id": 2, "name": "Luis"}
    ]

def create_user(data):
    # Aquí podrías agregar validaciones, base de datos, etc.
    return {"id": 3, "name": data.get("name")}
