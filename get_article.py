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

#%%

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
        subsection[p['id']] = paragraph
    return this_sec['id'], subsection

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

# TODO: finish organizing article into CONTENTS; to do so, might have to handle the Figure sections since <p> has no 'id' attr.
# restructure sentences in paragraph lists to be one sentence per element, each separated by a list of ref #s for the previous sentence.

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



# %%
            
with open("test.json", "w+") as outfile:
    json.dump(CONTENT, outfile, indent=4)

# %%
