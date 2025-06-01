import time  # لحساب الزمن المستغرق للتنفيذ
import csv  # للتعامل مع ملفات CSV
import os  # للتعامل مع نظام الملفات (مجلدات، مسارات، إلخ)
import soundfile as sf  # لحفظ الصوت بصيغة WAV
import torch  # مكتبة PyTorch لاستخدام الـ GPU
import torchaudio  # للتعامل مع الملفات الصوتية داخل PyTorch
import pandas as pd  # لتحليل البيانات وقراءة CSV
import numpy as np  # للتعامل مع المصفوفات الرقمية
import subprocess  # لتشغيل أوامر خارجية مثل ffmpeg
import math  # للعمليات الرياضية
import re  # للتعامل مع النصوص باستخدام Regular Expressions
from TTS.api import TTS  # لتحميل واستخدام نموذج XTTS من مكتبة TTS
from pydub import AudioSegment  # لتحرير ملفات الصوت (تقطيع، دمج...)
from pydub.silence import split_on_silence  # لتحديد وقص فترات السكوت في الصوت
from scipy.io.wavfile import read, write  # لقراءة وكتابة ملفات الصوت بصيغة WAV


# هاي عشان نعمل دالة لاستخراج التوقيتات والنص وننشئ عامود باسماء الفويسات
def Extract_text_and_time(file_path, output_csv):
    results = []  # قائمة لتخزين النتائج
    with open(file_path, "r", encoding="utf-8") as file:  # فتح الملف
        lines = file.readlines()  # قراءة كل الأسطر في الملف
    for index, line in enumerate(lines):  # لووب على كل سطر
        line = line.strip()  # هون ياسيدي بنحذف المسافات الزايدة من اول واخر السطر
        if line == "":  # اذا السطر فاضي روح على يلي بعده
            continue
        if "]" not in line:  # بنبحث اذا في علامة ] بالسطر
            print(f" سطر غير صالح (ما في ]): {line}")  # طباعة انه مش صالح
            continue  # روح على يلي بعده
        try:
            Time, Text = line.split(
                "]"
            )  # هون نقسم السطر يا غالي لنصين ،جزء بالنص وجزء بالوقت
            Time = Time[1:]  # هون بنحذف علامة [ من بداية الوقت
            text = Text.strip()  # هون بنحذف السبيسز الزايدة من النص

            if "-" in Time:  # بنفحص اذا في علامة - بالوقت
                start_time, end_time = Time.split(
                    "-"
                )  # ياغالي بنقسم الوقت هون لبداية ونهاية
                start_time = float(
                    start_time.strip()
                )  ##هون بنحذف السبيسز الزايدة من بداية الوقت
                end_time = float(
                    end_time.strip()
                )  # هون بنحذف السبيسز الزايدة من نهاية الوقت
            else:
                start_time = float(
                    Time.strip()
                )  # اخر وقت ما رح يكون فيه - فبنختار بداية الوقت بس
                end_time = start_time + 5  ## بنضيف 5 ثواني لنهاية الوقت من عندنا
                print(
                    f"ℹ تم إنشاء نهاية مؤقتة للسطر: {line}"
                )  # هون بنطبع انه عملنا نهاية مؤقتة للسطر

            # voices = f"sentence-voice_{index:03}.wav"
            voices = f"Voices_{index:03}.wav"  # هون بنعمل اسم للملف الصوتي بناءً على رقم السطر
            results.append(
                [voices, start_time, end_time, text]
            )  # هون بنضيف كل شي لقائمة النتائج
        except Exception as e:  # هون بنعمل كاتش للخطأ
            print(f" خطأ عند السطر {index}: {line} - {e}")  # بنطبع الخطأ

    with open(
        output_csv, "w", newline="", encoding="utf-8"
    ) as csv_file:  # هون بنفتح ملف CSV جديد
        writer = csv.writer(csv_file)  # هون بنعمل كاتب CSV
        writer.writerow(["voices", "start", "end", "text"])  # هون بنكتب اسماء الاعمدة
        writer.writerows(results)  # هون بنكتب كل النتائج في ملف CSV

    print(" تم استخراج البيانات وحفظها في timing_sentences_.csv")  # الحمدلله
    return


