# this file to Konw what output after API 
from django.urls import path
from . import views


urlpatterns = [
    path('check-video/', views.check_video, name='check_video'),
]