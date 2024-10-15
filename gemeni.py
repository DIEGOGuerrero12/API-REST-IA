from fastapi import FastAPI, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "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"  # Asegúrate de usar tu clave API aquí
URL = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_response(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "system", "content": "Proporciona respuestas en español sobre programación."},
            {"role": "user", "content": user_message}
        ],
        "model": "mixtral-8x7b-32768",
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    response = requests.post(URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise HTTPException(status_code=response.status_code, detail="Error en la API de Groq")

@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}

@app.get("/ia/{pregunta_id}")
def responder_ia(pregunta_id: str):
    try:
        respuesta = get_groq_response(pregunta_id)
        return {"ia_respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
