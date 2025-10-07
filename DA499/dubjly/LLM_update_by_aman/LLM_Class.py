#from Prompt_Class import Prompt
class The_LLM():
    def __init__(self, model,Text):
        self.model = model
        self.T_Text = Text # text with time
        self.C_Text = self.del_time(Text) # text without time
        self.Prompts = {
                        "Summarize" : "based on the following text that represente a video transcript, I want you to generate a summary for this video in the arabic language. The text :"+f"\n'''{self.C_Text }'''"   
                        ,"Keywords" : "based on the following text that represente a video transcript, I want you to specify the most improtant keywords (the words that are improtant to know for any one want to be good in the video filed) \
                            in the arabic language and give them to me with a short summary about each one of them also in the Arabic language. The text :"+f"\n'''{self.C_Text }'''" 
                        ,"Summarize & Keywords" : "based on the following text that represente a video transcript,I want you to generate a summary for this video in the arabic language then specify the most improtant keywords (the words that are improtant to know for any one want to be good in the video filed) \
                            in the arabic language and give them to me with a short summary about each one of them also in the Arabic language. The text :"+f"\n'''{self.C_Text }'''"
                        ,"Transcript": "based on the following text that represente a video transcript, I want you to convert it to arabic language.\
                            keep in your mind that i want it more similar from the time spending in the read. The English text :"+f"\n'''{self.T_Text }'''"
                        #,"Translate" : "based on the following text that represente a video transcript, I want you to translate the text to the arabic language. The text :"+f"\n'''{self.C_Text }'''"
                        ,"Quesitons & Answers" : "based on the following text that represente a video transcript, I want you to generate 5 test questions in the arabic language with them answers also in the Arabic. The text :"+f"\n'''{self.C_Text }'''"
                        ,"ChatBot Answer" : "based on the following text that represente a video transcript and your knowledge, answer the question that i will give to you. The text : "+f"\n'''{self.C_Text }''' \n"+" the question is : "
                        }

    def del_time(self,text):
        """
        Remove time from the text.
        """
        s = ""
        for i in text:
            if i == "\n":
                s += " "
            elif not i.isdigit():
                s += i
        print("Deleting Time Done")
        return s

    # def ollama_answer(self, question, modell = "llama3.1:latest"):
    #     """
    #     Generate an answer using the ollama models.
    #     This function will help us in test ollama models and compare between them.
    #     We can use it inside the other methods.
    #     """
    #     from ollama import chat
    #     from ollama import ChatResponse

        response: ChatResponse = chat(model=modell, messages=[{ 'role': 'user','content': question},])
        # response.message.content doesn't work, but response['message']['content']  work very well.
        #Notes :
            #retrun the response from the model in one line it's take less time than make a loop to get the response. 
            #s = ""
            #for chanke in response: s+= chanke['message']['content']

        return response['message']['content'] 
    
    def model_answer(self, question, model):
        """
        specify the model that we want to use it then generate an answer using it.
        This function will help us in test multiple models and compare between them.
        We can use it inside the other methods.
        """
        # Generate answer using the LLM model
        answer = self.model.generate(model, prompt = question)["response"]
        
        return answer

    def Summarize(self,text = None, model = "llama3.1:latest"):
        """
        Summarize the text using the LLM model.
        """
        if text is None:
            text = self.C_Text
        # Generate summary using the LLM model
        summary = self.ollama_answer(self.Prompts["Summarize"], model)
        
        return summary

    def Keywords(self,text = None, model = "llama3.1:latest"):
        """
        Extract keywords from the text using the LLM model.
        """
        if text is None:
            text = self.C_Text
        # Generate keywords using the LLM model
        keywords = self.model.generate(model, prompt =self.Prompts["Keywords"])["response"]
        
        return keywords
    
    def Summarize_Keywords(self,text = None, model = "llama3.1:latest"):
        """
        Summarize the text and extract keywords using the LLM model.
        So rather than using the two methods (Summarize & Keywords) we can use this method to do both of them in one time.
        This method is more efficient than the two methods above.
        """
        if text is None:
            text = self.C_Text

        # Generate summary and keywords using the LLM model
        summary_keywords = self.model.generate(model, prompt =self.Prompts["Summarize & Keywords"])["response"]
        
        return summary_keywords
    
    def Transcript(self,text = None, model = "llama3.1:latest"):
        """
        Generate a transcript using the LLM model.
        """
        if text is None:
            text = self.T_Text

        # Generate transcript using the LLM model
        transcript = self.model.generate(model, prompt =self.Prompts["Transcript"])["response"]
        
        return transcript
    
    
    def Questions_Answers(self,text = None, model = "llama3.1:latest"):
        """
        Generate test questions and answers using the LLM model.
        """
        if text is None:
            text = self.C_Text
        # Generate test questions and answers using the LLM model
        test_questions_answers = self.model.generate(model, prompt =self.Prompts["Quesitons & Answers"])["response"]
        
        return test_questions_answers
    
    def ChatBot_Answer(self,text = None, model = "llama3.1:latest", question = None):
        """
        Generate a chatbot answer using the LLM model.
        """
        if text is None:
            text = self.C_Text

        # Generate chatbot answer using the LLM model
        if question is None:
            raise ValueError("Question cannot be None.")
        
        question = self.Prompts["ChatBot Answer"] + question
        answer = self.model.generate(model, prompt =question)["response"]
        
        return answer
    
    def __str__(self):
        return f"LLM Class with model: {self.model} and text: {self.C_Text}"