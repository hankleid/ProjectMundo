from translation import Translator
from article import *
import os
import time

# doi = "10.1038/s41467-023-43444-3" # health
# doi = "10.1038/s41467-024-52834-0" # Hsu et al.
# doi = "10.1038/s41467-018-04608-8" # zou
# doi = "10.1038/s41467-023-42766-6" # cats
doi = "10.1038/s41467-017-00516-5" # Ahn et al.
# doi = "10.1038/s41467-019-11343-1" # Jelena

# folder_path = filename_from_DOI(doi=doi)

data = get_article(doi)
# f = open(f"index.xml", "w")
# f.write(data.prettify())
# f.close()

tl = Translator("gpt")
tl.use_context = False
languages = [l for l in load_langs()['translation'].keys() if l != "Korean"]
# languages = ["Chinese (simplified characters)","Bengali","Urdu","Marathi","Tamil","Telugu","Gujarati"]#, "Chinese (traditional characters)", "Japanese"]
# languages = ["Korean"]

if tl.use_context:
    fulltext_path = f"FullTexts/{filename_from_DOI(doi=doi)}/eng.txt"
    if not os.path.isfile(fulltext_path):
        save_fulltext(get_copy(data), f"FullTexts/{filename_from_DOI(doi=doi)}/eng.txt")
    tl.load_article(fulltext_path)
    print(tl.context)

t = time.time()
for lang in languages:
    print(lang)
    this_data = get_copy(data)

    if lang != "English":
        translate_article(this_data, tl, lang, split=6)
        print(f"{lang}: {tl.count_tokens()}")

    add_mathML(this_data)
    change_graphic_dir(this_data)

    # SAVING
    folder_path = f"lang/{load_langs()['translation'][lang]}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    fn = filename_from_DOI(doi=doi)
    # f = open(f"{folder_path}/{fn}_{tl.name}.xml", "w")
    f = open(f"{folder_path}/{fn}_nocontext.xml", "w")
    f.write(this_data.prettify())
    f.close()

    tl.reset()


t = time.time() - t
print(f"{len(languages)} language(s) took {round(t/60)} minutes.")