"""
sio.py

The server-side python-socketio code for queueing players and handling player input.
"""

from queue import Queue
from . import gamemanager as Manager

import os
import socketio

basedir = os.path.dirname(os.path.realpath(__file__))
SERVER = socketio.Server(async_mode='eventlet')
THREAD = None

PLAYER_QUEUE = Queue()

def server_update_thread():
    global SERVER
    while True:
        SERVER.sleep(10)
        _update_queue()
        SERVER.emit("connected", {"data" : "You are still connected"})

def run_thread():
    global SERVER
    global THREAD
    if THREAD is None:
        SERVER.start_background_task(server_update_thread)

def _update_queue():
    global PLAYER_QUEUE
    if PLAYER_QUEUE.qsize() >= 2:
        print("Attempting to start a game")
        player_1 = _get_player()
        player_2 = _get_player()
        # Instert start game here
        _start_game(player_1, player_2)

def _get_player():
    global PLAYER_QUEUE
    global SERVER
    player_sid = PLAYER_QUEUE.get()
    player_found = False
    while not player_found:
        try:
            session = SERVER.get_session(player_sid)
            # getting a session where the player has disconnected/closed raises a KeyError in engineio
            player_found = True
        except KeyError:
            player_sid = PLAYER_QUEUE.get()
    print("Found Player sid = " + str(player_sid))
    return player_sid

def _start_game(player_1, player_2):
    global SERVER
    print("Creating Game")
    event, data = Manager.create_game()
    game_name = data["game_name"]
    print(game_name + " created. Attempting to add players to room")
    SERVER.enter_room(player_1, game_name)
    SERVER.enter_room(player_2, game_name)
    print("Players added to room " + game_name + ". Alerting players")
    SERVER.emit(event, data = data, room = game_name)
    print("Players alerted")
    return

@SERVER.event
def connect(sid, environ):
    print("Player connected. sid = {sid}".format(sid=sid))
    SERVER.emit('connected', {'data' : 'You are connected'}, room=sid)

@SERVER.event
def disconnect(sid):
    SERVER.rooms(sid)
    print("Player disconnected. sid = {sid}".format(sid=sid))


@SERVER.on("enqueue")
def _queue_player(sid):
    print("Queueing player w/ sid {sid}".format(sid=sid))
    global PLAYER_QUEUE
    PLAYER_QUEUE.put(sid)
    SERVER.emit("enqueue_response", {"response" : "You have been queued"}, room=sid)

@SERVER.on("add_player")
def _register_player(sid, message):
    game_name = message["game_name"]
    player_id = message["player_id"]
    if game_name not in SERVER.rooms(sid):
        data = {"error": "You are not in " + game_name}
        SERVER.emit("error", data = data, room = sid)
        return
    event, data = Manager.add_player(game_name, player_id)
    print("In " + game_name + ", sid " + str(sid) + " will be player " + data["standin_id"])
    SERVER.emit(event, data = data, room = sid)
    if Manager.is_game_ready(game_name):
        print("Starting " + game_name)
        game_state = Manager.get_game_state(game_name)
        SERVER.emit("start_game", data = game_state, room = game_name)

@SERVER.on("player_action")
def _player_action(sid, message):
    game_name = message["game_name"]
    player_id = message["player_id"]
    action = message["action"]
    if game_name not in SERVER.rooms(sid):
        data = {"error": "You are not in " + game_name}
        SERVER.emit("error", data = data, room = sid)
        return
    event, data = Manager.player_action(game_name, player_id, action)
    if event == "error":
        SERVER.emit(event, data = data, room = sid)
    else:
        SERVER.emit(event, data = data, room = game_name)

@SERVER.on("dummy_message")
def _dummy_message(sid, message):
    print("A message was sent")
    SERVER.emit("message_received", data=message, room=sid)
