from transformers import M2M100Config, M2M100ForConditionalGeneration, M2M100Tokenizer

model = M2M100ForConditionalGeneration.from_pretrained("facebook/nllb-200-distilled-1.3B")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/nllb-200-distilled-1.3B", src_lang="zh", tgt_lang="ko")

src_text = "澳大利亚国防部称，5月4日一架澳海军直升机在黄海国际水域执行任务时遭中国军机拦截。张晓刚表示，澳方所言颠倒黑白，倒打一耙，中方对此坚决反对。"
tgt_text = "La vie est comme une boîte de chocolat."

model_inputs = tokenizer(src_text, text_target=tgt_text, return_tensors="pt")

loss = model(**model_inputs).loss  # forward pass


# translate Arabic to English
tokenizer.src_lang = "zh-CN"
encoded_ar = tokenizer(article_zh, return_tensors="pt")
generated_tokens = model.generate(
    **encoded_ar,
    forced_bos_token_id=tokenizer.lang_code_to_id["kor_Hang"]
)
tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)