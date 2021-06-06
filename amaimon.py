#AMAIMON 3.0#

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

#PÁGINAS#

#Cuenta con un bucle de filtros que obtienen la máxima cantidad recuperable de datos posible.
#Cuando no se obtienen datos, es porque el sistema muestra demasiados incluso para ser filtrados.

def paginas(lista, corpus, pais, ano1, ano2, medio):

    def cosecha(lista):
        import re
        from selenium.webdriver.common.keys import Keys

        direccion = re.compile(r"(cgi-bin\/crpsrvEx\.dll\?visualizar.+?marcas=\d)")

        driver.find_element_by_css_selector('select.texto:nth-child(1) > option:nth-child(3)').click()
        driver.find_element_by_xpath('/html/body/blockquote/table[4]/tbody/tr[2]/td[1]/input').click()

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

    import re
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from urllib.parse import quote_plus

    busqueda = []

    rae = "http://corpus.rae.es/cgi-bin/crpsrvEx.dll"
    specs1 = "?MfcISAPICommand=buscar&tradQuery=1&destino=" + str(corpus) + "&texto="
    specs2 = "&autor=&titulo=&ano1=" + str(ano1) + "&ano2=" + str(ano2) + "&medio=" + str(medio) + "&pais=" + str(pais) + "&tema=1000"

    cantidad = re.compile(r"((\d+) casos?)")

    driver = webdriver.Chrome()

    for i in range(len(lista)):
        busqueda.append([]) #input de cosecha es busqueda[i]
        formas = []
        formas.append(lista[i])
        formas.append(lista[i].capitalize())
        for f in formas:
            print(f)
            url = rae + specs1 + quote_plus(f, encoding='cp1252') + specs2
            #print(url)
            driver.get(url)
            codigo = driver.page_source
            resultados = cantidad.finditer(codigo)
            for resultado in resultados:
                dato = resultado.group(2)
                print("Resultados totales:", dato)
                if int(dato) < 1000:
                    print("Recogiendo páginas de datos")
                    cosecha(busqueda[i]) #Este sí va aquí
                else:
                    dato1 = int(dato)

                    filtro = driver.find_elements_by_xpath("/html/body/blockquote/table[3]/tbody/tr[4]/td/input")
                    
                    if len(filtro) > 0:
                        while dato1 > 1000:
                            if dato1 > 7999:                                
                                driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[4]/td/input").click()
                                    
                                codigo1 = driver.page_source
                                resultados = cantidad.finditer(codigo1)
                                for resultado in resultados:
                                    dato1 = int(resultado.group(2))
                                    print("Filtrado al 10%:", dato1)
                            else:
                                ratio = driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[2]/td[2]/input")
                                ratio.clear()
                                ratio.send_keys("2")
                                
                                driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[4]/td/input").click()
                                    
                                codigo1 = driver.page_source
                                resultados = cantidad.finditer(codigo1)
                                for resultado in resultados:
                                    dato1 = int(resultado.group(2))
                                    print("Filtrado al 50%:", dato1)
                                
                        print("Recogiendo páginas de datos")
                        cosecha(busqueda[i])

                    else:
                        print("OMG!", f ,"IT'S SO BIG!")
                        continue
    
    driver.close()
    return(busqueda)

#FICHAS#

#Recupera las fichas a partir de una cierta cantidad de palabras antes y después del acierto.
#Recupera los metadatos del texto.

