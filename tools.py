from article import *
import os
import json


def update_langs_dict():
    #
    # RE-RUN WHENEVER NEW LANGUAGES OR ARTICLES ARE ADDED. (first add the new language to the dict)
    #
    lang_dict = load_langs()
    codes = [l for l in lang_dict["translation"].values()]

    updated = {}
    for lang in codes:
        print(lang)
        # get all available article titles and dois
        articles = [file for file in os.listdir(f"lang/{lang}") if ".xml" in file]
        for i in range(len(articles)):
            info = {}
            with open(f"lang/{lang}/{str(articles[i])}", "r") as f:
                this_data = BeautifulSoup(str(f.read()), features="xml")
                info["doi"] = filename_from_DOI(xml=this_data)
                info["title"] = str_strip(this_data.find("article-title").string)
            articles[i] = info

        updated[lang] = {
            "name": lang_dict["codes"][lang]["name"],
            "articles": articles
        }

    lang_dict["codes"] = updated

    with open("lang.json", "w+") as f:
        json.dump(lang_dict, f, ensure_ascii=False, indent=2)


def update_dropdown_langs():
    #
    # POPULATE DROPDOWN LIST W/ ALL AVAILABLE LANGS
    # (links are blank -- they get populated by js/webscript.js)
    #
    html = BeautifulSoup(str(open("style/navigation.html").read()), features="html.parser")
    dropdown = html.find("div", {"id": "lang-dropdown"})
    dropdown.clear()
    
    lang_dict = load_langs()
    codes = [l for l in lang_dict["codes"].keys()]
    for code in codes:
        dropdown.append(BeautifulSoup(f"<a href='' id='{code}'>{lang_dict['codes'][code]['name']}</a>", features="html.parser"))
    
    with open("style/navigation.html", "w+") as f:
        f.write(html.prettify())

def update_index_files():
    #
    # CREATES NEW INDEX FILE FOR EACH LANGUAGE W/ TRANSLATED TITLES.
    # (currently uses the Korean index as the model)
    #
    html = BeautifulSoup(str(open("lang/kor/index.html").read()), features="html.parser")
    articles = html.find("div", {"class": "articles-index"})
    scripts = [s for s in html.find_all("script")]

    lang_dict = load_langs()
    codes = [l for l in lang_dict["codes"].keys()]
    for code in codes:
        # Add links to all available articles.
        articles.clear()
        for a in lang_dict["codes"][code]["articles"]:
            articles.append(BeautifulSoup(f"<a href='{a['doi']}.xml'>{a['title']}</a>", features="html.parser"))
        
        # Change the on-load script.
        script = scripts[-1]
        script.clear()
        script.append(BeautifulSoup("setTimeout(function() {configureDropdown('index', '"+code+"');}, 100);", features="html.parser"))

        with open(f"lang/{code}/index.html", "w+") as f:
            f.write(html.prettify())

update_langs_dict()
update_dropdown_langs()
update_index_files()



    # path = f"lang/{lang}/{filename_from_DOI(doi=doi)}.xml"
    # this_data = None
    # with open(path, "r") as f:
    #     this_data = BeautifulSoup(str(f.read()), features="xml")

    # title = this_data.find("article-title").string
    # print(title)

    # # add_mathML(this_data)
    # change_graphic_dir(this_data)

    # # SAVING
    # fn = filename_from_DOI(doi=doi)
    # f = open(path, "w+")
    # f.write(this_data.prettify())
    # f.close()
