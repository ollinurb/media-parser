from bs4 import BeautifulSoup
import requests
from datetime import datetime
import sqlite3
import pandas as pd 
import pickle
from trie import Trie

pickle_file = 'ids.pickle'

id_dict = Trie()

with open(pickle_file, "rb") as file:
    id_dict = pickle.load(file)

#Creacion de DB y creacion del cursor.
con = sqlite3.connect("/Users/bruno/Documents/lanacion-parser/medios.db")
cur = con.cursor()

date = datetime.now()
medio = 'lanacion'
print("\n\n====="+"PARSEO DEL " + str(date) +"=====\n\n")
url = "https://lanacion.com.ar"

response = requests.get(url)

soup = BeautifulSoup(response.content,'html.parser')

agregados = 0
estados = soup.find_all("article")
for x in estados:
    id = 0
    articulo = x.contents[0].contents[0]
    titulo = articulo.get("title")
    href = articulo.get("href")
    print(titulo)

    #ingrear al articulo para obtener el potencial ID
    article_url = "https://lanacion.com.ar"+ href
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    meta_tags = article_soup.find_all("meta")
    potential_id_tag = meta_tags[14]
    if potential_id_tag.get('name') == "vf:container_id":
        id = meta_tags[14].get('content')
        print("POTENCIAL ID: " + str(id))
        print("el ID esta presente: " + str(id_dict.search(id)))
        if(id_dict.search(id) == False):
            #query de insertado de articulo
            query = "INSERT INTO articulos (id, timestamp, medio, titulo, url) VALUES (?, ?, ?, ?, ?)"
            values = (id, date, medio, titulo, href)
            cur.execute(query, values)
            id_dict.insert(id)
            print("el ID esta presente: " + str(id_dict.search(id)))
            print("---AGREGADO---\n")
            agregados = agregados + 1
# Guardar los cambios en la base de datos
con.commit()

#guardar Trie
with open(pickle_file, "wb") as file:
    pickle.dump(id_dict, file)

print(str(agregados) + " articulos agregados.")