from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

API_KEY = "35.160.120.126"
url = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_response(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Mensaje introductorio si el usuario no proporciona una pregunta
    if not user_message.strip():
        return "¡Hola! Me complace responderte como un profesional en programación en español. " \
               "Cuéntame, ¿en qué puedo ayudarte? Estoy aquí para responder cualquier pregunta que " \
               "tengas sobre programación, desde conceptos básicos hasta temas avanzados. ¡Adelante y " \
               "hazme saber qué necesitas!"

    data = {
        "messages": [
            {"role": "system", "content": "Proporciona respuestas a las preguntas del usuario."},
            {"role": "user", "content": user_message}
        ],
        "model": "gemma-7b-it",
        "temperature": 0.7,
        "max_tokens": 150
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        raise HTTPException(status_code=500, detail="Error en la API de Groq")

@app.get("/ia/hola")
async def ask_groq(question: str = ""):
    try:
        answer = get_groq_response(question)
        return {"ia_pregunta": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
