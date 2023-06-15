from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from datetime import datetime, timedelta, timezone
import sqlite3
import pandas as pd 
import pickle
from trie import Trie

pickle_file = '/root/media-parser/ids.pickle'

id_dict = Trie()

with open(pickle_file, "rb") as file:
    id_dict = pickle.load(file)

#Creacion de DB y creacion del cursor.
con = sqlite3.connect("/root/media-parser/medios.db")
cur = con.cursor()


# Crear una timezone GMT-3 y obtener el now para GMT-3.
gmt_minus_3 = timezone(timedelta(hours=-3))
date = datetime.now(tz=gmt_minus_3)

medio = 'lanacion'
print("\n\n====="+"PARSEO DEL " + str(date) +"=====\n\n")
url = "https://lanacion.com.ar"

response = requests.get(url)

soup = BeautifulSoup(response.content,'html.parser')

estados = soup.find_all("article")
for x in estados:
    id = 0
    articulo = x.contents[0].contents[0]
    titulo = articulo.get("title")
    href = articulo.get("href")

    #ingrear al articulo para obtener el potencial ID
    article_url = "https://lanacion.com.ar"+ href
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    meta_tags = article_soup.find_all("meta")
    potential_id_tag = meta_tags[14]
    if potential_id_tag.get('name') == "vf:container_id":
        id = meta_tags[14].get('content')
        if(id_dict.search(id) == False):
            #extraer categoria
            categoria = href.split("/")[1]
            #extraer cuerpo articulo
            cuerponota_object = article_soup.find_all(attrs={"class":"cuerpo__nota"})
            if(len(cuerponota_object) > 0):
                cuerponota = cuerponota_object[0]
                parrafos = cuerponota.find_all('p')
                str_articulo = ""
                for x in parrafos:
                    print("cant de parrafos " + str(len(x)))
                    for i in range(len(x)):
                        print("parrafo " + str(i))
                        print(x.contents[i])
                        if(isinstance(x.contents[i], NavigableString)):
                            str_articulo = str_articulo + x.contents[i]
                        if(isinstance(x.contents[i], Tag) & len(x.contents[i]) > 0):
                            print("es un tag y dentro tiene " + str(len(x.contents[i])) + " cosas")
                            str_articulo = str_articulo + str(x.contents[i].contents[0])
                    str_articulo = str_articulo + '\n\n'
                contenido = str_articulo.replace("<strong>", "").replace("</strong>","")
                #query de insertado de articulo
                query = "INSERT INTO articulos (id, timestamp, medio, titulo, url, categoria, contenido) VALUES (?, ?, ?, ?, ?, ?, ?)"
                values = (id, date, medio, titulo, href, categoria, contenido)
                print(values)
                cur.execute(query, values)
                id_dict.insert(id)
# Guardar los cambios en la base de datos
con.commit()
con.close()
#guardar Trie
with open(pickle_file, "wb") as file:
    pickle.dump(id_dict, file)

print("--------_FIN_---------")
