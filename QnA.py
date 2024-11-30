from translation import Translator
from article import *
import json
import os

def make_fulltexts():
    langs = load_langs()['codes']
    for lang in langs.keys():
        articles = langs[lang]['articles']
        for article in articles:
            doi = filename_from_DOI(doi=article['doi'])
            fd = f"FullTexts/{doi}"
            if not os.path.isdir(fd):
                os.mkdir(fd)
            if not os.path.isfile(fd+f"/{lang}.txt"):
                xml = None
                with open(f"lang/{lang}/{doi}.xml", 'r') as f:
                    xml = "".join(f.readlines())
                    xml = BeautifulSoup(xml, features="xml")
                save_fulltext(get_copy(xml), f"{fd}/{lang}.txt")

def generate_qs(num_qs, fd):
    q_prompt = f"Please read the following scientific journal article. Generate {num_qs} detailed and specific questions to test a reader's understanding of the article. Each question should be unique. The questions should labeled 1-{num_qs}. The questions should be multiple choice with 5 possible answers labeled A-E. There should only be one correct answer from the options. The questions should cover as much of the entire article's content as possible. Please format your response as a JSON object with the question, possible answers, and correct answers. The JSON key to each question should be its number. Here is the article: "

    # q_prompt = f"Please read the following scientific journal article. Generate {num_qs} detailed and specific questions to test a reader's understanding, targeting the tables and figures only. Each question should be unique. The questions should labeled 1-{num_qs}. The questions should be multiple choice with 5 possible answers labeled A-E. There should only be one correct answer from the options. The questions should be as specific to the tables and figures as possible. Please format your response as a JSON object with the question, possible answers, and correct answers. The JSON key to each question should be its number. Here is the article and the figures: "

    res = tl.generate_qs(num_qs, f"{fd}/eng_full.txt", q_prompt, figs=False)
    qna = {}
    with open(f"{fd}/QnA.json", "w+") as f:
        f.write(res)
    with open(f"{fd}/QnA.json", "r") as f:
        qna = json.load(f)
    # print(qna)

    # check for duplicate questions
    qs_i, qs = [], []
    repeats = []
    for i in qna.keys():
        q =  qna[i]['question']
        if q in qs:
            repeats.append({i: q})
        qs_i.append(i)
        qs.append(q)
    print(repeats, len(repeats))

    # remove answer key and save it in separate file
    answerkey, questions = {}, {}
    for i in range(num_qs):
        key = str(i+1)
        answerkey[key] = qna[key]["correct_answer"]
        questions[key] = {
            "question": qna[key]["question"],
            "options": qna[key]["options"]
        }
    with open(f"{fd}/QnA_answerkey.json", "w+") as f:
        json.dump(answerkey, f, indent=4)
    with open(f"{fd}/QnA.json", "w+") as f:
        json.dump(questions, f, indent=4)

def translate_qs(lang, fd):
    res = tl.translate_qs(lang, fd+"/QnA.json")
    with open(f"{fd}/QnA_{load_langs()['translation'][lang]}.json", "w+") as f:
        f.write(res)
    
def quiz(lang, fd, text_fd):
    code = load_langs()['translation'][lang]
    if lang == "English":
        fn = "QnA"
    else:
        fn = f"QnA_{code}"
    res = tl.quiz_translation(lang, text_fd+f"/{code}_full.txt", fd+f"/{fn}.json", figs=False)
    with open(f"{fd}/QnA_{code}_answers.json", "w+") as f:
        f.write(res)

def grade(lang, fd):
    answerkey, test = {}, {}
    with open(f"{fd}/QnA_answerkey.json", "r") as f:
        answerkey = json.load(f)
    with open(f"{fd}/QnA_{load_langs()['translation'][lang]}_answers.json", "r") as f:
        test = json.load(f)
    
    incorrect = {}
    for i in answerkey.keys():
        answer = ""
        if isinstance(test[i], list):
            answer = test[i][0]
            correct = answerkey[i] == answer
        else:
            answer = test[i]
            correct = answerkey[i] == answer
        test[i] = [answer, correct]
        if not correct:
            incorrect[i] = answer

    with open(f"{fd}/QnA_{load_langs()['translation'][lang]}_answers.json", "w+") as f:
        json.dump(test, f, indent=4)
    
    return incorrect


if __name__ == "__main__":
    # make_fulltexts()
    tl = Translator("gpt")

    article1 = "10.1038/s41467-023-43444-3" # health
    article2 = "10.1038/s41467-018-04608-8" # zou
    article3 = "10.1038/s41467-023-42766-6" # cats
    article4 = "10.1038/s41467-017-00516-5" # Ahn et al.
    article5 = "10.1038/s41467-019-11343-1" # Jelena
    article6 = "10.1038/s41467-023-40666-3" # human behavior

    articles = [filename_from_DOI(doi=doi) for doi in [article1,article2,article3,article4,article5,article6]]

    for a in articles[-1:]:
        # a = articles[0]
        print(a)
        fd = f"FullTexts/{a}/20q_temp0_figs"
        text_fd = f"FullTexts/{a}"
        # tl.upload_images(a)

        tl.temp = 0
        generate_qs(20, text_fd)
        langs = [l for l in load_langs()['translation']]#[:-6]
        # langs = ["Spanish"]
        for lang in langs:
            tl.temp = 0
            translate_qs(lang, text_fd)
            try:
                tl.temp = 1
                quiz(lang, text_fd, text_fd)
                print(lang, grade(lang, text_fd))
            except:
                print(a)
            pass

