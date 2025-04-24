from pydub import AudioSegment
import os
import re

# مجلد الملفات المعالجة
input_folder = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\removed-voices"
output_path = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output.wav"

# اجلب كل الملفات wav ورتبهم حسب الرقم داخل الاسم
def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group()) if match else -1

files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
files = sorted(files, key=extract_number)

# ابدأ بمقطع فاضي
merged = AudioSegment.silent(duration=0)

# دمج الملفات
for filename in files:
    path = os.path.join(input_folder, filename)
    audio = AudioSegment.from_wav(path)
    merged += audio
    print(f"✅ أُضيف: {filename}")

# احفظ الملف النهائي
merged.export(output_path, format="wav")
print(f"\n🎉 تم دمج {len(files)} ملف في: {output_path}")

r"""
import os

cmd = r'''ffmpeg -i "C:\Users\sauui\XTTS-project\sayyid-work\input-silent-video.mp4" -i "C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output.wav" -c:v copy -map 0:v:0 -map 1:a:0 -shortest "C:\Users\sauui\XTTS-project\sayyid-work\final-video-with-voice.mp4"'''

os.system(cmd)
print("✅ تم دمج الفيديو مع الصوت بنجاح.")
"""