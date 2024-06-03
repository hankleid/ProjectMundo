# %%

import requests
from bs4 import BeautifulSoup
import json
from translation import Translator

# %%

key = ""
with open("../keys/nature_key.txt") as f:
      key = f.readline()

#%%
URL = "http://api.springernature.com/openaccess/jats?"


PARAMS = {
    "q": "doi:10.1038/s41467-019-11343-1",
    "api_key": key
}

r = requests.get(url=URL, params=PARAMS)

# %%

## TESTING NEW IDEA: CHANGING XML IN PLACE KINDA
## RETURN XML OF SAME FORMAT BUT WITH SENTENCES TRANSLATED
## REFERENCES AT THE END OF EACH SENTENCE.

data = BeautifulSoup(r.content, features="xml")
tl = Translator()

# seems like if you can get it to the <Par#> section, maybe we can feed to chatgpt

def parse_sups(this_sups):
    # returns a list of reference elements from a list of sup elements.
    refs = []
    for sup in this_sups:
        for ref in sup.find_all('xref'):
            refs.append(ref)
            refs.append(",")
    sup = BeautifulSoup("<sup></sup>",features='xml')
    for ref in refs:
        sup.sup.append(ref)
    return sup.sup

def parse_par(this_par):
    sentences = []
    sups = []
    curr_sent = ""
    new_par = BeautifulSoup("<p></p>",features='xml')
    for s in this_par.children:
        if s.name == 'sup':
            sups.append(s)
        elif s.name != None:
            sentences.append(curr_sent)
            curr_sent = ""
            sentences.append(s)
        elif s.string != None:
            if s.string[0] != '.':
                curr_sent += s.string
            else:
                # end of sentence. append the current one and start a new one.
                sentences.append(curr_sent)
                curr_sent = s.string

                # include the references for the previous sentence.
                sentences.append(parse_sups(sups))
                sups = []
    sentences.append(curr_sent)
    if sups != []:
        sentences[-1] = sentences[-1][0:-1] # remove period
        sentences.append(parse_sups(sups))
        sentences.append(".")

    
    new_par.p.extend(sentences)
    return new_par.p


front = data.front
body = data.body

title = front.find('article-title')
new_title = tl.translate_text(title.string, "Latin American Spanish")
title.clear()
title.append(new_title)

for ab in front.find_all('abstract'):
    translated_ab = tl.translate_xml(ab, "Latin American Spanish")
    new_ab = BeautifulSoup(translated_ab, features="xml")
    ab.clear()
    ab.extend(new_ab)
    # if ab.title != None:
    #     new_subtitle = tl.translate_word(ab.title.string, "Latin American Spanish")
    #     ab.title.clear()
    #     ab.title.append(new_subtitle)
    # for p in ab.find_all('p'):
    #     new_abstract = tl.translate_text(p.string, "Latin American Spanish")
    #     p.clear()
    #     p.append(new_abstract)

for p in body.find_all('p'):
    formatted_p = parse_par(p)
    p.clear()
    p.extend(formatted_p.contents)

for sec in body.find_all('sec'):
    translated_sec = tl.translate_xml(sec, "Latin American Spanish")
    new_sec = BeautifulSoup(translated_sec, features="xml")
    sec.clear()
    sec.extend(new_sec.contents)

print(data.prettify())


#%%
f = open("test.xml", "w")
f.write(data.prettify())
f.close()

print(tl.count_tokens())

# %%
