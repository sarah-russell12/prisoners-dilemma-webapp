from django.conf import settings
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
    
    def update_cooperative_score(self):
        if self.games_completed == 0:
            self.cooperative_score = 0
        else:
            self.cooperative_score = self.cooperative_actions / (self.games_completed * 10)
        self.save()
        return

    def completed_game(self, points, coop):
        self.points += points
        self.cooperative_actions += coop
        self.games_completed += 1
        self.save()

        self.update_cooperative_score()
        return


class Game(models.Model):
    name = models.CharField(primary_key=True, max_length = 200, verbose_name="name of the game")
    player_one = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="player one", related_name="+", blank=True, null=True)
    player_two = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="player two", blank=True, null=True)
    is_player_one_present = models.BooleanField(verbose_name="Is there an unregistered player one", default=False)
    is_player_two_present = models.BooleanField(verbose_name="Is there an unregistered player two", default=False)
    player_one_coop = models.IntegerField(verbose_name="player one's cooperative actions this game", default=0)
    player_two_coop = models.IntegerField(verbose_name="player two's cooperative actions this game", default=0)
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

    def add_player(self, player_id):
        if self.is_player_one_present == False:
            return self._add_player_one(player_id)
        elif self.is_player_two_present == False:
            return self._add_player_two(player_id)
        else:
            return self._response_player_addition(self.name + " is full", player_id, "NONE")

    def _add_player_one(self, player_id):
        if player_id != "NONE":
            try:
                self.player_one = PlayerUser.objects.get(pk=player_id)
            except ObjectDoesNotExist:
                return self._response_player_addition("Invalid player ID", player_id, "NONE")
        self.is_player_one_present = True
        self.save()
        return self._response_player_addition(None, player_id, "ONE")

    def _add_player_two(self, player_id):
        if player_id != "NONE":
            try:
                self.player_two = PlayerUser.objects.get(pk=player_id)
            except ObjectDoesNotExist:
                return self._response_player_addition("Invalid player ID", player_id, "NONE")
        self.is_player_two_present = True
        self.save()
        return self._response_player_addition(None, player_id, "TWO")

    def _response_player_addition(self, err, player_id, standin_id):
        return {"error" : err, "player_id" : player_id, "standin_id" : standin_id}

    def is_complete(self):
        return self.round == 10 and self.round_complete()

    def round_complete(self):
        return self.player_one_action != "NONE" and self.player_two_action != "NONE"

    def action(self, player_id, action):
        if self.is_complete():
            return self._error_completed_game()
        if player_id == self.player_one_id or player_id == "ONE":
            if self.player_one_action != "NONE":
                return self._error_already_acted()
            self.player_one_action = action
        elif player_id == self.player_two_id or player_id == "TWO":
            if self.player_two_action != "NONE":
                return self._error_already_acted()
            self.player_two_action = action
        else:
            return self._error_player_not_in_game()
        self.save()
        return self._resolve_round()

    def _error_completed_game(self):
        response = self.get_game_state()
        response["error"] = self.name + " is already completed"
        return response

    def _error_already_acted(self):
        response = self.get_game_state()
        response["error"] = "You have already acted this round"
        return response

    def _error_player_not_in_game(self):
        response = self.get_game_state()
        response["error"] = "You are not a player in " + self.name
        return response

    def _resolve_round(self):
        if self.is_complete():
            self._resolve_points()
            response = self.get_game_state()
            self._end_game()
        elif self.round_complete():
            self._resolve_points()
            response = self.get_game_state()
            self._next_round()
        else:
            response = self.get_game_state()
        return response

    def _resolve_points(self):
        if self.player_one_action == "COOP" and self.player_two_action == "COOP":
            self.player_one_points += 3
            self.player_two_points += 3
            self.player_one_coop += 1
            self.player_two_coop += 1
        elif self.player_one_action == "COOP" and self.player_two_action == "SELF":
            self.player_one_points += 0
            self.player_two_points += 5
            self.player_one_coop += 1
        elif self.player_one_action == "SELF" and self.player_two_action == "COOP":
            self.player_one_points += 5
            self.player_two_points += 0
            self.player_two_coop += 1
        else:
            self.player_one_points += 1
            self.player_two_points += 1
        self.save()
        return

    def _end_game(self):
        if self.player_one != None:
            player_one = PlayerUser.objects.get(pk=self.player_one_id)
            player_one.completed_game(self.player_one_points, self.player_one_coop)
            player_one.save()
        if self.player_two != None:
            player_two = PlayerUser.objects.get(pk=self.player_two_id)
            player_two.completed_game(self.player_two_points, self.player_two_coop)
            player_two.save()
        return

    def _next_round(self):
        self.round += 1
        self.player_one_action = "NONE"
        self.player_two_action = "NONE"
        self.save()

    def get_game_state(self):
        response = {}
        response["player_one_points"] = self.player_one_points
        response["player_two_points"] = self.player_two_points
        response["round"] = self._get_round()
        response["player_one_action"] = self._get_player_one_action()
        response["player_two_action"] = self._get_player_two_action()
        response["error"] = None
        return response

    def _get_round(self):
        if self.round_complete() and not self.is_complete():
            return self.round + 1
        else:
            return self.round

    def _get_player_one_action(self):
        if self.round_complete():
            if self.player_one_action == "COOP":
                return "cooperated"
            else:
                return "did not cooperate"
        else:
            if self.player_one_action != "NONE":
                return "acted"
            else:
                return "not acted yet"

    def _get_player_two_action(self):
        if self.round_complete():
            if self.player_two_action == "COOP":
                return "cooperated"
            else:
                return "did not cooperate"
        else:
            if self.player_two_action != "NONE":
                return "acted"
            else:
                return "not acted yet"

    @classmethod
    def new_game(self, game_name):
        game = Game.objects.create(name=game_name)
        game.save()
        return game

    @staticmethod
    def is_active_game(game_name):
        try:
            game = Game.objects.get(name=game_name)
        except ObjectDoesNotExist:
            return False
        return (not game.is_complete()) and game._are_both_players_present()

    def _are_both_players_present(self):
        return self.is_player_one_present and self.is_player_two_present
