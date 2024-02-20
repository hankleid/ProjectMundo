# %%

import requests
from bs4 import BeautifulSoup

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

for sec in body.children:
    print(sec.title.string)

sections = []
for sec in body.children:
    pars = []
    for p in sec.find_all('p'):
        # while!!!
        if p.string != None:
            pars.append(p.string)
        else:
            for s in p.contents:
                if s.string != None:
                    pars.append(s.string)
    sections.append(pars)

print(sections[0])

# %%
