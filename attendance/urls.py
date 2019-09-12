from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('index/register/<str:date>/', views.date),
    path('match_list', views.listdate),
    path('<str:date>/result', views.result, name='result'),
    path('matchlist/<str:date>/', views.list),
]