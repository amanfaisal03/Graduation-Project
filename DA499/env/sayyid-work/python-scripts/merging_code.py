from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import csv
import os

# 1. تحميل الفيديو الصامت
video_path = r"C:\Users\sauui\XTTS-project\silent_video.mp4"
video = VideoFileClip(video_path)

# 2. تحميل ملف CSV وتحديد مجلد الأصوات
csv_path = r"C:\Users\sauui\XTTS-project\timing_sentences_.csv"
audio_folder = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\original-video-voice"

# 3. تجهيز قائمة المقاطع الصوتية
audio_clips = []

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        audio_file = os.path.join(audio_folder, row["voices"])
        start = float(row["start"])

        if os.path.exists(audio_file):
            try:
                audio = AudioFileClip(audio_file).set_start(start)
                audio_clips.append(audio)
                print(f"✅ أضيف: {os.path.basename(audio_file)} عند {start} ثانية")
            except Exception as e:
                print(f"❌ خطأ في تحميل {audio_file}: {e}")
        else:
            print(f"⚠️ الملف غير موجود: {audio_file}")

# 4. التأكد من وجود مقاطع صوتية
if not audio_clips:
    print("🚫 لم يتم العثور على أي ملفات صوت لدمجها.")
    exit()

# 5. دمج المقاطع الصوتية وضبط المدة والتردد
final_audio = CompositeAudioClip(audio_clips).set_duration(video.duration).set_fps(44100)

# 6. دمج الصوت مع الفيديو
final_video = video.set_audio(final_audio)

# 7. حفظ الفيديو النهائي
output_path = r"C:\Users\sauui\XTTS-project\final_output_video_fixed.mp4"
final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

print(f"🎉 تم إنشاء الفيديو بنجاح: {output_path}")
