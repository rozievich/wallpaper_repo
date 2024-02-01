import translate

async def translate_txt(msg: str):
    translation = translate.Translator(from_lang='uz', to_lang='en')
    data = translation.translate(msg)
    return data
