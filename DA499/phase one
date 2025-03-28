import yt_dlp
import ffmpeg
import subprocess


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

video_url = input(" put your URL : ")
result = check_video(video_url)
print(result)

def convert_video_to_audio(video_url, audio_file_path):
    command = f"ffmpeg -i {video_url} -vn -acodec pcm_s16le -ar 44100 -ac 2 {audio_file_path}"
    subprocess.call(command, shell=True)

convert_video_to_audio("input_video.mp4", "output_audio.wav")

def stream_video_audio(video_url):
    command = ["ffplay", "-nodisp", "-autoexit", video_url]
    subprocess.call(command)


stream_video_audio(video_url)  
