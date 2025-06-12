from article import *
import os
import json
from translation import GPT



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
        
        if doi not in articles_dict.keys():
            articles_dict[doi] = {"langs":{}}

        for i in range(len(langs)):
            print(langs[i])
            if langs[i][:-len(".xml")] == langs[i][0:3]: # format HAS to be exactly [lang].xml to be displayed on the website.
                with open(f"articles/{doi}/{str(langs[i])}", "r") as f:
                    code = langs[i][0:3]
                    this_data = BeautifulSoup(str(f.read()), features="xml")
                    if code == "eng":
                        date = this_data.find("pub-date", {"publication-format":"electronic"})

                        contribs = this_data.find("contrib-group").find_all("contrib", {"contrib-type":"author"})
                        fns = [str_strip(c.find("given-names").string) for c in contribs if c.find("given-names")]
                        lns = [str_strip(c.find("surname").string) for c in contribs if c.find("surname")]

                        articles_dict[doi]["meta"] = {
                            "journal": str_strip(this_data.find("abbrev-journal-title").string),
                            "volume": str_strip(this_data.find("volume").string),
                            # "pages": str_strip(this_data.find("fpage").string)+"-"+str_strip(this_data.find("lpage").string),
                            "doi": str_strip(this_data.find("article-id", {"pub-id-type":"doi"}).string),
                            "date": str_strip(date.find("year").string)+"-"+str_strip(date.find("month").string)+"-"+str_strip(date.find("day").string),
                            "authors": ''.join([f"{f} {l}, " for f,l in zip(fns,lns)])[:-2]
                        }
                    # print(this_data.find("article-title").find_all(text=True))
                    title = ''.join([str_strip(s) for s in this_data.find("article-title").find_all(text=True)])
                    articles_dict[doi]["langs"][code] = title

    with open("articles.json", "w+") as f:
        json.dump(articles_dict, f, ensure_ascii=False, indent=2)

def update_dropdown_langs(langs):
    # ***DEPRECATED***
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

def date_score(date):
    # format: YYYY/(M)M/(D)D
    i = date.find("-")
    sum = int(date[0:i]) * 10000
    j = date[i+1:].find("-")
    sum += int(date[i+1:i+1+j])*100 + int(date[-2:])
    return sum

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

    _articles = []
    for code in codes:
        # Add links to all available articles.
        articles.clear()
        articles_with_lang = [doi for doi in dois if code in articles_dict[doi]['langs'].keys()]
        for a in articles_with_lang:
            m = articles_dict[a]["meta"]
            line1 = f"<div class='line1'><i>{m['journal']}</i> <b>{m['volume']}</b>, ({m['date'][0:4]})</div>"
            # line2 = f"<div class='line2'>DOI: {m['doi']}</div>"
            line2 = f"<div class='line2'>{m['authors']}</div>"

            html_str = f"<div class='index-entry'><div class='entry-link'><a href='/ProjectMundo/articles/{a}/{code}.xml'>{articles_dict[a]['langs'][code]}</a></div><div class='entry-meta'>{line1}{line2}</div></div>"

            _articles.append({date_score(m['date']): BeautifulSoup(html_str, features="html.parser")})
        
        _articles = sorted(_articles, key=lambda d: -list(d.keys())[0])
        for a in _articles:
            articles.append(list(a.values())[0])
        
        # Change the on-load script.
        script = scripts[-1]
        script.clear()
        script.append(BeautifulSoup("setTimeout(function() {configureDropdown('index', '"+code+"');}, 100);", features="html.parser"))

        with open(f"index/{code}.html", "w+") as f:
            f.write(html.prettify())

