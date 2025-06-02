import yt_dlp
import ffmpeg
import subprocess
import os
from faster_whisper import WhisperModel

class TTS():

    def __init__(self,url): # tts = TTS(url_video)
        self.video_url=url
        self.audio_name="audio.mp3"
        self.output_format='mp3'
        self.temp_audio_file = "temp_audio.m4a"
        self.video_name="video.mp4"
        self.video_format='mp4'
        self.model = WhisperModel('small', device='cuda', compute_type='float16')
        self.check_video()
        
    def check_video(self):
        ydl_opts = {
        "quiet": True, 
        "no_warnings": True,
        "noplaylist": True,  
        "extract_flat": True,  
        "force_generic_extractor": True,  
                    }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
               info = ydl.extract_info(self.video_url, download=False)

            return {
            "status": "Available",
            "title": info.get("title", "Unknown"),
            }

        except yt_dlp.utils.DownloadError:
             #return {"status": "Not Available", "message": "Video not found or restricted."}
             raise ValueError("Video not found or restricted.")
    

    def download_video(self):
        #  حذف الفيديو السابق إذا موجود
        if os.path.exists(self.video_name):
         os.remove(self.video_name)
         print(f"🗑️ تم حذف الفيديو السابق: {self.video_name}")
        ydl_opts = {
            'format': self.video_format,
            'outtmpl': self.video_name , 
            'noplaylist': True,
            'quiet': False,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.video_url])

    def extract_audio(self): # tts.extract_audio()

        #if self.output_format not in ['mp3', 'aac']:
        #    raise ValueError("Invalid output format. Choose 'mp3' or 'aac'.")

        yt_dlp_cmd = [
                   'yt-dlp', '-f', 'bestaudio', '-o', self.temp_audio_file, self.video_url
                   ]
        subprocess.run(yt_dlp_cmd, check=True)

        ffmpeg_cmd = [
        'ffmpeg','-y', '-i', self.temp_audio_file, '-vn',
        '-acodec', 'libmp3lame' if self.output_format == 'mp3' else 'aac',
        '-ar', '44100', '-ab', '192k', '-f', self.output_format, self.audio_name
            ]
        subprocess.run(ffmpeg_cmd, check=True)

        os.remove(self.temp_audio_file)


    def STT_M(self): # tts.TTS_M()
        segments=self.model.transcribe(self.audio_name, beam_size=5)[0]
        s = ""
        for segment in segments :
            new_line=f"[{segment.start:.2f} - {segment.end:.2f}]{segment.text}\n"
            s+= new_line
        return s
    
    def run_all(self): # tts.run_all()
        self.check_video()
        self.download_video()
        self.extract_audio()
        return self.STT_M()

    def __str__(self):
        return f"Video URL: {self.video_url}\n video File : {self.video_name} \n Audio File: {self.audio_name}\nOutput Format: {self.output_format}" 