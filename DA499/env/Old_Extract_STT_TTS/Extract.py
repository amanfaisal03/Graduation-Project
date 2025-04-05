from moviepy.video.io.VideoFileClip import VideoFileClip

# Define the input video file and output audio file
mp4_file = r"C:\Users\user\Videos\Screen Recordings\Screen Recording 2025-03-15 161003.mp4"
mp3_file = "audio.mp3"

# Load the video clip
video_clip = VideoFileClip(mp4_file)

# Extract the audio from the video clip
audio_clip = video_clip.audio

# Write the audio to a separate file
audio_clip.write_audiofile(mp3_file)

# Close the video and audio clips
audio_clip.close()
video_clip.close()

print("Audio extraction successful!")