#  CSV يهون بنعمل فنكشن لتوليد الصوت عن طريق قراءة ملف
def Generate_audio(csv_path, out_put_path, voice_file, language="ar"):
    device = "cuda" if torch.cuda.is_available() else "cpu"  # بنشوف اذا في gpu او لا
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(
        device
    )  # بنزل المودل وبنجهزه ياغالي

    with open(csv_path, "r", encoding="utf-8") as f:  # هون بنفتح ملف csv
        reader = csv.DictReader(f)  #  بنقرا كل سطر بالملف كديكشنوري
        for row in reader:
            filename = row["voices"]  # هون بنجيب اسم الملف الصوتي من السطر
            text = row["text"]  # هون بنجيب النص من السطر
            print(
                f"🎤 توليد الصوت للجملة: {text}"
            )  # بنطبع شو الجملة يلي رح نولدها صوتيا
            audio = tts.tts(  # توليد الصوت باستخدام المودل
                text=text,
                speaker_wav=voice_file,
                language=language,  # من سطر 69 لسطر 79 هذول هنه الباراميترز يلي جوا المودل لغايات تحسي الصوت
                temperature=0.75,
                top_k=40,
                top_p=0.9,
                repetition_penalty=8.0,
                gpt_cond_len=6,
                gpt_cond_chunk_len=6,
            )
            save_path = os.path.join(
                out_put_path, filename
            )  # بنسوي مسار للملف يلي رح نخزنه حسب اسم الفويس يلي مخزن بالكولم
            sf.write(
                save_path, audio, 24000
            )  #  بنخزن الصوت يلي طلع من المودل باستخدام soundfile بترردد 2400 هرتز
    print("✅ تم توليد كل ملفات الصوت بنجاح")


# بنجيب ملف csv كمان مرة وبنحط فيه كل الملفات يلي بدنا نحذف منها السايلنس
def Delete_silence_from_voices(csv_path, input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)  #  بنعمل مجلد جديد اذا ما كان موجود
    df = pd.read_csv(csv_path)  # اقرا الملف
    print(f" عدد الملفات في CSV: {len(df)}")  ##  طباعة عدد الملفات يلي موجودة بالملف

    failed_files = []  ##  قائمة لتخزين الملفات يلي فشلت بعملية الحذف

    for index, row in df.iterrows():  # هون بنعمل لووب على كل سطر بالملف
        filename = row["voices"].strip()  ## هون بنجيب اسم الملف الصوتي من السطر
        print(f" جاري معالجة: {filename}")  # بنطبع اسم الملف يلي عم نشتغل عليه
        input_path = os.path.join(
            input_folder, filename
        )  # هون بنعمل مسار للملف الصوتي حسب اسم الملف

        if not os.path.exists(input_path):  # هون بنشيك اذا الملف موجود ولا لا
            print(f" الملف غير موجود: {filename}")
            failed_files.append(
                (filename, "ملف غير موجود")
            )  ##  اذا مو موجود بنضيفه لقائمة الفشل
            continue

        try:
            rate, audio = read(input_path)  ## هون بنقرا الملف الصوتي باستخدام scipy
            if len(audio) == 0:  ##  اذا كان الملف فاضي بنطبع رسالة
                print(f" الملف فاضي: {filename}")  ##  هون بنطبع رسالة
                failed_files.append((filename, "ملف فاضي"))  ##  بنضيفه لقائمة الفشل
                continue

            correct_voices_after_deleted = AudioSegment(
                audio.tobytes(),
                frame_rate=rate,  # هون بنحول الملف الصوتي لبيانات صوتية باستخدام pydub
                sample_width=audio.dtype.itemsize,
                channels=1,
            )
            audio_chunks = (
                split_on_silence(  # هون بنقسم الصوت حسب السايلنس باستخدام pydub
                    correct_voices_after_deleted,
                    min_silence_len=1300,
                    silence_thresh=-45,
                    keep_silence=500,
                )
            )
            audio_processed = (
                sum(audio_chunks) if audio_chunks else correct_voices_after_deleted
            )  # هون بنجمع كل المقاطع الصوتية بعد تقسيمها
            audio_np = np.array(
                audio_processed.get_array_of_samples()
            )  # هون بنحول الصوت لمصفوفة  numpy
            output_path = os.path.join(
                output_folder, filename
            )  # هون بنعمل مسار للملف الصوتي بعد الحذف
            write(output_path, rate, audio_np)  #  هون بنخزن الصوت باستخدام scipy
            print(f" تم معالجة: {filename}")  #  هون بنطبع اسم الملف يلي تم معالجته

        except Exception as e:  # هون بنعمل كاتش للخطأ
            print(f" حصل خطأ في {filename}: {e}")  #  هون بنطبع الخطأ
            failed_files.append((filename, str(e)))  #  بنضيفه لقائمة الغلط

    print("\n📊 معالجة انتهت ✅")
    print(f"🔢 عدد الملفات التي نجحت: {len(df) - len(failed_files)}")
    print(f"❌ عدد الملفات التي فشلت: {len(failed_files)}")
    if failed_files:
        print("\n🧾 الملفات التي فشلت:")
        for fname, reason in failed_files:
            print(
                f" - {fname} => {reason}"
            )  #  هون بنطبع الملفات يلي فشلت بعملية الحذف وشو سبب الفشل


