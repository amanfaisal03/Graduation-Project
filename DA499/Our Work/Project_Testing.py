#here we will test our project, pipline and parts of it.
from Extract_Voice_and_STT_Aman.STT import *
from LLM_Saad.LLM_Online import *
from sayyid_work.python_scripts import *
from  Full_codes import *
from Run_main import Start_the_TTS_process
import yt_dlp
import ffmpeg
import subprocess
import os
from faster_whisper import WhisperModel
import time 

if __name__ == "__main__":

    """
    Test Phase 1: Extract Voice and STT
    """
    # New Test 42 seconed video : https://www.youtube.com/shorts/5xp0taGM3Kg
    video_url = input(" put your URL : ") #Video Link: https://www.youtube.com/watch?v=6M5VXKLf4D4
    tts = TTS(video_url)
    tts_text = tts.run_all()
    File = open("Transcript.txt", "w")
    File.write(tts_text)
    File.close()
    print(tts_text)

    file = open(r"Transcript.txt", "r")
    The_text = file.read()
    file.close()

    """
    Test Phase 2: LLM Class
    """
    text_file = open(r"LLM.txt", "w", encoding="utf-8") 
    # encoding="utf-8" is important for Arabic text to be saved correctly without any errors

    model = "meta-llama/llama-4-scout-17b-16e-instruct"
    Groq_key = "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"
    llm = Full_LLM(model=model, api_key=Groq_key, Text=The_text, Online=True)

    summary = llm.Summarize()
    print("The Summary :\n", summary)
    text_file.write("The Summary:\n" + summary + "\n")

    keywords = llm.Keywords()
    print("\nThe Keywords: \n", keywords)
    text_file.write("\nThe Keywords:\n" + keywords + "\n")

    Summary_Keywords = llm.Summarize_Keywords()
    print("\nSummrize & Keywords:\n", Summary_Keywords)
    text_file.write("\nSummrize & Keywords:\n" + Summary_Keywords + "\n")

    Transcript = llm.Transcript()  # the input text for TTS
    print("\nThe Transcript:\n", Transcript)
    text_file.write("\nThe Transcript:\n" + Transcript + "\n")

    Question_Answers = llm.Questions_Answers()
    print("\nQuestions & Answers:\n", Question_Answers)
    text_file.write("\nQuestions & Answers:\n" + Question_Answers + "\n")

    Question = "يخوي شو هو الموظوع تبع الفيديو"  # Example question, This should be user input
    ChatBot_Answer = llm.ChatBot_Answer(question=Question)
    print("\nChatBot Answer:\n", ChatBot_Answer)
    text_file.write("\nChatBot Answer:\n" + ChatBot_Answer)

    text_file.close()
    #print(llm)

    """
    Test Phase 3: Text to Speech (TTS)
    """
    # sayyid work
    Text_path = r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\OUR WORK\sayyid-work\test-text\Main_text.txt"     #هاي المسار تبع النص اللي بدنا نشتغل عليه
    with open(Text_path, "w", encoding="utf-8") as f:
        f.write(Transcript)  # هذا المتغير جاي من شغل التيم (الـ LLM)

    
    base_path = r"C:\Users\sauui\XTTS-project\Graduation-Project\DA499\OUR WORK"       #هاظ الباث عشان اذا حدا بده يعمل رن عنده يقدر يغير زي مابده بالمسار الاساسي بحيث يزبط  معه 
    Video = Start_the_TTS_process(base_path, text_input_path=Text_path)
    Video.run()