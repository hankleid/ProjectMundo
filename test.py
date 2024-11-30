from article import *
from translation import Translator

# doi = filename_from_DOI(doi="10.1038/s41467-017-00516-5") # ahn
# doi = filename_from_DOI(doi="10.1038/s41467-019-11343-1") # Jelena
# doi = filename_from_DOI(doi="10X1038_s41467-023-42766-6") # cats
# doi = filename_from_DOI(doi="10.1038/s41467-023-43444-3") # health
# doi = filename_from_DOI(doi="10.1038/s41467-018-04608-8") # zou
doi = filename_from_DOI(doi="10.1038/s41467-023-40666-3") # human behavior

lang = "zh1"
langs = [l for l in load_langs()['translation'].values()]#[-6:]
# langs = ["eng"]
xml = None
for l in langs:
    with open(f'lang/{l}/{doi}.xml', 'r') as f:
        xml = "".join(f.readlines())
        xml = BeautifulSoup(xml, features="xml")
        # xml = xml.find(xml.name)

    fd = f"FullTexts/{doi}/{l}_full.txt"
    print(fd)
    save_fulltext(xml, fd)


# tl = Translator("gpt")
# tl.upload_images(doi=doi)

# ret = tl.chat_prompt_with_figures("Please describe these images.")
# print(ret)