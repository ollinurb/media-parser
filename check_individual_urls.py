from bs4 import BeautifulSoup
import requests
from datetime import datetime

date = datetime.now()
medio = 'lanacion'

url = "https://lanacion.com.ar"

response = requests.get(url)

soup = BeautifulSoup(response.content,'html.parser')

estados = soup.find_all("article")
for x in estados:
    articulo = x.contents[0].contents[0]
    titulo = articulo.get("title")
    href = articulo.get("href")
    article_url = "https://lanacion.com.ar"+ href
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    meta_tags = article_soup.find_all("meta")
    print(titulo)
    potential_id = meta_tags[14]
    if potential_id.get('name') == "vf:container_id":
        print(meta_tags[14].get('content'))
    count = 0
    """
    for i in meta_tags:
        count = count + 1
        if i.get('name') == "vf:container_id":
            print("posicion del tag: " + str(count))
            potential_id = i.get('content')
            print(potential_id)
            #print(str(i.get('name')) + ": " + str(i.get('content')))
    """

#vf:container_id




