#フォーム作成https://arakan-pgm-ai.hatenablog.com/entry/2019/02/14/090000

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from . import forms
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
import threading
from threading import Thread
from .models import Match, Player, Team, Registerd, Registered, Table, Reported, PlayerResult, TeamResult, ClassWinRate, Blog, DeckCode
from django.contrib.auth.mixins import LoginRequiredMixin
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options


def leader():
    return ["エルフ","ロイヤル", "ウィッチ", "ドラゴン", "ヴァンパイア", "ネクロマンサー", "ビショップ", "ネメシス"]

def strdate(d):
    year = d.year
    month = d.month
    day = d.day
    return str(year) + "/" + str(month) + "/" + str(day)




def home(request):
# チームポイント順で並び替えて上位チームを選抜
    dic1 = {}
    dic2 = {}
    dic3 = {}
    dic4 = {}
#get top5 teams
    for t in Team.objects.all().order_by('-point')[:5]:

        name = t.team_name
        point = t.point
        grosspoint = t.grosspoint
        dic1[name] = {"name": name, "point": point, "grosspoint": grosspoint}
# 勝利数トップ5を抽出
    for p in Player.objects.all().order_by('-win')[:5]:

        name = p.player_name
        win = p.win
        lose = p.lose
        dic2[name] = {"name": name, "win": win, "lose": lose}

# リーダーごとの勝利数を回収
    for c in ClassWinRate.objects.all():
        name = c.leader
        rate = c.rate
        total = c.total
        dic3[name] = {"name": name, "rate": rate, "total": total}

#ブログ内容を回収
    for b in Blog.objects.all():
        title = b.title
        context = b.context
        dic4[title]= {"title": title, "context": context}

    return render(request, 'home.html', {"dic1": dic1, "dic2": dic2, "dic3": dic3, "dic4": dic4})

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
def report_register(request, date):

    def register(date):
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
    #PlayerResultとTeamResultに追加
        teamp = 0
        for d in dics:
            PlayerResult.objects.create(date = date, player = Player.objects.filter(player_name=d["player"]).order_by('-pk').first(), leader = d["leader"], wl = d["winlose"])
            if d["winlose"] == "win" :
                teamp+=1

        TeamResult.objects.create(date=date, team=team, point = teamp)
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

        # Teamポイントの初期化
        for t in Team.objects.all():
            t.point = 0
            t.grosspoint = 0
            t.save()

        #Playerポイントの初期化
        for p in Player.objects.all():
            p.win = 0
            p.lose = 0
            p.e_win = 0
            p.e_lose = 0
            p.nm_win = 0
            p.nm_lose = 0
            p.d_win = 0
            p.d_lose = 0
            p.b_win = 0
            p.b_lose = 0
            p.r_win = 0
            p.r_lose = 0
            p.v_win = 0
            p.v_lose = 0
            p.w_win = 0
            p.w_lose = 0
            p.nc_win = 0
            p.nc_lose = 0
            p.save()
    #ClassWinRateの初期化
        for c in ClassWinRate.objects.all():
            c.win = 0
            c.lose = 0
            c.rate = 0
            c.total = 0
            c.save()

        # point,grosspointの再計算
        for m in Match.objects.all():
            try:
                for t in Table.objects.filter(date=m):
                        point1 = TeamResult.objects.filter(date=m, team=t.team1.team_name).order_by("-pk").first().point
                        team1 = t.team1.team_name
                        point2 = TeamResult.objects.filter(date=m, team=t.team2.team_name).order_by("-pk").first().point
                        team2 = t.team2.team_name
                        x1 = Team.objects.filter(team_name=team1).order_by("-pk").first()
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

    # プレイヤーオブジェクトにクラス別戦績を追加
            for p in Player.objects.all():
                try:
                            pr = PlayerResult.objects.filter(date=m, player=p).order_by("-pk").first()
                            if pr.leader=="エルフ":
                                if pr.wl == "win":
                                    p.e_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="エルフ").get()
                                    c.win += 1
                                    c.save()


                                else:
                                    p.e_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="エルフ").get()
                                    c.lose += 1
                                    c.save()


                            elif pr.leader == "ネメシス":
                                if pr.wl == "win":
                                    p.nm_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ネメシス").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.nm_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ネメシス").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ドラゴン":
                                if pr.wl == "win":
                                    p.d_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ドラゴン").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.d_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ドラゴン").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ビショップ":
                                if pr.wl == "win":
                                    p.b_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ビショップ").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.b_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ビショップ").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ロイヤル":
                                if pr.wl == "win":
                                    p.r_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ロイヤル").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.r_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ロイヤル").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ヴァンパイア":
                                if pr.wl == "win":
                                    p.v_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ヴァンパイア").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.v_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ヴァンパイア").get()
                                    c.lose += 1
                                    c.save()

                            elif pr.leader == "ウィッチ":
                                if pr.wl == "win":
                                    p.w_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ウィッチ").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.w_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ウィッチ").get()
                                    c.lose += 1
                                    c.save()

                            else:
                                if pr.wl == "win":
                                    p.nc_win += 1
                                    p.win += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ネクロマンサー").get()
                                    c.win += 1
                                    c.save()

                                else:
                                    p.nc_lose += 1
                                    p.lose += 1
                                    p.save()
                                    c = ClassWinRate.objects.filter(leader="ネクロマンサー").get()
                                    c.lose += 1
                                    c.save()

                except AttributeError:
                        pass

        for c in ClassWinRate.objects.all():
           try:
                total = c.win+c.lose
                c.rate = c.win/total*100
                c.total = c.win + c.lose
                c.save()

           except   ZeroDivisionError:
               pass

    s_threading = threading.Thread(target=register(date))
    s_threading.start()

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

