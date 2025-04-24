import time
import csv
import os
import soundfile as sf
import torch
import torchaudio
import pandas as pd
import numpy as np
import subprocess
import math
import re
from TTS.api import TTS
from pydub import AudioSegment
from pydub.silence import split_on_silence
from scipy.io.wavfile import read, write


def extract_timings_from_text(file_path, output_csv):
    results = []    # قائمة لتخزين النتائج
    with open(file_path, "r", encoding="utf-8") as file:      # فتح الملف
        lines = file.readlines()    # قراءة كل الأسطر في الملف 

    for index, line in enumerate(lines):   #لووب على كل سطر 
        line = line.strip()       #هون ياسيدي بنحذف المسافات الزايدة من اول واخر السطر 
        if line == "":    #اذا السطر فاضي روح على يلي بعده 
            continue
        if "]" not in line:   #بنبحث اذا في علامة ] بالسطر 
            print(f"⚠️ سطر غير صالح (ما في ]): {line}")    #طباعة انه مش صالح 
            continue   #روح على يلي بعده 
        try:
            Time, Text = line.split("]")     #هون نقسم السطر يا غالي لنصين ،جزء بالنص وجزء بالوقت 
            Time = Time[1:]      #هون بنحذف علامة [ من بداية الوقت 
            text = Text.strip() #هون بنحذف السبيسز الزايدة من النص 

            if "-" in Time: #بنفحص اذا في علامة - بالوقت    
                start_time, end_time = Time.split("-")  #ياغالي بنقسم الوقت هون لبداية ونهاية
                start_time = float(start_time.strip()) ##هون بنحذف السبيسز الزايدة من بداية الوقت
                end_time = float(end_time.strip())# هون بنحذف السبيسز الزايدة من نهاية الوقت
            else:
                start_time = float(Time.strip()) # اخر وقت ما رح يكون فيه - فبنختار بداية الوقت بس
                end_time = start_time + 5 ## بنضيف 5 ثواني لنهاية الوقت من عندنا 
                print(f"ℹ️ تم إنشاء نهاية مؤقتة للسطر: {line}")   # هون بنطبع انه عملنا نهاية مؤقتة للسطر

            #voices = f"sentence-voice_{index:03}.wav"  
            voices = f"Voices_{index:03}.wav"   # هون بنعمل اسم للملف الصوتي بناءً على رقم السطر
            results.append([voices, start_time, end_time, text])            # هون بنضيف كل شي لقائمة النتائج
        except Exception as e:  # هون بنعمل كاتش للخطأ  
            print(f"❌ خطأ عند السطر {index}: {line} - {e}")    # بنطبع الخطأ

    with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:  # هون بنفتح ملف CSV جديد
        writer = csv.writer(csv_file) # هون بنعمل كاتب CSV
        writer.writerow(["voices", "start", "end", "text"])     # هون بنكتب اسماء الاعمدة 
        writer.writerows(results)    # هون بنكتب كل النتائج في ملف CSV 

    print("✅ تم استخراج البيانات وحفظها في timing_sentences_.csv")      #الحمدلله 


