import time
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="123"
)


def chat(messages):
    try:
        completion = client.completions.create(
            model="/home/user/.cache/huggingface/hub/models--meta-llama--Meta-Llama-3-8B-Instruct/snapshots/a8977699a3d0820e80129fb3c93c20fbd9972c41",
            # model="/home/user/.cache/huggingface/hub/models--Unbabel--TowerInstruct-7B-v0.2/snapshots/6ea1d9e6cb5e8badde77ef33d61346a31e6ff1d4",
            prompt=messages,
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

# messages=[] #messages list for context

# #set system prompt
# # messages.append({"role": "system", "content": "You are a helpful AI assistant."}) #this is your system prompt customized according to you.
# messages.append({"role": "system", "content": "You are a professional translator from Chinese to Korean."}) #this is your system prompt customized according to you.
# messages.append({"role": "user", "content": "Translate following text from Chinese to Korean."})


# user_message=input("Please enter text: ") #take input user message
# messages.append({"role": "user", "content": user_message})
# text = """
# 统筹推进信用基础设施建设方面，行动计划明确，优化信用信息平台功能；加快地方融资信用服务平台整合；加强对违法违规收集、篡改及泄露公共信用信息行为的监控，加强个人隐私、商业秘密的保护。
# """

# messages = f'Translate the following text from Chinese to Korean: "{text}"'
# response = chat(messages)

system_message = "You are a helpful AI assistant."
user_message = input("Please enter your question: ")

messages= f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant\n" #messages list for context
response = chat(messages)

for chunk in response:
    chunk_message = chunk.choices[0].text  # extract the message
    if chunk_message == None:
        continue
    print(chunk_message, end="", flush=True)
print("\n")