def deck_date(request):
    m = Match.objects.all().filter(register_release=True)
    dic = {}
    for x in m:
        id = x.id
        d = x.match_date
        dic[id] = strdate(d)

    context = {'dic': dic}
    return render(request, 'attendance/deck_date.html', context)

def deck_table(request, date):
    x = Match.objects.filter(pk=date).get()
    t = Table.objects.filter(date=x)
    dict={}
    for x in t:
        vs = x.team1.team_name+" vs "+x.team2.team_name
        dict[x.team1] = vs
    return render(request, 'attendance/deck_table.html', {"date": date, "dict": dict})

def deck_register(request, team, date):
    t = Team.objects.filter(team_name=team).get()
    m = Match.objects.filter(pk=date).get()
    table = Table.objects.filter(date=m, team1=t).get()
    team1 = table.team1
    team2 = table.team2
    player1 = Registered.objects.filter(date=m, team=team1).get()
    player2 = Registered.objects.filter(date=m, team=team2).get()
    list = []
    for p in [player1.first, player1.second, player1.third, player1.fourth, player1.fifth, player1.hoketsu]:
        list.append(p)
    for p in [player2.first, player2.second, player2.third, player2.fourth, player2.fifth, player2.hoketsu]:
        list.append(p)

    return render(request, "attendance/deck_register.html", {"date": date, "list": list, "team1": team1})

