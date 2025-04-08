import yt_dlp
import ffmpeg
import subprocess
import os
from faster_whisper import WhisperModel

def check_video(video_url):
    ydl_opts = {
        "quiet": True, 
        "no_warnings": True,
        "noplaylist": True,  
        "extract_flat": True,  
        "force_generic_extractor": True,  
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        return {
            "status": "Available",
            "title": info.get("title", "Unknown"),
        }

    except yt_dlp.utils.DownloadError:
        return {"status": "Not Available", "message": "Video not found or restricted."}

# video_url = input(" put your URL : ")
# result = check_video(video_url)
# print(result) 

def extract_audio(video_url, output_file, output_format='mp3'):

    if output_format not in ['mp3', 'aac']:
        raise ValueError("Invalid output format. Choose 'mp3' or 'aac'.")

    temp_audio_file = "temp_audio.m4a"

    yt_dlp_cmd = [
        'yt-dlp', '-f', 'bestaudio', '-o', temp_audio_file, video_url
    ]
    subprocess.run(yt_dlp_cmd, check=True)

    ffmpeg_cmd = [
        'ffmpeg', '-i', temp_audio_file, '-vn',
        '-acodec', 'libmp3lame' if output_format == 'mp3' else 'aac',
        '-ar', '44100', '-ab', '192k', '-f', output_format, output_file
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    os.remove(temp_audio_file)


# output_file = "extracted_audio.mp3"
# extract_audio(video_url, output_file, output_format='mp3')

model=WhisperModel('small',device='cuda',compute_type='float16')
segmints,info=model.transcribe(r"extracted_audio.mp3",beam_size=5)
s = ""
for segmint in segmints :
    new_line=f"[{segmint.start:.2f} - {segmint.end:.2f}]{segmint.text}\n"
    s+= new_line
    print(new_line,end="")
text_file = open("Text.txt", "w")
text_file.write(s)
text_file.close()