def fichas(lista):

    def cleanNflip(cadena,regexvar, flip = True):
        cadena = re.sub(r'<.+?>','', cadena)
        if flip == True:
            cadena = cadena[::-1]
            cadena = regexvar.match(cadena)
            cadena = cadena.group(0)
            cadena = cadena[::-1]
            return(cadena)
        else:
            cadena = regexvar.match(cadena)
            cadena = cadena.group(0)
            return(cadena)

    import requests
    import re
    import urllib
    from html import unescape

    corpus = "http://corpus.rae.es/"

    parrafo = re.compile(r"(Párrafo n. \d+.+?<A NAME=\"acierto\d+\">)(</A><A.+?Siguiente]\" BORDER=0>)(</A>.+?- -)")
    contexto = re.compile(r"(^(\W*?\w+){1,50})") #Vamos a usar la mísma fórmula para antes y después.
    contextito = re.compile(r"(^(\W*?\w+){1,10})")

    metachunk = re.compile(r"(AÑO: <\/TD>.+?TD>.+?PUBLICACIÓN: <\/TD>.+?TD>)")
    metaspecs = [re.compile(r"(AÑO: <\/TD>.+?TD>)"),
                re.compile(r"(AUTOR: <\/TD>.+?TD>)"),
                re.compile(r"(TÍTULO: <\/TD>.+?TD>)"),
                re.compile(r"(PAÍS: <\/TD>.+?TD>)"),
                re.compile(r"(TEMA: <\/TD>.+?TD>)"),
                re.compile(r"(PUBLICACIÓN: <\/TD>.+?TD>)")]

    print("Fichando...")

    fichas = []
    fichitas = []
    textInfo = []

    for url in lista:
        direccion = corpus + url
        pagina = requests.get(direccion, proxies=urllib.request.getproxies()) # Requests está tienendo muchos problemas. Hay que probar con Selenium.
        source = unescape(pagina.text)
        source = re.sub(r'\s',' ', source)
        
        #Si el corpus no está respondiendo manda un mensaje de error e interrumpe el proceso.
        if "<B>Pulse el botón de <i>Retroceso</i> de su navegador</B>" in source:
            print("Problemas con el corpus. Vuelve a intentar en un momento.")
            source = re.sub(r'<.+?>','', source)
            print(source)
            exit()
        
        chunks = parrafo.finditer(source)
        for chunk in chunks:
            previo = chunk.group(1)
            acierto = chunk.group(2)
            acierto = re.sub(r'<.+?>','', acierto)
            siguiente = chunk.group(3)

            fichas.append(cleanNflip(previo, contexto) + acierto + cleanNflip(siguiente, contexto, flip = False))
            fichitas.append(cleanNflip(previo, contextito) + acierto + cleanNflip(siguiente, contextito, flip = False))

        metadatos = metachunk.finditer(source)
        for metadato in metadatos:
            imprenta = []
            pieImprenta = metadato.group(0)
            for spec in metaspecs:
                datoEd = spec.finditer(pieImprenta)
                for dato in datoEd:
                    ed = dato.group(0)
                    ed = re.sub(r'<.+?>','', ed)
                    ed = re.sub(r'^[A-ZÍÓÑ]+?: ','', ed)
                    imprenta.append(ed)
            textInfo.append(imprenta)

    print(acierto, ". Fichas recuperadas:", len(fichitas))
    return([acierto, fichas, fichitas, textInfo])
    #print(len(fichas))
    #print(len(textInfo))

import csv

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

lema_forma = {"ahorita" : ["ahorita", "orita"], "perrito" : ["perrito", "perrita"]}

#Recuperación de los URLs de las páginas de resultados.
#La función Páginas arroja una lista por cada Key, que contiene tantas sublistas como valores haya en Value.
#Cada Key requiere una consulta, es decir, una búsqueda en el navegador (abriéndolo y cerrándolo).

datos = []

for i, key in enumerate(lema_forma):
    directorio = []
    fichero = []
    directorio = paginas(lema_forma[key], corpus = 0, pais = "1000", ano1 = 1975, ano2 = 1980, medio = "1000")
    for forma in directorio:
        fichero = fichas(forma)

        for j in range(len(fichero[1])):
            #print(key, fichero[0], fichero[1][j], fichero[2][j], fichero[3][j][0], fichero[3][j][1], fichero[3][j][2], fichero[3][j][3], fichero[3][j][4], fichero[3][j][5])
            datos.append([key.capitalize(), fichero[0].capitalize(), fichero[1][j], fichero[2][j], fichero[3][j][0], fichero[3][j][1], fichero[3][j][2], fichero[3][j][3], fichero[3][j][4], fichero[3][j][5]])

with open("fichas.csv", 'w+', newline='', encoding = 'utf-16le') as csvfile:
    salida = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    salida.writerow(["Lema", "Forma", "Contexto", "Ejemplo", "Año", "Autor", "Título", "País", "Tema", "Publicación"])

    for dato in datos:
        salida.writerow(dato)

print("CÓMO CITAR ESTE SOFTWARE: Granados, Daniel. 2021. Amaimon, software para la recuperación automática de datos. Versión: 3. Lenguaje: Python. México. https://github.com/gengisdan/fichador-amaimon/tree/amaimon3")

