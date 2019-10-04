from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class PlayerUser(AbstractUser):
    # tracks points earned from every game, as well as the number of times
    # the player has cooperated
    points = models.IntegerField(default=0)
    cooperative_actions = models.IntegerField(default=0)
    games_completed = models.IntegerField(default=0)
    
    cooperative_score = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    def __str__(self):
        return self.username
    
    def updateCooperativeScore(self):
        if self.games_completed == 0:
            self.cooperative_score = 0
        else:
            self.cooperative_score = self.cooperative_actions / (self.games_completed * 10)

class GameManager():
    def __init__(self):
        models.Manager.__init__(self)
        self.game_count = Game.objects.count()

    def create_game():
        self.game_count += 1
        name = "game{count}".format(count=self.game_count)
        game = Game(name=name)
        game.save()
        return name

    def register_player(game_name, is_player_one, player_id=None):
        game = Games.objects.get(name__iexact=game_name)
        if is_player_one and player_id:
            game.player_one = PlayerUser.objects.get(pk=player_id)
        elif player_id:
            game.player_two = PlayerUser.objects.get(pk=player_id)
        game.save()

    def update_game(game_name, is_player_one, action):
        game - Games.objects.get(name__iexact=game_name)
        messages = game.update(is_player_one, action)


class Game(models.Model):
    name = models.CharField(primary_key=True, verbose_name="name of the game")
    player_one = models.ForeignKey(PlayerUser, on_delete=models.SET_NULL, verbose_name="player one", blank=True, null=True)
    self.player_one
    player_two = models.ForeignKey(PlayerUser, on_delete=models.SET_NULL, verbose_name="player two", blank=True, null=True)
    round = models.IntegerField(verbose_name="current round of the game", default=1)
    
    PLAYER_ACTIONS = [
        ("COOP", "COOPERATE"),
        ("SELF", "NOT COOPERATE"),
        ("NONE", "AWAITING ACTION"),
    ]

    player_one_action = models.CharField(max_length=4, choices=PLAYER_ACTIONS, default="NONE", verbose_name="player one's action this round")
    player_two_action = models.CharField(max_length=4, choices=PLAYER_ACTIONS, default="NONE", verbose_name="player two's action this round")

    player_one_points = models.IntegerField(verbose_name="points player one has earned", default=0)
    player_two_points = models.IntegerField(verbose_name="points player two has earned", default=0)

    def update(is_player_one, action):
        if is_player_one:
            self.player_one_action = action
        else:
            self.player_two_action = action
        self.save()
        messages = _check_round_change()
        return messages

    def _check_round_change():
        messages = {}
        if is_complete():
            _end_game()
            messages = _get_end_game_messages()
        elif _round_over():
            pass
        else:
            pass
        return messages

    def is_complete():
        return (self.round == 10) and _round_over()

    def _end_game():
        if self.player_one:
            _update_player(1)
        if self.player_two:
            _update_player(2)

    def _update_player(player):
        pass


    def _round_over():
        return (self.player_one_action != "NONE") and (self.player_two_action != "NONE")
    
            