
from django.contrib import admin
from .models import Team, Player, Match, Registered, Table, Reported
# Register your models here.
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Registered)
admin.site.register(Table)
admin.site.register(Reported)
