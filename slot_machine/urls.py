from django.urls import path

from . import views

app_name = "slot_machine"
urlpatterns = [
    path('', views.play, name='play'),
    path('reset/', views.reset, name='reset'), 
    path('pull/', views.pull, name='pull'),
]