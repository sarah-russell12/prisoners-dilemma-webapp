"""
gamemanager.py

Creates games and passes input to them.  Returns events and data for socketio to process
"""

from .models import Game

from django.core.exceptions import ObjectDoesNotExist

def get_count():
    return Game.objects.count()

def create_game():
    try:
        name = "Game " + str(get_count() + 1)
        Game.new_game(name)
        response = {"game_name" : name, "error" : None}
        return "game_created", response
    except:
        response = {"error" : game_name + " is not the name of an existing game"}
        "error", response

def add_player(game_name, player_id):
    try:
        game = _get_game(game_name)
        return _add_player_to_existing_game(game, player_id)
    except ObjectDoesNotExist:
        response = {"error" : game_name + " is not the name of an existing game"}
        return "error", response

def _add_player_to_existing_game(game, player_id):
    response = game.add_player(player_id)
    if response["error"]:
        return "error", response
    return "player_added", response

def _get_game(game_name):
    return Game.objects.get(name=game_name)

def player_action(game_name, player_id, action):
    try:
        game = _get_game(game_name)
        return _player_action_in_existing_game(game, player_id, action)
    except ObjectDoesNotExist:
        response = {"error" : game_name + " is not the name of an existing game"}
        return "error", response

def _player_action_in_existing_game(game, player_id, action):
    prev_state = game.get_game_state()
    response = game.action(player_id, action)
    if response["error"]:
        return "error", response
    if game.is_complete():
        return "end_game", response
    elif prev_state["round"] < response["round"]:
        return "new_round", response
    else:
        return "player_action_response", response

def is_game_ready(game_name):
    return Game.is_active_game(game_name)

def get_game_state(game_name):
    try:
        game = _get_game(game_name)
        return game.get_game_state()
    except ObjectDoesNotExist:
        response = {"error" : game_name + " is not the name of an existing game"}
        return response
