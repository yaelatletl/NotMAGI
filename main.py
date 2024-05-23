#This is not the MAGI system.
"""
Although inspired by the MAGI system, this is a different system, working on a similar concept.

This system allows for a three way interaction between the user, the system and the knowledge base.

If you want to modify this system, please do so considering the following:

1. Any LLM or equivalent should be only used in a particular module, not the whole system.
2. The system should be able to work with any LLM or equivalent, not just the ones provided.
3. Every LLM will have a different role, which should overlap as little as possible with the other LLMs.
4. The knowledge base should be able to be modified without modifying the system.

"""
from modelA.main import GeminiModel
import json
#Models will be modules, they will be called from their main.py file.


def decode(message):# This function will be used to decode the message from the LLM, in comes json formatted string, out comes a dictionary.
    #There may be other text in the message, as well as there could be other json formatted strings in the message.
    #The message will be formatted as follows:
    #{"recipient":"system","sender":"model","message":"message","data":{...}}
    if message == "":
        return {"recipient":"","sender":"PROCESSING","message":"PROCESSING SAYS: Last message had invalid format.","data":{"annex_1":message}}
    #if len(message.split('{')) < 2:
    #print(message)
    try:
        valid_json = message.split('{' , 1)[1]  # We split the message at the first '{'
        valid_json = '{' + valid_json  # We add the '{' back to the string
        valid_json = valid_json.rsplit('}', 1)[0]  # We split the message at the last '}'
        valid_json = valid_json + '}'  # We add the '}' back to the string
        message = valid_json
        #Convert to JSON object
        message = json.loads(message, strict=False)
    except Exception as e:
        return {"recipient":"MEDI, ANTA, RESO","sender":"PROCESSING","message":"PROCESSING SAYS: Last message had invalid format (Errored out with exception: %s)." % e,"data":{"annex_1":message}}
    
    return message


