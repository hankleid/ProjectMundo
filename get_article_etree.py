# %%

import requests
import xml.etree.ElementTree as et

# %%

URL = "http://api.springernature.com/openaccess/jats?"

PARAMS = {
    "q": "doi:10.1038/s41467-019-11343-1",
    "api_key": "86e121ae7080eb66373361f62f04b07b"
}

r = requests.get(url=URL, params=PARAMS)

#%%

# print(r)
data = et.fromstring(r.content)
article = data[4][0]
print([x.tag for x in article])
print(f"front: {[x.tag for x in article[0]]}")
print(f"article meta: {[x.tag for x in article[0][1]]}")
print(f"body: {[x.tag for x in article[1]]}")
print(f"back: {[x.tag for x in article[2]]}")

# %%

front, body, back = article[0], article[1], article[2]
journal = front[0][1][0].text
doi = front[1][2].text
title = front[1][4][0].text
print(f"journal: {journal}")
print(f"doi: {doi}")
print(f"title: {title}")

# %%

authors = [f"{s.text}, {g.text}" for s,g in zip(front.iter('surname'), front.iter('given-names'))]
emails = [e.text for e in front[1][5].iter('email')]
print(f"authors: {authors}")
print(f"emails: {emails}")

# TO-DO: affiliations
# TO-DO: dates

# %%

abstract = []
# paragraphs of text that constitute the abstract.
for ab in front[1].findall('abstract'):
    abstract.append(ab.find('p').text)
print(f"abstract ({len(abstract)} paragraphs):\n{abstract}")

intro = []
# paragraphs of text that constitute the introduction.

# %%

print(f"article has {len(body)} sections: {[sec.find('title').text for sec in body.findall('sec')]}.")

body_txt = []
for sec in body.findall('sec'):
    section = []
    for paragraph in sec.findall('p'):
        print(et.tostring(paragraph, encoding='utf-8', method='text'))
        # node = paragraph
        # if paragraph.text != None:
        #     print(paragraph.text)
        # for n in node:
        #     if n.text != None:
        #         print(n.text)
        

    
    # body_txt.append(section)

# print(body_txt)


# %%
