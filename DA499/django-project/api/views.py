from rest_framework.response import Response 
from rest_framework.decorators import api_view
from Extract_Voice_and_STT_Aman.STT import * 
from .serializers import VideoSerializer
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import Video


#api_viwe(['GET'])
@api_view(['POST'])
def check_video(request):
    video_url = request.data.get('url')
    
    if not video_url: # check if user has entered the video link or not (empty)
        return Response({"error": "Missing video URL"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'No Title')

            # Check if video already exists in database 
            existing_video = Video.objects.filter(url=video_url).first()
            if existing_video:
                serializer = VideoSerializer(existing_video)
                return Response({
                    "message": "Video already exists",
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
    
