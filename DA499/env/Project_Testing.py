#here we will test our project, pipline and parts of it.
from Extract_Voice_and_STT_Aman.phase_one import *
from LLM_Saad.LLM_Online import *

if __name__ == "__main__":

    # Test Phase 1: Extract Voice and STT
    video_url = input(" put your URL : ")
    result = check_video(video_url)
    print(result)
    output_file = "extracted_audio.mp3"
    extract_audio(video_url, output_file, output_format='mp3') 

    model=WhisperModel('small',device='cuda',compute_type='float16')
    segmints,info=model.transcribe(r"extracted_audio.mp3",beam_size=5)
    The_text= ""
    for segmint in segmints :
        new_line=f"[{segmint.start:.2f} - {segmint.end:.2f}]{segmint.text}\n"
        The_text+= new_line
        #print(new_line,end="")
    text_file = open("Text.txt", "w")
    text_file.write(s)
    text_file.close()
    
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