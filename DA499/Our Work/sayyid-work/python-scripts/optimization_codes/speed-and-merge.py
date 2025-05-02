import os
import subprocess
import math

# --- [1] إعداد المسارات ---
video_path = r"C:\Users\sauui\XTTS-project\silent_video.mp4"
audio_path = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output.wav"
output_audio = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output_adjusted.wav"
final_video = r"C:\Users\sauui\XTTS-project\final-video-synced.mp4"

# --- [2] دالة لحساب مدة ملف (بالثواني) باستخدام ffprobe ---
def get_duration(path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout.decode().strip())

# --- [3] حساب مدة الفيديو والصوت ---
video_duration = get_duration(video_path)
audio_duration = get_duration(audio_path)

print(f"🎞️ مدة الفيديو: {round(video_duration, 2)} ثانية")
print(f"🔊 مدة الصوت : {round(audio_duration, 2)} ثانية")

# --- [4] حساب السرعة المطلوبة لتسريع الصوت ---
# احسب كم نحتاج نسرّع الصوت ليطابق مدة الفيديو
speed = round(audio_duration / video_duration, 3)


print(f"⚡ السرعة المطلوبة: {speed}x")

# --- [5] تجهيز فلتر atempo (يقسمه إذا أكثر من 2x) ---
if speed <= 2.0:
    atempo_filter = f"atempo={speed}"
else:
    # تقسيم السرعة الكبيرة إلى أكثر من atempo
    steps = []
    remaining = speed
    while remaining > 2.0:
        steps.append("atempo=2.0")
        remaining /= 2.0
    steps.append(f"atempo={round(remaining, 3)}")
    atempo_filter = ",".join(steps)

# --- [6] تسريع الصوت باستخدام FFmpeg ---
cmd_speed = fr'''ffmpeg -i "{audio_path}" -filter:a "{atempo_filter}" -vn "{output_audio}" -y'''
os.system(cmd_speed)
print("✅ تم تسريع الصوت.")

# --- [7] دمج الصوت المسرّع مع الفيديو ---
cmd_merge = fr'''ffmpeg -i "{video_path}" -i "{output_audio}" -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest "{final_video}" -y'''
os.system(cmd_merge)
print(f"🎉 تم إنتاج الفيديو النهائي مع الصوت المتزامن: {final_video}")
