# %%

import requests
from bs4 import BeautifulSoup
from translation import Translator

# %% ARTICLE ACQUISITION

key = ""
with open("../keys/nature_key.txt") as f:
      key = f.readline()


URL = "http://api.springernature.com/openaccess/jats?"


PARAMS = {
    "q": "doi:10.1038/s41467-017-00516-5",
    "api_key": key
}

r = requests.get(url=URL, params=PARAMS)

data = BeautifulSoup(r.content, features="xml")
# Enter correct XSLT style information.
data.contents[0].replace_with(BeautifulSoup('<?xml-stylesheet type="text/xsl" href="jats-html.xsl"?>', features="xml"))
# Remove the API response portion of the XML.
data.response.replace_with(data.records.article)

f = open(f"korean.xml", "w")
f.write(data.prettify())
f.close()

#%% TRANSLATION EXECUTION FUNCTIONS

def parse_sups(this_sups):
    # returns a list of reference elements from a list of sup elements.
    refs = []
    for sup in this_sups:
        i = 0
        for ref in sup.find_all('xref'):
            if i != 0:
                refs.append(",")
            refs.append(ref)
            i += 1

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


def translate(xml, tl, language, text=False):
    # translates the chunk in place.
        # xml: article to translate
        # tl: Translator object
        # language: language to translate to
        # text (bool): true if only want to translate string, not whole xml obj.
    
    if text:
        result = tl.translate_text(xml.string, language)
        xml.clear()
        xml.append(result)
    else:
        # translate entire xml
        result = tl.translate_xml(xml, language)
        new_xml = BeautifulSoup(result, features="xml")
        xml.clear()
        xml.extend(new_xml)

def translate_article(xml, tl, language):
    # edits xml in place with translated text.
        # xml: article to translate
        # tl: Translator object
        # language: language to translate to

    front = xml.front
    body = xml.body
    back = xml.back

    title = front.find('article-title')
    translate(title,tl,language,text=True)

    ab = front.find('abstract')
    translate(ab,tl,language)

    # Restructure the sentences.
    for p in body.find_all('p'):
        formatted_p = parse_par(p)
        p.clear()
        p.extend(formatted_p.contents)

    # Translate the body.
    for sec in body.find_all('sec'):
        translate(sec,tl,language)

    # Translate acknowledgements and author contributions.
    ack = back.find('ack')
    translate(ack,tl,language)
    contr = back.find('sec', {'sec-type': 'author-contribution'})
    translate(contr,tl,language)

    # Translate the (sub)titles in case they were missed.
    for title in data.find_all('title'):
        translate(title,tl,language,text=True)


def filename_from_DOI(xml):
    doi = xml.front.find('article-meta').find('article-id', {'pub-id-type': 'doi'}).string
    _ = doi.replace('/','_')
    filename = _.replace('.','X')
    return filename


#%% EXECUTION
tl = Translator()
translate_article(data, tl, "Korean")
print(tl.count_tokens())

#%% SAVING

fn = filename_from_DOI(data)
# f = open(f"{fn}.xml", "w")
f = open(f"index.xml", "w")
f.write(data.prettify())
f.close()

# %%
