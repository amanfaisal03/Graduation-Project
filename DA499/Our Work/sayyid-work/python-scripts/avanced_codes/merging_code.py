import os
import torch

if torch.cuda.is_available():
    print("✅ الكود يعمل على GPU:", torch.cuda.get_device_name(0))
else:
    print("❌ الكود يعمل على CPU فقط")

# مسارات الملفات
video_path = r"C:\Users\sauui\XTTS-project\silent_video.mp4"
audio_path = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output.wav"
output_path = r"C:\Users\sauui\XTTS-project\final-video-with-voice.mp4"

# أمر FFmpeg لدمج الصوت مع الفيديو
cmd = fr'''ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest "{output_path}"'''

# تنفيذ الأمر
os.system(cmd)

print("🎉 تم دمج الصوت مع الفيديو بنجاح!")
