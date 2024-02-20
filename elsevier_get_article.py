"""
Created on Sun Feb 18 19:34:13 2024

@author: oatpix
"""

#%%

import requests
import json
# import xml.etree.ElementTree as et

# %% 

import requests
import xml.etree.ElementTree as et

doi = "10.1016/S0014-5793(01)03313-0"

URL = f"https://api.elsevier.com/content/article/doi/{doi}?"

PARAMS = {
    "apiKey": "e340e68fa93f005b0ef7070c79c70a84"
}

r = requests.get(url=URL, params=PARAMS)

#%%

# print(r)
data = et.fromstring(r.content)
for child in data:
    print(child.tag)

print([c.tag for c in data[0]])

URL = "http://api.springernature.com/openaccess/jats?"

PARAMS = {
    "q": "doi:10.1038/s41467-019-11343-1",
    "api_key": "86e121ae7080eb66373361f62f04b07b"
}

r = requests.get(url=URL, params=PARAMS)

#%%

print(r)
data = r.json()
print(data)

# %%

print(data['apiMessage'])

# %%

URL = "http://api.springernature.com/meta/v2/json?"

PARAMS = {
    "q": "doi:10.1038/s41467-019-11343-1",
    "api_key": "86e121ae7080eb66373361f62f04b07b"
}

r = requests.get(url=URL, params=PARAMS)

# %%

print(r)
print(r.json())

# %%