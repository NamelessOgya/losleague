from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('index/register/<str:team>/<str:date>/', views.date),
    path('<str:team>/<str:date>/result/', views.result, name='result'),
]