def check_xml_errors(doi, lang):
    # returns the number of nesting errors in the translated xml
    code = load_langs()['translation'][lang]
    path = f"articles/{filename_from_DOI(doi=doi)}"
    with open(path+f"/{code}_qwen.xml", "r") as f:
        lang_data = BeautifulSoup(str(f.read()), features="xml")
    with open(path+f"/eng.xml", "r") as f:
        eng_data = BeautifulSoup(str(f.read()), features="xml")
    
    to_check = ["disp-formula", "fig", "table-wrap"]
    missing_p_errors, missing_fig_errors, nesting_errors = 0, 0, 0
    for name in to_check:
        _eng, _lang = eng_data.find_all(name), lang_data.find_all(name)
        if len(_eng) != len(_lang):
            print("Warning: there may be missing elements.", doi, lang, name, len(_eng), len(_lang))
            missing_fig_errors += len(_eng)-len(_lang)
        for eng_element, lang_element in zip(_eng,_lang):
            eng_dupes, lang_dupes = eng_element.find_all(name), lang_element.find_all(name)
            if len(eng_dupes) != len(lang_dupes):
                nesting_errors += len(lang_dupes)-len(eng_dupes)

    for eng_sec, lang_sec in zip(eng_data.find('body').find_all("sec"), lang_data.find('body').find_all("sec")):
        eng_ps, lang_ps = eng_sec.find_all("p",recursive=False), lang_sec.find_all("p",recursive=False) # remove recursive when support for lists and blocks is added.
        # print(len(eng_ps))
        if len(eng_ps) != len(lang_ps):
            print("Warning: there may be missing paragraphs.", doi, lang, len(eng_ps), len(lang_ps))
            missing_p_errors += len(eng_ps)-len(lang_ps)

    if missing_p_errors>1: missing_p_errors = 1
    if missing_fig_errors>1: missing_fig_errors = 1
    if nesting_errors>1: nesting_errors = 1  
    return missing_p_errors, missing_fig_errors, nesting_errors

def count_tokens(doi, lang):
    model = GPT()
    code = load_langs()['translation'][lang]
    path = f"articles/{filename_from_DOI(doi=doi)}"
    with open(path+f"/{code}.xml", "r") as f:
        data = BeautifulSoup(str(f.read()), features="xml")

    chunks, _,_ = chunkify(data)
    count = 0
    for chunk in chunks:
        count += sum([model.num_tokens(str(xml)) for xml in chunk])
    return count


