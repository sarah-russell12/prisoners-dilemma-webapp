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
