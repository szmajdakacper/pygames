from django.urls import path

from . import views

app_name = "four_in_a_row"
urlpatterns = [
    path('', views.play, name='play'),
    path('reset/', views.reset, name='reset'),
    path('<str:cord>/', views.clicked, name='clicked')
]