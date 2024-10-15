import requests
import json

API_KEY = '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'
url = "https://api.groq.com/openai/v1/chat/completions"

def respuesta_ia(texto: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": "Actúa como un asistente virtual."
            },
            {
                "role": "user",
                "content": texto
            }
        ],
        "model": "gemma-7b-it",
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False,
        "stop": None
    }

    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    
    return response_data['choices'][0]['message']['content']