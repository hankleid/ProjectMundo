from translation import Translator
from article import *
import os
import time

# doi = "10.1038/s41467-023-43444-3" # health
# doi = "10.1038/s41467-024-52834-0" # Hsu et al.
# doi = "10.1038/s41467-018-04608-8" # zou
# doi = "10.1038/s41467-023-42766-6" # cats
doi = "10.1038/s41467-017-00516-5" # Ahn et al.
# doi = "10.1038/s41467-019-11343-1" # physics/EE
# doi = "10.1038/s41467-023-40666-3" # human behavior

# doi = "10.1038/s41598-023-44786-0" # Le (vie)
# doi = "10.1038/s41467-022-29976-0" # Scuri (ita)
# doi = "10.1038/s41467-019-14096-z" # Roques-Carmes (fra)
# doi = "10.1038/s41586-024-07386-0" # Choi (kor)
# doi = "10.1038/s41467-021-21624-3" # Gyger (deu)
# doi = "10.1038/s41746-019-0216-8" # Ghorbani (per)

# folder_path = filename_from_DOI(doi=doi)

data = get_article(doi)
# f = open(f"index.xml", "w")
# f.write(data.prettify())
# f.close()

tl = Translator("llama")
tl.use_context = False
languages = [l for l in load_langs()['translation'].keys() if l!="Korean"]#[-6:]
# languages = ["Chinese (simplified characters)","Bengali","Urdu","Marathi","Tamil","Telugu","Gujarati"]#, "Chinese (traditional characters)", "Japanese"]
languages = ["English", "Spanish"]

if tl.use_context:
    fulltext_path = f"FullTexts/{filename_from_DOI(doi=doi)}/eng_full.txt"
    if not os.path.isfile(fulltext_path):
        save_fulltext(get_copy(data), f"FullTexts/{filename_from_DOI(doi=doi)}/eng_full.txt")
    tl.load_article(fulltext_path)
    print(tl.context)

t = time.time()
for lang in languages:
    print(lang)
    this_data = get_copy(data)

    if lang != "English":
        translate_article(this_data, tl, lang, split=4)
        print(f"{lang}: {tl.count_tokens()}")

    add_mathML(this_data)
    change_graphic_dir(this_data)

    # SAVING
    folder_path = f"lang/{load_langs()['translation'][lang]}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    fn = filename_from_DOI(doi=doi)
    # f = open(f"{folder_path}/{fn}_{tl.name}.xml", "w")
    f = open(f"{folder_path}/{fn}_test.xml", "w")
    f.write(this_data.prettify())
    f.close()

    # ADD THIS ARTICLE TO THE CATALOG.

    tl.reset()


t = time.time() - t
print(f"{len(languages)} language(s) took {round(t/60)} minutes.")