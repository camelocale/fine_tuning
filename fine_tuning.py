import pandas as pd
import numpy as np
import torch
import json
import wandb
import transformers
import bitsandbytes as bnb
from datasets import Dataset
from transformers import AdamW, AutoTokenizer, PreTrainedTokenizerFast, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from tqdm import tqdm
import os

# CUDA 오류 디버깅 설정
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

# 토크나이저 설정
tokenizer = tokenizer = AutoTokenizer.from_pretrained(model_id, eos_token='</s>', pad_token='</s>')

# 엑셀 파일 로드
file_path = "./data/formatted_dataset.xlsx"
df = pd.read_excel(file_path)

# 템플릿을 적용하여 Question과 Answer를 결합
def apply_template(row):
    return json.dumps([
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": row['Question']},
        {"role": "assistant", "content": row['Answer']}
    ])

df['text'] = df.apply(apply_template, axis=1)

# 데이터셋을 Hugging Face Dataset 형식으로 변환
dataset = Dataset.from_pandas(df)

# 토크나이제이션 함수 정의
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

# 데이터셋에 토크나이제이션 적용
tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset.column_names)

print(tokenized_dataset[0])

# BitsAndBytesConfig 설정
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

# 모델 로드
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)
model.gradient_checkpointing_enable()
model = prepare_model_for_kbit_training(model)

def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )

# QLoRA 구성
lora_config = LoraConfig(
    r=4,
    lora_alpha=16,
    target_modules=["q_proj", "up_proj", "o_proj", "k_proj", "down_proj", "gate_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

# 모델 로드 및 준비
model = get_peft_model(model, lora_config)
print_trainable_parameters(model)

# 훈련 인자 설정
training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=1,
    learning_rate=1e-4,
    fp16=True,
    logging_steps=10,
    output_dir="results",
    optim="paged_adamw_8bit",
)

# Trainer 설정
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

# 모델 학습
model.config.use_cache = False
trainer.train()

# 모델 저장
model.save_pretrained("./llama-3-8b-finetuned")
tokenizer.save_pretrained("./llama-3-8b-finetuned")
