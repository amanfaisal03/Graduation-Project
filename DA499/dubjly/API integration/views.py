from rest_framework.response import Response 
from rest_framework.decorators import api_view
from Extract_Voice_and_STT_Aman.STT import * 
from .serializers import VideoSerializer , QuestionSerializer
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import Video , Question
import os
import tempfile

#Import your existing code
from Extract_Voice_and_STT_Aman.STT import TTS
from LLM_Saad.LLM_Online import Full_LLM



#API Keys and model settings
LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_API_KEY = "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"


#api_viwe(['GET'])
@api_view(['POST'])
def check_video(request):
    video_url = request.data.get('url')
    
    if not video_url: # check if user has entered the video link or not (empty)
        return Response({"error": "Missing video URL , plaese input URL video "}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'No Title')

            # Check if video already exists in database 
            existing_video = Video.objects.filter(url=video_url).first()
            if existing_video:   
                serializer = VideoSerializer(existing_video)
                return Response({
                    "message": "Video already exists ",
                    "video": serializer.data
                })
            
            # save in data base 
            video_instance = Video.objects.create(
                name=title,
                url=video_url
            )
            serializer = VideoSerializer(video_instance)

            return Response({
                "message": "Video info fetched successfully",
                "title": title,
                "video": serializer.data
            })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
################################## saad work ###########################################

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

        A_transcript = llm.Transcript()
        # Save A_transcript to video object
        video.a_transcript = A_transcript
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
    
 
