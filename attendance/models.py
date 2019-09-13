
from django.db import models



class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_point = models.IntegerField(verbose_name='', blank=True, null=True, default=0)

    def __str__(self):
        return self.team_name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100)

    def __str__(self):
        return self.player_name

class Match(models.Model):
    match_date = models.DateTimeField('date published')
    match_table_release = models.BooleanField(verbose_name='マッチング表の公表', default=False)
    register_release = models.BooleanField(verbose_name='登録ページの公表', default=False,)


    def __str__(self):
        return str(self.match_date)

class Registered(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(max_length=100, default="")

    first = models.CharField(max_length=100, default="")#登録メンバー
    second = models.CharField(max_length=100, default="")
    third = models.CharField(max_length=100, default="")
    fourth = models.CharField(max_length=100, default="")
    fifth = models.CharField(max_length=100, default="")
    hoketsu = models.CharField(max_length=100, default="")

    def __str__(self):
            return str(self.date)+"/"+self.team


class Registerd(models.Model):
    date = models.CharField(max_length=100, default="")

class Table(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")

    def __str__(self):
            return self.team1.team_name+"/"+self.team2.team_name+"/"+str(self.date)

class Reported(models.Model):
    date = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(max_length=100, default="")

    first = models.CharField(max_length=100, default="")#登録メンバー
    second = models.CharField(max_length=100, default="")
    third = models.CharField(max_length=100, default="")
    fourth = models.CharField(max_length=100, default="")
    fifth = models.CharField(max_length=100, default="")

    firstl = models.CharField(max_length=100, default="")  # 登録メンバー
    secondl = models.CharField(max_length=100, default="")
    thirdl = models.CharField(max_length=100, default="")
    fourthl = models.CharField(max_length=100, default="")
    fifthl = models.CharField(max_length=100, default="")

    firstwl = models.CharField(max_length=100, default="")  # 登録メンバー
    secondwl = models.CharField(max_length=100, default="")
    thirdwl = models.CharField(max_length=100, default="")
    fourthwl = models.CharField(max_length=100, default="")
    fifthwl = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.date) + "/" + self.team





