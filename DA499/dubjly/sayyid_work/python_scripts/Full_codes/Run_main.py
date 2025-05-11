from sayyid_work.python_scripts.Full_codes.Sayyid_work_TTS import *
import os
import time

class Start_the_TTS_process:
    def __init__(self,text_input_path, base_dir=r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\dubjly"):
        self.generator = Generating_audio()
        self.merger = MergingAudio()

        self.BASE_DIR = base_dir
        self.TEXT_INPUT = text_input_path  # المسار الذي يحتوي على النص المُستخرج من سعد

        # مسارات الفيديو
        self.VIDEO_INPUT_ORIGINAL = os.path.join(base_dir, "video.mp4")
        self.VIDEO_OUTPUT_SILENT = os.path.join(base_dir, "sayyid_work", "video_and_csv", "silent_video.mp4")

        # مسار ملف CSV المؤقت للنصوص والتوقيتات
        self.CSV_PATH = os.path.join(base_dir, "sayyid_work", "video_and_csv", "timing_sentences_.csv")

        # مسار ملف العينة الصوتية
        self.VOICE_SAMPLE = os.path.join(base_dir, "sayyid_work", "input-test-voice", "غرباء.wav")

        # مجلدات الصوتيات
        self.ORIGINAL_AUDIO_FOLDER = os.path.join(base_dir, "sayyid_work", "output-test-voice", "original-video-voice")
        self.CLEANED_AUDIO_FOLDER = os.path.join(base_dir, "sayyid_work", "output-test-voice", "removed-voices")
        
        # مسارات ملفات الصوت النهائي
        self.MERGED_AUDIO = os.path.join(base_dir, "sayyid_work", "output-test-voice", "merged_output.wav")
        self.ADJUSTED_AUDIO = os.path.join(base_dir, "sayyid_work", "output-test-voice", "merged_output_adjusted.wav")
        
        # مسار الفيديو النهائي
        self.FINAL_VIDEO = os.path.join(base_dir, "media", "Final_video.mp4")

        # إنشاء المجلدات إذا لم تكن موجودة
        os.makedirs(os.path.dirname(self.CSV_PATH), exist_ok=True)
        os.makedirs(self.ORIGINAL_AUDIO_FOLDER, exist_ok=True)
        os.makedirs(self.CLEANED_AUDIO_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(self.MERGED_AUDIO), exist_ok=True)
        os.makedirs(os.path.dirname(self.ADJUSTED_AUDIO), exist_ok=True)
        os.makedirs(os.path.dirname(self.FINAL_VIDEO), exist_ok=True)

    def run(self):
        start_time = time.time()  # ⏱️ بدء العد الزمني

        # 1️⃣ إنشاء فيديو صامت من الفيديو الأصلي
        self.merger.Remove_Audio_From_Video(
            self.VIDEO_INPUT_ORIGINAL,
            self.VIDEO_OUTPUT_SILENT
        )

        # 2️⃣ استخراج التوقيت والنصوص من الملف النصي
        self.generator.Extract_text_and_time(
            self.TEXT_INPUT,
            self.CSV_PATH
        )

        # 3️⃣ توليد الصوت من النصوص
        self.generator.Generate_audio(
            self.CSV_PATH,
            self.ORIGINAL_AUDIO_FOLDER,
            self.VOICE_SAMPLE
        )

        # 4️⃣ حذف فترات السكوت من الصوتيات
        self.generator.Delete_silence_from_voices(
            self.CSV_PATH,
            self.ORIGINAL_AUDIO_FOLDER,
            self.CLEANED_AUDIO_FOLDER
        )

        # 5️⃣ دمج الصوتيات في ملف واحد
        self.merger.Merge_voices_in_one_voice(
            self.CLEANED_AUDIO_FOLDER,
            self.MERGED_AUDIO
        )

        # 6️⃣ ضبط سرعة الصوت ليتناسب مع مدة الفيديو
        self.merger.Optimize_speed_to_match_video(
            self.VIDEO_OUTPUT_SILENT,
            self.MERGED_AUDIO,
            self.ADJUSTED_AUDIO
        )

        # 7️⃣ دمج الصوت المعدل مع الفيديو الصامت
        self.merger.Merge_audio_with_video(
            self.VIDEO_OUTPUT_SILENT,
            self.ADJUSTED_AUDIO,
            self.FINAL_VIDEO
        )

        # ⏱️ نهاية التنفيذ
        end_time = time.time()
        print(f"\n⏱️ الوقت المستغرق: {end_time - start_time:.2f} ثانية")
