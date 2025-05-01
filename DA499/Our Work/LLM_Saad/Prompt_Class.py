class Prompt:

    def __init__(self,Text = None) :
        self.T_text = Text # text with time
        self.C_Text = self.del_time(Text) # text without time
    
    def summarize_prompt(self):
        """
        Prompt for summarizing the text.
        """
        prompt = f"""
        Summarize the following text:
        {self.C_Text}
        """
        return prompt

    
# Optimization :
'''
1. Class Name: Prompt
2. Make a Memory Conversaiton
3.  
'''