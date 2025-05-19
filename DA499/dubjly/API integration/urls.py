# this file to Konw what output after API 
from django.urls import path
from . import views


urlpatterns = [
    path('check-video/', views.check_video, name='check_video'),
    #path('getData/',views.gitData,name='gitData'),
    path('',views.check_video ,name='check_video'),
] 


########################## saad work ##################################

urlpatterns = [
    path('videos/process/', views.process_video_url, name='process_video_url'),
    path('videos/<int:video_id>/', views.get_video_info, name='get_video_info'),
    path('videos/<int:video_id>/summary/', views.generate_summary, name='generate_summary'),
    path('videos/<int:video_id>/keywords/', views.generate_keywords, name='generate_keywords'),
    path('videos/<int:video_id>/ask/', views.ask_question, name='ask_question'),
    path('videos/<int:video_id>/questions/', views.get_questions, name='get_questions'),
]