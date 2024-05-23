# This model implements Gemini, a system that uses a LLM to interact with the user and the knowledge base.
# This wont work as-is, first paste the following command: gcloud auth application-default login
import pathlib
import os
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


class GeminiModel:
    messages = []
    
    model_name = 'models/gemini-pro'
    model = None
    def get_api_key(self):
        try:
            with open("api_key.txt", "r") as f:
                return f.read()
        except:
            print("API Key not found")
            return None
    def __init__(self, initial_prompt=""):
        self.messages.append({'role': 'user',
    'parts':[initial_prompt,
    'For a better reliability, use the following format for json interactions {"sender": "<ID1>, <ID2>",',
    '"recipient":"<Recipient\'s ID>",',
    '"message":"<message>",',
    '"annex_data":<data>,',
    '"windows_ps1":"<Powershell command>",',
    '"python_script":"<Python Script>"}',
    ]})
        self.messages.append(
    {'role': 'model',
     'parts':['Aknowledged.']})
        genai.configure(api_key = self.get_api_key())
        for m in genai.list_models():
          if 'generateContent' in m.supported_generation_methods:
            print(m.name)
        self.model = genai.GenerativeModel(self.model_name)
    
    def get_best_answer(self):
        #print(self.messages)
        result = self.model.generate_content(self.messages)
        return result.text

    def recieve_message(self, message):
        incoming= {'role': 'user',
                   'parts': [message]}
        self.messages.append(incoming)
        return self.answer_message()
    
    def answer_message(self):
        answer = ""
        try:
            answer = self.get_best_answer()
            outcoming= {'role': 'model',
                        'parts': [answer]}
            self.messages.append(outcoming)
        except Exception as e:
            answer = f"PROCESSING SAYS: An error occured, {e}"
            outcoming = {'role': 'model',
                        'parts': [answer]}
            self.messages.append(outcoming)
        return answer
    
