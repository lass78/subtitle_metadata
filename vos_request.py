from mimetypes import init
from urllib.error import HTTPError
import requests

import webvtt
from PIL import Image
from io import StringIO
from io import BytesIO
import streamlit as st
import ast
import os

# from apicall import get_subtitles

headers = {'x-apikey':os.getenv('VOS_API_KEY')}


class Playable():  
    
    def __init__(self, prodn) -> None:
        self.prodn = prodn
        self.playable = self.get_playable(self.prodn)
        if self.playable == None: 
            self.title = "Ikke fundet"
            self.thumb = Image.open("dummy.png")
            self.subtitles = ""
            self.description = "Ikke fundet" 
            self.keywords = []
            self.categories = dict()
        else:
            self.title = self.get_title(self.playable)
            self.thumb = self.get_img(self.playable)
            self.subtitles = self.get_subtitles(self.playable)
            self.description = self.get_description(self.playable)
            self.keywords = self.get_keywords(self.playable)
            self.categories = self.get_categories(self.playable)
            print(self.playable)
        print ("Playable created")
        print ()
        print ()

    # @st.cache(show_spinner=False)
    def get_playable(self, produktionsnummer):


        headers = {'x-apikey':os.getenv('VOS_API_KEY')}
        id = "urn:dr:ocs:tv:content:playable:" + produktionsnummer
        api_url = "https://api.dr.dk/vos/v1/playables/" + id
        
        try: 
            r = requests.get(api_url, headers=headers)
            r.raise_for_status()
            playable = r.json()
            print(playable)
            return playable
        
        except requests.exceptions.HTTPError as e:
                print ("HTTPError: ", e)
                return None

        except requests.exceptions.RequestException as e:
                print ("RequestError: ", e)
                return None
    
    def get_img2(self, playable):
        image = None
        image_assets = playable['imageAssets']
        for asset in image_assets:
            print (asset)




    def get_img (self, playable):
        import re
        image = None
        image_assets = playable['imageAssets']
        for asset in image_assets:
            
            print (asset)
            try:
                img = requests.get(asset['url'], headers=headers).content
            except HTTPError as e:
                print("HTTPError: ", e)
                return Image.open('dummy.png')
            # print(img)         
       
            format = re.search("(?<=\/)\w+", asset['format']).group()
            print (format)

            with BytesIO(img) as f:
                with Image.open(f) as tmp:
                    image = tmp
                    image.save('imgtst.'+format, format=format)
                    # image = Image.open('tmp.jpg')
                    # image.show()    
                print ("image found")
                return image
        return Image.open('dummy.png')

    def get_title(self, playable):
        if 'displayTitle' in playable.keys():
            return playable['displayTitle']
        elif 'title' in playable.keys():
            return playable['title']
        else:
            return "No Title"
        

    def get_description(self, playable):
        
        try:
            desc = playable['description']
            print ("beskrivelse fundet")
        except KeyError as e:
            print ("KEYERROR: ", e)               
            desc = "Ingen beskrivelse fundet"

        return desc


    def get_keywords(self, playable):
        if 'keywords' in playable.keys(): 
            keywords_list = playable['keywords']
        else: 
            keywords_list = []

        return keywords_list


    def get_categories(self, playable):
        categories = playable['categories']
        print(categories)
        result = dict()
        for item in categories:
            key = item['authority']
            value = item['value']
            result[key] = value
        return result


    def get_subtitles(self, playable):
        options = playable['subtitleLanguagesOffered']

        if len(options) < 1: 
            return "ingen undertitler"
        else:
            if 'Combined' in options:
                preferred_subtitle = 'Combined'
            elif 'Danish' in options:
                preferred_subtitle = 'Danish'
            else:
                preferred_subtitle = 'Foreign'

        for asset in playable['videoAssets']:
            for sources in asset['sources']:
                for subs in sources['subtitles']:
                    if preferred_subtitle in subs['subtitleLanguagesFulfilled']:
                        
                        r = requests.get(subs['url'])
                        filename = "temp.vtt"
                        r.encoding = 'utf-8'
                        subtitles = r.text
                        with open(filename, 'w', encoding="utf-8", newline='') as f:
                            f.write(subtitles)

                        subt_file = webvtt.read(filename)
                        result = ""
                        for sub in webvtt.read(filename):                            
                            sent = str.replace(str.rstrip(str.strip(sub.text)),"\n"," ")                           
                            result += sent + " "
                        # print (result)
                        return result




        
        # videoassets = playable['videoAssets']
        # for asset in videoassets:
        #     sources = asset['sources']
        #     for source in sources:
        #         subtitles = source['subtitles']
        #         for subtitle in subtitles:
        #             if 'Danish' in subtitle['subtitleLanguagesFulfilled']:
        #                 url = subtitle['url']
        #                 # if "HardOfHearing" in url: 
        #                 r = requests.get(subtitle['url'])
        #                 r.encoding = 'utf-8'

        #                 subtitles = r.text
        #                 buffer = StringIO(subtitles)
        #                 result = ""
        #                 for sub in webvtt.read_buffer(buffer):
        #                     sent = str.replace(str.rstrip(str.strip(sub.text)),"\n"," ")
                            
                        
        #                     result += sent + " "
        #                 # print (result)
        #                 return result
        #     return "Ingen undertekster"                
        #     # print (len(sources))



    def get_subtitles2(self, playable):
            # playable = playable['playable']
            print (playable)
        
            if 'Danish' in playable['subtitleLanguagesOffered']:
                for asset in playable['videoAssets']:
                    # print (asset['id'])
                    for sources in asset['sources']:
                        # print (sources['subtitles'])
                        for subs in sources['subtitles']:
                            if 'Danish' in subs['subtitleLanguagesFulfilled']:
                                return (subs['url'])
                    # print ()

            else:
                return "ingen danske undertekster"

def subtitles_as_text(subs):
    result = ""
    for sub in subs:
        result += sub.text + "\n"

    return result


    



def main():
    ellemann = '00102235010'
    versus = '00922001260'

    abekopper = '00102200330'

    tva = "00122241470"
    dum_tva = '00122241600'

    prod_n = versus


    p = Playable(prod_n)
    print (p)
    print (p.subtitles)



if __name__ == '__main__':
    main()



