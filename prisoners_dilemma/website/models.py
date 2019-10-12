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
<<<<<<< HEAD

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
    name = models.CharField(primary_key=True, max_length = 200, verbose_name="name of the game")
    player_one = models.ForeignKey(PlayerUser, on_delete=models.SET_NULL, verbose_name="player one", related_name="+", blank=True, null=True)
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
=======
    
>>>>>>> parent of 8abdd42... Started integrating socketio into project
