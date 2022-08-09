from pip import main
import pysrt
import spacy
import nltk
from keybert import KeyBERT
import subprocess
import yake
import streamlit as st


nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords

sw = stopwords.words('danish')
extra_stopwords = ["kan", "tæt", "ved", "mest", "slags", "andre", "vores", "ser", "nye", "får", "mere", "sige"]

 

for word in extra_stopwords:
    sw.append(word)

# print (sw)

subs = pysrt.open("tmp.srt")

text = ""



@st.cache(show_spinner=False)
def get_keywords_yake(text, n):
    language = "da"
    max_ngram_size = 2
    deduplication_threshold = 0.9
    numOfKeywords = n
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None, stopwords=sw)
    keywords = custom_kw_extractor.extract_keywords(text)
    return keywords

@st.cache(show_spinner=False)
def get_entities_spacy(text, n, label):
    nlp = spacy.load("da_core_news_lg")
    doc = nlp(text)
    ents = doc.ents
    ent_dict = dict()
    
    for ent in ents:
        if (ent.label_ == label):
            if ent.text in ent_dict.keys():
                ent_dict[ent.text] +=1
            else:
                ent_dict[ent.text] = 1
    
    sorted_ents = sorted(ent_dict.items(), key=lambda kv: kv[1], reverse=True)

    return sorted_ents[:n]

@st.cache(show_spinner=False)
def get_keywords_keyBERT(text, n):
    model = KeyBERT(model="paraphrase-multilingual-MiniLM-L12-v2")
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=sw, top_n=n )
    return keywords


def kw_as_text(kw_list):
    result = ""
    c = 0
    for kw, v in kw_list:
        c+=1
        result = result + "(" + str(c) + ") " + kw + " - " + "{:.2f}".format(v) + "  \n "
    return result     



for sub in subs:
    text = text + sub.text + " "

print (text)



def main() -> int:
    print ("SPACY - Organisations")
    orgs = get_entities_spacy(text,5, "ORG")
    print (orgs)
    print (kw_as_text(orgs))

    print ()

    print ("keyBERT")
    kw = (get_keywords_keyBERT(text,10))
    print (kw_as_text(kw))
    print (kw)


    print ()



if __name__ == '__main__':
    main()
