from django.contrib.auth.models import AbstractUser
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class User(AbstractUser):
    is_player = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    birth_date = models.DateField(null=True, blank=True)
    games = models.ManyToManyField('Game', through='GamePlayer', related_name='players')

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='coach')

class Game(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='game_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='game_team2')
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()
    date = models.DateField(null=True, blank=True)

class GamePlayer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, related_name='game_players', null=True)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='game_players', null=True)
    score = models.IntegerField()
