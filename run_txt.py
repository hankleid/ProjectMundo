from translation import *
from article import load_text, save_text, filename_from_DOI, load_langs
import time

def chunkify(txt):
    # splits the full text article into chunks to translate.
    chunks = []
    i = 0
    stopper = '\n\n'
    while i != -1 and i < len(txt):
        j = txt[i:].find(stopper)+i
        chunks.append(txt[i:j])
        i = j+len(stopper)
    return chunks

def translate(tl, txts, lang):
    # translates each txt in txts into lang.
    # returns the translated list of txts.

    if isinstance(tl, GoogleTranslator):
        _, res = tl.translate(txts, lang)
    elif isinstance(tl, Translator): # LLM
        res = tl.translate_text(txts, lang)
    else:
        return None
    return res

def save_chunks(txts, savepath):
    # writes each txt in txtx to savepath.
    # puts \n\n between each chunk.
    save_text(savepath, '') # new file
    with open(savepath, 'a') as f:
        for txt in txts:
            f.write(txt+'\n\n')

if __name__ == "__main__":
    article10 = "10.1038/s41598-023-51013-3" # sci rep 2 **
    article11 = "10.1038/s41598-023-43026-9" # biochem, endochrinology, neuroscience **
    article12 = "10.1038/s41598-023-45072-9" # covid **
    article13 = "10.1038/s41467-023-43949-x" # quantum optics **
    article14 = "10.1038/s41467-023-43067-8" # drug delivery **
    article15 = "10.1038/s41467-023-43963-z" # materials science **

    articles = [filename_from_DOI(doi=d) for d in [article10,article11,article12,article13,article14,article15]]
    
    langs_dict = load_langs()['translation']
    langs = [l for l in langs_dict.keys()][1:]
    # langs = ["Chinese (simplified characters)"]

    for a in articles[-2:]:
        fd = f"FullTexts/{a}"
        loadpath = f"{fd}/eng_full.txt"

        chunks = chunkify(load_text(loadpath))

        tl = Translator("gpt")
        print(a)
        for lang in langs:
            try:
                new_chunks = translate(tl, chunks, lang)
                save_chunks(new_chunks, savepath=f"{fd}/{langs_dict[lang]}_gpt.txt")
            except Exception as e:
                print(a, lang)
                print(e)

            # time.sleep(1)
        


    # inputs, res = tl.translate(["hello!","goodbye!"],"Korean")
    # print(res)