import requests
import json


vllm_host = "http://localhost:8000"
url = f"{vllm_host}/generate"



def chat(messages):
    # headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": messages,
        "max_tokens": 2048,
        "stream": True,
        "temperature": 0.7,
        "stop": '<|im_end|>'
    }

    r = requests.post(url, json=data, stream=True)
    
    return r



# set system prompt
# messages.append({"role": "system", "content": "You are a helpful AI assistant."}) #this is your system prompt customized according to you.
# messages.append({"role": "system", "content": "You are a professional translator from Chinese to Korean."}) #this is your system prompt customized according to you.
# messages.append({"role": "user", "content": "Translate following text from Chinese to Korean."})


# user_message=input("Please enter text: ") #take input user message
# messages.append({"role": "user", "content": user_message})

system_message = "You are a helpful AI assistant."
user_message = input("Please enter your question: ")

messages= f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant\n" #messages list for context
# messages.append({"role": "system", "content": "You are a helpful AI assistant."})
# messages.append({"role": "user", "content": user_message})

response = chat(messages)
text_len = 0
for line in response.iter_content(chunk_size=2048):
    text = json.loads(str(line, encoding='utf-8'))['text'][0]
    print(text[text_len:], end="", flush=True)
    text_len = len(text)

print("\n")
# for chunk in response:
#     text = chunk.decode(encoding='utf-8')
#     print(text, end="", flush=True)
# print("\n")



i=0
while True: #you can increase the number of question 
    user_message=input("Please enter your "+ str(i+1)+" question: ") #take input user message
    if user_message == "quit":
        break

    # because 'openai.ChatCompletion.create()' function take specific format as list so we can add our user message.
    messages += f"<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant\n"
    # print(messages)

    response = chat(messages)
    print("Response for "+str(i+1)+" question: ") # just for display on the screen
    text_len = 0
    for line in response.iter_content(chunk_size=2048):
        text = json.loads(str(line, encoding='utf-8'))['text'][0]
        print(text[text_len:], end="", flush=True)
        text_len = len(text)

    print("\n")

    #for the context we also need to save openai response in our list so we can add list add openai resposne as well
    messages += f"{text}<|im_end|>\n"
    i += 1
