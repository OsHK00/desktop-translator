from googletrans import Translator
translator = Translator()



async def translate(text_ : str, to_ : str, from_ : str):
    try:
        if to_ == None:
            traducion = await translator.translate(text_,dest=to_)
        else:
            traducion = await translator.translate(text_,src=from_, dest=to_)
        return traducion.text
    except Exception as e:
        return("error traduciendo: ", e)
    

