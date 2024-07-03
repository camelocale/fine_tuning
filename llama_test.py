import requests

def chat(messages):
    vllm_host = "http://localhost:8000"
    url = f"{vllm_host}/generate"
    # headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": "<|im_start|>system\nYou a helpful assistant.<|im_end|>\n<|im_start|>user\n"+messages+"<|im_end|>\n<|im_start|>assistant\n",
        # "temperature": question.temperature,
        # "top_p": question.top_p,
        # "top_k": question.top_k,
        "max_tokens": 2048,
        "stop": '<|im_end|>',
        # "stream": True,
    }
    r = requests.post(url, json=data)
    return r

prompt = "Who are you?"
response = chat(prompt)

print(response.text)