if __name__ == "__main__":
    articles1 = [
        "10.1038/s41598-023-51013-3", # sci rep 2
        "10.1038/s41598-023-43026-9", # sci rep 3
        "10.1038/s41598-023-45072-9", # covid
        "10.1038/s41467-023-43949-x", # quantum optics
        "10.1038/s41467-023-43067-8", # drug delivery *
        "10.1038/s41467-023-43963-z", # materials science *
    ]

    articles2 = [
        # Health Sciences
        "10.1038/s41467-023-44276-x", #** Risk of COVID-19 death in adults who received booster COVID-19 vaccinations in England
        "10.1038/s41467-024-52894-2", #** Plasma proteomic and polygenic profiling improve risk stratification and personalized screening for colorectal cancer
        "10.1038/s41467-024-48700-8", #* Cosmic kidney disease: an integrated pan-omic, physiological and morphological study into spaceflight-induced renal dysfunction
        "10.1038/s41467-024-46116-y", #** Effect of gut microbiome modulation on muscle function and cognition: the PROMOTe randomised controlled trial
        # "10.1038/s41467-024-49634-x", #* Cohort study of cardiovascular safety of different COVID-19 vaccination doses among 46 million adults in England
        # Life and Biological Sciences
        "10.1038/s41467-024-45446-1", #** Children born after assisted reproduction more commonly carry a mitochondrial genotype associating with low birthweight
        "10.1038/s41467-024-47940-y", #** Gene editing for latent herpes simplex virus infection reduces viral load and shedding in vivo
        "10.1038/s41467-024-53453-5", #** 3D chromatin maps of a brown alga reveal U/V sex chromosome spatial organization
        "10.1038/s41467-024-52388-1", #** CRISPR/Cas9 editing of NKG2A improves the efficacy of primary CD33-directed chimeric antigen receptor natural killer cells
        # "10.1038/s41467-024-46089-y", #* Drug target prediction through deep learning functional representation of gene signatures
        # Social Science and Human Behavior
        "10.1038/s41467-024-46581-5", #* Worldwide divergence of values
        "10.1038/s41467-024-46161-7", #* The Persian plateau served as hub for Homo sapiens after the main out of Africa dispersal
        "10.1038/s41467-024-48512-w", #* Systematic review and meta-analysis of ex-post evaluations on the effectiveness of carbon pricing
        "10.1038/s41467-024-44770-w", #* People quasi-randomly assigned to farm rice are more collectivistic than people assigned to farm wheat
        # "10.1038/s41467-024-44693-6", #* Psychological well-being in Europe after the outbreak of war in Ukraine
        # Chemistry and Materials Science
        "10.1038/s41467-024-46016-1", #* The first demonstration of entirely roll-to-roll fabricated perovskite solar cell modules under ambient room conditions
        "10.1038/s41467-024-45461-2", #* DynamicBind: predicting ligand-specific protein-ligand complex structure with a deep equivariant generative model
        "10.1038/s41467-024-49753-5", #* Lithium-ion battery components are at the nexus of sustainable energy and environmental release of per- and polyfluoroalkyl substances
        "10.1038/s41467-024-48779-z", #* Physics-informed neural network for lithium-ion battery degradation stable modeling and prognosis
        # "10.1038/s41467-023-44481-8", #* Bioinspired structural hydrogels with highly ordered hierarchical orientations by flow-induced alignment of nanofibrils
        # Earth, Environmental and Planetary Sciences
        "10.1038/s41467-024-51355-0", #* Significantly wetter or drier future conditions for one to two thirds of the world’s population
        "10.1038/s41467-024-51879-5", #* Florida Current transport observations reveal four decades of steady state
        "10.1038/s41467-024-45487-6", #* Real-world time-travel experiment shows ecosystem collapse due to anthropogenic climate change
        "10.1038/s41467-023-43832-9", # The first ice-free day in the Arctic Ocean could occur before 2030
        # "10.1038/s41467-024-52631-9", #* Animal life in the shallow subseafloor crust at deep-sea hydrothermal vents
        # Physics
        "10.1038/s41467-024-49689-w", #* Amplification of electromagnetic fields by a rotating body
        "10.1038/s41467-024-48575-9", #* Zero-shot learning enables instant denoising and super-resolution in optical fluorescence microscopy
        "10.1038/s41467-024-45586-4", #* Current-induced switching of a van der Waals ferromagnet at room temperature
        "10.1038/s41467-024-46372-y", #* Ultra-fast switching memristors based on two-dimensional materials
        # "10.1038/s41467-024-45888-7", #* General-purpose programmable photonic processor for advanced radiofrequency applications
    ]
    
    articles3 = ["10.1038/s41467-024-48700-8","10.1038/s41467-024-51355-0","10.1038/s41467-023-43832-9"]

    languages2 = [
        "English",
        "Chinese (simplified characters)",
        "German",
        "French",
        "Hindi",
        "Spanish",
        "Hebrew",
        "Turkish",
        "Russian",
        "Farsi",
        "Swahili",
    ]
    # languages = list(load_langs()['translation'].keys())[1:-1]

    # num_errors = [check_xml_errors(doi, lang) for doi in articles2 for lang in languages2]
    # missing_p_errors = [e[0] for e in num_errors]
    # missing_fig_errors = [e[1] for e in num_errors] # figs, tables, equations
    # nesting_errors = [e[2] for e in num_errors]
    # print(sum(missing_p_errors), "missing paragraph errors out of", len(missing_p_errors), "translations")
    # print(sum(missing_fig_errors), "missing fig/table/equation errors out of", len(missing_fig_errors), "translations")
    # print(sum(nesting_errors), "nesting errors out of", len(nesting_errors), "translations")

    # tokens = [count_tokens(doi, lang) for doi in articles1 for lang in ['English']]
    # print(sum(tokens)/len(tokens))
    # print(tokens)

    
    # all_articles = [doi for doi in os.listdir(f"articles") if doi != ".DS_Store"]
    # all_langs = [lang for lang in load_langs()['translation'].keys()]

    # # articles = all_articles
    # update_catalog(['10X1038_s41467-024-46372-y'])
    # langs = all_langs
    # # langs = ['Chinese (simplified characters)']
    update_index_files(languages2)


    # for d in all_articles:
    #     for l in list(load_langs()['translation'].values()):
    #         path = f"articles/{d}/{l}.xml"
    #         if os.path.exists(path):
    #             data = None
    #             with open(path, "r") as f:
    #                 data = BeautifulSoup(str(f.read()), features="xml")

    #             # new_xsl_el = BeautifulSoup(f"<?xml-stylesheet type='text/xsl' href='/ProjectMundo/style/jats-html.xsl'?>", features="xml")
    #             # data.contents[0].replace_with(new_xsl_el)
    #             change_graphic_dir(data)
    #             print(d, l)

    #             with open(path, "w") as f:
    #                 f.write(data.prettify())

    # title = this_data.find("article-title").string
    # print(title)

    # # add_mathML(this_data)
    # change_graphic_dir(this_data)

    # # SAVING
    # fn = filename_from_DOI(doi=doi)
    # f = open(path, "w+")
    # f.write(this_data.prettify())
    # f.close()