##  بنعمل فنكشن لدمج  الفويسات
def Merge_voices_in_one_voice(input_folder, output_path):
    def extract_number(filename):  ##  هون بنعمل فنكشن لاستخراج الرقم من اسم الملف
        match = re.search(r"(\d+)", filename)  #  هون بنبحث عن الرقم باستخدام regex
        return int(match.group()) if match else -1  #  اذا ما لقي رقم بنرجع -1

    files = [
        f for f in os.listdir(input_folder) if f.endswith(".wav")
    ]  # هون بنجيب كل الملفات الصوتية من المجلد
    files = sorted(
        files, key=extract_number
    )  # هون بنرتب الملفات حسب الرقم يلي طلعناه من الفنكشن يلي فوق

    merged = AudioSegment.silent(duration=0)  #  هون بنعمل ملف صوتي فاضي
    for filename in files:  ##  هون بنعمل لووب على كل الملفات الصوتية
        path = os.path.join(
            input_folder, filename
        )  ##  هون بنعمل مسار للملف الصوتي حسب اسمه
        audio = AudioSegment.from_wav(path)  ##  هون بنقرا الملف الصوتي باستخدام pydub
        merged += audio  #  هون بنجمع كل الملفات الصوتية مع بعض
        print(f" أُضيف: {filename}")  ##  هون بنطبع اسم الملف يلي تم اضافته

    merged.export(
        output_path, format="wav"
    )  ##  هون بنخزن الملف الصوتي الناتج باستخدام pydub
    print(
        f"\n تم دمج {len(files)} ملف في: {output_path}"
    )  #  ##  هون بنطبع عدد الملفات يلي تم دمجها والمكان يلي تم تخزينها فيه


##  فنكشن لحساب مدة الصوت أو الفيديو
def Duration(path):
    result = (
        subprocess.run(  ##  هون بنستخدم subprocess لتشغيل ffprobe وهي اداة مع ffmpeg
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",  #  ##  هون بنستخدم ffprobe لحساب المدة
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                path,
            ],  ##  هون بنحدد الخيارات  ffprobe
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  ##  هون بنحدد مكان تخزين الناتج
        )
    )
    return float(
        result.stdout.decode().strip()
    )  ##  هون بنرجع المدة كعدد عشري وبنسوي ازالة للفراغات بالملف


##  فنكشن  لتعديل سرعة الصوت ليتناسب مع الفيديو
def Optimize_speed_to_match_video(video_path, audio_path, speeded_audio_path):
    video_duration = Duration(
        video_path
    )  ##  هون بنحسب مدة الفيديو باستخدامالفنكشن  يلي فوق
    audio_duration = Duration(
        audio_path
    )  ##  هون بنحسب مدة الصوت باستخدام الفنكشن  يلي فوق
    print(f" مدة الفيديو: {round(video_duration, 2)} ثانية")  #  هون بنطبع مدة الفيديو
    print(
        f" مدة الصوت : {round(audio_duration, 2)} ثانية"
    )  #        #  هون بنطبع مدة الصوت
    if audio_duration >= video_duration:  #  هون بنشيك اذا مدة الصوت اكبر من مدة الفيديو
        speed = round(
            audio_duration / video_duration, 3
        )  # ياسيدي هاي عشان نحاول نعرف شو افضل سرعة ممكنة نسرع فيه الصوت قسمنا مدة الصوت على مدة الفيديو
        print(f"⚡ السرعة المطلوبة: {speed}x")
    else:  #  هون بنشيك اذا مدة الفيديو اكبر من مدة الصوت
        speed = round(video_duration / audio_duration, 3)
        print(f"⚡ السرعة المطلوبة: {speed}x")
    if speed <= 2.0:  #  هون بنشيك اذا السرعة اقل من 2.0
        atempo_filter = f"atempo={speed}"  # هاي ياسيدي بحكيلنا انه السرعة المطلوبة اقل من 2.0 فبنستخدم atempo filter وهو عبارة عن خاصية بالffmpeg للسرعة والسرعة الافتراضية فيه من نص الى اثنين ،فعشان هيك بنحكيله انه اذا اقل فاستخدمه هو مباشرة اما اذا اكثر فلازم تروح ةتقسم السرعة
    else:  #  هون بنشيك اذا السرعة اكبر من 2.0
        steps = []  #  هون بنعمل قائمة فارغة لتخزين الخطوات
        remaining = speed  #  هون بنخزن السرعة المطلوبة
        while remaining > 2.0:  #  هون بنشيك اذا السرعة المطلوبة اكبر من 2.0
            steps.append("atempo=2.0")  #  #  هون بنضيف الخطوة للقائمة
            remaining /= 2.0  #  #  هون بنقسم السرعة المطلوبة على 2.0
        steps.append(f"atempo={round(remaining, 3)}")  #  هون بنضيف الباقي   للقائمة
        atempo_filter = ",".join(steps)  #  هون بنجمع الخطوات مع بعض باستخدام الفاصلة

    cmd_speed = rf"""ffmpeg -i "{audio_path}" -filter:a "{atempo_filter}" -vn "{speeded_audio_path}" -y"""  ##  هون بنعمل امر ffmpeg لتعديل سرعة الصوت
    os.system(cmd_speed)  ##  هون بنشغل الامر باستخدام os.system
    print(" تم تسريع الصوت.")


