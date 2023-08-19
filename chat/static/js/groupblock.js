console.log("Running from blockdetail.js")

let groupBlockContainer = document.querySelector("#groupBlockContainer");
let groupBlockMessageInput = document.querySelector("#groupBlockMessageInput");
let groupBlockMessageSend = document.querySelector("#groupBlockMessageSend");
let groupBlockOnlineUsers = document.querySelector("#groupBlockOnlineUsers")

function groupBlockOnlineUsersConnect(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let createOption = document.createElement("option");
    createOption.value = value;
    createOption.innerHTML = value;
    groupBlockOnlineUsers.appendChild(createOption);
}

function groupBlockOnlineUsersDisconnect(value) {
    let deleteOption = document.querySelector("option[value='" + value + "']");
    if (deleteOption !== null) deleteOption.remove();
}

groupBlockMessageInput.focus();

groupBlockMessageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {
        groupBlockMessageSend.click();
    }
}

groupBlockMessageSend.onclick = function () {
    if (groupBlockMessageInput.value.length === 0) return;
    blockSocket.send(JSON.stringify({
        'message': groupBlockMessageInput.value,
    }));
    console.log(groupBlockMessageInput.value);
    groupBlockMessageInput.value = "";

}

let messagesFetched = false;
let blockSocket = null;

let blockSlug = JSON.parse(document.getElementById("blockSlug").textContent);
let current_user_id = JSON.parse(document.getElementById("current_user_id").textContent);
console.log("Current login user: " + current_user_id)

console.log(blockSlug)

function displayMessages() {
    let slug = window.location.pathname.split('/').slice(-2, -1)[0];
    if (messagesFetched) return;

    fetch("/api_messages/" + slug + "/")
        .then(response => response.json())
        .then(messages => {
            messages.forEach(message => {
                let blockChatMessages = document.createElement('p');
                if (message.user.id === current_user_id) {
                    blockChatMessages.className = 'current_user';
                } else {
                    blockChatMessages.className = 'other_user';
                }

                blockChatMessages.textContent = message.user.username + ": " + message.content;
                groupBlockContainer.appendChild(blockChatMessages)
            });
            messagesFetched = true;
            groupBlockContainer.scrollTop = groupBlockContainer.scrollHeight;
        })
        .catch(error => console.log("Error fetching saved messages: ", error))
    //window.addEventListener("load", displayMessages);
}
displayMessages();

function connect() {

    blockSocket = new WebSocket("ws://" + window.location.host + "/ws/block/" + blockSlug + "/")

    blockSocket.onopen = function (e) {
        console.log("websocket connected successfully")
    }

    blockSocket.onclose = function (e) {
        console.log("web socket close unexpected. trying to reconnect .....")
        setTimeout(function () {
            console.log("reconnecting");
            connect();
        }, 2000);
    }

    blockSocket.onmessage = function (e) {
        console.log("message is initiated");
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case "user_list":
                for (let i = 0; i < data.users.length; i++) {
                    groupBlockOnlineUsersConnect(data.users[i]);
                }
                break;
            case "user_connect":
                let blockChatConnect = document.createElement('p');
                blockChatConnect.className = 'connection';
                blockChatConnect.textContent = data.user + " " + "is connected to the block";
                groupBlockContainer.appendChild(blockChatConnect);
                groupBlockOnlineUsersConnect(data.user);
                break;
            case "user_disconnect":
                let blockChatDisconnect = document.createElement('p');
                blockChatDisconnect.className = 'connection';
                blockChatDisconnect.textContent = data.user + " " + "is disconnected to the block";
                groupBlockContainer.appendChild(blockChatDisconnect);
                groupBlockOnlineUsersDisconnect(data.user);
                break;
            case "block_message":
                let blockChatMessages = document.createElement('p');
                if (data.user_id === current_user_id) {
                    blockChatMessages.className = 'current_user';
                } else {
                    blockChatMessages.className = 'other_user';
                }

                blockChatMessages.textContent = data.user + ": " + data.message;
                groupBlockContainer.appendChild(blockChatMessages)
                break;
            default:
                console.error("message type unrecognised")
                break;
        };
        groupBlockContainer.scrollTop = groupBlockContainer.scrollHeight;
    }

    blockSocket.onerror = function (err) {
        console.log("Web socket Error: " + err.message);
        console.log("closing  the socket")
        blockSocket.close();
    }

}
connect();