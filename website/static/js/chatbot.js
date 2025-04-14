function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

(function () {
    console.log("Chatbot script chargé !");

    let chatbotContainer = document.createElement("div");
    chatbotContainer.style.position = "fixed";
    chatbotContainer.style.bottom = "20px";
    chatbotContainer.style.right = "20px";
    chatbotContainer.style.width = "400px";
    chatbotContainer.style.height = "600px";
    chatbotContainer.style.minWidth = "250px";
    chatbotContainer.style.minHeight = "300px";
    chatbotContainer.style.resize = "both";
    chatbotContainer.style.overflow = "hidden";  // important !
    chatbotContainer.style.background = "#f8f9fa";
    chatbotContainer.style.borderRadius = "10px";
    chatbotContainer.style.boxShadow = "0px 0px 10px rgba(0,0,0,0.1)";
    chatbotContainer.style.display = "none";  // ne pas utiliser "flex" ici !
    chatbotContainer.style.fontFamily = "Arial, sans-serif";
    chatbotContainer.style.boxSizing = "border-box";
    
    // ➕ Conteneur interne flex
    let chatbotContent = document.createElement("div");
    chatbotContent.style.display = "flex";
    chatbotContent.style.flexDirection = "column";
    chatbotContent.style.height = "100%";
    chatbotContent.style.boxSizing = "border-box";
    
    // Ajout des composants dans le conteneur flex interne
    chatbotContent.appendChild(chatHeader);
    chatbotContent.appendChild(chatBody);
    chatbotContent.appendChild(chatInputContainer);
    
    // Puis on l’ajoute dans le conteneur principal
    chatbotContainer.appendChild(chatbotContent);
    

    let chatHeader = document.createElement("div");
    chatHeader.style.background = "#007bff";
    chatHeader.style.color = "white";
    chatHeader.style.padding = "10px";
    chatHeader.style.textAlign = "center";
    chatHeader.style.cursor = "pointer";
    chatHeader.innerText = "Chat avec OptiQuant";

    let chatBody = document.createElement("div");
    chatBody.style.flex = "1";
    chatBody.style.padding = "10px";
    chatBody.style.overflowY = "auto";

    let chatInputContainer = document.createElement("div");
    chatInputContainer.style.display = "flex";
    chatInputContainer.style.padding = "10px";

    let chatInput = document.createElement("input");
    chatInput.type = "text";
    chatInput.placeholder = "Écris un message...";
    chatInput.style.flex = "1";
    chatInput.style.padding = "5px";
    chatInput.style.border = "1px solid #ccc";
    chatInput.style.borderRadius = "5px";

    let sendButton = document.createElement("button");
    sendButton.innerText = "Envoyer";
    sendButton.style.marginLeft = "5px";
    sendButton.style.padding = "5px 10px";
    sendButton.style.background = "#007bff";
    sendButton.style.color = "white";
    sendButton.style.border = "none";
    sendButton.style.borderRadius = "5px";
    sendButton.style.cursor = "pointer";

    chatInputContainer.appendChild(chatInput);
    chatInputContainer.appendChild(sendButton);
    chatbotContainer.appendChild(chatHeader);
    chatbotContainer.appendChild(chatBody);
    chatbotContainer.appendChild(chatInputContainer);
    document.body.appendChild(chatbotContainer);

    let chatButton = document.createElement("div");
    chatButton.innerText = "💬";
    chatButton.style.position = "fixed";
    chatButton.style.bottom = "20px";
    chatButton.style.right = "20px";
    chatButton.style.width = "50px";
    chatButton.style.height = "50px";
    chatButton.style.background = "#007bff";
    chatButton.style.color = "white";
    chatButton.style.borderRadius = "50%";
    chatButton.style.display = "flex";
    chatButton.style.alignItems = "center";
    chatButton.style.justifyContent = "center";
    chatButton.style.cursor = "pointer";
    chatButton.style.boxShadow = "0px 0px 10px rgba(0,0,0,0.2)";

    document.body.appendChild(chatButton);

    chatButton.onclick = function () {
        chatbotContainer.style.display = chatbotContainer.style.display === "none" ? "flex" : "none";
    };

    sendButton.onclick = function () {
        let userText = chatInput.value.trim();
        if (!userText) return;

        let userMessage = document.createElement("div");
        userMessage.style.padding = "5px";
        userMessage.style.background = "#d1e7ff";
        userMessage.style.borderRadius = "5px";
        userMessage.style.margin = "5px 0";
        userMessage.innerText = "You : " + userText;
        chatBody.appendChild(userMessage);

        chatInput.value = "";
        chatBody.scrollTop = chatBody.scrollHeight;

        let botMessage = document.createElement("div");
        botMessage.style.padding = "5px";
        botMessage.style.background = "#e9ecef";
        botMessage.style.borderRadius = "5px";
        botMessage.style.margin = "5px 0";
        botMessage.innerText = "OptiQuantIA : ...";
        chatBody.appendChild(botMessage);
        chatBody.scrollTop = chatBody.scrollHeight;

        fetch("/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ message: userText })
        })
        .then(response => {
            if (!response.ok) {
                console.log(response);
                throw new Error("Réponse serveur non valide : " + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log("Réponse du bot :", data);
            if (data.reply) {
                botMessage.innerText = "Bot : " + data.reply;
            } else {
                botMessage.innerText = "Bot : Erreur dans la réponse du serveur";
                console.error("Réponse invalide :", data);
            }
            chatBody.scrollTop = chatBody.scrollHeight;
        })
        .catch(error => {
            botMessage.innerText = "Bot : Erreur de connexion";
            console.error("Erreur :", error);
        });
    };

    console.log("Chatbot script chargé --- END!");
})();
