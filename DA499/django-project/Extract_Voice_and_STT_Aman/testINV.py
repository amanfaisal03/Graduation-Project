import yt_dlp
import ffmpeg
import subprocess
import os
import torch
from transformers import pipeline

class TTS():

    def __init__(self, url): # tts = TTS(url_video)
        self.video_url = url
        self.audio_name = "audio.mp3"
        self.output_format = 'mp3'
        self.temp_audio_file = "temp_audio.m4a"
        self.video_name = "video.mp4"
        self.video_format = 'mp4'
        
        # Initialize Whisper model using public HuggingFace model
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Create the pipeline using a publicly available model (OpenAI's Whisper small)
        self.asr_pipeline = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-small",
            chunk_length_s=30,
            return_timestamps=True,
            device=device,
        )
        
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
            raise ValueError("Video not found or restricted.")
    
    def download_video(self):
        ydl_opts = {
            'format': self.video_format,
            'outtmpl': self.video_name, 
            'noplaylist': True,
            'quiet': False,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.video_url])

    def extract_audio(self): # tts.extract_audio()
        yt_dlp_cmd = [
            'yt-dlp', '-f', 'bestaudio', '-o', self.temp_audio_file, self.video_url
        ]
        subprocess.run(yt_dlp_cmd, check=True)

        ffmpeg_cmd = [
            'ffmpeg', '-i', self.temp_audio_file, '-vn',
            '-acodec', 'libmp3lame' if self.output_format == 'mp3' else 'aac',
            '-ar', '44100', '-ab', '192k', '-f', self.output_format, self.audio_name
        ]
        subprocess.run(ffmpeg_cmd, check=True)

        os.remove(self.temp_audio_file)

    def STT_M(self): # tts.TTS_M()
        # Use Whisper model for transcription
        result = self.asr_pipeline(self.audio_name)
        
        # Format the output to match the expected format
        s = ""
        
        # Whisper pipeline returns chunks with timestamps
        if "chunks" in result:
            for chunk in result["chunks"]:
                start = chunk.get("timestamp", [0, 0])[0]
                end = chunk.get("timestamp", [0, 0])[1]
                text = chunk.get("text", "")
                new_line = f"[{start:.2f} - {end:.2f}]{text}\n"
                s += new_line
        # Standard format with timestamps
        elif isinstance(result, dict) and "timestamps" in result:
            for timestamp in result["timestamps"]:
                start, end, text = timestamp
                new_line = f"[{start:.2f} - {end:.2f}]{text}\n"
                s += new_line
        # Whisper often provides chunks in this format
        elif isinstance(result, dict) and "text" in result and "chunks" in result:
            for chunk in result["chunks"]:
                start = chunk.get("start", 0)
                end = chunk.get("end", 0)
                text = chunk.get("text", "")
                new_line = f"[{start:.2f} - {end:.2f}]{text}\n"
                s += new_line
        # Fall back to simply parsing result structure
        else:
            try:
                # Try to extract timestamp from the standard OpenAI Whisper result format
                for segment in result.get("segments", []):
                    start = segment.get("start", 0)
                    end = segment.get("end", 0)
                    text = segment.get("text", "")
                    new_line = f"[{start:.2f} - {end:.2f}]{text}\n"
                    s += new_line
            except:
                # If all extraction methods fail, return the plain text
                s = result.get("text", "") if isinstance(result, dict) else str(result)
                
        return s
    
    def run_all(self): # tts.run_all()
        self.check_video()
        self.download_video()
        self.extract_audio()
        return self.STT_M()

    def __str__(self):
        return f"Video URL: {self.video_url}\n video File : {self.video_name} \n Audio File: {self.audio_name}\nOutput Format: {self.output_format}"