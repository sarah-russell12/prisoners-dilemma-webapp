"""
gamemanager.py

Creates games and passes input to them
"""

from .models import Game

class GameManager(object):
    @staticmethod
    def get_count():
        return Game.objects.count()

    @staticmethod
    def add_game(game_name):
        if not Game.is_active_game(game_name):
            game = Game.new_game(game_name, player_id)
        return

    @staticmethod
    def add_player(game_name, player_id, player_one=True):
        game = Game.objects.get(name=game_name)
        if player_one:
            game.player_one_id = player_id
        else:
            game.player_two_id = player_id
        game.save()
        return

