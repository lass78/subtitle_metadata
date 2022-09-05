import grequests
import pandas as pd
from webvtt import MalformedFileError, MalformedCaptionError


data = pd.read_pickle("data/vos_data_expanded.pkl")


def convert_response_to_text(r):
    import webvtt
    if r == None: return None
    filename = "temp.vtt"
    r.encoding = 'utf-8'
    subtitles = r.text
    with open(filename, 'w', encoding="utf-8", newline='') as f:
        f.write(subtitles)

    result = ""
    
    try:
        for sub in webvtt.read(filename):                            
            sent = str.replace(str.rstrip(str.strip(sub.text)),"\n"," ")                           
            result += sent + " "
        # print (result)

    except (MalformedFileError, MalformedCaptionError) as e:
        print('MalformedFileError:', e)
        
        result = None
    return result



mini = data

urls = mini['subtitleURL'].tolist()
for url in urls:
     print(url)

# urls = ["https://drod21s.akamaized.net/all/clear/none/0b/5f611165aa5a610ef83d780b/00921316570/subtitles/Foreign_HardOfHearing-17650910-428fa33f-737d-4103-96ef-ab9ef665f822.vtt"]

rs = (grequests.get(u) for u in urls)

results = grequests.map(rs)

subtitles = []

for result in results:
    # print (result)
    subtitles.append(convert_response_to_text(result))




sub_df = pd.DataFrame(subtitles)
mini = mini.assign(subtitleText=sub_df.values)



mini.to_pickle('data/expanded_with_subs.pkl')