from STT import *

if __name__ == "__main__":

    video_url = input(" put your URL : ")
    tts = TTS(video_url)
    Transcript = tts.run_all()
    File = open("Transcript.txt", "w")
    File.write(Transcript)
    File.close()
    print(Transcript)