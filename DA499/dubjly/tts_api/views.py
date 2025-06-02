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
        base_path = r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\dubjly"
        text_path = os.path.join(base_path, "sayyid_work", "test-text", "Main_text.txt")
        generated_path = os.path.join(base_path, f"media/video_outputs/video_{video_id}/Final_video_{video_id}.mp4")

        # ✅ جلب الفيديو من قاعدة البيانات
        video = Video.objects.get(id=video_id)

        # ✅ التحقق من وجود فيديو مولد سابقًا
        if video.generated_video_url:
            if os.path.exists(generated_path):
                return Response({
                    "status": "already_generated",
                    "video_url": video.generated_video_url
                }, status=status.HTTP_200_OK)
            else:
                # ✅ الملف مش موجود رغم وجود الرابط — احذف الرابط
                video.generated_video_url = ""
                video.save()

        # ✅ جلب النص من API سعد
        url = f"http://127.0.0.1:8000/api/videos/{video_id}/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        transcript = data.get("a_transcript", "")

        if not transcript:
            return Response({"error": "No transcript found"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ كتابة الترانسكريبت في ملف نصي
        if os.path.exists(text_path):
            os.remove(text_path)
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        # ✅ تشغيل البايبلاين
        video_process = Start_the_TTS_process(
            text_input_path=text_path,
            base_dir=base_path,
            video_id=video_id
        )
        video_process.run()

        # ✅ حفظ رابط الفيديو في قاعدة البيانات
        video.generated_video_url = f"/media/video_outputs/video_{video_id}/Final_video_{video_id}.mp4"
        video.save()

        # ✅ طباعة debug
        print("DEBUG path:", generated_path)
        print("File exists:", os.path.exists(generated_path))

        return Response({
            "status": "success",
            "video_url": video.generated_video_url
        }, status=status.HTTP_200_OK)

    except Video.DoesNotExist:
        return Response({"error": "Video not found in database"}, status=status.HTTP_404_NOT_FOUND)
    except requests.exceptions.RequestException as e:
        return Response({"error": f"Failed to fetch transcript: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)
    except Exception as e:
           import traceback
           print("EXCEPTION:", str(e))
           traceback.print_exc()
           return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
