import requests
import wget
import webvtt
headers = {'x-apikey':'zhBZ2JDWGyMohVxRRu4KHPYToD40LojAKywNgTWkfA4'}


def get_playable(produktionsnummer):

    id = "urn:dr:ocs:tv:content:playable:" + produktionsnummer
    api_url = "https://api.dr.dk/vos/playables/" + id
    r = requests.get(api_url, headers=headers)

    return r.json()

def get_img (produktionsnummer):
    playable = get_playable(produktionsnummer)
    

def get_title(produktionsnummer):
    playable = get_playable(produktionsnummer)
    return playable['title']

def get_description(produktionsnummer):
    playable = get_playable(produktionsnummer)
    return playable['description']

def get_subtitles(produktionsnummer):
    playable = get_playable(produktionsnummer)
    videoassets = playable['videoAssets']
    for asset in videoassets:
        sources = asset['sources']
        for source in sources:
            subtitles = source['subtitles']
            for subtitle in subtitles:
                if 'Combined' or 'Danish' in (subtitle['subtitleLanguagesFulfilled']):
                    url = subtitle['url']
                    if "HardOfHearing" in url: 
                        subtitles = requests.get(subtitle['url']).content
                        wget.download(url, "tmp.vtt", )
                        subs = None
                        with open('tmp.vtt') as file:
                            subs = webvtt.read('tmp.vtt')
                        return subtitles_as_text(subs)
                        #return subtitles
            
        print (len(sources))


def subtitles_as_text(subs):
    result = ""
    for sub in subs:
        result += sub.text + " "

    return result



ellemann = '00102235010'

prod_n = '00102200330'

print ("TITLE: ", get_title(prod_n))
print ("DESCRIPTION: ", get_description(prod_n))
print ("SUBTITLES: ", get_subtitles(ellemann))
