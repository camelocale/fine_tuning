from nltk import sent_tokenize
import fasttext
import re

model = fasttext.load_model('./lid.176.ftz')

def lang_tag(lang):
    if lang == "__label__zh":
        return "Chinese"
    elif lang == "__label__ru":
        return "Russian"
    elif lang == "__label__ko":
        return "Korean"
    elif lang == "__label__es":
        return "Spanish"
    elif lang == "__label__fr":
        return "French"
    elif lang == "__label__de":
        return "German"
    elif lang == "__label__it":
        return "Italian"
    elif lang == "__label__nl":
        return "Dutch"
    elif lang == "__label__pt":
        return "Portuguese"
    else:
        return "English"

def detect_lang(text):
    detected_lang = model.predict(text.replace("\n", ""))[0][0]
    language = lang_tag(detected_lang)
    return language

def preprocess_text(prompt):
    if detect_lang(prompt) == "Chinese":
        prompt = re.sub("[\s]", "", prompt)
        prompt = prompt.replace("，", ", ")
        prompt = prompt.replace("、", ", ")
        prompt = prompt.replace("？", "?")
        prompt = prompt.replace("！", "!")
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
    else: 
        return prompt

def sent_split(prompt):
    split_list = []
    buf = ""
    len_buf = 0

    preprocess_prompt = preprocess_text(prompt)
    tokenized_text = sent_tokenize(preprocess_prompt)

    for i, e in enumerate(tokenized_text):
        if len(e) >= 128:
            if buf != "" and len(split_list) != 0:
                prev_text = split_list.pop(-1)
                if len(prev_text) < len(e):
                    prev_added = prev_text + buf
                    split_list.append(prev_added)
                else:
                    present_added = buf + e
                    split_list.append(present_added)
            else: 
                if buf != "":
                    split_list.append(buf + e)
                else:
                    split_list.append(e)
        else:
            buf += e
            len_buf += len(e)

            if len_buf < 128:
                pass
            else:
                split_list.append(buf)
                buf = ""
                len_buf = 0

    return tokenized_text, split_list

def make_prompt_list(split_list):
    prompt_list = []
    for i in range(len(split_list)):
        system_message = "You are a helpful AI assistant."
        prompt_list.append(f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{split_list[i]}<|im_end|>\n<|im_start|>assistant\n")

    return prompt_list




tokenized_list, split_list = sent_split("""
位于广东省广

州市番禺区的广汽埃      
安新能源汽车    股份有限公司，有着占地面积8.76万平方米的总装车间。几乎每天，总装车间高级经理张自初都要把车间走一遍。
2023年4月12日，习近平总书记 来到广汽埃安新能源汽车股份有限公司考察，走进企业展厅、总装车间、电池生产车间等，了解企业突破关键核心技术和推动制造业高端化、智能化、绿色化等进展情况。
“总书记强调，‘要重视实体经济，走自力更生之路。’这让我们深受鼓舞。”张自初说，“我们奋力自主创新，生产线已由过去每60秒下线一台新能源汽车，缩短到现在的53秒。”
减少的这7秒，关联着上百台设备的节拍优化。“460名工人、220个工位，工作内容都进行了调整。”正说着，张自初在底盘线驻足。在底盘阻碍课题管理看板前，七八名工程师正围在一起讨论。看板上陈列着问题点，标注了原因、对策、效果。去年5月至今，这块看板见证了2000多条问题及改进意见的来来往往。
在电池车间，工程师陈泽峰刚在看板记录下涂胶设备的最新数据，又要赶往研发中心研究新课题。
去年6月，车间引入全自动化涂胶设备，但试制初期，却面临涂胶覆盖率不达标、单台涂胶胶重逼近标准上限等难题。成立跨部门攻关小组、各类问题日清日结……经过3个月的努力，涂胶覆盖率从75%增至98%，胶重由每台8.8公斤降至7.7公斤，单台成本节约44元。
车间内，是热火朝天的繁忙景象；车间外，是自主可控的产业链布局。半年来，旗下因湃电池工厂、锐湃电驱工厂先后竣工投产，广汽埃安在新能源“三电”领域实现全面自研自产。
在因湃电池智能生态工厂，近800台设备100%国产化，满产后每天能产出3.2万个电芯。“动力电池是新能源汽车的‘心脏’。”处于量产爬坡的关键时期，电芯工艺高级经理杨贤明带领着60人的工艺设备开发团队，连走路都加快了脚步。
“固态电池是新一代动力电池发展的重要方向。”广汽埃安研发中心，电池研发部革新体系平台高级经理史刘嵘刚刚分析完测试数据，“通过构建全固态电池电化学仿真模型，我们有效提升了研发效率，目前已完成兼具高能量密度和高安全性的全固态电池体系开发。”
""")


prompt_list = make_prompt_list(split_list)
print(prompt_list)

# len_split, split = sent_split("""
# Практический на каждой сессии форума спикеры с нескрываемой гордостью говорили о том, что, по данным Всемирного банка (который невозможно заподозрить в симпатиях к нашей стране), экономика России стала четвертой в мире по паритету покупательной способности. Первые три места занимают Китай, США и Индия
#  «Мы обогнали Японию», — констатировали чиновники и бизнесмены. Но то, что скрывается за этим позитивным антуражем, совсем не радует.
# «Россия стала 4-й экономикой мира по паритету покупательской способности? Мы три года уже четвертые, как следует из обновленных данных Всемирного банка. А почему этого никто не заметил? Потому что это не влияет ни на что. Это не имеет отношения к качеству жизни и экономики. Надо говорить об уровне благосостояния людей», — высказался глава комитета Госдумы по бюджету и налогам Андрей Макаров на деловом завтраке в рамках ПМЭФ.
# И действительно, если верить статистике, то Россия сегодня на пределе экономического роста. «Никогда в стране не было такой низкой безработицы (2,6%) и такой загрузки мощностей (81%)», — рассказал глава крупнейшего госбанка Герман Греф. «Эти факторы говорят о том, что мы находимся на пределе экономического роста», — подчеркнул он.
# Эксперты были солидарны в том, что бюджетные траты растут, а это приводит к тому, что предприятия повышают заработные платы. Происходит это очень быстрыми темпами. Люди становятся более состоятельными и идут в банки, получают кредиты, чтобы еще улучшить свою жизнь, даже по более высоким ставкам. В итоге экономика растет очень хорошими темпами, 5,4%. Звучит прекрасно, но такая модель развития экономики очень уязвима. По словам того же Грефа, она примитивна. «Товаров не становится больше. Больше производить не начинают. Цены растут. Производительность труда падает. Импорт ограничен», — продолжит он. Но спасение вроде как найдено.
# """)



# print(len_split)
# for i in range(len_split):
#     print(split[i])
#     print()

# print(len("Практический на каждой сессии форума спикеры с нескрываемой гордостью говорили о том, что, по данным Всемирного банка (который невозможно заподозрить в симпатиях к нашей стране), экономика России стала четвертой в мире по паритету покупательной способности"))