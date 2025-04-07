from groq import Groq

# This class for using a LLM from GROQ Cloud so rather than download the LLM on our system, we can use this class to use the LLM from the cloud.
class Groq_Env():

    def __init__(self, API_Key="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",Model="qwen-2.5-32b"):
        """
        initialize the Groq_Env class with the API key and model name.
        """
        self._client= Groq(api_key=API_Key)
        self.model = Model

    def Groq_chat_completion(self, role = "assistant", messages_content = "مرحبا, كيف الحال",
              temperature=0.6, max_completion_tokens=4096, top_p=0.95, stream=True, stop=None):
        """
        Generate an answer using the Groq model.
        this function will help us in test Groq models and compare between them.
        We can use it inside the other methods.
        """
        # Generate answer using the Groq model
        completion = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": role, "content": messages_content}],
                temperature=temperature,
                max_completion_tokens=max_completion_tokens,
                top_p=top_p,
                stream=stream,
                stop=stop,
                )
        return completion

    def Groq_chat_answer(self, role = "assistant", messages_content = "مرحبا, كيف الحال",
              temperature=0.6, max_completion_tokens=4096, top_p=0.95, stream=True, stop=None):
        """
        Generate an answer using the Groq model.
        this function will return the answer as a string not as a chunks.
        """
        #Generate the completion from the method chat_completion
        completion = self.Groq_chat_completion(role, messages_content, temperature, max_completion_tokens, top_p, stream, stop)
        
        #convert the completion to string
        answer = ""
        for chunk in completion:
            answer += chunk.choices[0].delta.content or ""
        return answer
    
    def Groq_chat_answer_stream(self, role = "assistant", messages_content = "مرحبا, كيف الحال",
              temperature=0.6, max_completion_tokens=4096, top_p=0.95, stream=True, stop=None):
        """
        Generate an answer using the Groq model.
        this function will return the answer as a stream of chunks.
        """
        #Generate the completion from the method chat_completion
        completion = self.chat_completion(role, messages_content, temperature, max_completion_tokens, top_p, stream, stop)
        for chunk in completion:
            yield chunk.choices[0].delta.content or "" #stream the answer by using the yield keyword

# This Class can accepte both Groq and Ollama models.
class Full_LLM(Groq_Env):
    def __init__(self, model = "qwen-2.5-32b" ,api_key="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",Text=None,Online=True):
        Groq_Env.__init__(self, api_key, model)
        self.online = Online
        self.T_text = Text # text with time
        self.C_Text = self.del_time(Text) # text without time
        self.Prompts = {
                        "Summarize" : "based on the following text that represente a video transcript, I want you to generate a summary for this video in the arabic language. The text :"+f"\n'''{self.C_Text }'''"   
                        ,"Keywords" : "based on the following text that represente a video transcript, I want you to specify the most improtant keywords (the words that are improtant to know for any one want to be good in the video filed) \
                            in the arabic language and give them to me with a short summary about each one of them also in the Arabic language. The text :"+f"\n'''{self.C_Text }'''" 
                        ,"Summarize & Keywords" : "based on the following text that represente a video transcript,I want you to generate a summary for this video in the arabic language then specify the most improtant keywords (the words that are improtant to know for any one want to be good in the video filed) \
                            in the arabic language and give them to me with a short summary about each one of them also in the Arabic language. The text :"+f"\n'''{self.C_Text }'''"
                        ,"Transcript": "based on the following text that represente a video transcript, I want you to convert it to arabic language.\
                            keep in your mind that i want it more similar from the time spending in the read. The English text :"+f"\n'''{self.C_Text }'''"
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

    def ollama_answer(self, question, modell = "llama3.1:latest"):
        """
        Generate an answer using the ollama models.
        This function will help us in test ollama models and compare between them.
        We can use it inside the other methods.
        """
        from ollama import chat
        from ollama import ChatResponse

        response: ChatResponse = chat(model=modell, messages=[{ 'role': 'user','content': question},])
        # response.message.content doesn't work, just response['message']['content']     
        return response['message']['content'] 
    
    def model_answer(self, question,role = "user"):
        """
        specify the model that we want to use it then generate an answer using it.
        This function will help us in test multiple models and compare between them.
        We can use it inside the other methods.
        """
        # Generate answer using the LLM model
        if self.online:
            answer = self.Groq_chat_answer(role=role, messages_content=question)
        else:
            answer = self.ollama_answer(question, self.model)
        return answer

    def Summarize(self,text = None, model = "llama3.1:latest"):
        """
        Summarize the text using the LLM model.
        """
        if text is None:
            text = self.C_Text
        # Generate summary using the LLM model & Return it as a string        
        return self.model_answer(self.Prompts["Summarize"])

    def Keywords(self,text = None, model = "llama3.1:latest"):
        """
        Extract keywords from the text using the LLM model.
        """
        if text is None:
            text = self.C_Text
        # Generate keywords using the LLM model & Return it as a string        
        return self.model_answer(self.Prompts["Keywords"])
    
    def Summarize_Keywords(self,text = None, model = "llama3.1:latest"):
        """
        Summarize the text and extract keywords using the LLM model.
        So rather than using the two methods (Summarize & Keywords) we can use this method to do both of them in one time.
        This method is more efficient than the two methods above.
        """
        if text is None:
            text = self.C_Text

        # Generate summary and keywords using the LLM model
        return self.model_answer(self.Prompts["Summarize & Keywords"])
    
    def Transcript(self,text = None, model = "llama3.1:latest"):
        """
        Generate a transcript using the LLM model.
        """
        if text is None:
            text = self.C_Text

        # Generate transcript using the LLM model & Return it as a string
        return self.model_answer(self.Prompts["Transcript"])
    
    def Questions_Answers(self,text = None, model = "llama3.1:latest"):
        """
        Generate test questions and answers using the LLM model.
        """
        if text is None:
            text = self.C_Text
        # Generate test questions and answers using the LLM model & Return it as a string        
        return self.model_answer(self.Prompts["Quesitons & Answers"])
    
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
        return self.model_answer(question)
    
    def __str__(self):
        return f"LLM Class with model: {self.model} and text: {self.C_Text}"
