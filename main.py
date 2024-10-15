from typing import Optional
from fastapi import FastAPI, HTTPException
from IA import respuesta_ia

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/ia/{texto}")
def responder_ia_endpoint(texto: str):
    try:
        respuesta = respuesta_ia(texto)
        return {"Respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
