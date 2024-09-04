import json #Librería para manejo de objetos json
from openai import OpenAI #SDK de OpenAI para API de ChatGPT (pip install openai)
from pydantic import BaseModel
from fastapi import FastAPI #Librería para crear entorno de API (pip installa fastapi[standard])
import uvicorn #Utilizado para levantar el servidor virtual (pip install uvicorn[standard])
from fastapi.middleware.cors import CORSMiddleware #Import librería especial para contrato CORS
from typing import List

app = FastAPI()

if __name__ == '__main__':
   uvicorn.run('main:app', port=8000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('Restaurantes/AlMacarone.json', 'r') as archivo:
    AlMacarone = json.load(archivo)

with open('Restaurantes/Comedor.json') as archivo:
    Comedor = json.load(archivo)

with open('Restaurantes/Subway.json') as archivo:
    Subway = json.load(archivo)

with open('Restaurantes/Gitane.json') as archivo:
    Gitane = json.load(archivo)

with open('Restaurantes/Manguito.json') as archivo:
    Manguito = json.load(archivo)

client = OpenAI()

InitialPrompt = {
    "role": "system",
    "content": f"Tu objetivo es brindar asistencia en la elección de comida basado en presupuesto y características saludables de estudiantes de la Universidad Rafael Landívar de Guatemala la cual cuenta con los siguientes restaurantes: {AlMacarone},{Subway}, {Comedor}, {Gitane}, {Manguito}. Si se menciona un restaurante o comida no incluidos en la información previa, responder 'Lamentablemente, esa opción no esta diponible en la URL, te motivamos a consultar el menú disponible'. Adicionalmente, si se realizar una solicitud que no esté relacionada con alimentación deberá notificar al usuario que ese no es el propósito del sistema."
}

class bodyChatRequest(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
   chat: str
   history: List[bodyChatRequest]

@app.post('/ConsultarLandivarEats')
def ConsultarLandivarEats(chat : ChatRequest):
    consulta = chat.chat

    if len(chat.history) <= 0:
        chat.history.append(InitialPrompt)

    chat.history.append({
        "role": "user",
        "content": consulta
    })

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=chat.history
    )

    response = completion.choices[0].message.content

    chat.history.append({
        "role": "assistant",
        "content": response
    })

    return {
        "chat": response,
        "history": chat.history,
    }
    