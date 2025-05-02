from Sayyid_work_TTS import *
import os 


class Start_the_TTS_process:
    def __init__(self, base_dir, text_input_path):
        self.generator = Generating_audio()
        self.merger = MergingAudio()

        self.BASE_DIR = base_dir
        self.TEXT_INPUT = text_input_path  # هاي المسار تبع النص اللي بدنا نشتغل عليه يلي اخذته من سعد 
        self.CSV_PATH = os.path.join(base_dir, "sayyid-work", "video_and_csv", "timing_sentences_.csv")
        self.VOICE_SAMPLE = os.path.join(base_dir, "sayyid-work", "input-test-voice", "غرباء.wav")
        self.ORIGINAL_AUDIO_FOLDER = os.path.join(base_dir, "sayyid-work", "output-test-voice", "original-video-voice")
        self.CLEANED_AUDIO_FOLDER = os.path.join(base_dir, "sayyid-work", "output-test-voice", "removed-voices")
        self.MERGED_AUDIO = os.path.join(base_dir, "sayyid-work", "output-test-voice", "merged_output.wav")
        self.ADJUSTED_AUDIO = os.path.join(base_dir, "sayyid-work", "output-test-voice", "merged_output_adjusted.wav")
        self.VIDEO_INPUT = os.path.join(base_dir, "sayyid-work", "video_and_csv", "silent_video.mp4")
        self.FINAL_VIDEO = os.path.join(base_dir, "final-video.mp4")

        # 📂 إنشاء المجلدات إذا غير موجودة
        os.makedirs(os.path.dirname(self.CSV_PATH), exist_ok=True)
        os.makedirs(self.ORIGINAL_AUDIO_FOLDER, exist_ok=True)
        os.makedirs(self.CLEANED_AUDIO_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(self.MERGED_AUDIO), exist_ok=True)
        os.makedirs(os.path.dirname(self.ADJUSTED_AUDIO), exist_ok=True)
        os.makedirs(os.path.dirname(self.FINAL_VIDEO), exist_ok=True)

    def run(self):
        start_time = time.time()  # هاي بس عشان احسب مدة تنفيذ الكود

        # 1️⃣ استخراج التوقيت والنص
        self.generator.Extract_text_and_time(self.TEXT_INPUT, self.CSV_PATH)

        # 2️⃣ توليد الصوت
        self.generator.Generate_audio(self.CSV_PATH, self.ORIGINAL_AUDIO_FOLDER, self.VOICE_SAMPLE)

        # 3️⃣ حذف السكوت
        self.generator.Delete_silence_from_voices(self.CSV_PATH, self.ORIGINAL_AUDIO_FOLDER, self.CLEANED_AUDIO_FOLDER)

        # 4️⃣ دمج المقاطع الصوتية
        self.merger.Merge_voices_in_one_voice(self.CLEANED_AUDIO_FOLDER, self.MERGED_AUDIO)

        # 5️⃣ تعديل السرعة
        self.merger.Optimize_speed_to_match_video(self.VIDEO_INPUT, self.MERGED_AUDIO, self.ADJUSTED_AUDIO)

        # 6️⃣ دمج الصوت المعدل مع الفيديو
        self.merger.Merge_audio_with_video(self.VIDEO_INPUT, self.ADJUSTED_AUDIO, self.FINAL_VIDEO)

        # ⏱️ نهاية المؤقت
        end_time = time.time()
        print(f"⏱️ الوقت المستغرق: {end_time - start_time:.2f} ثانية")





