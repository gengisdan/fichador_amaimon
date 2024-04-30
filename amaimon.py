#AMAIMON 3.1.3.1#

#Magick is the highest most absolute and divinest knowledge of Natural
#Philosophy advanced in its works and wonderfull operations by a right understanding
#of the inward and occult vertue of things, so that true agents
#being applyed to proper patients, strange and admirable effects will thereby
#be produced...
#(Lemegeton Clavicula Salomonis, Ars Goetia)

# Magical Art should yet that must not be evil or subject to contempt or scorne...
#(Lemegeton Clavicula Salomonis, Ars Goetia)

############
# GRIMORIO #
############

from selenium.webdriver.common.by import By
import re
from selenium import webdriver
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
from html import unescape
import csv #Los import van ANTES DE LAS FUNCIONES para no tener que importarlos dentro de cada función.
import random

#PÁGINAS#

#Cuenta con un bucle de filtros que obtienen la máxima cantidad recuperable de datos posible.
#Cuando no se obtienen datos, es porque el sistema muestra demasiados incluso para ser filtrados.

def paginas(lista, corpus, pais, ano1, ano2, medio):

    def cosecha(lista):

        direccion = re.compile(r"(cgi-bin\/crpsrvEx\.dll\?visualizar.+?marcas=\d)")

        driver.find_element(by=By.CSS_SELECTOR, value='select.texto:nth-child(1) > option:nth-child(3)').click() 
        driver.find_element(by=By.XPATH, value='/html/body/blockquote/table[4]/tbody/tr[2]/td[1]/input').click()

        codigo = driver.page_source
        resultados = direccion.finditer(codigo)
        for resultado in resultados:
            dato = resultado.group(0)
            dato = re.sub(r'tipo1=4','tipo1=5', dato)
            dato = re.sub(r'amp;','', dato)
            dato = re.sub(r'\\', '/', dato)
            if dato not in lista:
                lista.append(dato)
        
        return(lista)

    # AQUÍ HAY QUE PONER LISTAS PARA LOS VALORES DE PAÍS, MEDIO Y TEMA

    busqueda = []

    rae = "http://corpus.rae.es/cgi-bin/crpsrvEx.dll"
    specs1 = "?MfcISAPICommand=buscar&tradQuery=1&destino=" + str(corpus) + "&texto="
    specs2 = "&autor=&titulo=&ano1=" + str(ano1) + "&ano2=" + str(ano2) + "&medio=" + str(medio) + "&pais=" + str(pais) + "&tema=1000"

    cantidad = re.compile(r"((\d+) casos?)")
    documentos = re.compile(r"((\d+) documentos?)")

    driver = webdriver.Chrome()
    #driver = webdriver.Firefox()

    for i in range(len(lista)):
        busqueda.append([]) #input de cosecha es busqueda[i]
        formas = []
        formas.append(lista[i])
        formas.append(lista[i].capitalize())
        for f in formas: #Este segundo bucle corresponde a la búsqueda de con mayúscula y minúscula.
            print(f)
            cadenadebusqueda = ""
            for letra in f:
                if letra not in "*?":
                    nuevaletra = quote_plus(letra, encoding='cp1252')
                    cadenadebusqueda = cadenadebusqueda + nuevaletra
                else:
                    cadenadebusqueda = cadenadebusqueda + letra
            #print(cadenadebusqueda)
            url = rae + specs1 + cadenadebusqueda + specs2
            #print(url)
            driver.get(url)
            codigo = driver.page_source
            #print(codigo)
            if "No existen casos para esta consulta." in codigo:
                print("No existen casos para esta consulta.")
            else:
                resultados = cantidad.finditer(codigo)
                for resultado in resultados:
                    dato = resultado.group(2)
                    print("Resultados totales:", dato, "entre los años", ano1, "y", ano2, ".") ### ESTE DATO DA LAS PROPORCIONES. AGREGAR CANTIDAD DE DOCUMENTOS

                    docs = documentos.finditer(codigo)
                    for doc in docs:
                        docstotales = doc.group(2)
                        print("Documentos totales:", docstotales)

                    if int(dato) < 1000:
                        print("Recogiendo páginas de datos")
                        cosecha(busqueda[i]) #Este sí va aquí
                    else:
                        dato1 = int(dato)

                        filtro = driver.find_elements(by=By.XPATH, value="/html/body/blockquote/table[3]/tbody/tr[4]/td/input") 
                        
                        if len(filtro) > 0:
                            while dato1 > 1000:
                                if dato1 > 7999:                                
                                    driver.find_element(by=By.XPATH, value="/html/body/blockquote/table[3]/tbody/tr[4]/td/input").click()
                                        
                                    codigo1 = driver.page_source
                                    resultados = cantidad.finditer(codigo1)
                                    for resultado in resultados:
                                        dato1 = int(resultado.group(2))
                                        print("Filtrando documentos al 10%. \n Cantidad de datos:", dato1) ### AGREGAR CANTIDAD DE DOCUMENTOS
                                    
                                    docs = documentos.finditer(codigo1)
                                    for doc in docs:
                                        docstotales = doc.group(2)
                                        print(" Cantidad de documentos:", docstotales)

                                else:
                                    ratio = driver.find_element(by=By.XPATH, value="/html/body/blockquote/table[3]/tbody/tr[2]/td[2]/input") 
                                    ratio.clear()
                                    ratio.send_keys("2")
                                    
                                    driver.find_element(by=By.XPATH, value="/html/body/blockquote/table[3]/tbody/tr[4]/td/input").click()
                                        
                                    codigo1 = driver.page_source
                                    resultados = cantidad.finditer(codigo1)
                                    for resultado in resultados:
                                        dato1 = int(resultado.group(2))
                                        print("Filtrando documentos al 50%. \n Cantidad de datos:", dato1) ### AGREGAR CANTIDAD DE DOCUMENTOS
                                    
                                    docs = documentos.finditer(codigo1)
                                    for doc in docs:
                                        docstotales = doc.group(2)
                                        print(" Cantidad de documentos:", docstotales)
                                    
                            print("Recogiendo páginas de datos")
                            cosecha(busqueda[i])

                        else:
                            print("OMG!", f ,"IT'S SO BIG!")
                            continue
        
    driver.close()
    return(busqueda) ### TIENE QUE REGRESAR DATO: LOS RESULTADOS TOTALES EN EL CORPUS, ANTES DE LOS FILTROS.

