from numpy import place
import streamlit as st
from vos_request import Playable
from PIL import Image
import metadata
import pandas as pd
import plotly
import time

st.set_page_config(layout="wide")

# Initialization
if 'prodn' not in st.session_state:
    st.session_state['prodn'] = "Indtast det 11-cifrede produktionsnummer her - eller snup det fra MA"

if "summary" + st.session_state.prodn not in st.session_state:
    st.session_state["summary"+st.session_state['prodn']] = "INTET SUMMARY"

udsendelse = Playable(st.session_state.prodn)


st.title("Metadata Generator")

with st.sidebar:
        
    produktionsnummer = st.text_input("", key="prodn", placeholder="Indtast det 11-cifrede produktionsnummer her - eller snup det fra MA")
    st.caption('Vær opmærksom på, at nyhedsindhold forsvinder efter 30 dage, og at enkelte produktioner ikke rummer danske undertekster')

    img = udsendelse.thumb
    st.image(img)
    st.header("Titel")
    st.markdown(udsendelse.title)
    st.header("Beskrivelse")
    st.markdown(udsendelse.description)

    st.header('Keywords')

    if len(udsendelse.keywords) > 0:

        for e in udsendelse.keywords:
            #st.markdown("**" + e['name'] + "**")
            words_string = ""
            delimeter = ""
            for w in e['values']:
                words_string = words_string + delimeter + w
                delimeter = ", "

            st.markdown("**" + e['name'] + "**: " + words_string)

    else: st.markdown('Ingen keywords fundet')


    st.header('Kategoriseringer')

    print (udsendelse.categories)
    for key, value in udsendelse.categories.items():
        st.markdown("**" + key + "**: " + value)


with st.expander(label="Se undertekster"):
    st.write(udsendelse.subtitles)

st.write("Følgende er metadata genereret automatisk ud fra undertekst-filen")

col3, col4, col5 = st.columns(3)

with col3:
    
    col3.subheader("Personer")
    with st.spinner(text='Leder efter personer...'):
        
        col3.write(metadata.kw_as_text(metadata.get_entities_spacy(n=5, label="PER", text=udsendelse.subtitles)))
    col3.subheader("Steder")

    with st.spinner(text='Leder efter steder...'):       
        col3.write(metadata.kw_as_text(metadata.get_entities_spacy(n=5, label="LOC", text=udsendelse.subtitles)))

    col3.subheader("Organisationer")
    with st.spinner(text='Leder efter organisationer...'):        
        organisations = metadata.get_entities_spacy(n=5, label="ORG", text=udsendelse.subtitles)
        col3.write(metadata.kw_as_text(organisations))


with col4:
    col4.subheader("Keywords (Yake)")

    with st.spinner('Udtrækker keywords med YAKE-algoritmen'):
        yake_kw = metadata.get_keywords_yake(n=10,text=udsendelse.subtitles)
    
    col4.write(metadata.kw_as_text(yake_kw))
    df = pd.DataFrame(data=yake_kw, columns=["kw", "val"])
    df.set_index('kw', inplace=True)
    df['val']= df['val'].apply(lambda x: df['val'].max() - x)
    col4.bar_chart(data=df)

with col5:
    
    col5.subheader("Keywords (keyBERT)")

    with st.spinner('Udtrækker keywords med keyBERT-algoritmen'):
        keybert_kw = metadata.get_keywords_keyBERT(n=10,text=udsendelse.subtitles)
    
    col5.write(metadata.kw_as_text(keybert_kw))
    df = pd.DataFrame(data=keybert_kw, columns=["kw", "val"])
    df.set_index('kw', inplace=True)

    col5.bar_chart(data=df)

def gpt3_request(input_text, max_tokens):
    import os
    import openai


    if len(input_text) > (4 * max_tokens): input_text = input_text[:4*max_tokens]

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=input_text + "\n\nTl;dr",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    
    return response['choices'][0]['text']




def do_summary():
    print(st.session_state)
    print("CLICKED")
    
    st.session_state["summary"+st.session_state['prodn']] = gpt3_request(udsendelse.subtitles, 2000)
    st.write(st.session_state["summary"+st.session_state['prodn']])

st.header('GPT3 Summary')
gpt3_clicked = st.button(label="GPT3 Summary - advarsel det koster penge")
if gpt3_clicked: do_summary()


    

