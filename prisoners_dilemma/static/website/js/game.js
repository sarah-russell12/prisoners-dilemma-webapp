// JavaScript source code
const socket = io.connect();

// Receiving messages
socket.on('connected', (message) => {
    console.log(message);
});

socket.on('message_received', (message) => {
    console.log('Your message was received by the server');
    console.log(message);
});

socket.on('enqueue_response', (message) => {
    console.log(message);
});

socket.on('game_created', (message) => {
    console.log(message["game_name"] + " created");
    window.localStorage.setItem("game_name", message["game_name"]);
    add_player();
});

socket.on('player_added', (message) => {
    // client recieves a "ONE" or "TWO" from the purpose of updating the game display
    console.log("You are player " + message["standin_id"]);
    window.localStorage.setItem("standin_id", message["standin_id"]);
});

socket.on('error', (message) => {
    console.log("Error: " + message["error"]);
    error_display(message);
});

socket.on('start_game', (message) => {
    console.log("Starting game");
    game_status_display();
    update_game_status_display(message);
    player_choice_display();
});

socket.on('player_action_response', (message) => {
    console.log("Game has logged a player's action");
    update_game_status_display(message);
    console.log("You are player " + window.localStorage.getItem("standin_id"));
});

socket.on('new_round', (message) => {
    console.log("A new round has started");
    update_game_status_display(message);
    player_choice_display();
})

socket.on('end_game', (message) => {
    console.log("End of game");
    update_game_status_display(message);
    end_game_display();
});

// Sending messages
function enqueue() {
    console.log("Sending queue request");
    socket.emit("enqueue");
    console.log("Queue request sent");
    waiting_for_game_display();
}

function add_player() {
    // client sends player id, if applicable, to the server
    console.log("Sending add player request")
    data = {};
    data.player_id = window.localStorage.getItem("player_id");
    data.game_name = window.localStorage.getItem("game_name");
    console.log(data);
    socket.emit("add_player", data);
    console.log("Add player request sent");
}

function cooperate() {
    console.log("Sending cooperate action");
    data = get_game_data();
    data.action = "COOP";
    console.log(data);
    socket.emit("player_action", data);
    console.log("Action sent");
    console.log("You")
    waiting_for_next_round_display();
}

function do_not_cooperate() {
    console.log("Sending no cooperation action");
    data = get_game_data();
    data.action = "SELF";
    console.log(data);
    socket.emit("player_action", data);
    console.log("Action sent");
    waiting_for_next_round_display();
}

function leave_game() {
    console.log("Sending leave game request");
    data = get_game_data();
    socket.emit("leave_game", data);
    console.log("Request sent");
    left_game_display();
}

function get_game_data() {
    data = {};
    data.player_id = get_player_id();
    data.game_name = window.localStorage.getItem("game_name");
    return data;
}

function get_player_id() {
    player_id = window.localStorage.getItem("player_id");
    if (player_id == "NONE") {
        return window.localStorage.getItem("standin_id");
    } else {
        return parseInt(player_id);
    }
}

function waiting_for_game_display() {
    // Show a waiting div for the game
    var p = document.createElement("p");
    p.innerText = "Waiting for a game";
    var wait_div = create_div("waiting", p)
    remove_div("start");
    add_div(wait_div);
}

function player_choice_display() {
    // Remove any waiting divs and show the game form
    var form = make_game_form();    
    var game_div = create_div("game", form);
    remove_div("waiting");
    add_div(game_div);
}

function waiting_for_next_round_display() {
    // Remove game form and show a waiting div
    var p = document.createElement("p");
    p.innerText = "Waiting for the next round";
    var wait_div = create_div("waiting", p);
    remove_div("game");
    add_div(wait_div);
}

function game_status_display() {
    // New game status display
    var game_name = create_game_status_line("Game Name: ", "game_name");
    var round = create_game_status_line("Round: ", "round");
    var your_points = create_game_status_line("Your Points: ", "your_points");
    var opponent_points = create_game_status_line("Oppponent's Points: ", "opponent_points");
    var your_action = create_game_status_line("Your Action: ", "your_action");
    var opponent_action = create_game_status_line("Opponent's Action: ", "opponent_action");
    var status_div = create_div("status", game_name);
    status_div.append(round, your_points, opponent_points, your_action, opponent_action);
    add_div(status_div);
}

function end_game_display() {
    var p = document.createElement("p");
    p.innerText = "Game Over! Would you like to play again?";
    var end_div = create_div("game", p);
    var button = document.createElement("button");
    button.type = "button";
    button.onclick = start_display;
    button.innerText = "Play Again";
    end_div.appendChild(button);
    add_div(end_div);
}

function start_display() {
    remove_div("game");
    remove_div("status");
    var p = document.createElement("p");
    p.innerText = "Press the button to queue for a game!";
    var start_div = create_div("start", p);
    var button = document.createElement("button");
    button.type = "button";
    button.onclick = "enqueue()";
    button.innerText = "Queue Up";
    start_div.appendChild(button);
    add_div(start_div);
}

function update_game_status_display(message) {
    document.getElementById("game_name").innerText = window.localStorage.getItem("game_name");
    document.getElementById("round").innerText = message["round"].toString();
    if (window.localStorage.getItem("standin_id") == "ONE") {
        update_status_player_one(message);
    }
    else if (window.localStorage.getItem("standin_id") == "TWO") {
        update_status_player_two(message);
    }
}

function error_display(message) {
    var err_p = document.createElement("p");
    err_p.innerText = message["error"];
    err_p.style.color = "red";
    var err_div = create_div("error", err_p);
    add_div(err_div);
}

function update_status_player_one(message) {
    document.getElementById("your_points").innerText = message["player_one_points"].toString();
    document.getElementById("your_action").innerText = message["player_one_action"];
    document.getElementById("opponent_points").innerText = message["player_two_points"].toString();
    document.getElementById("opponent_action").innerText = message["player_two_action"];
}

function update_status_player_two(message) {
    document.getElementById("your_points").innerText = message["player_two_points"].toString();
    document.getElementById("your_action").innerText = message["player_two_action"];
    document.getElementById("opponent_points").innerText = message["player_one_points"].toString();
    document.getElementById("opponent_action").innerText = message["player_one_action"];
}

function create_div(id, child) {
    var div = document.createElement("div");
    div.id = id;
    div.appendChild(child);
    return div;
}

function add_div(div) {
    document.getElementById("game_container").appendChild(div);
}

function remove_div(id) {
    var div = document.getElementById(id);
    document.getElementById("game_container").removeChild(div);
}

function make_game_form() {
    var form = document.createElement("form");
    var coop_button = create_cooperation_button();
    var self_button = create_self_button();
    var leave_button = create_leave_button();
    form.appendChild(coop_button);
    form.appendChild(self_button);
    form.appendChild(leave_button);
    return form;
}

function create_cooperation_button() {
    var button = document.createElement("button");
    button.innerText = "Cooperate";
    button.type = "button";
    button.onclick = cooperate;
    return button;
}

function create_self_button() {
    var button = document.createElement("button");
    button.innerText = "Don't Cooperate";
    button.type = "button";
    button.onclick = do_not_cooperate;
    return button;
}

function create_leave_button() {
    var button = document.createElement("button");
    button.innerText = "Leave Game";
    button.type = "button";
    // server side leave game not yet implemented
    // button.onclick = "leave_game()";
    return button;
}

function create_game_status_line(text, id) {
    var p = document.createElement("p");
    var span = document.createElement("span");
    span.id = id;
    p.append(text, span);
    return p;
}
