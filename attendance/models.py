
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
    match_table_release =  models.BooleanField(verbose_name='マッチング表の公表', default=False,)
    register_release = models.BooleanField(verbose_name='登録ページの公表', default=False,)
    def __str__(self):
        return str(self.match_date)

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

class Table(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name = "team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name = "team2")










#Matchをdateではなくpkで管理したい。Matchに対してfor繰り返しができれば辞書化できるができないのでおぎゃ

