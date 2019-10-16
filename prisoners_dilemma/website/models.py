from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
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

    def is_complete(self):
        return self.round == 10 and self._round_complete()

    def _round_complete(self):
        return self.player_one_action is not "NONE" and self.player_two_action is not "NONE"

    def resolve_round(self):
        if self._round_complete():
            messages = self._resolve_points()
            self._next_round()
        else:
            messages = self._waiting_on_player()
        return messages

    def _resolve_points(self):
        if self.player_one_action == "COOP" and self.player_two_action == "COOP":
            messages = self._both_cooperate()
        elif self.player_one_action == "COOP" and self.player_two_action == "SELF":
            messages = self._player_two_advantage()
        elif self.player_one_action == "SELF" and self.player_two_action == "COOP":
            messages = self._player_one_advantage()
        else:
            messages = self._both_selfish()
        return messages

    def _both_cooperate(self):
        self.player_one_points += 3
        self.player_two_points += 3
        self.save()
        message_1 = {"your_action" : "cooperate", "opponent_action" : "cooperate", "your_points" : self.player_one_points, "opponent_points" : self.player_two_points}
        message_2 = {"your_action" : "cooperate", "opponent_action" : "cooperate", "your_points" : self.player_two_points, "opponent_points" : self.player_one_points}
        return (message_1, message_2)

    def _player_two_advantage(self):
        self.player_one_points += 0
        self.player_two_points += 5
        self.save()
        message_1 = {"your_action" : "cooperate", "opponent_action" : "not cooperate", "your_points" : self.player_one_points, "opponent_points" : self.player_two_points}
        message_2 = {"your_action" : "not cooperate", "opponent_action" : "cooperate", "your_points" : self.player_two_points, "opponent_points" : self.player_one_points}
        return (message_1, message_2)

    def _player_one_advantage(self):
        self.player_one_points += 5
        self.player_two_points += 0
        self.save()
        message_1 = {"your_action" : "not cooperate", "opponent_action" : "cooperate", "your_points" : self.player_one_points, "opponent_points" : self.player_two_points}
        message_2 = {"your_action" : "cooperate", "opponent_action" : "not cooperate", "your_points" : self.player_two_points, "opponent_points" : self.player_one_points}
        return (message_1, message_2)

    def _both_selfish(self):
        self.player_one_points += 1
        self.player_two_points += 1
        self.save()
        message_1 = {"your_action" : "not cooperate", "opponent_action" : "not cooperate", "your_points" : self.player_one_points, "opponent_points" : self.player_two_points}
        message_2 = {"your_action" : "not cooperate", "opponent_action" : "not cooperate", "your_points" : self.player_two_points, "opponent_points" : self.player_one_points}
        return (message_1, message_2)

    def _next_round(self):
        self.round += 1
        self.player_one_action = "NONE"
        self.player_two_action = "NONE"
        self.save()

    def _waiting_on_player(self):
        if self.player_one_action == "NONE":
            message_1 = {"status" : "your opponent has acted"}
            message_2 = {"status" : "waiting on your opponent"}
        else:
            message_1 = {"status" : "waiting on your opponent"}
            message_2 = {"status" : "your opponent has acted"}
        return (message_1, message_2)

    @classmethod
    def new_game(game_name):
        game = Game.objects.create(name=game_name)
        return game

    @staticmethod
    def is_active_game(game_name):
        try:
            game = Game.objects.get(name=game_name)
        except ObjectDoesNotExist:
            return False
        return not game.is_complete()
