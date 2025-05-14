from django.urls import path
from .views import generate_dubbed_video

urlpatterns = [
    path('generate/<int:video_id>/', generate_dubbed_video, name='generate_dubbed_video'),
]
