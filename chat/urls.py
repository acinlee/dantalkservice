from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<room_name>/', views.room, name='room'),
]