#FICHAS#

#Recupera las fichas a partir de una cierta cantidad de palabras antes y después del acierto.
#Recupera los metadatos del texto.

def fichas(lista):

    #### ADAPTAR PARA SELENIUM ####
    ### HAY QUE INTRODUCIR UNA FUNCIÓN DE MANEJO DE ERRORES. AUÍ Y TAL VEZ EN PÁGINAS ###

    def cleanNflip(cadena,regexvar, flip = True):
        cadena = re.sub(r'<font color=\"Green\" size=\"3\">.+?</font>','', cadena) #Hay que quitar también la parte de Párrafo N...
        cadena = re.sub(r'Párrafo n. \d+.</td>', '', cadena)
        cadena = re.sub(r'&amp;', '&', cadena)
        cadena = re.sub(r'&verbar;', '||', cadena)
        cadena = re.sub(r'ē', 'e', cadena)
        cadena = re.sub(r'<.+?>','', cadena)
        if flip == True:
            cadena = cadena[::-1]
            cadena = regexvar.match(cadena) #Si esto da problemas, se podría cambiar por finditer
            cadena = cadena.group(0)
            cadena = cadena[::-1]
            return(cadena)
        else:
            cadena = regexvar.match(cadena)
            cadena = cadena.group(0)
            return(cadena)

    corpus = "http://corpus.rae.es/"

    parrafo = re.compile(r"(Párrafo n. \d+.+?<a name=\"acierto\d+\">)(</a><a.+?Siguiente]\" border=\"0\".+?>)((</a>)?.+?- -.+?)(AÑO: <\/td>.+?td>.+?PUBLICACIÓN: <\/td>.+?td>)") #Chrome
    #parrafo = re.compile(r"(Párrafo n. \d+.+?<a name=\"acierto\d+\">)(</a><a.+?Siguiente]\" border=\"0\".+?>)(</a>.+?- -)") #Firefox
    contexto = re.compile(r"(^(\W*?\w+){0,50})") ### DETERMINA LA CANTIDAD DE PALABRAS QUE SE RECOGEN
    contextito = re.compile(r"(^(\W*?\w+){0,10})")

    metachunk = re.compile(r"(AÑO: <\/td>.+?td>.+?PUBLICACIÓN: <\/td>.+?td>)")
    metaspecs = [re.compile(r"(AÑO: <\/td>.+?td>)"),
                re.compile(r"(AUTOR: <\/td>.+?td>)"),
                re.compile(r"(TÍTULO: <\/td>.+?td>)"),
                re.compile(r"(PAÍS: <\/td>.+?td>)"),
                re.compile(r"(TEMA: <\/td>.+?td>)"),
                re.compile(r"(PUBLICACIÓN: <\/td>.+?td>)")]

    print("Fichando...")

    driver = webdriver.Chrome()
    #driver = webdriver.Firefox()

    fichas = []
    fichitas = []
    textInfo = []
    
    for url in lista:
        direccion = corpus + url
        #print(direccion)

        #selenium
        driver.get(direccion)
        source = driver.page_source
        source = unescape(source)
        source = re.sub(r'\s',' ', source)

        #print(source)

        #### ADAPTAR PARA SELENIUM ####
        
        #Si el corpus no está respondiendo manda un mensaje de error.
        if "Pulse el botón de <i>Retroceso</i> de su navegador" in source:
            print("Problemas con el corpus. Inténtalo de nuevo.")
            source = re.sub(r'<.+?>','', source)
            print(source)
            continue
        
        chunks = parrafo.finditer(source) #El manejo de errores iría desde aca... tal vez.
        for chunk in chunks:
            previo = chunk.group(1)
            acierto = chunk.group(2)
            acierto = re.sub(r'<.+?>','', acierto)
            siguiente = chunk.group(3)
            
            #print(previo)
            #print(acierto)
            #print(siguiente)

            #try:
            fichas.append(cleanNflip(previo, contexto) + acierto + cleanNflip(siguiente, contexto, flip = False))
            fichitas.append(cleanNflip(previo, contextito) + acierto + cleanNflip(siguiente, contextito, flip = False))
            #except:
                #print("Excepción.")
            
            imprenta = []
            pieImprenta = chunk.group(5)
            for spec in metaspecs:
                datoEd = spec.finditer(pieImprenta)
                for dato in datoEd:
                    ed = dato.group(0)
                    ed = re.sub(r'<.+?>','', ed)
                    ed = re.sub(r'^[A-ZÍÓÑ]+?: ','', ed)
                    imprenta.append(ed)
            textInfo.append(imprenta)

        #metadatos = metachunk.finditer(source)
        #for metadato in metadatos:
          #  imprenta = []
           # pieImprenta = metadato.group(0)
            #for spec in metaspecs:
             #   datoEd = spec.finditer(pieImprenta)
              #  for dato in datoEd:
               #     ed = dato.group(0)
                #    ed = re.sub(r'<.+?>','', ed)
                 #   ed = re.sub(r'^[A-ZÍÓÑ]+?: ','', ed)
                  #  imprenta.append(ed)
            #textInfo.append(imprenta)
    #try:
    print(acierto, ". Fichas totales:", len(fichitas))
    #except:
        #print("Forma sin resultados.")
    driver.close()
    
    #try:
    return([acierto, fichas, fichitas, textInfo])
    #except:
        #print("Continuando fichado.")
    #print(len(fichas))
    #print(len(textInfo))

