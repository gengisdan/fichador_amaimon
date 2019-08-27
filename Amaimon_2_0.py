## AMAIMON 2.0 ##

#Amaymon:
#Rey infernal.
#Enseña astrología y artes liberales; descubre a sus amigos los tesoros guardados por los demonios.

#O you great mighty and Powerfull kinge Amaymon, who beareth rule by the power of thy supreame god El
#over all spirits both superior and Inferiour of the Infernal order in the Dominion of the Earth [East],
#I invocate and command you by the especial and truest name of your god and by god that you worship and obey, 
#and by the seal of ye Creation, & by the most mighty & powerfull name of god Jehovah Tetragrammaton...
#(Lemegeton Clavicula Salomonis, Ars Goetia)

from Grimorio_2_0 import asmodeo
from Grimorio_2_0 import paginas
from Grimorio_2_0 import fichas
import csv
import io
import random

#Introducción de los verbos que se ficharán

verbos = []

cadena = input("Introduce uno o más verbos en infinitivo separados por coma: ")

verbos = cadena.split(", ")

#Recuperación del paradigma verbal a través de Asmodeo

diccionario = asmodeo(verbos)

#Recuperación de páginas de resultados por medio de Fichas 1.5

directorio = []

for i, key in enumerate(diccionario):
    #print(i, key)
    directorio.append(paginas(sorted(diccionario[key]), corpus = 0, pais = "13", ano1 = 1980, ano2 = 2004, medio = "0&medio=1&medio=2"))

#Crea un diccionario de diccionarios con las páginas y las formas verbales

diccionario_conjugaciones = {}

for i, key in enumerate(diccionario):
    conjugaciones = {}
    for j in range(len(diccionario[key])):
        conjugaciones[diccionario[key][j]] = directorio[i][j]
        diccionario_conjugaciones[key] = conjugaciones

#Obtiene las fichas con la funcion Fichas y las imprime en un CSV.

with open("fichas.csv", 'w+', newline='', encoding = 'utf-16le') as csvfile:
    salida = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    salida.writerow(["verbo", "forma", "contexto", "ejemplo", "anno", "autor", "titulo", "pais", "tema", "publicacion"])
    
    for key in diccionario_conjugaciones:
        fichado = []
        verbos = []
        datos = []
        muestra = []

        for k in diccionario_conjugaciones[key]:
            verbos.append([key, k])

        for k in diccionario_conjugaciones[key]:
            corpus = diccionario_conjugaciones[key][k]
            fichado.append(fichas(corpus))

        for i in range(len(fichado)):
            for j in range(len(fichado[i][0])):
                #print(verbos[i][0], verbos[i][1], fichado[i][0][j], fichado[i][1][j], *fichado[i][2][j], '\n')
                datos.append([verbos[i][0], verbos[i][1], fichado[i][0][j], fichado[i][1][j], *fichado[i][2][j]])

        if len(datos) <= 2000:
            print(key, "Datos totales: ", len(datos))
            random.shuffle(datos)
            for dato in datos:
                salida.writerow(dato)
        else:
            muestra = random.sample(datos, 2000)
            print(key, "Datos totales: ", len(datos), "Muestra: ", len(muestra))
            for m in muestra:
                salida.writerow(m)

print("CÓMO CITAR ESTE SOFTWARE: Granados, Daniel. 2019. Amaimon, software para la recuperación automática de datos. Versión: 2.0. Lenguaje: Python. México. https://github.com/gengisdan/fichador_amaimon")
