## GRIMORIO 2.0 ##

#I conjure ye anew, and I powerfully urge ye, O Demons, in whatsoever part of the world ye may be,
#so that ye shall be unable to remain in air, fire, water, earth, or in any part of the universe,
#or in any pleasant place which may attract ye; but that ye come promptly to accomplish our desire,
#and all things that we demand from your obedience. (Clavicula Salomonis, 1:5)

## PÁGINAS 1.5
## Recupera los URLs de los resultados.
## Novedad: Cuando son más de mil, los filtra por documento.
## Novedad: Filtros integrados: México, 1980-2004, Libros, Periódicos y Revistas

def paginas(lista, corpus, pais, ano1, ano2, medio):
    #Corpus 0 = CREA
    #Corpus 1 = CORDE
    
    def cosecha(lista):
        import re
        from selenium.webdriver.common.keys import Keys 
        #from selenium.webdriver.common.by import By
        
        direccion = re.compile(r"(cgi-bin\/crpsrvEx\.dll\?visualizar.+?marcas=\d)")
        
        listOfElements = []
        listOfElements.append(driver.find_elements_by_css_selector('select.texto:nth-child(1) > option:nth-child(3)'))
        listOfElements.append(driver.find_elements_by_xpath('/html/body/blockquote/table[4]/tbody/tr[2]/td[1]/input'))
        
        if len(listOfElements[0]) > 0:
            driver.find_element_by_css_selector('select.texto:nth-child(1) > option:nth-child(3)').click()
            if len(listOfElements[1]) > 0:
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
            #else:
                #continue
        #else:
            #continue
        
        return(lista)
        
        
    import re
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    #from selenium.webdriver.common.by import By
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
            url = rae + specs1 + quote_plus(f, encoding='cp1252') + specs2
            #print(url)
            driver.get(url)
            codigo = driver.page_source
            resultados = cantidad.finditer(codigo)
            for resultado in resultados:
                dato = resultado.group(2)
                #print(dato)
                if int(dato) < 1000:
                    #print("OK")
                    cosecha(busqueda[i])
                else:
                    #Aquí tendría que pasar por el filtro de documentos
                    #print(f, "Too big to fit in here!")
                    filtro = driver.find_elements_by_xpath("/html/body/blockquote/table[3]/tbody/tr[4]/td/input")
                    if len(filtro) > 0:
                        #print(filtro)
                        driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[4]/td/input").click()
                        cosecha(busqueda[i])
                    else:
                        print(f, "OMG! IT'S SO BIG!")
                        #continue
                    
                    
    driver.close()
    
    return(busqueda)

## FICHAS 1.0
## Recupera las fichas a partir del código fuente de las páginas de resultados.
## Novedad: Incluye tres oraciones antes y tres oraciones desupes a partir del contexto buscado.
## Novedad: Se incluyeron puntos al inicio y fin de párrafo para acotar mejor el texto recuperado.

def fichas(lista):
    import requests
    from html import unescape
    import re
    import urllib
    #import time

    signos = "<> /(:-=*)\",;"
    signos1 = '<> /(:-=*)\",;0123456789[]'

    def limpia(x, signos):
        import re
        #signos = "<> /(:-=*)\",;"
        #signos1 = '<> /(:-=*)\",;0123456789'
        x = re.sub(r'<.+?>','', x)
        x = x.strip(signos)
        return(x)

    def sincampos(x):
        import re
        x = re.sub(r'[A-ZÑÍÓ]+: ','', x)
        return(x)


    ficha = re.compile(r"(([^.?!]*[\.?!]){3}([^.?!]*<A NAME=\"acierto\d+\">.+?Siguiente.+?[\.?!])([^.?!]* [^.]*[\.?!]){3})")

    metachunk = re.compile(r"(AÑO: <\/TD>.+?TD>.+?PUBLICACIÓN: <\/TD>.+?TD>)")

    metaspecs = [re.compile(r"(AÑO: <\/TD>.+?TD>)"),
                re.compile(r"(AUTOR: <\/TD>.+?TD>)"),
                re.compile(r"(TÍTULO: <\/TD>.+?TD>)"),
                re.compile(r"(PAÍS: <\/TD>.+?TD>)"),
                re.compile(r"(TEMA: <\/TD>.+?TD>)"),
                re.compile(r"(PUBLICACIÓN: <\/TD>.+?TD>)")]
    
    corpus = "http://corpus.rae.es/"

    chunks = []
    contextos = []
    chunks_datos = []
    metadata = []

    for url in lista:
        direccion = corpus + url
        pagina = requests.get(direccion, proxies=urllib.request.getproxies())
        #time.sleep(3)
        source = unescape(pagina.text)
        source = re.sub(r'\s',' ', source)
        source = re.sub(r'\.</td></tr>','. . . .</td></tr>', source)
        source = re.sub(r'\"justify\">- -', '\"justify\">. . . .- -', source)
        
        fragmentos = ficha.finditer(source)
        for fragmento in fragmentos:
            chunks.append(limpia(fragmento.group(0), signos = signos1))
            contextos.append(limpia(fragmento.group(3), signos = signos1)) #Mismo grupo que antes.

        metadatos = metachunk.finditer(source)
        for metadato in metadatos:
            chunks_datos.append(metadato.group(0))
    
    for i in range(len(chunks_datos)): 
        metadata.append([])
        for spec in metaspecs:
            pie_imprenta = spec.finditer(chunks_datos[i])
            for pie in pie_imprenta:
                y = (limpia(pie.group(0), signos = signos))
                metadata[i].append(sincampos(y))
    
    return([chunks, contextos, metadata])

