from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user),
    path('index/', views.index, name='index'),
    path('index/register/<str:date>/', views.date),
    path('match_list', views.listdate),
    path('<str:date>/result', views.result, name='result'),
    path('matchlist/<str:date>/', views.list),
    path('report_date/report/<str:date>/', views.report),
    path('report_date/report/<str:date>/result', views.report_register),
    path('report_date/', views.reportdate),
    path('match_result', views.match_result),
    path('deck_date', views.deck_date),
    path('deck_table/<str:date>', views.deck_table),
    path('deck_table/deck_register/<str:date>/<str:team>/', views.deck_register),
    path('<str:date>/<str:team1>/deck_result', views.deck_result),
]