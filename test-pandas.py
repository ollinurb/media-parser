import pandas as pd
import numpy as np
import sqlite3

#Creacion de DB y creacion del cursor.
con = sqlite3.connect("/Users/bruno/Documents/lanacion-parser/medios.db")

query = pd.read_sql_query("SELECT DISTINCT id FROM articulos;", con)

query.to_csv('ids.txt', sep=" ", index=False)
con.close()
