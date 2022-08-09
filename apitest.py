import requests

import webvtt
from PIL import Image
from io import StringIO
from io import BytesIO
import json
import pandas as pd


headers = {'x-apikey':'zhBZ2JDWGyMohVxRRu4KHPYToD40LojAKywNgTWkfA4'}
id = ""
api_url = "https://api.dr.dk/vos/v1/playables/" + id

itemlist = []
loop = True

while loop:

        try: 
                r = requests.get(api_url, headers=headers)
                r.raise_for_status()
                result = r.json()
                # json_object = json.dumps(result, indent=4)
                # with open("tmp.json", "a") as file:
                #         file.write(json_object)
                
                for item in result['items']:
                        itemlist.append(item)


                if 'next' in result.keys():
                        loop = True
                        print (result['next'])
                        api_url = result['next']
                else:
                        loop = False
           

        except requests.exceptions.HTTPError as e:
                print ("HTTPError: ", e)
        

        except requests.exceptions.RequestException as e:
                print ("RequestError: ", e)

        # print ("ItemList Len: ", len(itemlist))


df = pd.DataFrame(data=itemlist)
df = df.set_index('id')
print (df)
df.to_csv('vos_data.csv')