##  فنكشن  لدمج الصوت مع الفيديو
def Merge_audio_with_video(video_path, audio_path, final_output_path):
    cmd_merge = rf"""ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest "{final_output_path}" -y"""  ##  هون بنعمل امر ffmpeg لدمج الصوت مع الفيديو
    os.system(cmd_merge)  ##  هون بنشغل الامر باستخدام os.system
    print(f" تم إنتاج الفيديو النهائي مع الصوت المتزامن: {final_output_path}")


# هاي المين تبع كلشي يا غالي
def Start_the_operation():
    import os
    import time

    # 🟢 جذر المشروع
    BASE_DIR = os.path.join(
        "C:\\Users\\sauui\\XTTS-project", "Graduation-Project", "DA499", "Our Work"
    )

    # 📁 المسارات المهمة
    TEXT_INPUT = os.path.join(BASE_DIR, "sayyid-work", "test-text", "نص-التجربة.txt")
    CSV_PATH = os.path.join(
        BASE_DIR, "sayyid_work", "video_and_csv", "timing_sentences_.csv"
    )
    VOICE_SAMPLE = os.path.join(
        BASE_DIR, "sayyid_work", "input-test-voice", "غرباء.wav"
    )
    ORIGINAL_AUDIO_FOLDER = os.path.join(
        BASE_DIR, "sayyid_work", "output-test-voice", "original-video-voice"
    )
    CLEANED_AUDIO_FOLDER = os.path.join(
        BASE_DIR, "sayyid_work", "output-test-voice", "removed-voices"
    )
    MERGED_AUDIO = os.path.join(
        BASE_DIR, "sayyid_work", "output-test-voice", "merged_output.wav"
    )
    ADJUSTED_AUDIO = os.path.join(
        BASE_DIR, "sayyid_work", "output-test-voice", "merged_output_adjusted.wav"
    )
    VIDEO_INPUT = os.path.join(
        BASE_DIR, "sayyid_work", "video_and_csv", "silent_video.mp4"
    )
    FINAL_VIDEO = os.path.join(BASE_DIR, "final-video.mp4")

    # 📂 إنشاء المجلدات إذا غير موجودة
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    os.makedirs(ORIGINAL_AUDIO_FOLDER, exist_ok=True)
    os.makedirs(CLEANED_AUDIO_FOLDER, exist_ok=True)
    os.makedirs(os.path.dirname(MERGED_AUDIO), exist_ok=True)
    os.makedirs(os.path.dirname(ADJUSTED_AUDIO), exist_ok=True)
    os.makedirs(os.path.dirname(FINAL_VIDEO), exist_ok=True)

    # 🕒 بدء المؤقت
    start_time = time.time()

    # 1️⃣ استخراج التوقيت والنص
    Extract_text_and_time(TEXT_INPUT, CSV_PATH)

    # 2️⃣ توليد الصوت
    Generate_audio(CSV_PATH, ORIGINAL_AUDIO_FOLDER, VOICE_SAMPLE)

    # 3️⃣ حذف السكوت
    Delete_silence_from_voices(CSV_PATH, ORIGINAL_AUDIO_FOLDER, CLEANED_AUDIO_FOLDER)

    # 4️⃣ دمج المقاطع الصوتية
    Merge_voices_in_one_voice(CLEANED_AUDIO_FOLDER, MERGED_AUDIO)

    # 5️⃣ تعديل السرعة
    Optimize_speed_to_match_video(VIDEO_INPUT, MERGED_AUDIO, ADJUSTED_AUDIO)

    # 6️⃣ دمج الصوت المعدل مع الفيديو
    Merge_audio_with_video(VIDEO_INPUT, ADJUSTED_AUDIO, FINAL_VIDEO)

    # ⏱️ نهاية المؤقت
    end_time = time.time()
    print(f" الوقت المستغرق: {end_time - start_time:.2f} ثانية")


# بلشلي المشروع اول ما تعمل رن
if __name__ == "__main__":
    Start_the_operation()
