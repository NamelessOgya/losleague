#フォーム作成https://arakan-pgm-ai.hatenablog.com/entry/2019/02/14/090000

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from . import forms
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf

from .models import Match, Player, Team, Registerd, Registered, Table, Reported, PlayerResult, TeamResult
from django.contrib.auth.mixins import LoginRequiredMixin

def leader():
    return ["エルフ","ロイヤル", "ウィッチ", "ドラゴン", "ネクロマンサー", "ビショップ", "ネメシス"]

def strdate(d):
    year = d.year
    month = d.month
    day = d.day
    return str(year) + "/" + str(month) + "/" + str(day)




def home(request):
# Teamポイントの初期化
    for t in Team.objects.all():
        t.point = 0
        t.grosspoint = 0
        t.save()

# point,grosspointの再計算
    for m in Match.objects.all():
        try:
            for t in Table.objects.filter(date=m):
                point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
                team1 = t.team1.team_name
                point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
                team2 = t.team2.team_name
                x1 = Team.objects.filter(team_name = team1).order_by("-pk").first()
                x1.grosspoint += point1

                x2 = Team.objects.filter(team_name=team2).order_by("-pk").first()
                x2.grosspoint += point2
                if point1 >= 3:
                    x1.point += 1
                else:
                    x2.point += 1
                x1.save()
                x2.save()
        except AttributeError:
            pass
# チームポイント順で並び替えて上位チームを選抜
    dic = {}
    for t in Team.objects.all().order_by('-point')[:5]:
        name = t.team_name
        point = t.point
        grosspoint = t.grosspoint
        dic[name] = {"name": name, "point": point, "grosspoint": grosspoint}


    return render(request, 'home.html',{"dic": dic})


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

            dic[id] = strdate(d)

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
        dic[id] = strdate(d)

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
            DDD = strdate(d)
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

        dic[id] = strdate(d)

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

    dics = [{"player": first, "leader": firstl, "winlose": firstwl},
           {"player": second, "leader": secondl, "winlose": secondwl},
           {"player": third, "leader": thirdl, "winlose": thirdwl},
           {"player": fourth, "leader": fourthl, "winlose": fourthwl},
           {"player": fifth, "leader": fifthl, "winlose": fifthwl}]
# レポートに登録
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
#TeamResultに追加
    teamp = 0
    for d in dics:
        PlayerResult.objects.create(date = date, player = Player.objects.filter(player_name=d["player"]).order_by('-pk').first(), leader = d["leader"], wl = d["winlose"])
        if d["winlose"] == "win" :
            teamp+=1

    TeamResult.objects.create(date=date, team=team, point = teamp)

    return render(request, 'attendance/report_request.html')

def match_result(request):
    dicts = {}
    dic = {}
    for m in Match.objects.all():
            for t in Table.objects.filter(date=m):
                try:
                    point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
                    team1 = t.team1.team_name
                    point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
                    team2 = t.team2.team_name
                    dic[team1+" vs "+team2] = {"team1": team1, "point1": point1,"team2":team2,"point2": point2}
                except AttributeError:
                    pass
            date = strdate(m.match_date)
            dicts[date] = dic
            dic = {}



    return render(request, 'attendance/match_result.html', {'dicts': dicts})