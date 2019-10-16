// JavaScript source code
const socket = io.connect();

socket.on('connected', (message) => {
    console.log(message);
});

function enqueue() {
    console.log("Sending queue request");
    socket.emit("enqueue");
    console.log("Queue request sent");
}

socket.on("enqueue_response", (message) => {
    console.log(message);
    document.getElementById("queue").style.display = "none";
    document.getElementById("waiting").style.display = "initial";
});

socket.on("game_found", (message) => {
    console.log(message);
    document.getElementById("waiting").style.display = "none";
    document.getElementById("game").style.display = "initial";
    document.getElementById("game_name").innerText = message["game_name"];
    var data = {};
    data["player_id"] = $("#player_id").text();
    data["game_name"] = message["game_name"];
    socket.emit("connect_game", data);
});

socket.on("start_game", (message) => {
    console.log(message);
    document.getElementById("waiting").style.display = "none";
    document.getElementById("game").style.display = "initial";
    document.getElementById("game_name").innerText = message["game_name"];
});