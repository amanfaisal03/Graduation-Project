r'''
import pandas as pd
import numpy as np
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from scipy.io.wavfile import read, write

# المسارات
csv_path = r"C:\Users\sauui\XTTS-project\timing2_sentences_.csv"
input_folder = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\original-video-voice"
output_folder = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\removed-voices"

# تأكد أن مجلد الإخراج موجود
os.makedirs(output_folder, exist_ok=True)

# اقرأ ملف CSV
df = pd.read_csv(csv_path)

# افترض أن العمود الذي يحتوي على اسم الملف اسمه "filename" أو ما شابه (عدله حسب الحاجة)
for index, row in df.iterrows():
    filename = row["voices"]  # غيّر "filename" حسب اسم العمود الصحيح في CSV
    input_path = os.path.join(input_folder, filename)

    # اقرأ الملف الصوتي
    try:
        rate, audio = read(input_path)
        aud = AudioSegment(audio.tobytes(), frame_rate=rate,
                           sample_width=audio.dtype.itemsize, channels=1)

        # إزالة السكوت
        audio_chunks = split_on_silence(
            aud,
            min_silence_len=1500,
            silence_thresh=-45,
            keep_silence=500
        )

        if len(audio_chunks) > 0:
            audio_processed = sum(audio_chunks)
        else:
            audio_processed = aud  # إذا ما في سكوت، خليه كما هو

        # حول إلى numpy
        audio_np = np.array(audio_processed.get_array_of_samples())

        # احفظ الملف الناتج بنفس الاسم
        output_path = os.path.join(output_folder, filename)
        write(output_path, rate, audio_np)

        print(f"✅ Processed: {filename}")
    except Exception as e:
        print(f"❌ Error with {filename}: {e}")
'''
import pandas as pd
import numpy as np
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from scipy.io.wavfile import read, write

csv_path = r"C:\Users\sauui\XTTS-project\timing_sentences_.csv"
input_folder = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\original-video-voice"
output_folder = r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\removed-voices"

os.makedirs(output_folder, exist_ok=True)

df = pd.read_csv(csv_path)
print(f"📄 عدد الملفات في CSV: {len(df)}")

failed_files = []

for index, row in df.iterrows():
    filename = row["voices"].strip()  # تأكد من إزالة الفراغات

    print(f"🔄 جاري معالجة: {filename}")

    input_path = os.path.join(input_folder, filename)

    if not os.path.exists(input_path):
        print(f"❌ الملف غير موجود: {filename}")
        failed_files.append((filename, "ملف غير موجود"))
        continue

    try:
        rate, audio = read(input_path)

        if len(audio) == 0:
            print(f"⚠️ الملف فاضي: {filename}")
            failed_files.append((filename, "ملف فاضي"))
            continue

        aud = AudioSegment(audio.tobytes(), frame_rate=rate,
                           sample_width=audio.dtype.itemsize, channels=1)

        audio_chunks = split_on_silence(
            aud,
            min_silence_len=1300,
            silence_thresh=-45,
            keep_silence=500
        )

        if len(audio_chunks) > 0:
            audio_processed = sum(audio_chunks)
        else:
            audio_processed = aud

        audio_np = np.array(audio_processed.get_array_of_samples())
        output_path = os.path.join(output_folder, filename)
        write(output_path, rate, audio_np)

        print(f"✅ تم معالجة: {filename}")

    except Exception as e:
        print(f"❌ حصل خطأ في {filename}: {e}")
        failed_files.append((filename, str(e)))

# ⏹️ تقرير نهائي
print("\n📊 معالجة انتهت ✅")
print(f"🔢 عدد الملفات التي نجحت: {len(df) - len(failed_files)}")
print(f"❌ عدد الملفات التي فشلت: {len(failed_files)}")

if failed_files:
    print("\n🧾 الملفات التي فشلت:")
    for fname, reason in failed_files:
        print(f" - {fname} => {reason}")


