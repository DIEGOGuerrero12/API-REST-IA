from typing import Union
from fastapi import FastAPI
import requests
import json

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/ia/{pregunta_id}")
def responder_ia(pregunta_id: str):
    
    API_KEY = '35.160.120.126'
    url = "https://api.groq.com/openai/v1/chat/completions"


    headers = {
                "content-type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }

    data = {
            "messages": [
                    {
                    "role": "system",
                    "content": 
                    "Contestame como un profesional en programacion, solo español."
                  
           
                    },
                    {
                        "role": "user",
                        "content": pregunta_id
                    }
                ],
                "model": "mixtral-8x7b-32768",  # Cambia el modelo si es necesario
                "temperature": 1,        # Ajusta la temperatura para la aleatoriedad de las respuestas
                "max_tokens": 1024,      # Máximo de tokens en la respuesta
                "top_p": 1,              # Para el muestreo de núcleo
                "stream": False,
                "stop": None
        }   

    response = requests.post(url, json=data, headers=headers)

    respuesta= json.loads(response.text)

    return {"ia_pregunta": respuesta['choices'][0]['message']['content']}