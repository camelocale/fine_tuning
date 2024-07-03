import fasttext
model = fasttext.load_model('./lid.176.ftz')
text = """
Por favor
"""

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
    model = fasttext.load_model('./lid.176.ftz')
    detected_lang = model.predict(text.replace("\n", ""))[0][0]
    language = lang_tag(detected_lang)
    return language

print(detect_lang(text))
