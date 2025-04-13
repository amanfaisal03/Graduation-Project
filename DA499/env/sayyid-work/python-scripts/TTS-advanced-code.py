import csv
import os
import soundfile as sf
import torch
from TTS.api import TTS
import torchaudio


device = "cuda" if torch.cuda.is_available() else "cpu"
# تحميل نموذج XTTS (مرّة وحدة فقط)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# تحديد مسار ملف CSV
text_file= "C:\\Users\\sauui\\XTTS-project\\timing_sentences_.csv"

# تحديد مجلد الإخراج
output_dir = "C:\\Users\\sauui\\XTTS-project\\sayyid-work\\output-test-voice\\original-video-voice"

# إنشاء المجلد إذا ما كان موجود
#os.makedirs(output_dir, exist_ok=True)

# تحديد إعدادات XTTS
speaker_wav = "C:\\Users\\sauui\\XTTS-project\\sayyid-work\\input-test-voice\\sayyid-voice.wav"  # صوتك المرجعي
language = "ar"

# قراءة CSV وتنفيذ التوليد
with open(text_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        filename = row["voices"]
        text = row["text"]

        print(f"🎤 توليد الصوت للجملة: {text}")

        # توليد الصوت باستخدام XTTS
        audio = tts.tts(
            text=text,
            speaker_wav=speaker_wav,
            language=language,
            temperature=0.75,
            top_k=40,
            top_p=0.9,
            repetition_penalty=8.0,
            gpt_cond_len=6,
            gpt_cond_chunk_len=6
        )

        # تحديد مسار الملف النهائي
        save_path = os.path.join(output_dir, filename)

        # حفظ الصوت
        sf.write(save_path, audio, 24000)

print("✅ تم توليد كل ملفات الصوت بنجاح في مجلد voices_test_output")
