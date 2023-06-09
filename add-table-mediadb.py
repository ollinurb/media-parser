import sqlite3

#conexion a la db
con = sqlite3.connect("/Users/bruno/Documents/lanacion-parser/medios.db")
cur = con.cursor()

nombre = input("Nombre de la tabla: ")

cantidad_columnas = int(input("Cantidad de columnas: "))

columnas = ''
for x in range(0, cantidad_columnas):
    nombre_columna = input("Columna " + str(x) + ": ")
    if(x == 0):
        columnas = nombre_columna
    else:
        columnas = columnas + ", " + nombre_columna

print(nombre)
print(columnas)
query = "CREATE TABLE {} ({})".format(nombre, columnas)
cur.execute(query)

# Guardar los cambios en la base de datos
con.commit()
