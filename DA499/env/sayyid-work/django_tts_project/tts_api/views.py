from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import sys
sys.path.append(r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\env\sayyid-work")
from Run_main import Start_the_TTS_process


@csrf_exempt
def generate_dubbed_video(request):
    if request.method == "POST":
        text = request.POST.get("text", "")
        if not text:
            return JsonResponse({"error": "No text provided"}, status=400)

        # كتابة النص في ملف Main_text.txt
        base_path = r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\env"
        text_path = os.path.join(base_path, "sayyid-work", "test-text", "Main_text.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text)

        # تشغيل البايبلاين
        try:
            video_process = Start_the_TTS_process(base_path, text_input_path=text_path)
            video_process.run()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        # الفيديو الناتج
        video_url = "/media/merged_output.mp4"
        return JsonResponse({"status": "success", "video_url": video_url})

    return JsonResponse({"error": "Only POST allowed"}, status=405)
