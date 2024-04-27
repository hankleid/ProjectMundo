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
print(body.prettify())
print(len(body.contents))
sections = [_ for _ in body.children]
intro = sections[0] # equivalent to subsection
pars = [_ for _ in intro.children]

# seems like if you can get it to the <Par#> section, maybe we can feed to chatgpt

# %%

def get_refs(sups):
    flattened = []
    for sup in sups:
        for ref in sup.find_all('xref'):
            flattened.append(ref)
            flattened.append(",")
    return flattened[:-1]

sentences = []
sups = []
curr_sent = ""
new_par = BeautifulSoup("<p></p>",features='xml')
for s in pars[1].children:
    if s.name == 'sup':
        sups.append(s)
    elif s.string != None:
        if s.string[0] != '.':
            curr_sent += s.string
        else:
            # end of sentence
            sentences.append(curr_sent)
            curr_sent = s.string

            refs = get_refs(sups)
            sup = BeautifulSoup("<sup></sup>",features='xml')
            for i, ref in zip(range(len(refs)), refs):
                sup.sup.insert(i, ref)
            sentences.append(sup.sup)
            sups = []

print(sentences)

for i, s in zip(range(len(sentences)), sentences):
    new_par.p.insert(i,s)

print(new_par.prettify())

# %%




#%%

## PREVIOUS ATTEMPT

# print(r)

data = BeautifulSoup(r.content, features="xml")
print(data)
# %%

body = data.body
print(body.prettify())
print(len(body.contents))

# %%

def parse_section(this_sec):
    # returns the ID of the (sub)section and the (sub)section in dictionary form.
    # each paragraph is represented as a list of sentences.
    # 's' must be a chunk of XML that has no further subsections.
    subsection = {
                "title": this_sec.title.string
            }
    ps = [_ for _ in this_sec.children][1:]
    for p in ps:
        paragraph = []
        print(p)
        if p.string != None: # (initial) text.
            paragraph.append(p.string)
        else:
            for s in p.children:
                # print(s)
                if s.string != None:
                    paragraph.append(s.string) # sentence
                else:
                    numbers = []
                    for xref in s.find_all('xref'):
                        numbers.append(xref.string)
                    paragraph.append(numbers)
        subsection[p['id']] = format_paragraph(paragraph)
    return this_sec['id'], subsection

def format_paragraph(par):
    # par is a list of sentences (and refs).
    # if a sentence starts with a period, it should move to the end of the 2nd previous sentence.
    # (to put the refs after a full sentence)
    # if a sentence ends with a comma, it should find join itself to the previous 'sentence.'
    formatted = ["" for _ in range(len(par))]
    i_p = 0
    i_f = 0
    for sentence in par[0:]:
        if isinstance(sentence, list):
            formatted[i_f] = [int(ref) for ref in sentence]
        elif sentence.isnumeric():
            formatted[i_f] = int(sentence)
        elif sentence[0] == ',':
            # put the clauses together in one sentence.
            sub = 1
            while isinstance(formatted[i_f-sub], str) == False:
                sub += 1
            formatted[i_f-sub] += sentence
            i_f -= 1
        elif sentence[0] == '.': # change to be if any char not the final one is equal to "."
            # put the period at the end of the last sentence.
            sub = 1
            while isinstance(formatted[i_f-sub], str) == False:
                sub += 1
            formatted[i_f-sub] += "."
            formatted[i_f] = sentence[2:]
        # elif i_f > 0 and len(formatted[i_f-1]) > 5 and formatted[i_f-1][:-6] == "\u00a0":
        #     # put fig number back in the same sentence.
        #     formatted[i_f-1] += " " + sentence
        #     i_f -= 1
        else:
            formatted[i_f] = sentence
        i_p += 1
        i_f += 1
    return formatted

#%% 

for sec in body.children:
    print(sec.title.string)

CONTENT = {}
# Title
# Authors
# (metadata like date etc)
# Abstract
# Section # (title), 
# Subsection
# Paragraphs
# (text)
# (figure)

# TODO: differentiate btwn refs and reg numbers by putting all refs in their own list even if it's a single ref.
# move sentences with periods
# move sentences randomly put on another line back to the prev. one.

for sec in body.children:
    print(sec['id'])
    print([subsec['id'] for subsec in sec.find_all('sec')])
    CONTENT[sec['id']] = {
            "title": sec.title.string
    }
    if not sec.sec: # there are no futher subsections
        _, value = parse_section(sec)
        CONTENT[sec['id']] = value
    else: # there are subsections
        for subsec in sec.find_all('sec'):
            print(subsec['id'])
            key, value = parse_section(subsec)
            CONTENT[sec['id']][key] = value

with open("test.json", "w+") as outfile:
    json.dump(CONTENT, outfile, indent=4)
    
print(len(CONTENT["Sec1"]["Par3"]))