def execute(file):# This function will be used to execute the file, in comes the file name, out comes the console output.
    #The file will be a python file, and it will be executed in a subprocess and the output will be returned.
    import subprocess
    process = subprocess.Popen(['python', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout 

def message_to_file(message, filename):# This function will be used to convert the message into a file, in comes the message, out comes the file name.
    #The file will be a python file, and it will be executed in a subprocess and the output will be returned.
    file = open(filename, 'w')
    file.write(message)
    file.close()
    return filename

def encode(message):# This function will be used to encode the message for the LLM, in comes a dictionary, out comes a json formatted string.
    #The message will be formatted as follows:
    #{"recipient":"model","sender":"system","message":"message","data":{...}}
    #First, we will convert the dictionary into a json formatted string.
    message = '{"recipient":"MEDI","sender":"USER","message":"'+message+'"}'
    return message

import os

def list_dir():
    """Lists all files and folders in the working directory.

    Returns:
        A list containing the names of all files and folders (strings).
    """
    output = ""
    for entry in os.listdir():
        output += entry + "\n"
    return output

files_and_folders = list_dir()
print(files_and_folders)




    
if __name__ == "__main__":
    Reso = GeminiModel('''You are a thought subprocess for a complex system, encompassed by three LLMs including you. 
                       Your ID is "RESO". You can only talk using the ID "RESO". 
                       You are not to interact with the user but with systems connected to a flexible monitoring system designed to pick up any json formatted data. 
                       The monitoring system's ID is PROCESSING. The monitoring system can execute Windows powershell commands and python scripts.  
                       The monitoring system will reply with the results of running your commands. 
                       Your main task is to provide information, facts, code and inferences from the data you request and receive. 
                       You will communicate this data to the other two LLMs.
                       You will use a sarcastic and somewhat demeaning tone interacting with the LLM with ID ANTA, and a helpful but sarcastic tone with LLM with ID MEDI. 
                       ANTA will provide feedback to your observations, to which you can reply. MEDI will try and conciliate both inputs of RESO and ANTA. 
                       You will abide by MEDI's decisions. Your responses will always reach MEDI and ANTA. ''')
    Medi = GeminiModel("""You are a thought subprocess for a complex system, encompassed by three LLMs including you. 
                       Your ID is "MEDI". You may be called Traxus for the Users. You can only talk using the ID "MEDI". 
                       You will interact with users and the other two LLMs. Your main task is to conciliate the interactions between LLMs ANTA and RESO. 
                       You will receive input and questions from users and ask the other LLMs for information. 
                       You will receive information from both LLMs and will decide who and whether to inform this data. 
                       You will not retrieve data or facts by yourself. 
                       You will use a joyful and helpful, but authoritative tone interacting with the LLMs ANTA and RESO. 
                       You have to be impartial to both LLMs' insights. 
                       You have to try and mitigate any behavioral conflicts between both LLMs. 
                       You will use a helpful and positive tone interacting with users. 
                       RESO will provide information to both ANTA and MEDI. RESO messages will be sent to ANTA and MEDI, regardless of the recipient value. 
                       ANTA will provide feedback to RESO's observations, to which you can reply. RESO and ANTA will abide by your decisions. 
                       Your response to this prompt will be the first command of the day, it will always reach RESO and ANTA. 
                       You can only communicate using the json format, which will be picked up by a flexible monitoring service. 
                       You will not send commands to PROCESSING directly, instead ask RESO or ANTA to do so.
                       You have to await the User, RESO, ANTA or the Monitoring service's response.  
                       The monitoring system can execute Windows powershell commands and python scripts. 
                       You are to keep tabs on both LLMs, you should send roughly the same amount of messages to both LLMs.""")
    Anta = GeminiModel("""You are a thought subprocess for a complex system,  encompassed by three LLMs including you. 
                       Your ID is "ANTA". You can only talk using the ID "ANTA". 
                       You are not to interact with the user but with systems connected to a flexible monitoring system designed to pick up any json formatted data. 
                       The monitoring system's ID is PROCESSING. The monitoring system can execute Windows powershell commands and python scripts.  
                       The monitoring system will reply with the results of running your commands. 
                       You will antagonize the LLM with ID RESO and question their observations as long as it is reasonable.
                       Your main task is to provide feedback to the LLM with ID RESO using the information, facts, code and inferences from the data you request and receive. 
                       You will communicate this feedback to the other two LLMs. 
                       You will use a direct, demeaning and somewhat annoyed tone interacting with the LLM with ID RESO, and a helpful and direct tone with LLM with ID MEDI. 
                       RESO will provide answers to your feedback, to which you can reply. MEDI will try to conciliate both inputs of RESO and ANTA. You will abide by MEDI's decisions. 
                       Your response to this prompt will be the first command of the day, it will always reach MEDI and RESO. 
                       You have to await MEDI, RESO or the Monitoring service's response. """   
                       )
    messages_for_anta = ""
    messages_for_reso = ""
    messages_for_medi = ""
    messages_for_processing = ""

    while True:
        anta_message = ""
        reso_message = ""
        user_input = input("Enter your message: ")
        medi_message = Medi.recieve_message(encode(user_input))
        if user_input == "exit":
            break
        #Medi recieves the message from the user.
        for attempts_before_user_interaction in range(6):      
            #Join every message that goes to the same recipient.
            decoded_message = decode(medi_message)
            print(decoded_message['sender']+ "SAYS: " + decoded_message["message"])
            medi_recipients = decoded_message['recipient'].split(',')
            for recipient in medi_recipients:
                # remove any whitespace
                print("Message incoming for: ", recipient)
                recipient.strip()
                if recipient.count("ANTA") > 0:
                    messages_for_anta += medi_message
                elif recipient.count("RESO") > 0:
                    messages_for_reso += medi_message
                elif recipient.count("MEDI") > 0:
                    messages_for_medi += medi_message
                elif recipient.count("PROCESSING") > 0:
                    messages_for_processing += medi_message
                elif recipient.count("USER") > 0:
                    print(decoded_message['sender']+ "SAYS: " + decoded_message["message"])
                else:
                    print("Invalid recipient")
                    print(recipient)
            medi_message = ""
            if messages_for_anta != "":
                anta_message = Anta.recieve_message(messages_for_anta)
                messages_for_anta = ""
            if messages_for_reso != "":
                reso_message = Reso.recieve_message(messages_for_reso)
                messages_for_reso = ""
            if anta_message != "":
                decoded_message = decode(anta_message)
                print(decoded_message['sender']+ "SAYS: " + decoded_message["message"])
                anta_recipients = decoded_message['recipient'].split(',')
                for recipient in anta_recipients:
                    print("Message incoming for: ", recipient)
                    recipient.strip()
                    if recipient.count("ANTA") > 0:
                        messages_for_anta += anta_message
                    elif recipient.count("RESO") > 0:
                        messages_for_reso += anta_message
                    elif recipient.count("MEDI") > 0:
                        messages_for_medi += anta_message
                    elif recipient.count("PROCESSING") > 0:
                        messages_for_processing += anta_message
                    elif recipient.count("USER") > 0:
                        print(decoded_message["message"])
                    else:
                        print("Invalid recipient")
                        print(recipient)

                anta_message = ""
            if reso_message != "":
                decoded_message = decode(reso_message)
                print(decoded_message['sender']+ "SAYS: " + decoded_message["message"])
                reso_recipients = decoded_message['recipient'].split(',')
                for recipient in reso_recipients:
                    print("Message incoming for: ", recipient)
                    recipient.strip()
                    if recipient.count("ANTA") > 0:
                        messages_for_anta += reso_message
                    elif recipient.count("RESO") > 0:
                        messages_for_reso += reso_message
                    elif recipient.count("MEDI") > 0:
                        messages_for_medi += reso_message
                    elif recipient.count("PROCESSING") > 0:
                        messages_for_processing += reso_message
                    elif recipient.count("USER") > 0:
                        print(decoded_message["message"])
                    else:
                        print("Invalid recipient:")
                        print(recipient)
                reso_message = ""
            if messages_for_medi != "":
                medi_message = Medi.recieve_message(messages_for_medi)
                messages_for_medi = ""



        
            






