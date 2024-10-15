from typing import Union
from fastapi import FastAPI, HTTPException
import requests
import json

app = FastAPI()

API_KEY = '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'  # Asegúrate de usar la clave API correcta
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
REST_API_URL = "https://api-rest-ia-1.onrender.com"  # URL de la API REST externa
NEW_API_URL = "http://35.160.120.126"  # La nueva API que deseas añadir

def IA_groq(pregunta: str) -> str:
    """Función para obtener la respuesta de la IA a partir de una pregunta."""
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": "Contéstame como un profesional en programación, solo español."
            },
            {
                "role": "user",
                "content": pregunta
            }
        ],
        "model": "mixtral-8x7b-32768",  # Cambia el modelo si es necesario
        "temperature": 1,                # Ajusta la temperatura para la aleatoriedad de las respuestas
        "max_tokens": 1024,              # Máximo de tokens en la respuesta
        "top_p": 1,                      # Para el muestreo de núcleo
        "stream": False,
        "stop": None
    }

    response = requests.post(GROQ_URL, json=data, headers=headers)

    if response.status_code == 200:
        respuesta = response.json()
        return respuesta['choices'][0]['message']['content']
    else:
        raise HTTPException(status_code=response.status_code, detail="Error en la API de Groq")

def llamar_api_rest(pregunta: str) -> str:
    """Función para llamar a la API REST externa."""
    try:
        response = requests.post(f"{REST_API_URL}/ia", json={"pregunta": pregunta})
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        data = response.json()
        return data['respuesta']  # Asegúrate de que la clave 'respuesta' exista en la respuesta JSON
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

def llamar_nueva_api(pregunta: str) -> str:
    """Función para llamar a la nueva API en 35.160.120.126."""
    try:
        response = requests.get(f"{NEW_API_URL}/endpoint", params={"pregunta": pregunta})
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        data = response.json()
        return data['respuesta']  # Asegúrate de que la clave 'respuesta' exista en la respuesta JSON
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/ia/{pregunta_id}")
def responder_ia(pregunta_id: str):
    """Endpoint para responder a preguntas usando la IA de Groq o la API REST."""
    # Intenta primero con la IA Groq
    try:
        respuesta = IA_groq(pregunta_id)
    except HTTPException:
        # Si Groq falla, intenta con la API REST
        respuesta = llamar_api_rest(pregunta_id)

    return {"Pregunta": pregunta_id, "Respuesta": respuesta}

@app.get("/nueva-api/{pregunta}")
def usar_nueva_api(pregunta: str):
    """Endpoint para llamar a la nueva API en 35.160.120.126."""
    respuesta = llamar_nueva_api(pregunta)
    return {"Pregunta": pregunta, "Respuesta": respuesta}
