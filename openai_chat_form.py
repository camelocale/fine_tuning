import time
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="123"
)


def chat(messages):
    try:
        completion = client.chat.completions.create(
            model="/home/user/.cache/huggingface/hub/models--meta-llama--Meta-Llama-3-8B-Instruct/snapshots/a8977699a3d0820e80129fb3c93c20fbd9972c41",
            # model="/home/user/.cache/huggingface/hub/models--Unbabel--TowerInstruct-7B-v0.2/snapshots/6ea1d9e6cb5e8badde77ef33d61346a31e6ff1d4",
            messages=messages,
            extra_body={
                "stop": ["<|im_end|>"]
            },
            stream=True,
            temperature=0.8,
            max_tokens=2048
        )
        return completion
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

messages=[] #messages list for context

#set system prompt
messages.append({"role": "system", "content": "You are a helpful AI assistant."}) #this is your system prompt customized according to you.
# messages.append({"role": "system", "content": "You are a professional translator from Chinese to Korean."}) #this is your system prompt customized according to you.
# messages.append({"role": "user", "content": "Translate following text from Chinese to Korean."})

i=0
while True: #you can increase the number of question 
    user_message=input("Please enter your "+ str(i+1)+" question: ") #take input user message
    if user_message == "quit":
        break

    # because 'openai.ChatCompletion.create()' function take specific format as list so we can add our user message.
    messages.append({"role": "user", "content": user_message})
    # print(messages)

    response = chat(messages)
    print("Response for "+str(i+1)+" question: ") # just for display on the screen
    collected_messages = ""
    for chunk in response:
        chunk_message = chunk.choices[0].delta.content  # extract the message
        if chunk_message == None:
            continue
        collected_messages += chunk_message
        print(chunk_message, end="", flush=True)
    print("\n")


    #for the context we also need to save openai response in our list so we can add list add openai resposne as well
    messages.append({"role": "assistant", "content": collected_messages})
    i += 1