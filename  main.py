from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/ia/hola")
def ia_hola():
    return {
        "ia_pregunta": "¡Hola! Me complace responderte como un profesional en programación en español. "
                       "Cuéntame, ¿en qué puedo ayudarte? Estoy aquí para responder cualquier pregunta "
                       "que tengas sobre programación, desde conceptos básicos hasta temas avanzados. "
                       "Adelante y hazme saber qué necesitas. ¡Buena suerte en tu viaje de aprendizaje en programación!"
    }
