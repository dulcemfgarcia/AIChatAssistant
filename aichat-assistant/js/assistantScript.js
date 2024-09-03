const inputEl = document.querySelector(".input-chat");
const btnEl = document.querySelector(".fa-paper-plane");
const cardBodyEl = document.querySelector(".card-body");

var HistorialChat = []

let userMessage;

async function manageChat(){
    userMessage = inputEl.value.trim();

    if(!userMessage) return;
    inputEl.value = "";
    
    cardBodyEl.appendChild(messageEl(userMessage, "user"));

    const mensaje = await ConsumirLandivarEats(userMessage);

    cardBodyEl.appendChild(messageEl(mensaje, "chat-bot"));
}

//messages
const messageEl = (message, className) => {
    const chatEl = document.createElement("div");
    chatEl.classList.add("chat", `${className}`);
    let chatContent =
     className === "chat-bot" 
     ?  `<span class="user-icon"><i class="fa fa-robot"></i></span>
    <p>${message}</p>`
    : `<span class="user-icon"><i class="fa fa-user"></i></span>
    <p>${message}</p>`;
    chatEl.innerHTML = chatContent;
    return chatEl;
};

btnEl.addEventListener("click", manageChat);

//  Función para llamado a API de consulta ChatGPT
async function ConsumirLandivarEats(consulta) {
    datos = {
        "chat": consulta,
        "history": HistorialChat
    }

    try {
        const respuesta = await fetch('http://localhost:8000/ConsultarLandivarEats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });
    
        if(!respuesta.ok){
            throw new Error('Error: ${respuesta.status}');
        }
    
        const resultado = await respuesta.json();

        HistorialChat = resultado.history

        return resultado.chat;
    } catch (error) {
        console.error('Error:', error);
        return "Ha ocurrido un error"
    }
}