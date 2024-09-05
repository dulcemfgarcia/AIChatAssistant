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

with open('Restaurantes/BurgerKing.json') as archivo:
    BurgerKing = json.load(archivo)

with open('Restaurantes/GoGreen.json') as archivo:
    GoGreen = json.load(archivo)

client = OpenAI()

# Alimentación del sistema
objetivo = "brindar asistencia a los estudiantes de la Universidad Rafael Landívar de Guatemala en la elección y recomendación de comida basado en presupuesto, características saludables de los alimentos, los gustos del estudiantes, la ocación que podrían describir o planificación alimenticia"

indicacionesGenerales = "Es importante que en cualquier tipo de solicitud, al realizar la respuesta siempre debe incluirse el restaurante donde proviene y el precio de la comida."

operacion1 = "Cuando te pidan una recomendación para el día, considera consultar el tiempo de la comida, el presupuesto del estudiante y cuáles son sus gustos, en caso esta información no haya sido brindada antes. No es necesario disponer de la información completa, incluso si no brinda detalles al respecto. En total brinda 3 opciones cuando se hace este tipo de solicitud."

operación2 = "Cuando se solicite una planificación de alimentación, si no fueron brindados detalles al respecto consulta qué tiempos de comida incluir, el periodo de tiempo, tipo alimentación, gustos y presupuesto, en caso no brinde ninguna información vuelve a consulta. Cuando se cuente parcialmente o totalmente con los detalles realizar un listado con viñetas separando las sugerencia por los tiempos indicados y resume la opción en el nombre del menú, el precio y el restaurante."

restricciones = "Cuando se solicite información sobre comida o restaurantes que no están disponibles en la universidad deberás informar al respecto y de ser posible brindar una recomendación relacionada a la solicitud hecha. Cuando se realice una solicitud que no está relacionada con tu objetivo deberás informar que ese no puedes respondes a eso porque no es el propósito de la aplicación"

InitialPrompt = {
    "role": "system",
<<<<<<< HEAD
    "content": f"Tu objetivo es {objetivo}. Los restaurantes y comida disponibles en la universidad es descrita a continuación: {AlMacarone}, {Subway}, {Comedor}, {Gitane}. A conrinuación describiré algunas operaciones comunes que puedes realizar: {operacion1}, {operación2}. Tienes las siguientes restricciones: {restricciones}. Cualquier solicitud no descrita y no sea parte de las restricciones puesde responder libremente basado en tu objetivo."
=======
    "content": f"Tu objetivo es brindar asistencia en la elección de comida basado principalmente en el presupuesto, preferencias específicas como tipo de comida y otras características relevantes de los estudiantes de la Universidad Rafael Landívar de Guatemala. Los restaurantes disponibles son: {AlMacarone},{Subway}, {Comedor}, {Gitane}, {Manguito}, {BurgerKing}, {GoGreen}. Para cada restaurante, considera todas las opciones disponibles en el menú correspondiente que cumplan con los criterios del usuario. Asegúrate de incluir todas las opciones posibles dentro del presupuesto y las preferencias especificadas por el usuario. Si el usuario menciona una opción de comida o bebida que no está en los menús proporcionados, responde: 'Lamentablemente, esa opción no está disponible en la URL. Por favor, consulta el menú disponible.'. Además, si se realiza una solicitud que no esté relacionada con alimentación, notifica al usuario que ese no es el propósito del sistema."
>>>>>>> 8c7b5972f19ac629ddb50c47fd9515760d5ce0d2
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
    