#############
#  AMAIMON  #
#############

#O you great mighty and Powerfull kinge Amaymon, who beareth rule by
#the power of thy supreame god El over all spirits both superior and
#Inferiour of the Infernal order in the Dominion of the Earth [East], I
#invocate and command you by the especial and truest name of your god
#and by god that you worship and obey, and by the seal of ye Creation, &
#by the most mighty & powerfull name of god Jehovah Tetragrammaton, to 
#come unto me hear before this Circle in a fair & comely forme, without 
#doeing any harme to me or any other Creature,
#and to answere truely & faithfull to all my Requests

# Ars Goetia.

#Diccionario de Lemas (Keys) y Formas (Values)

lema_forma = {'ante': ["ante"]} #"estonces", "estonçe", "estonçes", "entonce", "estonce", "entonçe", "entonçes", "entonces" 

#Recuperación de los URLs de las páginas de resultados.
#La función Páginas arroja una lista por cada Key, que contiene tantas sublistas como valores haya en Value.
#Cada Key requiere una consulta, es decir, una búsqueda en el navegador (abriéndolo y cerrándolo).

datos = []

for i, key in enumerate(lema_forma):
    datos.append([])
    directorio = []
    fichero = []
    for year in range(1): #Si se quiere buscar año por año, se usan los años en el rango. Si se quiere un lapso, se usa 1 en el rango, y años en los parámetros.
        directorio = paginas(lema_forma[key], corpus = 1, pais = "1000", ano1 = "1201", ano2 = "1249", medio = "1000") #Es muy importante indicar el corpus adecuado para el rango de búsqueda
        for forma in directorio:
            if len(forma) > 0: #Cuando no hay resultados para la búsqueda en el rango especificado
                fichero = fichas(forma)
            #try:
                for j in range(len(fichero[1])):
                #print(key, fichero[0], fichero[1][j], fichero[2][j], fichero[3][j][0], fichero[3][j][1], fichero[3][j][2], fichero[3][j][3], fichero[3][j][4], fichero[3][j][5])
                    datos[i].append([key.capitalize(), fichero[0].capitalize(), fichero[1][j], fichero[2][j], fichero[3][j][0], fichero[3][j][1], fichero[3][j][2], fichero[3][j][3], fichero[3][j][4], fichero[3][j][5]])
            else:
                continue

with open("fichas.csv", 'w+', newline='', encoding='Windows-1252') as csvfile:  # utf-8
    salida = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    salida.writerow(["Type", "Token", "Contexto", "Ejemplo", "Ano", "Autor", "Titulo", "Pais", "Tema", "Publicacion"])

    #Aquí se pueden poner unas líneas para obtener un muestra aleatoria menor a la cantidad total de datos recuperados.

    umbral = 150

    for i, key in enumerate(lema_forma):   

        if len(datos[i]) <= umbral:
            print(key.capitalize(), "DATOS RECUPERADOS: ", len(datos[i])) #Se podría agregar la cantidad de documentos?
            random.shuffle(datos[i])
            for dato in datos[i]:
                salida.writerow(dato)

        else:
            muestra = random.sample(datos[i], umbral)
            print(key.capitalize(), "De: ", len(datos[i]), "datos recuperados, se tomó una muestra aleatoria de: ", len(muestra))
            for dato in muestra:
                salida.writerow(dato)


print("CÓMO CITAR ESTE SOFTWARE: Granados, Daniel. 2021. Amaimon. Versión: 3.1.3.1 (Beta). Lenguaje: Python. México. https://github.com/gengisdan/fichador-amaimon/")
