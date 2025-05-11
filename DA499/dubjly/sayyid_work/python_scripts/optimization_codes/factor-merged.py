import os
import subprocess

# -------- إعداد المسارات --------
video_path = r"C:\Users\sauui\XTTS-project\silent_video.mp4"
audio_path = (
    r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output.wav"
)
output_audio_template = r"C:\Users\sauui\XTTS-project\temp_speed_adjusted_{tag}.wav"
final_video_template = r"C:\Users\sauui\XTTS-project\synced_output_{tag}.mp4"

# -------- عوامل التصحيح التي نريد تجربتها --------
correction_factors = [1.00, 1.03, 1.05, 1.07, 1.04]


# -------- دالة لحساب مدة الصوت والفيديو --------
def get_duration(path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return float(result.stdout.decode().strip())


# -------- احسب السرعة الأساسية --------
video_duration = get_duration(video_path)
audio_duration = get_duration(audio_path)
base_speed = audio_duration / video_duration
print(f"📊 السرعة المحسوبة: {base_speed:.3f}x (قبل التصحيح)")

# -------- أنشئ فيديوهات بعدة سرعات --------
for factor in correction_factors:
    tag = str(int(factor * 100))  # مثال: 103 = 1.03
    speed = round(base_speed * factor, 4)
    print(f"\n⚙️ إنتاج نسخة بسرعة: {speed}x (factor={factor})")

    # تجهيز atempo filter
    if speed <= 2.0:
        atempo = f"atempo={speed}"
    else:
        steps = []
        remaining = speed
        while remaining > 2.0:
            steps.append("atempo=2.0")
            remaining /= 2.0
        steps.append(f"atempo={round(remaining, 4)}")
        atempo = ",".join(steps)

    # 1. تسريع الصوت
    output_audio = output_audio_template.format(tag=tag)
    cmd_speed = (
        rf"""ffmpeg -i "{audio_path}" -filter:a "{atempo}" -vn "{output_audio}" -y"""
    )
    os.system(cmd_speed)
    print(f"✅ تم إنشاء ملف صوت مسرّع: {output_audio}")

    # 2. دمج الصوت مع الفيديو
    final_video = final_video_template.format(tag=tag)
    cmd_merge = rf"""ffmpeg -i "{video_path}" -i "{output_audio}" -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest "{final_video}" -y"""
    os.system(cmd_merge)
    print(f"🎬 تم إنشاء الفيديو النهائي: {final_video}")

print("\n🎉 تم إنشاء جميع النسخ! جرّبها واختر الأفضل.")
