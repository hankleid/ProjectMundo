import os
from article import *

def fn():
    all_langs = list(load_langs()["translation"].values())
    langs = [l for l in all_langs if l != "eng"]
    for lang in langs:
        articles = [file for file in os.listdir(f"lang/{lang}") if file[-len(".xml"):] == ".xml"]
        for i in range(len(articles)):
            folder_name = articles[i][:-len(".xml")]
            fd = f"../Files/{folder_name}"

            doi = ""
            with open(f"lang/{lang}/{str(articles[i])}", "r") as f:
                this_data = BeautifulSoup(str(f.read()), features="xml")
                doi = filename_from_DOI(xml=this_data)
                # info["title"] = str_strip(this_data.find("article-title").string)
            if articles[i][:-len(".xml")] == doi:
                # format HAS to be exactly [doi].xml to be displayed on the website.
                # articles[i] = info
                if not os.path.isdir(fd):
                    os.mkdir(fd)
                os.rename(f"../Files/lang/{lang}/{articles[i]}",f"../Files/{folder_name}/{lang}.xml")

if __name__ == "__main__":
    fn()