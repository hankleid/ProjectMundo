from translation import Translator
from article import *
import os
import time

doi = "10.1038/s41467-017-00516-5"

# folder_path = filename_from_DOI(doi=doi)
folder_path = "lang/kor"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

data = get_article(doi)
# f = open(f"index.xml", "w")
# f.write(data.prettify())
# f.close()

tl = Translator()
# languages = [l for l in load_langs().keys() if l != "English"]
languages = ["Korean"]

t = time.time()
for lang in languages:
    this_data = get_copy(data)
    
    translate_article(this_data, tl, lang)
    print(f"{lang}: {tl.count_tokens()}")

    add_mathML(this_data)
    change_graphic_dir(this_data)

    # SAVING
    fn = filename_from_DOI(doi=doi)
    f = open(f"{folder_path}/{fn}.xml", "w")
    f.write(this_data.prettify())
    f.close()

    tl.clear_tokens()

t = time.time() - t
print(f"{len(languages)} language(s) took {round(t/60)} minutes.")