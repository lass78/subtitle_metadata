from urllib import response
import requests
import json

def get_MAinfo(p):
    api_url = "http://manis.net.dr.dk/api/mediaassets?productionNumber=" + p + "&intentionType=Standard&system=od"

    response = requests.get(api_url)
    return response.json()[0]


def get_subtitles(MA_info):
    media_elements = MA_info['mediaElements']

    for e in media_elements:
        if (e['mediaType'] == 'Subtitle'):
            return (e)

info = get_MAinfo("00951216010")
# print (type(info))
# print(info)
subt = get_subtitles(info)
print (subt)
