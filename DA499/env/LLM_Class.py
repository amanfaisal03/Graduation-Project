class The_LLM:
    def __init__(self, model,Text):
        self.model = model
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

    def ollama_answer(self, question, modell = "llama3.1:latest"):
        """
        Generate an answer using the ollama models.
        This function will help us in test ollama models and compare between them.
        We can use it inside the other methods.
        """
        from ollama import chat
        from ollama import ChatResponse

        response: ChatResponse = chat(model=modell, messages=[{ 'role': 'user','content': question}])
        message = response.message.content # or response['message']['content']     
        return message
    
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
        summary = self.model.generate(model, prompt = self.Prompts["Summarize"])["response"]
        
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
            text = self.C_Text

        # Generate transcript using the LLM model
        transcript = self.model.generate(model, prompt =self.Prompts["Transcript"])["response"]
        
        return transcript
    
        '''    def Translate(self,text = None, model = "llama3.1:latest"):
                """
                Translate the text using the LLM model.
                """
                if text is None:
                    text = self.C_Text

                # Generate translation using the LLM model
                translation = self.model.generate(model, prompt =self.Prompts["Translate"])["response"]
                
                return translation'''
    
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

#main code
if __name__ == "__main__":
    import ollama

    #Video Link: https://www.youtube.com/watch?v=6M5VXKLf4D4
    #Tool that i use it to get the English Transcript from the video : https://notegpt.io/youtube-transcript-generator
    text ="""
    00:00:00	ever wondered how google translates an entire web page to a different language in a matter of seconds or your phone gallery group's images based on their location all of this is a product of deep learning but what exactly is deep learning deep learning is a subset of machine learning which in turn is a subset of artificial intelligence artificial intelligence is a technique that enables a machine to mimic human behavior machine learning is a technique to achieve ai through algorithms trained with data and finally deep learning is a
    00:00:34	type of machine learning inspired by the structure of the human brain in terms of deep learning this structure is called an artificial neural network let's understand deep learning better and how it's different from machine learning say we create a machine that could differentiate between tomatoes and cherries if done using machine learning we'd have to tell the machine the features based on which the two can be differentiated these features could be the size and the type of stim on them with deep learning on the other hand the
    00:01:04	features are picked out by the neural network without human intervention of course that kind of independence comes at the cost of having a much higher volume of data to train our machine now let's dive into the working of neural networks here we have three students each of them write down the digit 9 on a piece of paper notably they don't all write it identically the human brain can easily recognize the digits but what if a computer had to recognize them that's where deep learning comes in here's a neural network trained to
    00:01:39	identify handwritten digits each number is present as an image of 28 times 28 pixels now that amounts to a total of 784 pixels neurons the core entity of a neural network is where the information processing takes place each of the 784 pixels is fed to a neuron in the first layer of our neural network this forms the input layer on the other end we have the output layer with each neuron representing a digit with the hidden layers existing between them the information is transferred from one layer to another over connecting
    00:02:16	channels each of these has a value attached to it and hence is called a weighted channel all neurons have a unique number associated with it called bias this bias is added to the weighted sum of inputs reaching the neuron which is then applied to a function known as the activation function the result of the activation function determines if the neuron gets activated every activated neuron passes on information to the following layers this continues until the second last layer the one neuron activated in the
    00:02:52	output layer corresponds to the input digit the weights and bias are continuously adjusted to produce a well-trained network so where is deep learning applied in customer support when most people converse with customer support agents the conversation seems so real they don't even realize that it's actually a bot on the other side in medical care neural networks detect cancer cells and analyze mri images to give detailed results self-driving cars what seem like science fiction is now a reality apple tesla and nissan are only
    00:03:29	a few of the companies working on self-driving cars so deep learning has a vast scope but it too faces some limitations the first as we discussed earlier is data while deep learning is the most efficient way to deal with unstructured data a neural network requires a massive volume of data to train let's assume we always have access to the necessary amount of data processing this is not within the capability of every machine and that brings us to our second limitation computational power training in neural
    00:04:03	network requires graphical processing units which have thousands of cores as compared to cpus and gpus are of course more expensive and finally we come down to training time deep neural networks take hours or even months to train the time increases with the amount of data and number of layers in the network so here's a short quiz for you arrange the following statements in order to describe the working of a neural network a the bias is added b the weighted sum of the inputs is calculated c specific
    00:04:41	neuron is activated d the result is fed to an activation function leave your answers in the comments section below three of you stand a chance to win amazon vouchers so hurry some of the popular deep learning frameworks include tensorflow pytorch keras deep learning 4j cafe and microsoft cognitive toolkit considering the future predictions for deep learning and ai we seem to have only scratched the surface in fact horus technology is working on a device for the blind that uses deep learning with
    00:05:14	computer vision to describe the world to the users replicating the human mind at the entirety may be not just an episode of science fiction for too long the future is indeed full of surprises and that is deep learning for you in short if you enjoyed this video do like and share it also subscribe to our channel if you haven't yet as we have a lot more exciting videos coming up fun learning till then
    """
    llm = The_LLM(ollama, text)
    model = "llama3.1:latest"
    print(type(model))

    print(llm.Summarize())
    print(llm.Keywords())
    print(llm.Summarize_Keywords())
    print(llm.Transcript())
    print(llm.Translate())
    print(llm.Questions_Answers())
    print(llm.ChatBot_Answer(question="What is the main topic of the text?"))
    print(llm)
    pirnt(help(llm.Summarize_Keywords))