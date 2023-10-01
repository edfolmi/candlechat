console.log("Running from blockblock.js")

let privateBlockContainer = document.querySelector('#privateBlockContainer');
let privateBlockMessageInput = document.querySelector('#privateBlockMessageInput');
let privateBlockMessageSend = document.querySelector('#privateBlockMessageSend');

privateBlockMessageInput.focus();

privateBlockMessageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {
        privateBlockMessageSend.click();
    }
}

privateBlockMessageSend.onclick = function () {
    if (privateBlockMessageInput.value.length === 0) return;
    privateChatSocket.send(JSON.stringify({
        'message': privateBlockMessageInput.value
    }));

    console.log(privateBlockMessageInput.value);
    privateBlockMessageInput.value = "";
}

let current_user_id = JSON.parse(document.getElementById('current_user_id').textContent);
console.log("Current login user: " + current_user_id)

let messagesFetched = false;

function displayMessages() {
    let user_id = window.location.pathname.split('/').slice(-2, -1)[0];
    if (messagesFetched) return;

    fetch("/private_api_messages/" + user_id + "/")
        .then(response => {
            console.log(response);
            return response.json();
        })
        .then(messages => {
            console.log(messages);
            messages.forEach(message => {
                let blockMessage = document.createElement('p');
                //console.log("message user id: " + message.user.id);
                if (message.user.id === current_user_id) {
                    blockMessage.className = 'current_user';
                } else {
                    blockMessage.className = 'other_user';
                }
                blockMessage.textContent = message.message;
                privateBlockContainer.appendChild(blockMessage);
            });
            messagesFetched = true;
            privateBlockContainer.scrollTop = privateBlockContainer.scrollHeight;
        })
        .catch(error => console.log("Error fetching saved messages: ", error));
}

displayMessages();

let privateChatSocket = null;

//let userId = JSON.parse(document.getElementById('userId').textContent);
//let userId = event.target.dataset.userId;
function connect() {
    let userId = window.location.pathname.split('/').slice(-2, -1)[0];
    privateChatSocket = new WebSocket("ws://" + window.location.host + "/ws/privateblock/" + userId + "/");

    privateChatSocket.onopen = function (e) {
        console.log("private websocket connected")
    }

    privateChatSocket.onclose = function (e) {
        console.log("private websocket closed unexpected. trying to reconnect .....")
        setTimeout(function () {
            console.log("reconnecting...")
            connect();
        }, 2000);
    }

    privateChatSocket.onmessage = function (e) {
        console.log("private message initiated")
        const data = JSON.parse(e.data)
        console.log(data)

        switch (data.type) {
            case "private_block_message":
                let blockMessage = document.createElement('p');
                console.log("This is data user id: " + data.user_id);
                if (data.user_id === current_user_id) {
                    blockMessage.className = 'current_user';
                } else {
                    blockMessage.className = 'other_user';
                }

                blockMessage.textContent = data.message;
                privateBlockContainer.appendChild(blockMessage);
                break;
            default:
                console.error("private message not recognised");
                break;
        };
        privateBlockContainer.scrollTop = privateBlockContainer.scrollHeight;
    }

    privateChatSocket.onerror = function (err) {
        console.log("private web socket error: " + err.message);
        console.log("closing socket...")
        privateChatSocket.close()
    }
}
connect();

