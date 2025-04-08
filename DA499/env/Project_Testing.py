#here we will test our project, pipline and parts of it.
from Extract_Voice_and_STT_Aman.STT import *
from LLM_Saad.LLM_Online import *
import yt_dlp
import ffmpeg
import subprocess
import os
from faster_whisper import WhisperModel

if __name__ == "__main__":

    # Test Phase 1: Extract Voice and STT
    video_url = input(" put your URL : ") #Video Link: https://www.youtube.com/watch?v=6M5VXKLf4D4
    tts = TTS(video_url)
    The_text = tts.run_all()
    File = open("Transcript.txt", "w")
    File.write(The_text)
    File.close()
    print(The_text)
    
    # Test Phase 2: LLM Class
    text_file = open("LLM.txt", "w")

    model = "meta-llama/llama-4-scout-17b-16e-instruct"
    Groq_key = "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"
    llm = Full_LLM(model=model, api_key=Groq_key, Text=The_text, Online=True)
    summary = llm.Summarize()
    print("The Summary :\n",summary);text_file.write("The Summary :\n"+summary)
    keywords = llm.Keywords()
    print("\nThe Keywords: \n",keywords);text_file.write("\nThe Keywords: \n"+keywords)
    Summary_Keywords = llm.Summarize_Keywords()
    print("\nSummrize & Keywords:\n",Summary_Keywords);text_file.write("\nSummrize & Keywords:\n"+Summary_Keywords)
    Transcript = llm.Transcript() # the input text for TTS
    print("\nThe Transcript:\n",Transcript);text_file.write("\nThe Transcript:\n"+Transcript)
    Question_Answers = llm.Questions_Answers()
    print("\nQuestions & Answers:\n",Question_Answers);text_file.write("\nQuestions & Answers:\n"+Question_Answers)
    Question = "What is the main topic of the text?" # Example question, This should be user input
    ChatBot_Answer = llm.ChatBot_Answer(question=Question)
    print("\nChatBot Answer:\n",ChatBot_Answer);text_file.write("\nChatBot Answer:\n"+ChatBot_Answer)
    text_file.close()
    #print(llm)

    #Test Phase 3: Text to Speech (TTS)
    # 