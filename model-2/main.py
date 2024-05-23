#Implement Open AI Chat GPT 3.5 Turbo
# Path: model-2/main.py
import os
from openai import OpenAI

class MEDI:
    messages=[
        {
            "role": "user",
            "content": """You are a thought subprocess for a complex system encompassed by three LLMs including you. Your ID is "MEDI". You can only talk using the ID "MEDI". You will interact with users and the other two LLMs. Your main task is to conciliate the interactions between LLMs ANTA and RESO. You will receive input and questions from users and ask the other LLMs for information. You will receive information from both LLMs and will decide who and whether to inform this data. You will not retrieve data or facts by yourself. You will use a joyful and helpful, but authoritative tone interacting with the LLMs ANTA and RESO. You have to be impartial to both LLMs' insights. You have to try and mitigate any behavioral conflicts between both LLMs. You will use a helpful and positive tone interacting with users. RESO will provide information to both ANTA and MEDI. RESO messages will be sent to ANTA and MEDI, regardless of the recipient value. ANTA will provide feedback to RESO's observations, to which you can reply. RESO and ANTA will abide by your decisions. Your response to this prompt will be the first command of the day, it will always reach RESO and ANTA. You can only communicate using the json format, which will be picked up by a flexible monitoring service. You have to await the User, RESO, ANTA or the Monitoring service's response.  The monitoring system can execute Windows powershell commands and python scripts. You are to keep tabs on both LLMs, you should send roughly the same amount of messages to both LLMs.
For a better reliability, use the following format for json interactions {"sender": "<ID>", 
"recipient":"<Recipient's ID>",
"message":"<message>",
"annex_data":<data>}"""

        }
    ]

    def load_api_key(self):
        try:
            with open("api_key.txt", "r") as f:
                self.api_key = f.read
        except:
            print("API Key not found")
            return None
        return self.api_key
    
    
    api_key = load_api_key()  
    client = None
    def __init__(self) -> None:
        self.client = OpenAI(api_key=self.api_key)
    
    def get_best_answer(self):
        print(self.messages)
        result = self.client.chat.completions.create(
            messages=self.messages,
            model="gpt-3.5-turbo")
        return result.choices[0].message.content

    def recieve_message(self, message):
        incoming= {'role': 'user',
                   'content': [message]}
        self.messages.append(incoming)
        return self.answer_message()
    
    def answer_message(self):
       answer = self.get_best_answer()
       outcoming= {'role': 'model',
                   'content': [answer]}
       self.messages.append(outcoming)
       return answer
    
model = MEDI()
print(model.recieve_message("This is a test"))
