from LLM_Class import The_LLM
from groq import Groq

class Groq_Env(The_LLM):

    def __init__(self, API_Key="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",Model="qwen-2.5-32b"):
        """
        initialize the Groq_Env class with the API key and model name.
        """
        self._client= Groq(api_key=API_Key)
        self._model = Model

    def chat_completion(self, role = "assistant", messages_content = "مرحبا, كيف الحال",
              temperature=0.6, max_completion_tokens=4096, top_p=0.95, stream=True, stop=None):
        """
        Generate an answer using the Groq model.
        this function will help us in test Groq models and compare between them.
        We can use it inside the other methods.
        """
        # Generate answer using the Groq model
        completion = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": role, "content": messages_content}],
                temperature=temperature,
                max_completion_tokens=max_completion_tokens,
                top_p=top_p,
                stream=stream,
                stop=stop,
                )
        return completion

    def chat_answer(self, role = "assistant", messages_content = "مرحبا, كيف الحال",
              temperature=0.6, max_completion_tokens=4096, top_p=0.95, stream=True, stop=None):
        """
        Generate an answer using the Groq model.
        this function will return the answer as a string not as a chunks.
        """
        #Generate the completion from the method chat_completion
        completion = self.chat_completion(role, messages_content, temperature, max_completion_tokens, top_p, stream, stop)
        
        #convert the completion to string
        answer = ""
        for chunk in completion:
            answer += chunk.choices[0].delta.content or ""
        return answer
    
    def chat_answer_stream(self, role = "assistant", messages_content = "مرحبا, كيف الحال",
              temperature=0.6, max_completion_tokens=4096, top_p=0.95, stream=True, stop=None):
        completion = self.chat_completion(role, messages_content, temperature, max_completion_tokens, top_p, stream, stop)
        for chunk in completion:
            yield chunk.choices[0].delta.content or "" #stream the answer by using the yield keyword

#Main Code
if __name__ == "__main__":
    G = Groq_Env("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", "qwen-2.5-32b")
    print(G.chat_answer(role="user", messages_content="ما تاريخ اخر معلومات انت تدربت عليها ؟"))




