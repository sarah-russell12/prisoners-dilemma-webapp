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
    document.getElementById("waiting").style.display = "normal";
});

socket.on("game_found", (message) => {
    console.log(message);
    document.getElementById("waiting").style.display = "none";
    document.getElementById("game_name").innerText = message["game_name"];
});