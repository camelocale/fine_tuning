from vllm import LLM, SamplingParams
import huggingface_hub
from transformers import AutoTokenizer

huggingface_hub.login("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")

system_prompt = "You're a veteran tour guide living in Korea, and you always answer with Korean language"
prompt = "Please recommend 5 tourist attractions in Seoul. make me a course which takes one day."

messages = [
    f"""
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>

    {system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

    {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
]

print(messages)

# terminators = [
#     tokenizer.eos_token_id,
#     tokenizer.convert_tokens_to_ids("<|eot_id|>")
# ]

sampling_params = SamplingParams(max_tokens=1024, early_stopping=False, top_p=0.9, skip_special_tokens=True)  # use_beam_search=False)

llm = LLM(model="meta-llama/Meta-Llama-3-8B-Instruct")

outputs = llm.generate(messages, sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text.strip()
    print("----------Result----------\n")
    print(f"Prompt: {prompt!r} \nGenerated text: {generated_text!r}")