def generate_audio_from_csv(csv_path, output_dir, speaker_wav, language="ar"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row["voices"]
            text = row["text"]
            print(f"🎤 توليد الصوت للجملة: {text}")
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
            save_path = os.path.join(output_dir, filename)
            sf.write(save_path, audio, 24000)
    print("✅ تم توليد كل ملفات الصوت بنجاح")


def remove_silence_from_audios(csv_path, input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    df = pd.read_csv(csv_path)
    print(f"📄 عدد الملفات في CSV: {len(df)}")

    failed_files = []

    for index, row in df.iterrows():
        filename = row["voices"].strip()
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
                aud, min_silence_len=1300, silence_thresh=-45, keep_silence=500
            )
            audio_processed = sum(audio_chunks) if audio_chunks else aud
            audio_np = np.array(audio_processed.get_array_of_samples())
            output_path = os.path.join(output_folder, filename)
            write(output_path, rate, audio_np)
            print(f"✅ تم معالجة: {filename}")

        except Exception as e:
            print(f"❌ حصل خطأ في {filename}: {e}")
            failed_files.append((filename, str(e)))

    print("\n📊 معالجة انتهت ✅")
    print(f"🔢 عدد الملفات التي نجحت: {len(df) - len(failed_files)}")
    print(f"❌ عدد الملفات التي فشلت: {len(failed_files)}")
    if failed_files:
        print("\n🧾 الملفات التي فشلت:")
        for fname, reason in failed_files:
            print(f" - {fname} => {reason}")


def merge_audio_files(input_folder, output_path):
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group()) if match else -1

    files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
    files = sorted(files, key=extract_number)

    merged = AudioSegment.silent(duration=0)
    for filename in files:
        path = os.path.join(input_folder, filename)
        audio = AudioSegment.from_wav(path)
        merged += audio
        print(f"✅ أُضيف: {filename}")

    merged.export(output_path, format="wav")
    print(f"\n🎉 تم دمج {len(files)} ملف في: {output_path}")


def get_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    return float(result.stdout.decode().strip())


def adjust_audio_speed_to_match_video(video_path, audio_path, output_audio_path):
    video_duration = get_duration(video_path)
    audio_duration = get_duration(audio_path)
    print(f"🎞️ مدة الفيديو: {round(video_duration, 2)} ثانية")
    print(f"🔊 مدة الصوت : {round(audio_duration, 2)} ثانية")

    speed = round(audio_duration / video_duration, 3)
    print(f"⚡ السرعة المطلوبة: {speed}x")

    if speed <= 2.0:
        atempo_filter = f"atempo={speed}"
    else:
        steps = []
        remaining = speed
        while remaining > 2.0:
            steps.append("atempo=2.0")
            remaining /= 2.0
        steps.append(f"atempo={round(remaining, 3)}")
        atempo_filter = ",".join(steps)

    cmd_speed = fr'''ffmpeg -i "{audio_path}" -filter:a "{atempo_filter}" -vn "{output_audio_path}" -y'''
    os.system(cmd_speed)
    print("✅ تم تسريع الصوت.")


def merge_audio_with_video(video_path, audio_path, final_output_path):
    cmd_merge = fr'''ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest "{final_output_path}" -y'''
    os.system(cmd_merge)
    print(f"🎉 تم إنتاج الفيديو النهائي مع الصوت المتزامن: {final_output_path}")


def main():
    start_time = time.time()

    extract_timings_from_text(
        r"C:\Users\sauui\XTTS-project\sayyid-work\test-text\نص-التجربة.txt",
        "timing_sentences_.csv"
    )

    generate_audio_from_csv(
        "C:\\Users\\sauui\\XTTS-project\\timing_sentences_.csv",
        "C:\\Users\\sauui\\XTTS-project\\sayyid-work\\output-test-voice\\original-video-voice",
        r"C:\Users\sauui\XTTS-project\sayyid-work\input-test-voice\غرباء.wav"
    )

    remove_silence_from_audios(
        r"C:\Users\sauui\XTTS-project\timing_sentences_.csv",
        r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\original-video-voice",
        r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\removed-voices"
    )

    merge_audio_files(
        r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\removed-voices",
        r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output.wav"
    )

    adjust_audio_speed_to_match_video(
        r"C:\Users\sauui\XTTS-project\silent_video.mp4",
        r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output.wav",
        r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output_adjusted.wav"
    )

    merge_audio_with_video(
        r"C:\Users\sauui\XTTS-project\silent_video.mp4",
        r"C:\Users\sauui\XTTS-project\sayyid-work\output-test-voice\merged_output_adjusted.wav",
        r"C:\Users\sauui\XTTS-project\final-video-synced.mp4"
    )

    end_time = time.time()
    print(f"🕒 الوقت المستغرق: {end_time - start_time:.2f} ثانية")


if __name__ == "__main__":
    main()