def deck_result(request, date, team1):
    m = Match.objects.filter(pk=date).get()
    t = Team.objects.filter(team_name=team1).get()
    player = Player.objects.filter(player_name=request.GET.get('player')).get()
    opp = Player.objects.filter(player_name=request.GET.get('opposite')).get()
    code = request.GET.get('code')
    table = Table.objects.filter(date=m, team1=t).get()


    URL = 'https://shadowverse-portal.com/deckbuilder/classes?lang=jahttps://shadowverse-portal.com/deckbuilder/classes?lang=ja'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    element = driver.find_element_by_id("deckCode")
    element.send_keys(code)
    button = driver.find_element_by_link_text("決定")
    button.click()
    driver.implicitly_wait(60)
    cardlist = []
    countlist = []
    n = 1
    while True:
        try:
            driver.implicitly_wait(10)
            card = '/html/body/div/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div[3]/div[2]/ul/li[' + str(
                n) + ']/div/p[3]/span'
            count = '/html/body/div/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div[3]/div[2]/ul/li[' + str(
                n) + ']/div/span'
            card = driver.find_element_by_xpath(card)
            count = driver.find_element_by_xpath(count)
            cardlist.append(card.text)
            countlist.append(count.text)
            n += 1
            if n == 31:
                break
        except NoSuchElementException:
            cardlist.append("")
            countlist.append("")
            n += 1
            if n == 31:
                break
    card1= cardlist[0]
    card2= cardlist[1]
    card3= cardlist[2]
    card4= cardlist[3]
    card5= cardlist[4]
    card6= cardlist[5]
    card7= cardlist[6]
    card8= cardlist[7]
    card9= cardlist[8]
    card10= cardlist[9]
    card11= cardlist[10]
    card12= cardlist[11]
    card13= cardlist[12]
    card14= cardlist[13]
    card15= cardlist[14]
    card16= cardlist[15]
    card17= cardlist[16]
    card18= cardlist[17]
    card19= cardlist[18]
    card20= cardlist[19]
    card21= cardlist[20]
    card22= cardlist[21]
    card23= cardlist[22]
    card24= cardlist[23]
    card25= cardlist[24]
    card26= cardlist[25]
    card27= cardlist[26]
    card28= cardlist[27]
    card29= cardlist[28]
    card30= cardlist[29]

    cost1= countlist[0]
    cost2= countlist[1]
    cost3= countlist[2]
    cost4= countlist[3]
    cost5= countlist[4]
    cost6= countlist[5]
    cost7= countlist[6]
    cost8= countlist[7]
    cost9= countlist[8]
    cost10= countlist[9]
    cost11= countlist[10]
    cost12= countlist[11]
    cost13= countlist[12]
    cost14= countlist[13]
    cost15= countlist[14]
    cost16= countlist[15]
    cost17= countlist[16]
    cost18= countlist[17]
    cost19= countlist[18]
    cost20= countlist[19]
    cost21= countlist[20]
    cost22= countlist[21]
    cost23= countlist[22]
    cost24= countlist[23]
    cost25= countlist[24]
    cost26= countlist[25]
    cost27= countlist[26]
    cost28= countlist[27]
    cost29= countlist[28]
    cost30= countlist[29]

    DeckCode.objects.create(
        table=table,
        player_name=player,
        op_name=opp,
        card1=card1,
        card2=card2,
        card3=card3,
        card4=card4,
        card5=card5,
        card6=card6,
        card7=card7,
        card8=card8,
        card9=card9,
        card10=card10,
        card11=card11,
        card12=card12,
        card13=card13,
        card14=card14,
        card15=card15,
        card16=card16,
        card17=card17,
        card18=card18,
        card19=card19,
        card20=card20,
        card21=card21,
        card22=card22,
        card23=card23,
        card24=card24,
        card25=card25,
        card26=card26,
        card27=card27,
        card28=card28,
        card29=card29,
        card30=card30,

        cost1=cost1,
        cost2=cost2,
        cost3=cost3,
        cost4=cost4,
        cost5=cost5,
        cost6=cost6,
        cost7=cost7,
        cost8=cost8,
        cost9=cost9,
        cost10=cost10,
        cost11=cost11,
        cost12=cost12,
        cost13=cost13,
        cost14=cost14,
        cost15=cost15,
        cost16=cost16,
        cost17=cost17,
        cost18=cost18,
        cost19=cost19,
        cost20=cost20,
        cost21=cost21,
        cost22=cost22,
        cost23=cost23,
        cost24=cost24,
        cost25=cost25,
        cost26=cost26,
        cost27=cost27,
        cost28=cost28,
        cost29=cost29,
        cost30=cost30

    )
    driver.quit()
    return render(request, "attendance/deck_result.html")