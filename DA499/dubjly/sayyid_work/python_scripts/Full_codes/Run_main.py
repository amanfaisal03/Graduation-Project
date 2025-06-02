from sayyid_work.python_scripts.Full_codes.Sayyid_work_TTS import *
import os
import time
import shutil
class Start_the_TTS_process:
    def __init__(self, text_input_path, base_dir=r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\dubjly", video_id=None):
        self.generator = Generating_audio()
        self.merger = MergingAudio()

        self.BASE_DIR = base_dir
        self.TEXT_INPUT = text_input_path
        self.video_id = video_id or "default"

        # المجلد الخاص بالفيديو الحالي
        self.OUTPUT_DIR = os.path.join(base_dir, "media", "video_outputs", f"video_{self.video_id}")

        # المسارات
        
       
       # self.VIDEO_INPUT_ORIGINAL = os.path.join(base_dir, "media", "video_outputs", f"video_{self.video_id}", f"original_video_{self.video_id}.mp4")
        self.VIDEO_OUTPUT_SILENT = os.path.join(self.OUTPUT_DIR, "silent_video.mp4")
        self.VIDEO_INPUT_ORIGINAL = os.path.join(base_dir,"video.mp4")
        self.CSV_PATH = os.path.join(self.OUTPUT_DIR, "timing_sentences_.csv")
        self.VOICE_SAMPLE = os.path.join(base_dir, "sayyid_work", "input-test-voice", "صوت اذاعي.wav")

        self.ORIGINAL_AUDIO_FOLDER = os.path.join(self.OUTPUT_DIR, "original-video-voice")
        self.CLEANED_AUDIO_FOLDER = os.path.join(self.OUTPUT_DIR, "removed-voices")
        self.MERGED_AUDIO = os.path.join(self.OUTPUT_DIR, "merged_output.wav")
        self.ADJUSTED_AUDIO = os.path.join(self.OUTPUT_DIR, "merged_output_adjusted.wav")
        self.FINAL_VIDEO = os.path.join(self.OUTPUT_DIR, f"Final_video_{self.video_id}.mp4")
        
        # إنشاء جميع المجلدات
        os.makedirs(self.ORIGINAL_AUDIO_FOLDER, exist_ok=True)
        os.makedirs(self.CLEANED_AUDIO_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(self.CSV_PATH), exist_ok=True)
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
        # 8️⃣ حفظ نسخة من ملف النص في مجلد الفيديو
        
        try:
            target_text_path = os.path.join(self.OUTPUT_DIR, "a_text.txt")
            shutil.copyfile(self.TEXT_INPUT, target_text_path)
            print(f"✔ تم حفظ نسخة من النص في: {target_text_path}")
        except Exception as e:
            print(f"❌ فشل في حفظ النص مع الفيديو: {e}")

        # ⏱️ نهاية التنفيذ
        end_time = time.time()
        print(f"\n⏱️ الوقت المستغرق: {end_time - start_time:.2f} ثانية")
