# %%

import requests
from bs4 import BeautifulSoup
import json

# %%

URL = "http://api.springernature.com/openaccess/jats?"

PARAMS = {
    "q": "doi:10.1038/s41467-019-11343-1",
    "api_key": "86e121ae7080eb66373361f62f04b07b"
}

r = requests.get(url=URL, params=PARAMS)

# %%

## TESTING NEW IDEA: CHANGING XML IN PLACE KINDA
## RETURN XML OF SAME FORMAT BUT WITH SENTENCES TRANSLATED
## REFERENCES AT THE END OF EACH SENTENCE.

data = BeautifulSoup(r.content, features="xml")
body = data.body
# print(body.prettify())
# print(len(body.contents))
sections = [_ for _ in body.children]
intro = sections[0] # equivalent to subsection
pars = [_ for _ in intro.children]

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

#print(parse_par(body.contents[0].contents[0]).prettify())


for sec in body:
    pars = sec.find_all("p")
    for p in sec.find_all("p"):
        new_p = parse_par(p)
        p.clear()
        p.extend(new_p.contents)
print(body.prettify())

#%%
with open("test.json", "w+") as outfile:
    json.dump(CONTENT, outfile, indent=4)
    
print(len(CONTENT["Sec1"]["Par3"]))