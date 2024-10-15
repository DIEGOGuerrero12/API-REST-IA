from typing import Union
from fastapi import FastAPI, HTTPException
import requests
import json

app = FastAPI()

# Configuración de la API
API_KEY = "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"  # Reemplaza con tu clave real
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_response(pregunta: str) -> str:
    """
    Realiza una solicitud a la API de Groq con la pregunta del usuario.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": "Contestame como un profesional en programación, solo en español."
            },
            {
                "role": "user",
                "content": pregunta
            }
        ],
        "model": "mixtral-8x7b-32768",  # Cambia el modelo si es necesario
        "temperature": 1,        # Ajusta la temperatura para la aleatoriedad de las respuestas
        "max_tokens": 1024,      # Máximo de tokens en la respuesta
        "top_p": 1,              # Para el muestreo de núcleo
        "stream": False
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Verifica si hubo un error HTTP

        response_data = response.json()
        
        # Verifica que la estructura de la respuesta sea la esperada
        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"]
        else:
            return "No se pudo obtener una respuesta adecuada de la API de Groq."

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error en la conexión con la API de Groq: {str(e)}")

@app.get("/ia/{pregunta_id}")
def responder_ia(pregunta_id: str):
    """
    Endpoint para obtener una respuesta de la IA a una pregunta específica.
    """
    if not pregunta_id.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    try:
        respuesta = get_groq_response(pregunta_id)
        return {"ia_pregunta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
