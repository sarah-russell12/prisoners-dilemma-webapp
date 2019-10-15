"""
sio.py

The server-side python-socketio code for queueing players and handling player input.
"""

from queue import Queue

import os
import socketio

basedir = os.path.dirname(os.path.realpath(__file__))
SERVER = socketio.Server(async_mode='eventlet')
THREAD = None

COUNT = 0

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
    if PLAYER_QUEUE.qsize() > 2:
        player_1 = _get_player()
        player_2 = _get_player()
        # Instert start game here
        _start_game(player_1, player_2)

def _get_player():
    global PLAYER_QUEUE
    global SERVER
    player_sid = PLAYER_QUEUE.get()
    while True:
        try:
            session = SERVER.get_session(player_sid)
            # getting a session where the player has disconnected/closed raises a KeyError in engineio
            break
        except KeyError:
            player_sid = PLAYER_QUEUE.get()
    return player_sid

def _start_game(player_1, player_2):
    global COUNT
    global SERVER
    COUNT += 1
    room = "Game " + str(COUNT)
    SERVER.enter_room(player1, room)
    SERVER.enter_room(player2, room)
    data = {"game_name" : room}
    SERVER.emit("game_found", data = data, room = room)
    return

@SERVER.event
def connect(sid, environ):
    print("Player connected. sid = {sid}".format(sid=sid))
    server.emit('connected', {'data' : 'You are connected'}, room=sid)

@SERVER.event
def disconnect(sid):
    print("Player disconnected. sid = {sid}".format(sid=sid))


@SERVER.on("enqueue")
def _queue_player(sid):
    print("Queueing player w/ sid {sid}".format(sid=sid))
    global PLAYER_QUEUE
    PLAYER_QUEUE.put(sid)
    SERVER.emit("enqueue_response", {"response" : "You have been queued"}, room=sid)

