import requests
import feedparser
import html
import json
from bs4 import BeautifulSoup, NavigableString, Tag

bottoken = 'ADD TOKEN HERE'
with open('data.txt') as f:
    data = json.load(f)

last_etag = data['etag']
last_modified = data['last_modified']

d = feedparser.parse('https://www.mindfactory.de/xml/rss/mindstar_artikel.xml', etag=last_etag, modified=last_modified)
if d.status != 304 and last_etag != d.etag and last_modified != d.modified:
    data = {}
    data['etag'] = d.etag
    data['last_modified'] = d.modified
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
    for entries in d.entries:
        item = []
        item.append(entries.title)
        soup = BeautifulSoup(entries.summary, 'html.parser')
        for br in soup.find_all('br'):
            next_s = br.nextSibling
            if not (next_s and isinstance(next_s,NavigableString)):
                continue
            next2_s = next_s.nextSibling
            if next2_s and isinstance(next2_s,Tag) and next2_s.name == 'br':
                text = str(next_s).strip()
                if text and next_s.find("Preis: €") != -1:
                    item.append(next_s.replace("Ã¤", "ä"))

        item.append(entries.link)
        text = "\n".join(str(e) for e in item)
        #print(text)
        r = requests.get('https://api.telegram.org/bot'+bottoken+'/sendMessage?chat_id=@mindstar_dach&text=' + text)

