#here we will test our project, pipline and parts of it.
from Extract_Voice_and_STT_Aman.phase_one import *
from LLM_Saad.LLM_Online import *
import SpeechToText as stt
import sys
import os


if __name__ == "__main__":

    # Test Phase 1: Extract Voice and STT
    video_url = input(" put your URL : ")
    result = check_video(video_url)
    print(result)
    output_file = "extracted_audio.mp3"
    extract_audio(video_url, output_file, output_format='mp3') 
    The_text = "" # here we will put the method that will use it to extract the text from the audio file, and it will be the input for the LLM.
    
    # Test Phase 2: LLM Class
    model = "meta-llama/llama-4-scout-17b-16e-instruct"
    Groq_key = "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"
    llm = Full_LLM(model=model, api_key=Groq_key, Text=The_text, Online=True)
    print(llm.Summarize())
    print(llm.Keywords())
    print(llm.Summarize_Keywords())
    Transcript = llm.Transcript() # the input text for TTS
    print(Transcript)
    print(llm.Questions_Answers())
    print(llm.ChatBot_Answer(question="What is the main topic of the text?"))
    print(llm)

    #Test Phase 3: Text to Speech (TTS)
    # 