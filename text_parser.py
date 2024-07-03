from nltk import sent_tokenize



def para_tokenize(prompt): 
    tokenized_para = []
    split= prompt.split("\n")
    buf = ""
    first = True
    print(split)
    for i in range(len(split)):
        split_text = split[i].strip()
        if first and split_text=="" and tokenized_para!=0:
            if len(buf) < 64:
                if buf != "":
                    if buf[-1] in [".", ",", "!", "?"]:
                        pass
                    else:
                        buf += "."
                else: pass
            else:
                tokenized_para.append(buf.strip())
                buf = ""
            first = False
        elif split_text!="":
            if buf != "":
                if buf[-1] in [".", ",", "!", "?"]:
                    buf += split_text
                else:
                    buf += "." + split_text
            else:
                buf = split_text
            first = True
    if buf != "":
        tokenized_para.append(buf)

    return tokenized_para

def preprocess_text(prompt):
    prompt = prompt.replace("，", ", ")
    prompt = prompt.replace("、", ", ")
    prompt = prompt.replace("？", "?")
    prompt = prompt.replace("！", "!")
    prompt = prompt.replace("：", ":")
    prompt = prompt.replace("“", ' "')
    prompt = prompt.replace("”", '" ')
    prompt = prompt.replace("‘", "'")
    prompt = prompt.replace("’", "'")
    prompt = prompt.replace('。"', '。" ')
    prompt = prompt.replace("。'", "。' ")
    prompt = prompt.replace("。", ". ")
    prompt = prompt.replace('. "', '."')
    prompt = prompt.replace(". '", ".'")
    return prompt


def sentence_split(prompt):
        split_list = []
        buf = ""
        len_buf = 0
        preprocess_prompt = preprocess_text(prompt)
        tokenized_para = para_tokenize(preprocess_prompt)
        print(tokenized_para)

        for j in range(len(tokenized_para)):
            tokenized_sent = sent_tokenize(tokenized_para[j])
            for i, e in enumerate(tokenized_sent):
                if len(e) >= 128:
                    if buf != "" and len(split_list) != 0:
                        prev_text = split_list.pop(-1)
                        if len(prev_text) < len(e):
                            prev_added = prev_text + " " + buf
                            split_list.append(prev_added)
                            buf = ""
                            len_buf = 0
                        else:
                            present_added = buf + " " + e
                            split_list.append(present_added)
                            buf = ""
                            len_buf = 0
                    else: 
                        if buf != "":
                            split_list.append(buf + " " + e)
                            buf = ""
                            len_buf = 0
                        else:
                            split_list.append(e)
                            buf = ""
                            len_buf = 0
                else:
                    if buf == "":
                        buf = e
                        len_buf = len(e)
                    else:
                        buf += " " + e
                        len_buf += len(e)

                    if len_buf < 128:
                        if i == len(tokenized_sent)-1:
                            split_list.append(buf)
                            buf = ""
                            len_buf = 0
                        else:
                            pass
                    else:
                        split_list.append(buf)
                        buf = ""
                        len_buf = 0
        return split_list



text = """
Уважаемый менеджер Лю,

Здравствуйте!

Меня зовут Ван Цян, я менеджер по закупкам компании XYZ Computers. Большое спасибо за то, что нашли время прочитать это письмо.

В связи с реализацией нашего нового поколения компьютерной продукции, нам необходимо закупить партию высококачественных комплектующих для удовлетворения потребностей производства. По результатам детального анализа рынка, мы пришли к выводу, что комплектующие, производимые вашей компанией, соответствуют нашим требованиям по качеству и характеристикам. Поэтому мы хотели бы установить с вами сотрудничество и закупить партию комплектующих.

Конкретные потребности следующие:

Наименование комплектующей: Процессор Intel i7

Модель: i7-10700K
Количество: 5000 шт.
Наименование комплектующей: Оперативная память DDR4 16GB

Модель: DDR4-3200
Количество: 5000 шт.
Наименование комплектующей: SSD 1TB

Модель: SATA III
Количество: 3000 шт.
Наименование комплектующей: Видеокарта RTX 3070

Количество: 3000 шт.
Для обеспечения бесперебойного хода производственного плана, мы надеемся как можно скорее организовать поставку после получения вашего подтверждения. Пожалуйста, ответьте на следующие вопросы:

Котировка цен: Пожалуйста, предоставьте цену за единицу и общую стоимость указанных комплектующих.
Срок поставки: Укажите, пожалуйста, предполагаемое время поставки и сроки выполнения заказа.
Условия оплаты: Опишите, пожалуйста, условия и способы оплаты, которые предлагает ваша компания.
Другие условия: Если есть другие важные условия или вопросы, пожалуйста, сообщите нам.
Кроме того, если у вас есть какие-либо вопросы по нашим требованиям или вам нужны дополнительные технические спецификации, пожалуйста, не стесняйтесь обращаться ко мне. Мы с нетерпением ждем возможности установить долгосрочные и стабильные партнерские отношения с вашей компанией.

Благодарим вас за внимание и поддержку, ждем вашего ответа!

С уважением,

Ван Цян
Менеджер по закупкам компании XYZ Computers
Электронная почта: wang.qiang@xyzcomputers.com
Телефон: +86 123 4567 8900
"""

p = sentence_split(text)

print(len(p), p)