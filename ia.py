response = requests.post(URL, headers=headers, json=data)

print(response.status_code)  # Imprime el código de estado
print(response.text)         # Imprime la respuesta completa de la API

if response.status_code == 200:
    return response.json()["choices"][0]["message"]["content"]
else:
    raise HTTPException(status_code=response.status_code, detail="Error en la API de Groq")
