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

# subs = pysrt.open("tmp.srt")

# text = ""



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
def get_keywords_keyBERT(text, n, max_len=10000):
    print (len(text))
    if len(text) > max_len:
        text = text[0:max_len]
    model = KeyBERT(model="paraphrase-multilingual-mpnet-base-v2")
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=sw, top_n=n )
    return keywords


def kw_as_text(kw_list):
    result = ""
    c = 0
    for kw, v in kw_list:
        c+=1
        result = result + "(" + str(c) + ") " + kw + " - " + "{:.2f}".format(v) + "  \n "
    return result     



def reduce_to_baseform(text):
    import lemmy
    lemmatizer = lemmy.load('da')
    words = text.split()
    lemmatized_text = ""
    delemiter = ""
    for word in words:
        lem_word = lemmatizer.lemmatize("", word.strip(",. -"))
        
        # print(word, ": ", lem_word[0])
        lemmatized_text = delemiter + lemmatized_text + lem_word[0] + " "
        delemiter = " "
    return lemmatized_text




def main():
    import ast
    import time
    from transformers import AutoModelForSeq2SeqLM
    from vos_request import Playable
    prodn = "00102200330" #abekopper
    # prodn = "00122244310" #vingegaard
    prodn = "00102200400" #explainer bier
    prodn = "00102200410" #explainer atomkraft
    subt = Playable(prodn).subtitles
    print (subt)
    with open('thesaurus_keywords.txt') as f:
        thesaurus = ast.literal_eval(f.read())

    print (reduce_to_baseform(subt))

    modelnames = [
        "all-mpnet-base-v2",
        "multi-qa-mpnet-base-dot-v1",
        "all-distilroberta-v1",
        "all-MiniLM-L12-v2",
        "multi-qa-distilbert-cos-v1",
        "all-MiniLM-L6-v2",
        "multi-qa-MiniLM-L6-cos-v1",
        "paraphrase-multilingual-mpnet-base-v2",
        "paraphrase-albert-small-v2",
        "paraphrase-multilingual-MiniLM-L12-v2",
        "paraphrase-MiniLM-L3-v2",
        "distiluse-base-multilingual-cased-v1",
        "distiluse-base-multilingual-cased-v2",
    ]




    for modelname in modelnames:
        model = KeyBERT(model=modelname)
        keywords = model.extract_keywords(subt, keyphrase_ngram_range=(1, 1), stop_words=sw, top_n=10)
        keywords_lemmatized = model.extract_keywords(reduce_to_baseform(subt), keyphrase_ngram_range=(1, 1), stop_words=sw, top_n=10)
        print ("MODEL: ", modelname)
        print(keywords)
        print(keywords_lemmatized)

        print()
        print ("------------------------------")




if __name__ == '__main__':
    main()
