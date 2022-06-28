import ttconv.stl.reader
import json
import pysrt
import spacy
from collections import Counter
from string import punctuation
import nltk
from keybert import KeyBERT
import subprocess
import yake
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


# convert from STL to SRT format
filename = "tekstfiler/stojbergtva.xs1"

subprocess.run('tt convert -i ' + filename + ' -o tmp.srt --itype STL')

nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords

sw = stopwords.words('danish')
extra_stopwords = ["kan", "tæt", "ved", "mest", "slags", "andre", "vores", "ser", "nye", "får", "mere", "sige"]

 

for word in extra_stopwords:
    sw.append(word)

print (sw)

subs = pysrt.open("tmp.srt")

text = ""

for sub in subs:
    text = text + sub.text + " "

print (text)



def get_keywords_yake(text, n):
    language = "da"
    max_ngram_size = 2
    deduplication_threshold = 0.9
    numOfKeywords = n
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None, stopwords=sw)
    keywords = custom_kw_extractor.extract_keywords(text)
    return keywords


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

def get_keywords_keyBERT(text, n):
    model = KeyBERT(model="paraphrase-multilingual-MiniLM-L12-v2")
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=sw, top_n=n )
    return keywords

print ("SPACY - Organisations")
print (get_entities_spacy(text,5, "ORG"))
print ()

print ("SPACY - Locations")
print (get_entities_spacy(text,5, "LOC"))
print ()

print ("SPACY - Persons")
print (get_entities_spacy(text,5, "PER"))
print ()

print ("keyBERT")
print (get_keywords_keyBERT(text,10))
print ()

print ("YAKE")
print (get_keywords_yake(text,10))
print ()





