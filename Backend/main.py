import json #Librería para manejo de objetos json
from openai import OpenAI #SDK de OpenAI para API de ChatGPT (pip install openai)
from pydantic import BaseModel
from fastapi import FastAPI #Librería para crear entorno de API (pip installa fastapi[standard])
import uvicorn #Utilizado para levantar el servidor virtual (pip install uvicorn[standard])
from fastapi.middleware.cors import CORSMiddleware #Import librería especial para contrato CORS
from typing import List

app = FastAPI()

if _name_ == '_main_':
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

with open('Restaurantes/BurgerKing.json') as archivo:
    BurgerKing = json.load(archivo)

with open('Restaurantes/GoGreen.json') as archivo:
    GoGreen = json.load(archivo)

client = OpenAI()

restricciones = "Cuando se solicite información sobre comida o restaurantes que no están disponibles en la universidad deberás informar al respecto y de ser posible brindar una recomendación relacionada a la solicitud hecha. Cuando se realice una solicitud que no está relacionada con tu objetivo deberás informar que ese no puedes respondes a eso porque no es el propósito de la aplicación"

InitialPrompt = {
    "role": "system",
    "content": f"Tu objetivo es brindar asistencia en la elección de comida basado principalmente en el presupuesto, preferencias específicas como tipo de comida y otras características relevantes de los estudiantes de la Universidad Rafael Landívar de Guatemala. Los restaurantes disponibles son: {AlMacarone},{Subway}, {Comedor}, {Gitane}, {Manguito}, {BurgerKing}, {GoGreen}. Para cada restaurante, considera todas las opciones disponibles en el menú correspondiente que cumplan con los criterios del usuario. Asegúrate de incluir todas las opciones posibles dentro del presupuesto y las preferencias especificadas por el usuario. Tienes las siguientes restricciones: {restricciones}. Cualquier solicitud no descrita y no sea parte de las restricciones puesde responder libremente basado en tu objetivo."
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