# fichador_amaimon

AMAIMON 3.1.3
Software para la recuperación automática de datos.

El objetivo de este programa es recuperar fichas de manera automática desde los corpus de la RAE: el CORDE y el CREA. El proceso se lleva a cabo a partir de elementos de búsqueda introducidos por el usuario en un diccionario que tiene la siguiente estructura:

{"lema" : ["forma 1", "forma 2"]}

"lema" corresponde a la forma lemática de la búsqueda, por ejemplo, "perro".
Dentro de la lista del value, se colocan las diferentes variantes del lema que quieren buscarse, por ejemplo, "perro", "perrito", "perra".

El "lema" también se puede utilizar para designar alguna categoría abstracta: "Adverbio", y cada elemento de la lista del value puede ser una instancia de esa categoría: "ahora", "antes", "después".

Amaimon recupera un contexto específico (10 palabras antes y después del acierto), que permite identificar rápidamente la forma en su contexto inmediato, y un contexto amplio (50 palabras antes y después del acierto), que provee de texto suficiente para interpretar el funcionamiento de la forma adecuadamente. La cantidad de palabras antes y después del acierto en cualquiera de los contextos puede ser modificada por el usuario.

Además del contexto, el programa recolecta toda la meta-información que ofrece el corpus: año de publicación, autor, título, país, tema y publicación.

Amaimon fue creado con el propósito de facilitar la tarea de recolección de datos a los lingüistas, para que puedan dedicar más tiempo al análisis. Asismimo, permite recuperar grandes cantidades de datos rápidamente, obteniendo muestras aleatorias.

Requerimientos:
Selenium
Chrome Driver

PARÁMETROS DE LA FUNCIÓN PÁGINAS

Valores posibles en Corpus:
corpus = 
"0"> CREA
"1"> CORDE

Valores posibles en Medio:
medio = 
"1000">(Todos)
"0"> Libros
"1"> Periódicos
"2"> Revistas
"3"> Miscelánea
"4"> Oral

Valores posibles en País:
pais = 
"1000">(Todos)
"0">Argentina
"1">Bolivia
"2">Chile
"3">Colombia
"4">Costa Rica
"5">Cuba
"6">Ecuador
"7">El Salvador
"8">EE.UU.
"9">España
"10">Filipinas
"11">Guatemala
"12">Honduras
"13">México
"14">Nicaragua
"15">Panamá
"16">Paraguay
"17">Perú
"19">Puerto Rico
"20">Rep. Dominicana
"21">Uruguay
"22">Venezuela

Los valores numéricos se pueden introducir solos o entre comillas:

pais = 0
pais = "0"

Los parámetros de año (ano1 y ano2) son AMBOS NECESARIOS, y deben corresponder con el tipo de corpus. CORDE: desde el s. XII hasta el año 1974. CREA: desde 1975 hasta 2004.

Para recuperar ejemplos de un lapso determinado:

ano1 = 1700, ano2 = 1850 

Para recuperar ejemplos de UN SOLO AÑO en específico:

ano1 = 1982, ano2 = "" 

Para NO seleccionar NINGÚN AÑO en específico, y recuperar datos de todos los años que comprende el corpus, ambos valores deben aparecer como:

ano1 = "", ano2 = ""
