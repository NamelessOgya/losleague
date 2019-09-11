
from django.db import models



class Team(models.Model):
    team_name = models.CharField(max_length=100)
    def __str__(self):
        return self.team_name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100)

    def __str__(self):
        return self.player_name

class Match(models.Model):
    match_date = models.DateTimeField('date published')

class Registered(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(max_length=100)
    first = models.CharField(max_length=100)
    second = models.CharField(max_length=100)
    third = models.CharField(max_length=100)
    fourth = models.CharField(max_length=100)
    fifth = models.CharField(max_length=100)
    hoketsu = models.CharField(max_length=100)

class Registerd(models.Model):
    date = models.CharField(max_length=100)








#Matchをdateではなくpkで管理したい。Matchに対してfor繰り返しができれば辞書化できるができないのでおぎゃ

