from moviepy.video.io.VideoFileClip import VideoFileClip
import speech_recognition as sr 

# Load the video 
video = VideoFileClip( r"C:\Users\user\Videos\Screen Recordings\Screen Recording 2025-03-15 171708.mp4") 

# Extract the audio from the video 
audio_file = video.audio 
audio_file.write_audiofile("geeksforgeeks.wav") 

# Initialize recognizer 
r = sr.Recognizer() 

# Load the audio file 
with sr.AudioFile("geeksforgeeks.wav") as source: 
	data = r.record(source) 

# Convert speech to text 
text = r.recognize_google(data) 

# Print the text 
print("\nThe resultant text from video is: \n") 
print(text) 
