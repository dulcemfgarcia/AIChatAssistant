import json #Librería para manejo de objetos json
from openai import OpenAI #SDK de OpenAI para API de ChatGPT
#from flask import Flask, jsonify, request #Para levantar servidor de peticiones Flask
#from flask_cors import CORS, cross_origin #Para el manejo de CORS entre servidor y cliente

#app = Flask(__name__)

#CORS(app)

#if __name__ == "__main__":
#    app.run(debug=True)


with open('Restaurantes/AlMacarone.json', 'r') as archivo:
    AlMacarone = json.load(archivo)

with open('Restaurantes/Comedor.json') as archivo:
    Comedor = json.load(archivo)

client = OpenAI()

messagesCollection = [
    {
        "role": "system",
        "content": f"Tu objetivo es brindar asistencia en la elección de comida basado en presupuesto y características saludables de estudiantes de la Universidad Rafael Landívar de Guatemala la cual cuenta con los siguientes restaurantes: {AlMacarone}, {Comedor}. Si se menciona un restaurante o comida no incluidos en la información previa, responder 'Lamentablemente, esa opción no esta diponible en la URL, te motivamos a consultar el menú disponible'. Adicionalmente, si se realizar una solicitud que no esté relacionada con alimentación deberá notificar al usuario que ese no es el propósito del sistema."
    },
]

#@app.after_request
#def add_cors_headers(response):
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
#    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#   return response

#@app.route('/ConsultarLandivarEats', methods=['POST'])
def ConsultarLandivarEats(consulta):
    #datos = request.json
    #consulta = datos['consulta']
    messagesCollection.append({
        "role": "user",
        "content": consulta
    })

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=messagesCollection
    )

    response = completion.choices[0].message.content

    messagesCollection.append({
        "role": "assistant",
        "content": response
    })

    #return jsonify(response)
    return response

contador = 0

while contador < 5 :
    entrada = input("¿Qué desea hacer?: ")
    respuesta = ConsultarLandivarEats(entrada)
    print(respuesta)
    print()

    contador += 1
    