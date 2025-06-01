from django.urls import path
from .views import generate_dubbed_video

urlpatterns = [
    path('generate/', generate_dubbed_video),
]
