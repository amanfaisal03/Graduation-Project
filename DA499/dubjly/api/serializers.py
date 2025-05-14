from rest_framework import serializers
from .models import Video, Question

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'url', 'title', 'transcript', 'summary', 'keywords', 'created_at', 'generated_video_url']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'video', 'question_text', 'answer_text', 'created_at']