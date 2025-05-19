from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import requests
from django.conf import settings

from sayyid_work.python_scripts.Full_codes.Run_main import Start_the_TTS_process
from api.models import Video



@api_view(['GET'])
def generate_dubbed_video(request, video_id):
    try:
        # جلب النص من API سعد
        url = f"http://127.0.0.1:8000/api/videos/{video_id}/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        transcript = data.get("transcript", "")

        if not transcript:
            return Response({"error": "No transcript found"}, status=status.HTTP_400_BAD_REQUEST)

        # تحديد المسارات
        base_path = r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\dubjly"
        text_path = os.path.join(base_path, "sayyid_work", "test-text", "Main_text.txt")

        if os.path.exists(text_path):
            os.remove(text_path)

        with open(text_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        # تشغيل البايبلاين
        video_process = Start_the_TTS_process(text_input_path=text_path, base_dir=base_path)

        video_process.run()
        video = Video.objects.get(id=video_id)
        video.generated_video_url = "/media/Final_video.mp4"
        video.save()


        print("DEBUG path:", os.path.join(base_path, "media", "Final_video.mp4"))
        print("File exists:", os.path.exists(os.path.join(base_path, "media", "Final_video.mp4")))
        return Response({
            "status": "success",
            "video_url": "/media/Final_video.mp4"
        }, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        return Response({"error": f"Failed to fetch transcript: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    