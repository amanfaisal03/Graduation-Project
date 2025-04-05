from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import speech_recognition as sr

# Extract audio from video file
ffmpeg_extract_audio(r"C:\Users\user\Videos\Screen Recordings\Screen Recording 2025-03-15 171708.mp4", "geeksforgeeks.wav")

# Initialize recognizer
r = sr.Recognizer()  # Ensure the recognizer is defined here

# Load the audio file
with sr.AudioFile("geeksforgeeks.wav") as source:
    data = r.record(source)

# Convert speech to text
text = r.recognize_google(data)

# Print the text
print("\nThe resultant text from video is: \n")
print(text)
