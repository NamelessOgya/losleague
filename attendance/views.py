#フォーム作成https://arakan-pgm-ai.hatenablog.com/entry/2019/02/14/090000

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from . import forms
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf

from .models import Match, Player, Team, Registerd, Registered
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    return render(request, 'home.html')

def logout(request):
    return render(request, 'logout.html')

@login_required
def index(request):
    m = Match.objects.all()
    dic = {}
    for x in m:
        id = x.id
        d = x.match_date
        year = d.year
        month = d.month
        day = d.day
        date = str(year)+"/"+str(month)+"/"+str(day)
        dic[id] = date

    context = {'dic': dic}
    return render(request, 'attendance/index.html', context)



@login_required
def date(request, date):
    x = Team.objects.filter(team_name=request.user).get()
    mylist = []
    for m in x.player_set.all():
        mylist.append(m.player_name)

    return render(request, 'attendance/date.html', {"date": date, "team_member": mylist})
@login_required
def result(request, date):
    # フォーム送信された値を受け取る
    first = request.GET.get('first')
    second = request.GET.get('second')
    third = request.GET.get('third')
    fourth = request.GET.get('fourth')
    fifth = request.GET.get('fifth')
    hoketsu = request.GET.get('hoketsu')
    #データベースに変更を加えるぉ
    m = Match.objects.all()
    match_instance = m.get(pk=int(date))
    Registered.objects.create(date=match_instance, team=request.user, first=first, second=second, third=third, fourth= fourth, fifth=fifth, hoketsu=hoketsu)

    r = Registered.objects.filter(team=request.user)
    m = Match.objects.all()
    dic = {}
    for x in m:  # Matchをforで回して、そのなかで一番古い登録データからfirst,...を抜く。未登録の場合は..
        try:
            order = r.filter(date=x).order_by('-pk').first()
            first = order.first
            second = order.second
            third = order.third
            fourth = order.fourth
            fifth = order.fifth
            hoketsu = order.hoketsu

            d = x.match_date
            year = d.year
            month = d.month
            day = d.day
            DDD = str(year) + "/" + str(month) + "/" + str(day)
            dic[DDD] = {'一番手': first, '二番手': second, '三番手': third, '四番手': fourth, '五番手': fifth,
                           'リザーバー': hoketsu}
        except AttributeError:
            pass

    return render(request, 'attendance/result.html', {'dic': dic})



