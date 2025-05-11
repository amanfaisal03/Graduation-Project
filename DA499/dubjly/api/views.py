import os
import tempfile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Video, Question
from .serializers import VideoSerializer, QuestionSerializer

#Import your existing code
from Extract_Voice_and_STT_Aman.STT import TTS
from LLM_Saad.LLM_Online import Full_LLM

#API Keys and model settings
LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_API_KEY = "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"

@api_view(['POST'])
def process_video_url(request):
    """
    Process a video URL, extract transcript
    """
    if 'url' not in request.data:
        return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    video_url = request.data['url']
    
    # Check if video already exists in database
    existing_video = Video.objects.filter(url=video_url).first()
    if existing_video and existing_video.transcript:
        serializer = VideoSerializer(existing_video)
        return Response({
                         'message': 'Video processed successfully',
                         'video': serializer.data,
                         'video_url': '/media/Final-video.mp4'  
})

    
    try:
        # Create or get video object
        video, created = Video.objects.get_or_create(url=video_url)
        
        # Use your existing TTS code
        tts = TTS(video_url)
        transcript = tts.run_all()
        
        # Save transcript to video object
        video.transcript = transcript
        video.save()
        
        serializer = VideoSerializer(video)
        return Response({'message': 'Video processed successfully', 'video': serializer.data})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_video_info(request, video_id):
    """
    Get video info including transcript
    """
    try:
        video = Video.objects.get(pk=video_id)
        serializer = VideoSerializer(video)
        return Response(serializer.data)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def generate_summary(request, video_id):
    """
    Generate summary for a video
    """
    try:
        video = Video.objects.get(pk=video_id)
        
        # Check if summary already exists
        if video.summary:
            return Response({'message': 'Summary already exists', 'summary': video.summary})
        
        # Use your LLM code to generate summary
        llm = Full_LLM(model=LLM_MODEL, api_key=GROQ_API_KEY, Text=video.transcript, Online=True)
        summary = llm.Summarize()
        
        # Save summary to video object
        video.summary = summary
        video.save()
        
        return Response({'message': 'Summary generated successfully', 'summary': summary})
    
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def generate_keywords(request, video_id):
    """
    Generate keywords for a video
    """
    try:
        video = Video.objects.get(pk=video_id)
        
        # Check if keywords already exist
        if video.keywords:
            return Response({'message': 'Keywords already exist', 'keywords': video.keywords})
        
        # Use your LLM code to generate keywords
        llm = Full_LLM(model=LLM_MODEL, api_key=GROQ_API_KEY, Text=video.transcript, Online=True)
        keywords = llm.Keywords()
        
        # Save keywords to video object
        video.keywords = keywords
        video.save()
        
        return Response({'message': 'Keywords generated successfully', 'keywords': keywords})
    
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def ask_question(request, video_id):
    """
    Ask a question about the video content
    """
    try:
        video = Video.objects.get(pk=video_id)
        
        if 'question' not in request.data:
            return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        question_text = request.data['question']
        
        # Create question object
        question = Question.objects.create(
            video=video,
            question_text=question_text
        )
        
        # Use your LLM code to generate answer
        llm = Full_LLM(model=LLM_MODEL, api_key=GROQ_API_KEY, Text=video.transcript, Online=True)
        answer = llm.ChatBot_Answer(question=question_text)
        
        # Save answer to question object
        question.answer_text = answer
        question.save()
        
        return Response({
            'message': 'Question answered successfully',
            'question': question_text,
            'answer': answer
        })
    
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_questions(request, video_id):
    """
    Get all questions for a specific video
    """
    try:
        video = Video.objects.get(pk=video_id)
        questions = Question.objects.filter(video=video)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)