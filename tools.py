from article import *
import os
import json



def update_catalog(dois):
    #
    # RE-RUN WHENEVER NEW ARTICLES ARE ADDED.
    #
    articles_dict = load_articles()
    # dois = [lang_dict["translation"][l] for a in articles]

    for doi in dois:
        print(doi)
        # get all available article titles and dois
        langs = [file for file in os.listdir(f"articles/{doi}") if file[-len(".xml"):] == ".xml"]
        for i in range(len(langs)):
            if langs[i][:-len(".xml")] == langs[i][0:3]: # format HAS to be exactly [lang].xml to be displayed on the website.
                with open(f"articles/{doi}/{str(langs[i])}", "r") as f:
                    this_data = BeautifulSoup(str(f.read()), features="xml")
                    title = str_strip(this_data.find("article-title").string)
                    if doi in articles_dict.keys():
                        articles_dict[doi][langs[i][0:3]] = title
                    else:
                        articles_dict[doi] = {langs[i][0:3]: title}

    with open("articles.json", "w+") as f:
        json.dump(articles_dict, f, ensure_ascii=False, indent=2)


def update_dropdown_langs(langs):
    #
    # POPULATE DROPDOWN LIST W/ ALL AVAILABLE LANGS
    # (links are blank -- they get populated by js/webscript.js)
    #
    html = BeautifulSoup(str(open("style/navigation.html").read()), features="html.parser")
    dropdown = html.find("div", {"id": "lang-dropdown"})
    dropdown.clear()
    
    lang_dict = load_langs()
    codes = [lang_dict["translation"][l] for l in langs]
    for code in codes:
        dropdown.append(BeautifulSoup(f"<a href='' id='{code}'>{lang_dict['codes'][code]}</a>", features="html.parser"))
    
    with open("style/navigation.html", "w+") as f:
        f.write(html.prettify())

def update_index_files(langs):
    #
    # CREATES NEW INDEX FILE FOR EACH LANGUAGE W/ TRANSLATED TITLES.
    # (currently uses the Korean index as the model)
    #
    html = BeautifulSoup(str(open("index/kor.html").read()), features="html.parser")
    articles = html.find("div", {"class": "articles-index"})
    scripts = [s for s in html.find_all("script")]

    lang_dict = load_langs()
    codes = [lang_dict["translation"][l] for l in langs]
    articles_dict = load_articles()
    dois = list(articles_dict.keys())

    for code in codes:
        # Add links to all available articles.
        articles.clear()
        articles_with_lang = [doi for doi in dois if code in articles_dict[doi].keys()]
        for a in articles_with_lang:
            articles.append(BeautifulSoup(f"<a href='/articles/{a}/{code}.xml'>{articles_dict[a][code]}</a>", features="html.parser"))
        
        # Change the on-load script.
        script = scripts[-1]
        script.clear()
        script.append(BeautifulSoup("setTimeout(function() {configureDropdown('index', '"+code+"');}, 100);", features="html.parser"))

        with open(f"index/{code}.html", "w+") as f:
            f.write(html.prettify())

if __name__ == "__main__":
    all_articles = [doi for doi in os.listdir(f"articles") if doi != ".DS_Store"]
    all_langs = [lang for lang in load_langs()['translation'].keys()]

    articles = all_articles
    # update_catalog(articles)
    langs = all_langs
    update_dropdown_langs(all_langs)
    update_index_files(all_langs)



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