## ASMODEO 1.0
## Recupera del DLE los paradigmas verbales de los verbos introducidos.
## Novedad: Ahora constituye una función que se conjura en Amaimon desde el Grimorio.
## Novedad: Puede funcionar con input().

def asmodeo(verbos):
    # Tu vero es Asmoday. (Lemegeton Clavicula Salomonis, Ars Goetia)
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    import re
    import time
    
    verbos = sorted(verbos)
    print(verbos)

    conjugaciones = {}

    #driver
    driver = webdriver.Chrome()

    #DLE
    #url = "http://dle.rae.es/srv/fetch?w="
    url = "https://dle.rae.es/?w="

    #listas
    signos = ">< "
    excepciones = ['usted', 'imperativo', 'yo', 'pronombres', 'nosotros',
                    'pretérito', 'vosotros', 'presente', 'personas', 'tú',
                    'indicativo', 'formas', 'condicional', 'ellos', 'futuro',
                    'número', 'él', 'participio', 'subjuntivo', 'infinitivo', 'o',
                    'gerundio', 'ustedes', '1', 'u']

    paradigma = []

    #RegEx
    identificadores = re.compile(r"(\?id=\w+)")
    #id_conjugacion = re.compile(r"(fetch\?id=\w+)")
    #id_articulo = re.compile(r"(article id=\"\w+\")")
    CodigoParte = re.compile(r"(<article id.+</article>)")
    palabras = re.compile(r"(> ?\w+ ?)") #NO RECOGE TODAS LAS PALABRAS

    #Extracción del paradigma
    for j in range(5):
        for i in range(len(verbos)):
            paradigma.append([])
            lista = []
            #lista2 = []
            if len(paradigma[i]) == 0:
                path = url + verbos[i]
                driver.get(path)
                time.sleep(5)
                codigo = driver.page_source
                #print(codigo)
                aidis = []

                resultados = identificadores.finditer(codigo)
                for resultado in resultados:
                    aidis.append(resultado.group(0))
                #print(aidis)

                if len(aidis) > 2:
                    comando = "conjugar('" + aidis[0] + "','" + verbos[i] + "','/" + aidis[1] + "') ; return false;"
                    #print(comando)
                    driver.execute_script(comando)
                    time.sleep(3)

                    codigo = driver.page_source
                    minus = codigo.lower()
                    #print(minus)
                    segmentos = CodigoParte.finditer(minus)
                    for segmento in segmentos:
                        articulo = segmento.group(0)
                        #print(articulo)

                    resultados = palabras.finditer(articulo) 
                    for resultado in resultados:
                        lista.append(resultado.group(0))
                    for l in lista:
                        l = l.strip(signos)
                        if l not in excepciones:
                            if l not in paradigma[i]:
                                paradigma[i].append(l)
                else:
                    continue

            #print(verbos[i])
            #print(paradigma[i])

    driver.close()

    for i in range(len(verbos)):
        conjugaciones[verbos[i]] = sorted(paradigma[i])
    
    #print(conjugaciones)
    return(conjugaciones)
