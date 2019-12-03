"""
gamemanager.py

Creates games and passes input to them.  Returns events and data for socketio to process
"""

from .models import Game

from django.core.exceptions import ObjectDoesNotExist

def get_count():
    return Game.objects.count()

def create_game():
    response = {}
    try:
        name = "Game " + str(get_count() + 1)
        Game.new_game(name)
        response["game_name"] = name
        response["error"] = None
        return "game_created", response
    except:
        response["error"] = "Unable to create game"
        "error", response

def add_player(game_name, player_id):
    response = {}
    try:
        game = _get_game(game_name)
        return _add_player_to_existing_game(game, player_id)
    except ObjectDoesNotExist:
        return "error", response

def _add_player_to_existing_game(game, player_id):
    response = game.add_player(player_id)
    if response["error"]:
        return "error", response
    return "player_added_successfully", response

def _get_game(game_name):
    return Game.objects.get(name=game_name)