#フォーム作成https://arakan-pgm-ai.hatenablog.com/entry/2019/02/14/090000

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from . import forms
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf

from .models import Match, Player, Team, Registerd, Registered, Table, Reported
from django.contrib.auth.mixins import LoginRequiredMixin

def leader():
    return ["エルフ","ロイヤル", "ウィッチ", "ドラゴン", "ネクロマンサー", "ビショップ", "ネメシス"]



def home(request):
    return render(request, 'home.html')


def user (request):
    return render(request, 'attendance/user.html')

def logout(request):
    return render(request, 'logout.html')

def listdate(request):
        m = Match.objects.all().filter(match_table_release=True)
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

        return render(request, 'attendance/listdate.html', context)



def list(request, date):
    t = Table.objects.filter(date=Match.objects.filter(pk=date).get())

    dic = {}
    c = 0
    for x in t:
        c+=1
        try:
            r1 = Registered.objects.filter(date=x.date, team=x.team1).order_by('-pk').first()
            r2 = Registered.objects.filter(date=x.date, team=x.team2).order_by('-pk').first()
            order1 = [r1.first, r1.second, r1.third, r1.fourth, r1.fifth, r1.hoketsu]
            order2 = [r2.first, r2.second, r2.third, r2.fourth, r2.fifth, r2.hoketsu]
            dic[str(c)+x.team1.team_name+" vs "+x.team2.team_name] = {x.team1.team_name: order1, x.team2.team_name: order2}
        except AttributeError:
            dic[str(c)] = {c: "", c: ""}
    return render(request, 'attendance/table.html', {'dic': dic})

@login_required
def index(request):
    m = Match.objects.all().filter(register_release=True)
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

@login_required
def reportdate(request):
    m = Match.objects.all()#あとでfilterつける
    dic = {}
    for x in m:
        id = x.id
        d = x.match_date
        year = d.year
        month = d.month
        day = d.day
        date = str(year) + "/" + str(month) + "/" + str(day)
        dic[id] = date

    context = {'dic': dic}

    return render(request, 'attendance/reportdate.html', context)
@login_required
def report(request, date):

    r = Registered.objects.filter(team = request.user).filter(date=Match.objects.all().filter(pk=date).get()).order_by('-pk').first()
    mylist = [r.first, r.second, r.third, r.fourth, r.fifth, r.hoketsu]
    context = {'team_member': mylist, 'winlose': ["win", "lose"], 'leader': leader(), 'date': date}
    return render(request, 'attendance/report.html', context)
@login_required
def report_register(request,date):
    team = request.user
    date = Match.objects.filter(pk=date).order_by('-pk').first()

    first = request.GET.get('first')
    second = request.GET.get('second')
    third = request.GET.get('third')
    fourth = request.GET.get('fourth')
    fifth = request.GET.get('fifth')

    firstl = request.GET.get('firstl')
    secondl = request.GET.get('secondl')
    thirdl = request.GET.get('thirdl')
    fourthl = request.GET.get('fourthl')
    fifthl = request.GET.get('fifthl')

    firstwl = request.GET.get('firstwl')
    secondwl = request.GET.get('secondwl')
    thirdwl = request.GET.get('thirdwl')
    fourthwl = request.GET.get('fourthwl')
    fifthwl = request.GET.get('fifthwl')

    Reported.objects.create(
    date=date,
    team=team,

    first = first,
    second = second,
    third = third,
    fourth = fourth,
    fifth = fifth,

    firstl = firstl,
    secondl =secondl,
    thirdl = thirdl,
    fourthl = fourthl,
    fifthl = fifthl,

    firstwl = firstwl,
    secondwl = secondwl,
    thirdwl = thirdwl,
    fourthwl = fourthwl,
    fifthwl = fifthwl,
    )

    return render(request, 'attendance/report_request')

