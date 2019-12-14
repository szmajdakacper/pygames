from django.urls import path

from . import views

app_name = "hangman"
urlpatterns = [
    path('', views.play, name='play'),
    path('reset/', views.reset, name='reset'), 
    path('<str:letter>/', views.shot, name='shot'),
]